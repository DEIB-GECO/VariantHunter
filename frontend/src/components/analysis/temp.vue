<template>
  <HeatMap></HeatMap>
    <!-- HEATMAP SECTION  ----------------------------------------------------->
    <SectionElement icon='mdi-chart-gantt' title='DIFFUSION HEATMAP'>
      <HeatMap :dateLabel='computeDateLabels()' :plotData='plotsInfo.data' :plotTitle='plotsInfo.title' />
    </SectionElement>

    <!-- CHART SECTION  ------------------------------------------------------->
    <SectionElement icon='mdi-chart-line' title='DIFFUSION TREND CHART'>
      <LineChart :dateLabel='computeDateLabels()' :plotData='plotsInfo.data' :plotTitle='plotsInfo.title'
                 :weekSeq='plotsInfo.support' />
    </SectionElement>

    <!-- ODD RATIO SECTION  --------------------------------------------------->
    <SectionElement icon='mdi-align-vertical-bottom' title='DIFFUSION ODD RATIO' collapsed
                    :tabs='["Week-by-week","Week-to-first-week","All"]' @tabChange='(selected) => oddRatioType=selected'>
      <OddRatioChart :dateLabel='computeDateLabels()' :plotData='plotsInfo.data' :plotTitle='plotsInfo.title' :type='oddRatioType'/>
    </SectionElement>
</template>

<script>
import HeatMap from "@/components/plots/HeatMap";
export default {
  name: "temp",
  components: {HeatMap}
}
</script>

<style scoped>

</style>