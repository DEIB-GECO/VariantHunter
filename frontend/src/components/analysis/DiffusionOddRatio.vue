<!--

  Component:    DiffusionOddRatio
  Description:  Plot of the odd ratio for the diffusion data. Implemented using vue-plotly.

-->

<template>
  <section-element icon='mdi-align-vertical-bottom' assign-id="odd-ratio"
                   title='Log<sub>2</sub> odd ratio'
                   :subtitle="getCurrentPlotTitle"
                   caption="To visualize specific mutations, select the corresponding rows from the table"
                   collapsed :tabs='["Week-by-week","Week-to-first-week","All"]'
                   @tabChange='(selected) => type=selected'>
    <!-- Odd ratio app-tour -->
    <odd-ratio-intro/>

    <div class='regular-plot plotly-container'>

      <!-- Week-by-week odd ratio -->
      <plotly v-if='type!==1' :data='dataSubsWeeks' :layout='layoutSubsWeeks' :displaylogo='false'
              :modeBarButtonsToRemove="['lasso2d', 'select2d', 'toggleSpikelines']"/>

      <!-- Week-to-first week odd ratio -->
      <plotly v-if='type>=1' :data='dataFirstWeekRef' :layout='layoutFirstWeekRef' :displaylogo='false'
              :modeBarButtonsToRemove="['lasso2d', 'select2d', 'toggleSpikelines']"/>

    </div>
  </section-element>
</template>

<script>
import {Plotly} from '@rleys/vue-plotly'
import SectionElement from "@/components/analysis/SectionElement";
import {mapGetters} from "vuex";
import OddRatioIntro from "../intros/OddRatioIntro";
import {palette} from "@/utils/colorService";

