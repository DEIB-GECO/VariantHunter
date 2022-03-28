<!--
  Component:    Lineages breakdown
  Description:  Lineages breakdown plots. Implemented using vue-plotly.

  Props:
  └── lineagesData: Raw lineages' data for the lineage breakdown plot. Required.
-->

<template>
  <div class='plotly-container'>
    <!-- Lineage Breakdown plot -->
    <Plotly :data='data' :layout='layout' :displaylogo='false' :displayModeBar='false'/>
  </div>
</template>

<script>
import { Plotly } from 'vue-plotly'
import { diffToDate } from '@/utils/dateService'

export default {
  name: 'LineagesBreakdown',
  components: {
    Plotly
  },
  props: {
    /** Raw lineages' data for the lineage breakdown plot. Required. */
    lineagesData: { required: true }
  },
  computed: {
    /** Data processed for the plot */
    data () {
      return this.lineagesData.map(element => {
        return {
          x: element['data'].map(x => diffToDate(x.date)),
          y: element['data'].map(x => x.count),
          name: element['name'],
          stackgroup: 'one',
          barmode: 'stack',
          groupnorm: 'percent',
          line: { width: 0 },
          hovertemplate: '%{y:.0f}%'
        }
      })
    },

    /** Layout data for the plot */
    layout () {
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
