<template>
  <div style="width: 100%;">
    <div :id="'div_barchart_' + plotlyId" style="width: 100%; height: 500px;"><!-- Plotly chart will be drawn inside this DIV --></div>
  </div>
</template>

<script>
import {mapActions, mapMutations} from "vuex";

export default {
  name: "NewBarChart",
  props: {
    tableForLinePlot: {required: true,},
    plotlyId:{required: true,},
    title:{required: true},
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
    loadLinePlot() {
      const divId = `div_barchart_${this.plotlyId}`
      Plotly.purge(divId);

      if (this.myTimeout)
        clearTimeout(this.myTimeout);

      this.myTimeout = setTimeout(() => {
        var colors = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8',
          '#f58231', '#911eb4', '#42d4f4', '#f032e6',
          '#bfef45', '#fabed4', '#469990', '#dcbeff',
          '#9A6324', '#fffac8', '#800000', '#aaffc3',
          '#808000', '#ffd8b1', '#000075', '#a9a9a9']

        function get_trace(l, i) {
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
        }

        var data = this.tableForLinePlot.map((e, idx) => get_trace(e, idx))

        //var data = [get_trace(this.tableForLinePlot[1], 1), get_trace(this.tableForLinePlot[2], 2)]


        var layout = {
          colorway: colors,
          title: this.title,
          xaxis: {
            tickmode: "array", // If "array", the placement of the ticks is set via `tickvals` and the tick text is `ticktext`.
            tickvals: [1, 2, 3, 4],
            ticktext: ['28-22 days before', '21-15 days before', '14-8 days before', '7-0 days before']
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
            }
          },
          legend: {
            x: -0.3,
            y: 1.0,
            bgcolor: 'rgba(255, 255, 255, 0)',
            bordercolor: 'rgba(255, 255, 255, 0)'
          },
          barmode: 'group',
          bargap: 0.15,
          bargroupgap: 0.1
        };

        Plotly.newPlot(`div_barchart_${this.plotlyId}`, data, layout);
      }, 1000);
    }
  },
  mounted() {
    this.loadLinePlot()
  },
  watch: {
    tableForLinePlot(val, oldVal) {
      console.log("whatch su tableForLinePlot")
      this.loadLinePlot()
    }

  }
}





</script>

<style scoped>

</style>