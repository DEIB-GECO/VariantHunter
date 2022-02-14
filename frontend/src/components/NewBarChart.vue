<template>
  <div style="width: 100%;">
    <div id='myDiv3' style="width: 100%; height: 500px;"><!-- Plotly chart will be drawn inside this DIV --></div>
  </div>
</template>

<script>
import {mapActions, mapMutations} from "vuex";

export default {
  name: "NewBarChart",
  props: {
    tableForLinePlot: {required: true,},
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
    loadLinePlot(){
      var colors = ['DarkSeaGreen', 'Bisque', 'Blue', 'ForestGreen',
      'Chocolate', 'DarkCyan', 'DarkKhaki', 'DarkKhaki',
      'DarkGreen', 'DarkSlateGrey', 'BurlyWood', 'Crimson']

    function get_trace(l, i) {
      var trace = {
        x: [1, 2, 3, 4],
        y: [l.f1, l.f2, l.f3, l.f4],
        name: l.protein + "_" + l.mut,
        marker: {color: colors[i]},
        type: 'scatter'
      };
      return trace
    }

    var data = this.tableForLinePlot.map((e, idx) => get_trace(e, idx))

    //var data = [get_trace(this.tableForLinePlot[1], 1), get_trace(this.tableForLinePlot[2], 2)]


    var layout = {
      title: 'Top 5 decreasing + Top 5 increasing mutations',
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

    Plotly.newPlot('myDiv3', data, layout);
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