<template>
  <div style="width: 100%;">
    <Plotly :data="data" :layout="layout"/>
  </div>
</template>

<script>

import {Plotly} from 'vue-plotly'

export default {
  name: "HeatMap",
  components: {
    Plotly
  },
  props: {
    tableForHeatMap: {required: true,},
    referenceDate: {required: true},
    plotlyId: {required: true,},
    title: {required: true},
  },
  data() {
    return {
      myTimeout: null,
    }
  },
  computed: {
    data() {
      return [
        {
          z: this.tableForHeatMap.map((e) => [e.f1, e.f2, e.f3, e.f4]),
          // x: ['28-22 days before', '21-15 days before', '14-8 days before', '7-0 days before'],
          x: [this.computeDateLabel(28, 22), this.computeDateLabel(21, 15), this.computeDateLabel(14, 8), this.computeDateLabel(7, 0)],
          y: this.tableForHeatMap.map((e) => e.protein + "_" + e.mut),
          zmax: 100,
          zmin: 0,
          type: 'heatmap',
          hoverongaps: false
        }
      ]
    },
    layout() {
      return {
        title: this.title,
        yaxis: {
          tickfont: {
            size: 14,
            color: 'rgb(68, 68, 68)'
          },
          automargin: true
        },
        xaxis: {
          automargin: true
        },

      }
    },
  },
  methods: {
    /**
     *
     * @param from
     * @param to
     */
    computeDateLabel(from, to) {
      const referenceDate = new Date(this.referenceDate);
      const fromDate = new Date(referenceDate);
      const toDate = new Date(referenceDate);

      fromDate.setDate(referenceDate.getDate() - from);
      toDate.setDate(referenceDate.getDate() - to);
      return fromDate.toISOString().slice(0, 10).replaceAll('-', '/') + " - " + toDate.toISOString().slice(0, 10).replaceAll('-', '/');
    },
    loadHeatmap() {
      /*
       const divId = `div_heatmap_${this.plotlyId}`
      Plotly.purge(divId);
      if (this.myTimeout)
        clearTimeout(this.myTimeout);

      this.myTimeout = setTimeout(() => {
        this.data = [
          {
            z: this.tableForHeatMap.map((e) => [e.f1, e.f2, e.f3, e.f4]),
            // x: ['28-22 days before', '21-15 days before', '14-8 days before', '7-0 days before'],
            x: [this.computeDateLabel(28, 22), this.computeDateLabel(21, 15), this.computeDateLabel(14, 8), this.computeDateLabel(7, 0)],
            y: this.tableForHeatMap.map((e) => e.protein + "_" + e.mut),
            zmax: 100,
            zmin: 0,
            type: 'heatmap',
            hoverongaps: false
          }
        ];

        this.layout = {
          title: this.title,
          yaxis: {
            tickfont: {
              size: 14,
              color: 'rgb(107, 107, 107)'
            }
          },
          margin: {
            l: 200
          }
        };/*
        Plotly.newPlot(divId, this.data, this.layout);
      }, 1000);*/
    }
  },
  mounted() {
    this.loadHeatmap()
  },
  watch: {
    tableForHeatMap(val, oldVal) {
      this.loadHeatmap()
    }

  }
}


</script>

<style scoped>
</style>