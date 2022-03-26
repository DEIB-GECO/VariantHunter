<!--
  Component:    ExplorerHistogram
  Description:  Lineage breakdown and sequence count plots. Implemented using vue-plotly.

  Props:
  ├── sequenceData:   Raw sequence data for the seq count plot. Required.
  └── lineagesData: Raw lineages' data for the lineage breakdown plot. Required.
-->

<template>
  <div style='width: 100%;'>
    <!-- ExplorerHistogram plot -->
    <Plotly id='explorer' :data='data' :layout='layout' :displaylogo='false' :displayModeBar='true' />
  </div>
</template>

<script>
import { Plotly } from 'vue-plotly'
import { diffToDate } from '@/utils/dateService'

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
      timeScale: 'ALL',

      /** Visibility flag for the lineage breakdown */
      showLineageBreakdown: false
    }
  },
  computed: {
    /** Data processed for the histogram plot */
    dataHistogram () {
      return {
        x: this.sequenceData.map(element => diffToDate(element['date'])),
        y: this.sequenceData.map(element => element['seq_count']),
        mode: 'lines',
        type: 'bar',
        hovertemplate: '%{y} sequences<extra></extra>'
      }
    },

    /** Data processed for the lineage breakdown plot */
    dataBreakdown () {
      return this.lineagesData.map(element => {
        return {
          x: element['data'].map(x => diffToDate(x.date)),
          y: element['data'].map(x => x.count),
          name: element['name'],
          // stackgroup: 'one',
          type: 'bar',
          barmode: 'stack',
          groupnorm: 'percent',
          xaxis: 'x',
          yaxis: 'y2',
          hoveron: 'points+fills',
          line: { width: 0 }
        }
      })

      //   hovertemplate: '%{y} sequences<extra></extra>'
    },

    /** Data processed for the whole plot */
    data () {
      const data = [this.dataHistogram]
      return data/* .concat(this.dataBreakdown)*/
    },

    /** Layout data for the plot */
    layout () {
      return {
        /* grid: {
          rows: 2,
          columns: 1,
          roworder: 'bottom to top'
        },*/
        height: /* 765, */ 355,
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
          /* domain: [0, 0.55]*/
        },
        /* yaxis2: {
          autorange: true,
          fixedrange: false,
          automargin: true,
          domain: [0.66, 0.97]
        },*/
        margin: {
          b: 55,
          t: 30,
          pad: 4
        },
        annotations: [
          /* {
            text: 'LINEAGES BREAKDOWN <br><sub>NOT AVAILABLE</sub>',
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
          }*/
        ],
        hovermode: 'closest',
        showlegend: false,
        autosize: true
      }
    },

    /** Selector options for the plot */
    selectorOptions () {
      return {
        xanchor: 'center',
        x: 0.5,
        y: -0.8, /* -0.4,*/
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
    manageRangeChange () {
      // TODO @mousemove=''
      // const gd = document.getElementById('explorer')
      // console.log(gd.layout.xaxis.range)
    }
  },
  updated () {
    /** Capture the change of the selector status to track the timeScale value*/
    const that = this
    try {
      const buttons = document.querySelector('.rangeselector').querySelectorAll('.button')
      Array.from(buttons).forEach(b => {
        b.addEventListener('click', function (event) {
          that.timeScale = this.textContent
        })
      })
    } catch (ignored) {
      // Not able to locate the plotly buttons. Graph is empty.
    }
  },
  watch: {
    timeScale (newVal) {
      this.showLineageBreakdown = newVal === '4 WEEKS'
    }
  }
}
</script>
