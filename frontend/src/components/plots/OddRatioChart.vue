<!--
  Component:    OddRatioChart
  Description:  Plot of the odd ratio for the diffusion data. Implemented using vue-plotly.

  Props:
  ├── plotTitle:  Title for the plot. Required.
  ├── plotData:   Data for the plot. Required.
  ├── dateLabel:  Array of data labels for the periods
  └── weekSeq:    Total number of sequences collected per week
-->

<template>
  <div style='width: 100%;'>
    <Plotly :data='data' :layout='layout' :displaylogo='false'
            :modeBarButtonsToRemove="['lasso2d', 'select2d', 'toggleSpikelines']"  />
  </div>
</template>

<script>
import { Plotly } from 'vue-plotly'

export default {
  name: 'OddRatioChart',
  components: {
    Plotly
  },
  props: {
    /** Title for the plot. Required. */
    plotTitle: { required: true },

    /** Raw data for the plot. Required. */
    plotData: { required: true },

    /** Array of data labels for the periods */
    dateLabel: { required: true }
  },
  computed: {
    /** Data processed for the plot */
    data () {
      return this.plotData.map(element => {
        return {
          x: [1, 2, 3, 4],
          y: [
            1,
            (element['f1'] === 0) ? '0' : element['f2'] / element['f1'],
            (element['f2'] === 0) ? '0' : element['f3'] / element['f2'],
            (element['f3'] === 0) ? '0' : element['f4'] / element['f3']
          ],
          name: element['protein'] + '_' + element['mut'],
          customdata: [
            ['initial', element['f1'].toPrecision(3)],
            [element['f1'].toPrecision(3), element['f2'].toPrecision(3)],
            [element['f2'].toPrecision(3), element['f3'].toPrecision(3)],
            [element['f3'].toPrecision(3), element['f4'].toPrecision(3)]
          ],
          meta: element['protein'] + '_' + element['mut'],
          hovertemplate: '%{meta}, %{y:.2f} (from %{customdata[0]}% to %{customdata[1]}%) <extra></extra>',
          hoverlabel: {
            bordercolor: 'transparent',
            font: {
              color: 'rgb(68,68,68)'
            }
          },
          marker: {
            size: 10,
            line: { width: 0 }
          },
          line: { width: 3 },
          showlegend: true,
          type: 'scatter'
        }
      })
    },

    /** Layout data for the plot */
    layout () {
      return {
        height: this.plotData.length >= 20 ? 450 : 410,
        colorway:
          [
            '#ef5378', '#5ee171', '#f3df67', '#6685f1',
            '#fda05f', '#d46ff5', '#71daf1', '#f37fed',
            '#cfee82', '#fcb0ca', '#7ed7cd', '#dac4f8',
            '#efc69a', '#fffac8', '#d24f32', '#aaffc3',
            '#808000', '#ffd8b1', '#575793', '#a9a9a9'
          ],
        title: this.plotTitle,
        xaxis: {
          tickmode: 'array',
          tickvals: [1, 2, 3, 4],
          ticktext: [this.dateLabel['w1'], this.dateLabel['w2'], this.dateLabel['w3'], this.dateLabel['w4']],
          tickfont: {
            size: 11
          },
          automargin: true,
          showline: false,
          zeroline: false
        },
        yaxis: {
          tickfont: {
            size: 14
          },
          zeroline: false,
          showline: false,
          automargin: true
        },
        legend: {
          x: 1.0,
          y: 1.0,
          bgcolor: 'trasparent',
          bordercolor: 'trasparent',
          yanchor: 'top',
          ticks: 'outside',
          itemsizing: 'constant'
        },
        barmode: 'group',
        bargap: 0.15,
        bargroupgap: 0.1,
        hovermode: 'closest',
        margin: {
          b: 50,
          t: 80,
          pad: 10
        },
        autosize: true
      }
    }
  }
}
</script>
<style scoped>
/* Plotly container */
.plotly-container {
  border-radius: var(--border-radius);
  width: 100%;
  background: white;
}

/* Custom style for the list in the dialog */
li {
  padding-bottom: 25px;
}

ul {
  list-style-type: none;
}

/* Button spacing options */
.plot-controls {
  padding-bottom: 15px;
}
</style>

<style>
/* Overwite plotly rules to hide legend markers */
.legendsymbols {
  display: none !important;
}
</style>
