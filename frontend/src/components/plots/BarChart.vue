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
    <Plotly :data="data" :layout="layout" :displaylogo="false"
            :modeBarButtonsToRemove="['lasso2d','select2d','toggleSpikelines']"/>
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

    /** Data for the plot. Required. */
    plotData: {required: true},

  },
  computed: {

    /** Data processed for the plot */
    data() {
      return this.plotData.map((element) => {
        return {
          x: [1, 2, 3, 4],
          y: [100, 200, 300, 400],
          hovertemplate: 'y',
          hoverlabel: {
            bordercolor: 'transparent',
            font: {
              color: "rgb(68,68,68)"
            }
          },
          showlegend: true,
          type: 'bar'
        }
      })
    },

    /** Layout data for the plot */
    layout() {
      return {
        title: "Available sequences",
        xaxis:
            {
              tickmode: "array", // If "array", the placement of the ticks is set via "tickvals" and the tick text is "ticktext"
              tickvals: [1, 2, 3, 4],
              // ticktext: [],
              tickfont:
                  {
                    size: 11,
                  },
              automargin: true,
              showline: false,
              zeroline: false
            },
        yaxis:
            {
              title: 'Frequency in %',
              titlefont:
                  {
                    size: 16,
                  },
              tickfont:
                  {
                    size: 14,
                  },

              dtick: 10,
              zeroline: false,
              showline: false,
              automargin: true
            },
        legend:
            {
              x: 1.0,
              y: 1.0,
              bgcolor: 'trasparent',
              bordercolor: 'trasparent',
              yanchor: "top",
              ticks: "outside",
              itemsizing: 'constant'
            },
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.1,
        hovermode: "closest"
      }
    },
  },
  methods: {}
}
</script>
<style scoped>

/* Plotly container */
.plotly-container {
  border-radius: var(--border-radius);
  width: 100%;
  background: white;
}

</style>
