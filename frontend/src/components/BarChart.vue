<template>
  <div style="width: 100%;">
    <Plotly :data="data" :layout="layout"/>
  </div>
</template>

<script>

import {Plotly} from 'vue-plotly'

export default {
  name: "BarChart",
  components: {
    Plotly
  },
  props: {
    tableForLinePlot: {required: true,},
    referenceDate: {required: true},
    plotlyId:{required: true,},
    title:{required: true},
  },
  data() {
    return {
    }
  },
  computed:{
    data(){
      return this.tableForLinePlot.map((e, idx) => this.get_trace(e, idx))
    },
    layout() {
      return {
        colorway: ['#e6194B', '#3cb44b', '#ffe119', '#4363d8',
          '#f58231', '#911eb4', '#42d4f4', '#f032e6',
          '#bfef45', '#fabed4', '#469990', '#dcbeff',
          '#9A6324', '#fffac8', '#800000', '#aaffc3',
          '#808000', '#ffd8b1', '#000075', '#a9a9a9'],
        title: this.title,
        xaxis: {
          tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
          tickvals: [1, 2, 3, 4],
          //ticktext: ['28-22 days before', '21-15 days before', '14-8 days before', '7-0 days before']
          ticktext: [this.computeDateLabel(28, 22), this.computeDateLabel(21, 15), this.computeDateLabel(14, 8), this.computeDateLabel(7, 0)],
          automargin: true
        },
        yaxis: {
          title: 'Frequency',
          titlefont: {
            size: 16,
            color: 'rgb(107, 107, 107)'
          },
          tickfont: {
            size: 14,
            color: 'rgb(107, 107, 107)'
          },
          automargin: true
        },
        legend: {
          x: 1.0,
          y: 1.0,
          bgcolor: 'rgba(255, 255, 255, 0)',
          bordercolor: 'rgba(255, 255, 255, 0)',
          yanchor:"top",
          ticks:"outside"
        },
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.1
      }
    }
  },
  methods: {
    get_trace(l, i) {
          var trace = {
            x: [1, 2, 3, 4],
            y: [l.f1, l.f2, l.f3, l.f4],
            name: l.protein + "_" + l.mut,
            //set showlegend to true, otherwise, with only one element it doesn't show it.
            showlegend: true,
            // marker: {color: colors[i]},
            type: 'scatter'
          };
          return trace
        },
    computeDateLabel(from, to) {
      const referenceDate = new Date(this.referenceDate);
      const fromDate = new Date(referenceDate)
      const toDate = new Date(referenceDate)

      fromDate.setDate(referenceDate.getDate() - from);
      toDate.setDate(referenceDate.getDate() - to);
      return fromDate.toISOString().slice(0, 10).replaceAll('-', '/') + " - " + toDate.toISOString().slice(0, 10).replaceAll('-', '/');
    }
  }
}
</script>

<style scoped>

</style>