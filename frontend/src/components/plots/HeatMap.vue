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

    /** Data processed for the plot */
    data() {
      return this.plotData.map((element) => {
        return {
          x: [this.dateLabel[3], this.dateLabel[2], this.dateLabel[1], this.dateLabel[0]],
          y: element['protein'] + "_" + element['mut'],
          z: [element['f1'], element['f2'], element['f3'], element['f4']],
          zmax: 100,
          zmin: 0,
          type: 'heatmap',
          hoverongaps: false
        }
      })
    },

    /** Layout data for the plot */
    layout() {
      return {
        title: this.plotTitle,
        yaxis:
            {
              tickfont:
                  {
                    size: 14,
                    color: 'rgb(68, 68, 68)'
                  },
              automargin: true
            },
        xaxis:
            {
              automargin: true
            }
      }
    },
  }
}


</script>
