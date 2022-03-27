<!--
  Component:    ExplorerHistogram
  Description:  Lineage breakdown and sequence count plots. Implemented using vue-plotly.

  Props:
  ├── sequenceData:   Raw sequence data for the seq count plot. Required.
  └── lineagesData: Raw lineages' data for the lineage breakdown plot. Required.
-->

<template>
  <div style='width: 100%;'>
    <!-- Explorer Histogram plot -->
    <Plotly id='explorer' :data='dataHistogram' :layout='layoutHistogram' :displaylogo='false' :displayModeBar='false' @afterplot='updateListeners'/>

    <!-- Lineage Breakdown plot TODO split component -->
    <Plotly v-if='showLineageBreakdown' id='breakdown' :data='dataBreakdown' :layout='layoutBreakdown' :displaylogo='false' :displayModeBar='false'/>
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

      /** Currently selected time range */
      currentRange: null,

      /** Visibility flag for the lineage breakdown */
      showLineageBreakdown: false

    }
  },
  computed: {
    /** Data processed for the histogram plot */
    dataHistogram () {
      return [{
        x: this.sequenceData.map(element => diffToDate(element['date'])),
        y: this.sequenceData.map(element => element['seq_count']),
        mode: 'lines',
        type: 'bar',
        hovertemplate: '%{y} sequences<extra></extra>'
      }]
    },

    /** Data processed for the lineage breakdown plot */
    dataBreakdown () {
      console.log('UPDATING BREAKDOWN')
      console.log(this.lineagesData)
      return this.lineagesData.map(element => {
        return {
          x: element['data'].filter(x => x.count > 0).map(x => diffToDate(x.date)),
          y: element['data'].filter(x => x.count > 0).map(x => x.count),
          name: element['name'],
          stackgroup: 'one',
          barmode: 'stack',
          groupnorm: 'percent',
          line: { width: 0 },
          hovertemplate: '%{y:.0f}%'
        }
      })
    },

    /** Layout data for the histogram plot */
    layoutHistogram () {
      return {
        height: 370,
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
          b: 10,
          t: 20, // 68,
          pad: 40
        },
        showlegend: false,
        autosize: true
      }
    },

    /** Layout data for the lineage breakdown plot */
    layoutBreakdown () {
      return {
        title: '<sub>Lineages breakdown for lineages affecting at least 10% of the sequences of each day</sub>',
        colorway:
          [
            '#ef5378', '#5ee171', '#f3df67', '#6685f1',
            '#1def05', '#ff3f00', '#ffea00', '#003aff',
            '#ef8439', '#d46ff5', '#4fcbe7', '#f37fed',
            '#ff6900', '#9a02ff', '#00fff7', '#ff00f2',
            '#bbef39', '#fcb0ca', '#7ed7cd', '#ef479e',
            '#ffbc73', '#fffac8', '#c56100', '#aaffc3',
            '#808000', '#ffd8b1', '#575793', '#29b7d5',
            '#00c710', '#6b6868', '#b2b2b2', '#000000'
          ],
        height: 300,
        xaxis: {
          automargin: true,
          hoverformat: '%Y-%m-%d' // prevent hours info
        },
        yaxis: {
          ticksuffix: '%',
          autorange: true,
          fixedrange: false,
          automargin: true
        },
        margin: {
          b: 10,
          t: 20, // 68,
          pad: 40
        },
        showlegend: true,
        autosize: true
      }
    },

    /** Selector options for the plot */
    selectorOptions () {
      return {
        xanchor: 'center',
        x: 0.5,
        y: -1,
        buttons: [
          { step: 'all', label: 'ALL' },
          { step: 'day', stepmode: 'backward', count: 28, label: '4 WEEKS' },
          { step: 'month', stepmode: 'backward', count: 6, label: '6 MONTHS' },
          { step: 'year', stepmode: 'backward', count: 1, label: '1 YEAR' }
        ]
      }
    }
  },
  methods: {
    /** Adds the listeners for the range selectors and update the selected range */
    updateListeners () {
      /** Capture the change of the selector status to track the timeScale value*/
      const that = this
      try {
        // TODO fix not unique id
        const buttons = document.querySelector('.rangeselector').querySelectorAll('.button')
        Array.from(buttons).forEach(b => {
          console.log('Located')
          b.addEventListener('click', function (event) {
            console.log('event listener')
            that.timeScale = this.textContent
          })
        })
      } catch (ignored) {
        console.log('Unable to locate plotly commands' + ignored)
      // Not able to locate the plotly buttons. Graph is empty.
      }
      try {
        const range = document.getElementById('explorer').layout.xaxis.range
        this.currentRange = [range[0].substr(0, 10), range[1].substr(0, 10)]
      } catch (ignored) {
        console.log('Unable to fetch current range')
      // Not able to locate the plotly buttons. Graph is empty.
      }
    }

  },
  watch: {
    timeScale (newVal) {
      console.log('Scale change to ' + newVal)
      this.showLineageBreakdown = newVal === '4 WEEKS'
      if (this.showLineageBreakdown && newVal !== null) {
        console.log('emitting event with ' + newVal)
        this.$emit('lineageBreakdownRequest', this.currentRange)
      }
    },
    currentRange (newVal) {
      console.log('range changed to ' + newVal)
      if (this.showLineageBreakdown && newVal !== null) {
        console.log('emitting event with ' + newVal)
        this.$emit('lineageBreakdownRequest', newVal)
      }
    }
  }
}
</script>
