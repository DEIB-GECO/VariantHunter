<!--
  Component:    ExplorerHistogram
  Description:  Lineage breakdown and sequence count plots. Implemented using vue-plotly.

  Props:
  ├── sequenceData:   Raw sequence data for the seq count plot. Required.
  └── lineagesData: Raw lineages' data for the lineage breakdown plot. Required.
-->

<template>
  <div style='width: 100%;' @mousemove='show'>
    <!-- ExplorerHistogram plot -->
    <Plotly id='explorer' :data='data' :layout='layout' :displaylogo='false' :displayModeBar='true' />
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
    /** Raw sequence data for the seq count plot. Required. */
    sequenceData: { required: true },

    /** Raw lineages' data for the lineage breakdown plot. Required. */
    lineagesData: { required: true }
  },
  data () {
    return {
      /** Currently selected timescale */
      timeScale: 'ALL'
    }
  },
  computed: {
    /** Values for the x-axis of the barchart: dates */
    x () {
      const startDate = new Date('2020-01-01')
      return this.sequenceData.map(element => {
        const date = new Date(startDate)
        // Dates from the server are relative and must be added to the start date
        date.setDate(startDate.getDate() + element['date'])
        return date
      })
    },

    /** Values for the y-axis of the barchart: seq_count */
    y () {
      return this.sequenceData.map(element => element['seq_count'])
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
      return this.lineagesData.map(element => {
        // const startDate = new Date('2020-01-01')
        // const date = new Date(startDate)
        // date.setDate(startDate.getDate() + element['date'])

        return {

        }
      })
      return [
        { x: ['2022-01-01', '2022-01-02', '2022-01-03'], y: [2, 1, 4], stackgroup: 'one', groupnorm: 'percent', xaxis: 'x',
          yaxis: 'y2' },
        { x: ['2022-01-01', '2022-01-02', '2022-01-03'], y: [1, 1, 2], stackgroup: 'one', xaxis: 'x',
          yaxis: 'y2' },
        { x: ['2022-01-01', '2022-01-02', '2022-01-03'], y: [3, 0, 2], stackgroup: 'one', xaxis: 'x',
          yaxis: 'y2' }
      ]
      // return {
      //   x: this.x,
      //   y: this.y,
      //   xaxis: 'x',
      //   yaxis: 'y2',
      //   mode: 'lines',
      //   type: 'bar',
      //   hovertemplate: '%{y} sequences<extra></extra>'
      // }
    },

    /** Data processed for the whole plot */
    data () {
      const data = [this.dataHistogram]
      return data.concat(this.dataBreakdown)
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
          domain: [0.66, 0.97]
        },
        margin: {
          b: 55,
          t: 30,
          pad: 4
        },
        annotations: [
          {
            text: 'LINEAGES BREAKDOWN<br><b><sub>THIS FEATURE IS NOT YET AVAILABLE</sub></b>',
            font: { size: 14 },
            showarrow: false,
            align: 'center',
            y: 1.015,
            xref: 'paper',
            yref: 'paper'
          },
          {
            text: 'SEQUENCE COUNTS',
            font: { size: 14 },
            showarrow: false,
            align: 'center',
            y: 0.575,
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
  methods: {
    show () {
      // const gd = document.getElementById('explorer')
      // console.log(gd.layout.xaxis.range)
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
