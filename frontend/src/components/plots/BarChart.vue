<!--
  Component:    BarChart
  Description:  Barchart plot. Implemented using vue-plotly.

  Props:
  ├── plotTitle:  Title for the plot. Required.
  ├── plotData:   Data for the plot. Required.
  └── dateLabel:  Array of data labels for the periods
-->

<template>
  <div style="width: 100%;">
    <!-- BarChart plot -->
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

    /** Title for the plot. Required. */
    plotTitle: {required: true},

    /** Data for the plot. Required. */
    plotData: {required: true},

    /** Array of data labels for the periods */
    dateLabel: {required: true}
  },
  computed: {

    /** Data processed for the plot */
    data() {
      return this.plotData.map((element) => {
        return {
          x: [1, 2, 3, 4],
          y: [element['f1'], element['f2'], element['f3'], element['f4']],
          name: element['protein'] + "_" + element['mut'],
          /*marker: { size: 10, symbol: "x"},*/
          showlegend: true,
          type: 'scatter'
        }
      })
    },

    /** Layout data for the plot */
    layout() {
      return {
        colorway:
            ['#e6194B', '#3cb44b', '#ffe119', '#4363d8',
              '#f58231', '#911eb4', '#42d4f4', '#f032e6',
              '#bfef45', '#fabed4', '#469990', '#dcbeff',
              '#9A6324', '#fffac8', '#800000', '#aaffc3',
              '#808000', '#ffd8b1', '#000075', '#a9a9a9'],
        title: this.plotTitle,
        xaxis:
            {
              tickmode: "array", // If "array", the placement of the ticks is set via "tickvals" and the tick text is "ticktext"
              tickvals: [1, 2, 3, 4],
              ticktext: [this.dateLabel[3], this.dateLabel[2], this.dateLabel[1], this.dateLabel[0]],
              automargin: true
            },
        yaxis:
            {
              title: 'Frequency',
              titlefont:
                  {
                    size: 16,
                    color: 'rgb(107, 107, 107)'
                  },
              tickfont:
                  {
                    size: 14,
                    color: 'rgb(107, 107, 107)'
                  },
              automargin: true
            },
        legend:
            {
              x: 1.0,
              y: 1.0,
              bgcolor: 'rgba(255, 255, 255, 0)',
              bordercolor: 'rgba(255, 255, 255, 0)',
              yanchor: "top",
              ticks: "outside"
            },
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.1
      }
    }
  }
}
</script>
