<!--
  Component:    LineChart
  Description:  Barchart plot. Implemented using vue-plotly.

  Props:
  ├── plotTitle:  Title for the plot. Required.
  ├── plotData:   Data for the plot. Required.
  ├── dateLabel:  Array of data labels for the periods
  └── weekSeq:    Total number of sequences collected per week
-->

<template>
  <div class='regular-plot plotly-container'>

    <!-- LineChart plot -->
    <Plotly :data='data' :layout='layout' :displaylogo='false'
            :modeBarButtonsToRemove="['lasso2d', 'select2d', 'toggleSpikelines']" />

    <!-- Markers/lines Dialog -->
    <v-container class='plot-controls'>
      <v-layout justify-center row wrap>
        <DialogOpener :button-prefix='false' title='Chart interpretation'>
          <ul class='ul-table'>
            <li class='li-table'>
              <div class='li-name'>Cross marker<br />
                <v-icon>mdi-close-thick</v-icon>
              </div>
              <div class='li-content'>It is used to represent points supported by 5 or fewer observations.</div>
            </li>
            <li class='li-table'>
              <div class='li-name'>Circle marker<br />
                <v-icon>mdi-circle</v-icon>
              </div>
              <div class='li-content'>It is used to represent points supported by more than 5 observations.</div>
            </li>
            <li class='li-table'>
              <div class='li-name'>Solid line<br />
                <v-icon>mdi-minus-thick</v-icon>
              </div>
              <div class='li-content'>It is used to represent mutations such that for at least one week
                the observations are greater than 5.
              </div>
            </li>
            <li class='li-table'>
              <div class='li-name'>Dashed line<br />
                <v-icon>mdi-dots-horizontal</v-icon>
              </div>
              <div class='li-content'>It is used to represent mutations such that for all the 4 weeks the
                observations are 5 or less.
              </div>
            </li>
          </ul>
        </DialogOpener>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import { Plotly } from 'vue-plotly'
import DialogOpener from '@/components/general/DialogOpener'

export default {
  name: 'LineChart',
  components: {
    DialogOpener,
    Plotly
  },
  props: {
    /** Title for the plot. Required. */
    plotTitle: { required: true },

    /** Raw data for the plot. Required. */
    plotData: { required: true },

    /** Array of data labels for the periods */
    dateLabel: { required: true },

    /** Total number of sequences collected per week */
    weekSeq: { required: true }
  },
  computed: {
    /** Data processed for the plot */
    data () {
      return this.plotData.map(element => {
        return {
          x: [1, 2, 3, 4],
          y: [element['f1'], element['f2'], element['f3'], element['f4']],
          name: element['protein'] + '_' + element['mut'],
          customdata: [element['w1'], element['w2'], element['w3'], element['w4']],
          meta: element['protein'] + '_' + element['mut'],
          hovertemplate: '%{meta}, %{customdata}, %{y:.1f}% <extra></extra>',
          hoverlabel: {
            bordercolor: 'transparent',
            font: {
              color: 'rgb(68,68,68)'
            }
          },
          marker: {
            size: 10,
            symbol: this.computeMarkerSymbol(element),
            line: { width: 0 }
          },
          line: this.computeLineStyle(element),
          showlegend: true,
          type: 'scatter'
        }
      })
    },

    /** Layout data for the plot */
    layout () {
      return {
        height: this.plotData.length >= 20 ? 530 : 490,
        colorway:
          [
            '#ef5378', '#5ee171', '#f3df67', '#6685f1',
            '#fda05f', '#d46ff5', '#71daf1', '#f37fed',
            '#cfee82', '#fcb0ca', '#7ed7cd', '#dac4f8',
            '#efc69a', '#fffac8', '#d24f32', '#aaffc3',
            '#808000', '#ffd8b1', '#575793', '#a9a9a9'
          ],
        title: this.plotTitle,
        xaxis: {
          tickmode: 'array',
          tickvals: [1, 2, 3, 4],
          ticktext: this.computeEnrichedLabels(),
          tickfont: {
            size: 11
          },
          automargin: true,
          showline: false,
          zeroline: false
        },
        yaxis: {
          title: 'Frequency in %',
          titlefont: {
            size: 16
          },
          tickfont: {
            size: 14
          },
          range: [0, 100],
          dtick: 10,
          zeroline: false,
          showline: false,
          automargin: true
        },
        legend: {
          x: 1.0,
          y: 1.0,
          bgcolor: 'trasparent',
          bordercolor: 'trasparent',
          yanchor: 'top',
          ticks: 'outside',
          itemsizing: 'constant'
        },
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.1,
        hovermode: 'closest',
        margin: {
          b: 50,
          t: 75,
          pad: 10
        },
        autosize: true
      }
    }
  },
  methods: {
    /**
     * Compute enriched labels for the x-axis containing period and total period samples
     * @returns {Array} An array containing the 4 labels
     */
    computeEnrichedLabels () {
      const labels = []
      for (let i = 1; i <= 4; i++) {
        labels.push(
          '<br>' + this.dateLabel['w' + i] + '<br>Tot. seq.: ' + this.weekSeq[i - 1]
        )
      }
      return labels
    },

    /**
     * Compute the markers' symbol for a given row based on the number of observations
     * @param element   The row to be considered
     * @returns {Array} An array of markers' symbols ('X' if #observations<6, otherwise 'O')
     */
    computeMarkerSymbol (element) {
      const symbols = []
      for (let i = 1; i <= 4; i++) {
        symbols.push(element['w' + i] < 6 ? 'x' : 'circle')
      }
      return symbols
    },

    /**
     * Compute the line style for a given row based on the number of observations
     * @param element   The row to be considered
     * @returns {Object} Dashed style if all the 4 points have less than 6 observations
     */
    computeLineStyle (element) {
      let style = { width: 3 }
      if (element['w1'] < 6 && element['w2'] < 6 && element['w3'] < 6 && element['w4'] < 6) {
        style = { width: 3, dash: 'dash' }
      }
      return style
    }
  }
}
</script>
<style scoped>

/* Custom style for the list in the dialog */
li {
  padding-bottom: 25px;
}

ul {
  list-style-type: none;
}

/* Button spacing options */
.plot-controls {
  padding-bottom: 15px;
}
</style>

<style>
/* Overwite plotly rules to hide legend markers */
.legendsymbols {
  display: none !important;
}
</style>
