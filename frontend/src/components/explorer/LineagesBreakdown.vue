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
import {Plotly} from 'vue-plotly'
import {diffToDate} from '@/utils/dateService'

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
        colorway:
            [
              '#ef5378', '#5ee171', '#f3df67', '#6685f1',
              '#1def05', '#ff3f00', '#ffea00', '#003aff',
              '#ef8439', '#d46ff5', '#4fcbe7', '#f37fed',
              '#ff6900', '#9a02ff', '#00fff7', '#ff00f2',
              '#bbef39', '#fcb0ca', '#7ed7cd', '#ef479e',
              '#ffbc73', '#fffac8', '#c56100', '#aaffc3',
              '#808000', '#ffd8b1', '#575793', '#29b7d5',
              '#099917', '#6b6868', '#b2b2b2', '#000000'
            ],
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
