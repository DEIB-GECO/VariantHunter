<!--
  Component:    BarChart
  Description:  Barchart plot. Implemented using vue-plotly.

  Props:
  └── plotData:   Data for the plot. Required.
-->

<template>
  <div style="width: 100%;">
    <!-- BarChart plot -->
    <Plotly :data='data' :layout='layout' :displaylogo='false' :displayModeBar='false' />
  </div>
</template>

<script>
import { Plotly } from 'vue-plotly'

export default {
  name: 'BarChart',
  components: {
    Plotly
  },
  props: {
    /** Raw data for the plot. Required. */
    plotData: { required: true }
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

    /** Data processed for the plot */
    data () {
      return [
        {
          x: this.x,
          y: this.y,
          mode: 'lines',
          type: 'bar',
          hovertemplate: '%{y} sequences<extra></extra>'
        }
      ]
    },

    /** Layout data for the plot */
    layout () {
      return {
        height: 355,
        xaxis: {
          rangeselector: this.selectorOptions,
          rangeslider: {},
          automargin: true,
          hoverformat: '%Y-%m-%d' // prevent hours info
        },
        yaxis: {
          autorange: true,
          fixedrange: false,
          automargin: true
        },
        margin: {
          b: 55,
          t: 30,
          pad: 4
        }
      }
    },

    /** Selector options for the plot */
    selectorOptions () {
      return {
        xanchor: 'center',
        x: 0.5,
        y: -0.8,
        buttons: [
          { step: 'all', label: 'ALL' },
          { step: 'day', stepmode: 'backward', count: 28, label: '4 WEEKS' },
          { step: 'month', stepmode: 'backward', count: 1, label: '1 MONTH' },
          { step: 'month', stepmode: 'backward', count: 6, label: '6 MONTHS' },
          { step: 'year', stepmode: 'backward', count: 1, label: '1 YEAR' }
        ]
      }
    }
  }
}
</script>
