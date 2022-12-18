<!--

  Component:    DiffusionHeatMap
  Description:  HeatMap plot. Implemented using vue-plotly.

-->

<template>
  <section-element icon='mdi-chart-gantt' assign-id="diffusion-heatmap"
                   title="Diffusion heatmap"
                   :subtitle="getCurrentPlotTitle"
                   caption="To visualize specific mutations, select the corresponding rows from the table"
                   :tabs='tabs' v-model="type">
    <!-- Heatmap app-tour -->
    <heatmap-intro/>

    <!-- Actual heatmap -->
    <div class="regular-plot" style="width: 100%;">
      <plotly :data='data' :layout='layout' :displaylogo='false'/>
    </div>
  </section-element>
</template>

<script>
import {Plotly} from '@rleys/vue-plotly'
import SectionElement from "@/components/analysis/SectionElement";
import {mapGetters} from "vuex";
import HeatmapIntro from "@/components/intros/HeatmapIntro";

export default {
  name: 'DiffusionHeatmap',
  components: {HeatmapIntro, SectionElement, Plotly},

  data() {
    return {
      /** Possible views */
      tabs: {
        0: {
          icon: 'mdi-percent-outline',
          title: 'Diffusion',
          subtitle: 'Regular heatmap',
          description: 'Regular heatmap with colors scaled between 1 and 100 based on the prevalence of amino acid ' +
              'changes (dark blue = low prevalence, red = high prevalence). ',
          hint: 'Best suited to quickly identify the most prevalent amino acid changes.'
        },
        1: {
          icon: 'mdi-speedometer',
          title: 'Growth speed',
          subtitle: 'Highlights trend',
          description: 'Heatmap with colors scaled based on the ratio between the minimum and maximum ' +
              'prevalence of every amino acid change. ',
          hint: 'Best suited to quickly identify amino acid changes that had an increase or ' +
              'decrease in prevalence (dark blue to red = increase; red to dark blue = decrease).'
        },
      },

      /**
       * Type of heatmap to be displayed.
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

    /** Values for the x-axis of the heatmap: dates periods */
    x() {
      return [this.dateLabel['w1'], this.dateLabel['w2'], this.dateLabel['w3'], this.dateLabel['w4']]
    },

    /** Values for the y-axis of the heatmap: protein_mut */
    y() {
      return this.getCurrentPlotRows.map(
          element => element['protein'] + '_' + element['mut']
      )
    },

    /** Values for the z-axis of the heatmap for the regular view: mutation frequencies in % */
    z() {
      return this.getCurrentPlotRows.map(element => [
        element['f1'], element['f2'], element['f3'], element['f4']
      ])
    },

    /** Values for the z-axis of the heatmap for the speed view: mutation frequencies in % divided by the minimum */
    zSpeed() {
      return this.getCurrentPlotRows.map(({f1, f2, f3, f4}) => {
        const min = Math.min(f1, f2, f3, f4)
        return [((f1 + 1) / (min + 1)), ((f2 + 1) / (min + 1)), ((f3 + 1) / (min + 1)), ((f4 + 1) / (min + 1))]
      })
    },

    /** Absolute value for the z-axis of the heatmap */
    absValue() {
      return this.getCurrentPlotRows.map(element => [
        element['w1'], element['w2'], element['w3'], element['w4']
      ])
    },

    /** Data processed for the plot */
    data() {
      return [
        {
          x: this.x,
          y: this.y,
          z: this.type === 0 ? this.z : this.zSpeed,
          customdata: this.absValue,

          hovertemplate:
              'Period:     %{x}<br>Mutation:  %{y}<br>Diffusion:  %{z:.2f}%  (%{customdata})<extra></extra>',
          zmax: this.type === 0 ? 100 : undefined,
          zmin: this.type === 0 ? 0 : undefined,
          type: 'heatmap',
          hoverongaps: false,
          //showscale: this.type === 0,
        }
      ]
    }
    ,

    /** Layout data for the plot */
    layout() {
      return {
        height: this.getCurrentPlotRows.length * 25 + 250,
        // title: this.getCurrentPlotTitle,
        annotations: this.annotations,
        yaxis: {
          tickfont: {size: 14},
          automargin: true
        },
        xaxis: {automargin: true},
        hovermode: 'closest',
        margin: {
          b: 50,
          t: 55,
          pad: 10
        },
        autosize: true
      }
    }
    ,

    /** Produce the annotations for the heatmap: z values to be displayed as annotations */
    annotations() {
      const annotations = []
      for (let i = 0; i < this.y.length; i++) {
        for (let j = 0; j < this.x.length; j++) {
          const annotation = {
            xref: 'x1',
            yref: 'y1',
            x: this.x[j],
            y: this.y[i],
            text: this.z[i][j].toPrecision(3) + '%',
            font: {
              color: 'white'
            },
            showarrow: false
          }
          annotations.push(annotation)
        }
      }
      return annotations
    }
  }
}
</script>
