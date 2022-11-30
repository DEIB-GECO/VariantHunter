<!--
  Component:    HeatMap
  Description:  HeatMap plot. Implemented using vue-plotly.

  Props:
  ├── plotTitle:  Title for the plot. Required.
  ├── plotData:   Data for the plot. Required.
  └── dateLabel:  Array of data labels for the periods
-->

<template>
  <section-element icon='mdi-chart-gantt' assign-id="diffusion-heatmap"
                   title="Diffusion heatmap"
                   :subtitle="plotTitle"
                   caption="To visualize specific mutations, select the corresponding rows from the table">
    <heatmap-intro/>
    <div class="regular-plot" style="width: 100%;">
      <Plotly :data='data' :layout='layout' :displaylogo='false'/>
    </div>
  </section-element>
</template>

<script>
import {Plotly} from 'vue-plotly'
import SectionElement from "@/components/analysis/SectionElement";
import {mapGetters} from "vuex";
import HeatmapIntro from "@/components/intros/HeatmapIntro";

export default {
  name: 'DiffusionHeatmap',
  components: {
    HeatmapIntro,
    SectionElement,
    Plotly
  },
  props: {},
  computed: {
    ...mapGetters(['getCurrentPlotRows', 'getCurrentPlotTitle', 'getCurrentAnalysis']),

    plotData() {
      return this.getCurrentPlotRows
    },

    plotTitle() {
      return this.getCurrentPlotTitle
    },

    dateLabel() {
      return this.getCurrentAnalysis.query.weeks
    },

    /** Values for the x-axis of the heatmap: dates periods */
    x() {
      return [this.dateLabel['w1'], this.dateLabel['w2'], this.dateLabel['w3'], this.dateLabel['w4']]
    },

    /** Values for the y-axis of the heatmap: protein_mut */
    y() {
      return this.plotData.map(
          element => element['protein'] + '_' + element['mut']
      )
    },

    /** Values for the z-axis of the heatmap: mutation frequencies in % */
    z() {
      return this.plotData.map(element => [
        element['f1'], element['f2'], element['f3'], element['f4']
      ])
    },

    /** Absolute value for the z-axis of the heatmap */
    absValue() {
      return this.plotData.map(element => [
        element['w1'], element['w2'], element['w3'], element['w4']
      ])
    },

    /** Data processed for the plot */
    data() {
      return [
        {
          x: this.x,
          y: this.y,
          z: this.z,
          customdata: this.absValue,
          hovertemplate:
              'Period:     %{x}<br>Mutation:  %{y}<br>Diffusion:  %{z:.2f}%  (%{customdata})<extra></extra>',
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
        height: this.plotData.length * 25 + 250,
        // title: this.plotTitle,
        annotations: this.annotations,
        yaxis: {
          tickfont: {size: 14},
          automargin: true
        },
        xaxis: {automargin: true},
        hovermode: 'closest',
        margin: {
          b: 50,
          t: 55,
          pad: 10
        },
        autosize: true
      }
    },

    /** Produce the annotations for the heatmap: z values to be displayed as annotations */
    annotations() {
      const annotations = []
      for (let i = 0; i < this.y.length; i++) {
        for (let j = 0; j < this.x.length; j++) {
          const annotation = {
            xref: 'x1',
            yref: 'y1',
            x: this.x[j],
            y: this.y[i],
            text: this.z[i][j].toPrecision(3) + '%',
            font: {
              color: 'white'
            },
            showarrow: false
          }
          annotations.push(annotation)
        }
      }
      return annotations
    }
  }
}
</script>
