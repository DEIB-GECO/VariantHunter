<!--
  Component:    ExplorerHistogram
  Description:  Barchart plot. Implemented using vue-plotly.

  Props:
  └── plotData:   Data for the plot. Required.
-->

<template>
  <div style='width: 100%;'>
    <!-- ExplorerHistogram plot -->
    <Plotly :data='data' :layout='layout' :displaylogo='false' :displayModeBar='true' />
  </div>
</template>

<script>
import { Plotly } from 'vue-plotly'

export default {
  name: 'ExplorerHistogram',
  components: {
    Plotly
  },
  props: {
    /** Raw data for the plot. Required. */
    plotData: { required: true }
  },
  data () {
    return {
      /** Currently selected time scale */
      timeScale: 'ALL'
    }
  },
  computed: {
    /** Values for the x-axis of the barchart: dates */
    x () {
      const startDate = new Date('2020-01-01')
      return this.plotData.map(element => {
        const date = new Date(startDate)
        // Dates from the server are relative and must be added to the start date
        date.setDate(startDate.getDate() + element['date'])
        return date
      })
    },

    /** Values for the y-axis of the barchart: seq_count */
    y () {
      return this.plotData.map(element => element['seq_count'])
    },

    /** Data processed for the histogram plot */
    dataHistogram () {
      return {
        x: this.x,
        y: this.y,
        mode: 'lines',
        type: 'bar',
        hovertemplate: '%{y} sequences<extra></extra>'
      }
    },

    /** Data processed for the lineage breakdown plot */
    dataBreakdown () {
      return {
        x: this.x,
        y: this.y,
        xaxis: 'x',
        yaxis: 'y2',
        mode: 'lines',
        type: 'bar',
        hovertemplate: '%{y} sequences<extra></extra>'
      }
    },

    /** Data processed for the whole plot */
    data () {
      return [this.dataHistogram, this.dataBreakdown]
    },

    /** Layout data for the plot */
    layout () {
      return {
        grid: {
          rows: 2,
          columns: 1,
          roworder: 'bottom to top'
        },
        height: 665, // 355
        xaxis: {
          rangeselector: this.selectorOptions,
          rangeslider: {},
          automargin: true,
          hoverformat: '%Y-%m-%d' // prevent hours info
        },
        yaxis: {
          autorange: true,
          fixedrange: false,
          automargin: true,
          domain: [0, 0.55]
        },
        xaxis2: {
          rangeselector: this.selectorOptions,
          rangeslider: {},
          automargin: true,
          hoverformat: '%Y-%m-%d' // prevent hours info
        },
        yaxis2: {
          autorange: true,
          fixedrange: false,
          automargin: true,
          domain: [0.66, 1]
        },
        margin: {
          b: 55,
          t: 30,
          pad: 4
        },
        annotations: [
          {
            text: 'First subplot',
            font: {
              size: 16
            },
            showarrow: false,
            align: 'center',
            y: 1.02,
            xref: 'paper',
            yref: 'paper'
          },
          {
            text: 'Second subplot',
            font: {
              size: 16
            },
            showarrow: false,
            align: 'center',
            y: 0.485,
            xref: 'paper',
            yref: 'paper'
          }
        ],
        showlegend: false,
        autosize: true
      }
    },

    /** Selector options for the plot */
    selectorOptions () {
      return {
        xanchor: 'center',
        x: 0.5,
        y: -0.4,
        buttons: [
          { step: 'all', label: 'ALL' },
          { step: 'day', stepmode: 'backward', count: 28, label: '4 WEEKS' },
          { step: 'month', stepmode: 'backward', count: 1, label: '1 MONTH' },
          { step: 'month', stepmode: 'backward', count: 6, label: '6 MONTHS' },
          { step: 'year', stepmode: 'backward', count: 1, label: '1 YEAR' }
        ]
      }
    }
  },
  mounted () {
    /** Capture the change of the selector status to track the timeScale value
     const that = this
     const buttons = document.querySelector('.rangeselector').querySelectorAll('.button')
     Array.from(buttons).forEach(b => {
      b.addEventListener('click', function (event) {
        that.timeScale = this.textContent
      })
    })*/
  }
}
</script>
