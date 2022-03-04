<!--
  Component:    HeatMap
  Description:  HeatMap plot. Implemented using vue-plotly.

  Props:
  ├── plotTitle:  Title for the plot. Required.
  ├── plotData:   Data for the plot. Required.
  └── dateLabel:  Array of data labels for the periods
-->

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

    /** Title for the plot. Required. */
    plotTitle: {required: true},

    /** Data for the plot. Required. */
    plotData: {required: true},

    /** Array of data labels for the periods */
    dateLabel: {required: true}
  },
  computed: {

    /** Values for the x axis of the heatmap */
    x() {
      return [this.dateLabel[3], this.dateLabel[2], this.dateLabel[1], this.dateLabel[0]]
    },

    /** Values for the y axis of the heatmap */
    y() {
      return this.plotData.map((element) => element['protein'] + "_" + element['mut'])
    },

    /** Values for the z axis of the heatmap */
    z() {
      return this.plotData.map((element) => [element['f1'], element['f2'], element['f3'], element['f4']])
    },

    /** Data processed for the plot */
    data() {
      return [
        {
          x: this.x,
          y: this.y,
          z: this.z,
          zmax: 100,
          zmin: 0,
          type: 'heatmap',
          hoverongaps: false
        }
      ]
    },

    /** Layout data for the plot */
    layout() {
      return {
        title: this.plotTitle,
        annotations: this.annotations,
        yaxis: {
          tickfont: {size: 14, color: 'rgb(68, 68, 68)'},
          automargin: true
        },
        xaxis: {automargin: true}
      }
    },

    /** Produce the annotations for the heatmap: z values to be displayed as annotations */
    annotations() {
      const annotations = [];
      for (var i = 0; i < this.y.length; i++) {
        for (var j = 0; j < this.x.length; j++) {
          var annotation = {
            xref: 'x1',
            yref: 'y1',
            x: this.x[j],
            y: this.y[i],
            text: this.z[i][j].toFixed(3),
            font: {
              color: 'white'
            },
            showarrow: false,
          };
          annotations.push(annotation);
        }
      }
      return annotations
    },
  }
}


</script>