export default {
  name: 'DiffusionOddRatio',
  components: {OddRatioIntro, SectionElement, Plotly},

  data() {
    return {
      /**
       * Type of odd ratio to be displayed.
       * 0: week-by-week; 1: week-to-first-week; 2: all
       */
      type: 0,
    }
  },

  computed: {
    ...mapGetters(['getCurrentPlotRows', 'getCurrentPlotTitle', 'getCurrentAnalysis']),

    /** Date labels */
    dateLabel() {
      return this.getCurrentAnalysis.query.weeks
    },

    /** Data for the week-by-week odd ratio plot */
    dataSubsWeeks() {
      return this.getCurrentPlotRows.map(el => {
        return this.computeData(el, false)
      })
    },

    /** Data for the week-to-first-week odd ratio plot */
    dataFirstWeekRef() {
      return this.getCurrentPlotRows.map(el => {
        return this.computeData(el, true)
      })
    },

    /** Layout for the week-by-week odd ratio plot */
    layoutSubsWeeks() {
      return this.computeLayout(false)
    },

    /** Layout for the week-to-first-week odd ratio plot */
    layoutFirstWeekRef() {
      return this.computeLayout(true)
    }
  },

  methods: {
    /**
     * Compute the data for the odd ratio plots given a mutation
     * @param mut                 The mutation to be considered
     * @param referToFirstWeek    Flag to compute the odd ratio wrt to the first week
     * @returns {Object}  The data object for the odd ratio plot
     */
    computeData(mut, referToFirstWeek) {
      const yBeforeLog = this.computeY(mut, referToFirstWeek)

      return {
        name: mut['protein'] + '_' + mut['mut'],        //  mutation name for the legend
        x: [1, 2, 3, 4],                                //  weeks
        y: this.logY(yBeforeLog),         //  odd ratio for the 4 weeks

        // Hover label info
        meta: mut['protein'] + '_' + mut['mut'], //  mutation name for hover label
        customdata: this.computeReferences(mut, referToFirstWeek, yBeforeLog),   //  references for hover label
        hovertemplate:
            '%{meta}, %{y:.2f} (from %{customdata[0]}% to %{customdata[1]}%) <br />' +
            (referToFirstWeek
                ? 'The diffusion is %{customdata[2]:0%} compared to the first week'
                : 'The diffusion is %{customdata[2]:0%} compared to the previous week') +
            '<extra></extra>',
        hoverlabel: {
          bordercolor: 'transparent',
          font: {color: 'rgb(68,68,68)'}
        },

        // Marker and line styling
        marker: {
          size: 10,
          line: {width: 0}
        },
        line: {width: 3},
        type: 'scatter'
      }
    },

    /**
     * Computes the odd ratio values fot a given mutation over the analysis period
     * @param mut               The mutation to be considered
     * @param referToFirstWeek  Flag to compute the odd ratio wrt to the first week
     */
    computeY(mut, referToFirstWeek) {
      if (referToFirstWeek) {
        // The odd ratio is computed for each week wrt to the first one
        return [
          1,                                                // odd ratio w1-w1
          (mut['f1'] === 0) ? '-' : mut['f2'] / mut['f1'],  // odd ratio w2-w1
          (mut['f1'] === 0) ? '-' : mut['f3'] / mut['f1'],  // odd ratio w3-w1
          (mut['f1'] === 0) ? '-' : mut['f4'] / mut['f1']   // odd ratio w4-w1
        ]
      } else {
        // The odd ratio is computed for each week wrt to the previous one
        return [
          1,                                                // odd ratio w1-w1
          (mut['f1'] === 0) ? '-' : mut['f2'] / mut['f1'],  // odd ratio w2-w1
          (mut['f2'] === 0) ? '-' : mut['f3'] / mut['f2'],  // odd ratio w3-w2
          (mut['f3'] === 0) ? '-' : mut['f4'] / mut['f3']   // odd ratio w4-w3
        ]
      }
    },

    /**
     * Computes the log2 of the values for the odd ratio
     * @param yValues Array of 4 odd radio values (possibly '-' if not defined)
     */
    logY(yValues) {
      return yValues.map((oddRatio) => (oddRatio === 0 || oddRatio === '-') ? '-' : Math.log2(oddRatio))
    },

    /**
     * Compute additional custom data  for the plot labels for a given mutation.
     * @param mut               The mutation to be considered
     * @param referToFirstWeek  Flag to compute the odd ratio wrt to the first week
     * @param percValue         Percentage values for the weeks (i.e., y values before log)
     * @returns {Array} Array whose elements represent a step of the frequency change.
     */
    computeReferences(mut, referToFirstWeek, percValue) {
      if (referToFirstWeek) {
        // The odd ratio is computed for each week wrt to the first one
        const firstWeekFreq = mut['f1'].toPrecision(3)
        return [
          ['initial', firstWeekFreq, percValue[0]],     // [from,to,change] 1st week
          [firstWeekFreq, mut['f2'].toPrecision(3), percValue[1]], // [from,to,change] 2nd week
          [firstWeekFreq, mut['f3'].toPrecision(3), percValue[2]], // [from,to,change] 3rd week
          [firstWeekFreq, mut['f4'].toPrecision(3), percValue[3]]  // [from,to,change] 4th week
        ]
      } else {
        // The odd ratio is computed for each week wrt to the previous one
        return [
          ['initial', mut['f1'].toPrecision(3), percValue[0]],                // [from,to,change] 1st week
          [mut['f1'].toPrecision(3), mut['f2'].toPrecision(3), percValue[1]], // [from,to,change] 2nd week
          [mut['f2'].toPrecision(3), mut['f3'].toPrecision(3), percValue[2]], // [from,to,change] 3rd week
          [mut['f3'].toPrecision(3), mut['f4'].toPrecision(3), percValue[3]]  // [from,to,change] 4th week
        ]
      }
    },

    /**
     * Compute the data for the odd ratio plots given a mutation
     * @param referToFirstWeek   Flag to compute the odd ratio wrt to the first week
     * @returns {Object}  The portion of the object common to both the odd ratio plots
     */
    computeLayout(referToFirstWeek) {
      return {
        title: this.type === 2 ? (referToFirstWeek ? '<br>Log<sub>2</sub> odd ratio week-to-first-week' : '<br>Log<sub>2</sub> odd ratio week-by-week') : '',

        xaxis: {
          tickmode: 'array',
          tickvals: [1, 2, 3, 4],
          ticktext: // date labels
              [
                this.dateLabel['w1'], this.dateLabel['w2'],
                this.dateLabel['w3'], this.dateLabel['w4']
              ],
          tickfont: {size: 11},
          automargin: true, // auto-adjust margins for labels
          showline: false,  // hide bold bottom x-axis line
          zeroline: false   // hide bold zero line
        },

        yaxis: {
          tickfont: {size: 14},
          automargin: true, // auto-adjust margins for labels
          showline: false,  // hide bold bottom x-axis line
          zeroline: false   // hide bold zero line
        },

        legend: {
          x: 1.0,   // position to left
          y: 1.0,   // position to left
          bgcolor: 'trasparent',
          bordercolor: 'trasparent',
          yanchor: 'top',
          ticks: 'outside',
          itemsizing: 'constant'
        },
        colorway: palette, // color palette for the legend
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.1,
        hovermode: 'closest',

        height: this.getCurrentPlotRows.length >= 20 ? 430 : 390,  // plot height
        autosize: true,
        margin: {
          b: this.type === 2 && referToFirstWeek ? 50 : 40,
          t: this.type === 2 && referToFirstWeek ? 55 : 75,
          pad: 10
        }
      }
    }
  }
}
</script>

