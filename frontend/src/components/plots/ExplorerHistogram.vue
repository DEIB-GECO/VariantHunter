<!--
  Component:    ExplorerHistogram
  Description:  Sequences counts and lineages breakdown plots. Implemented using vue-plotly.

  Props:
  └──  sequenceData:   Raw sequence data for the seq count plot. Required.

  Events:
  └──  timeRangeChange:   Emitted whenever the timerange selected changes, together with the new value.

-->

<template>
  <div class='plotly-container'>
    <!-- Explorer Histogram plot -->
    <Plotly :id='_uid.toString()' :data='data' :layout='layout' :displaylogo='false'
            :displayModeBar='false' @afterplot='updateTimeRange'/>
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
    sequenceData: { required: true }
  },
  data () {
    return {
      /** Currently selected timescale */
      timeScale: 'ALL',

      /** Currently selected time range */
      timeRange: null
    }
  },
  computed: {
    /** Data processed for the plot */
    data () {
      return [{
        x: this.sequenceData.map(element => diffToDate(element['date'])),
        y: this.sequenceData.map(element => element['seq_count']),
        mode: 'lines',
        type: 'bar',
        hovertemplate: '%{y} sequences<extra></extra>'
      }]
    },

    /** Layout data for the plot */
    layout () {
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
          t: 20,
          pad: 40
        },
        showlegend: false,
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
    /** Update the selected time range */
    updateTimeRange () {
      try {
        const range = document.getElementById(this._uid.toString()).layout.xaxis.range
        this.timeRange = [range[0].substr(0, 10), range[1].substr(0, 10)]
      } catch (ignored) {
        console.log('Unable to fetch current range')
        // Not able to locate plotly.
      }
    }

  },
  watch: {
    /** On time range changes emit new value */
    timeRange (newVal, oldVal) {
      if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
        this.$emit('timeRangeChange', newVal)
      }
    }
  }
}
</script>
