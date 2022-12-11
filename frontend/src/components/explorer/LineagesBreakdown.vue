<!--
  Component:    Lineages breakdown
  Description:  Lineages breakdown plots. Implemented using vue-plotly.

  Props:
  └── lineagesData: Raw lineages' data for the lineage breakdown plot.

-->

<template>
  <v-col class='plotly-container'>
    <!-- Lineage Breakdown plot -->
    <plotly :data='data' :layout='layout' :displaylogo='false' :displayModeBar='false'/>
  </v-col>
</template>

<script>
import {Plotly} from '@rleys/vue-plotly'
import {diffToDate} from '@/utils/dateService'
import {palette} from "@/utils/colorService";

export default {
  name: 'LineagesBreakdown',
  components: {Plotly},

  props: {
    /** Raw lineages' data for the lineage breakdown plot. */
    lineagesData: {required: true}
  },

  computed: {
    /** Data processed for the plot */
    data() {
      return Object.entries(this.lineagesData).sort().map(element => {
        return {
          x: Object.keys(element[1]).map(x => diffToDate(parseInt(x))),
          y: Object.values(element[1]),
          name: element[0],
          stackgroup: 'one',
          barmode: 'stack',
          groupnorm: 'percent',
          line: {width: 0},
          hovertemplate: '%{y:.0f}%'
        }
      })
    },

    /** Layout data for the plot */
    layout() {
      return {
        title: '<sub>Daily lineage breakdown</sub>',
        colorway: palette,
        height: 400,
        xaxis: {
          automargin: true,
          hoverformat: '%Y-%m-%d' // prevent hours info
        },
        yaxis: {
          ticksuffix: '%',    // attach % symbol to y-axis values
          autorange: true,
          fixedrange: false,
          automargin: true
        },
        margin: {
          b: 10,
          t: 30,
          pad: 35
        },
        showlegend: true,
        autosize: true
      }
    }
  }
}
</script>
