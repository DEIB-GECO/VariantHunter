<template>
  <div style="width: 100%;">
    <div :id="'div_heatmap_' + plotlyId" style="width: 100%; height: 500px;"><!-- Plotly chart will be drawn inside this DIV --></div>
  </div>
</template>

<script>
import {mapActions, mapMutations} from "vuex";

export default {
  name: "NewHeatMap",
  props: {
    tableForHeatMap: {required: true,},
    plotlyId: {required: true,},
  },
  data() {
    return {
      overlay: false,
      allGeo: null,
      selectedGeo: 'world',
      possibleGeo: ['world', 'continent', 'country', 'region'],
      selectedSpecificGeo: null,
      possibleSpecificGeo: [],

      selectedLineage: null,
      possibleLineage: [],

      expansionPanels: [],

      rowsTableSubPlaces: [],
    }
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    loadHeatmap(){

      var data = [
        {
          z: this.tableForHeatMap.map((e) => [e.f1, e.f2, e.f3, e.f4]),
          x: ['28-22 days before', '21-15 days before', '14-8 days before', '7-0 days before'],
          y: this.tableForHeatMap.map((e) => e.protein + "_" + e.mut),
          type: 'heatmap',
          hoverongaps: false
        }
      ];

      var layout = {
      title: 'Top 5 decreasing + Top 5 increasing mutations',
      yaxis: {
        tickfont: {
          size: 14,
          color: 'rgb(107, 107, 107)'
        }
      },
        margin:{
        l:200
        }
    };

      Plotly.newPlot(`div_heatmap_${this.plotlyId}`, data, layout);

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