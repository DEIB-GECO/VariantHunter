<!--

  Component:    TakeScreenshot
  Description:  Take a full page screenshot of the current view of the tool

-->

<template>
  <!-- Action button -->
  <v-list-item link dense @click='onDownloadClick'>
    <v-icon v-if="!downloadLoading" class="pr-3" color="primary">mdi-monitor-screenshot</v-icon>
    <v-progress-circular v-else indeterminate color="warning"/>
    <v-list-item-content>
      <v-list-item-title class="primary--text">Take a screenshot</v-list-item-title>
      <v-list-item-subtitle>Download panel as .png file</v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import {mapGetters} from "vuex";
import {getFileName} from "@/utils/parserService";
import domtoimage from "dom-to-image-more";

export default {
  name: "TakeScreenshot",

  data() {
    return {
      /* Boolean download flag set to true if a file download is in progress */
      downloadLoading: false,
    }
  },

  computed: {
    ...mapGetters(['getCurrentAnalysis']),
  },

  methods: {
    /**
     * Click manager for the download option
     */
    onDownloadClick() {
      setTimeout(this.downloadScreen, 500) // wait for the menu to close
    },

    /**
     * Downloads a screenshot of the table, heatmap and line chart
     */
    downloadScreen() {
      this.downloadLoading = true
      // Retrieve section to be printed
      const fileName = getFileName(this.getCurrentAnalysis.query)
      const sectionToPrint = document.getElementById('app')

      domtoimage
          .toPng(sectionToPrint)
          .then((dataUrl) => {
            // Anchor element to download the file
            const anchor = document.createElement('a')
            anchor.download = fileName + '.png'
            anchor.href = dataUrl
            document.body.appendChild(anchor)

            // Simulate click and remove element
            anchor.click()
            document.body.removeChild(anchor)
            this.downloadLoading = false
          });
    },
  }
}
</script>

<style scoped>

</style>