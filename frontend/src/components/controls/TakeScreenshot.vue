<!--

  Component:    TakeScreenshot
  Description:  Take a full page screenshot of the current view of the tool

-->

<template>
  <!-- Action button -->
  <v-list-item link dense @click='onDownloadClick'>
    <v-icon v-if="!downloadLoading" class="pr-3" color="primary">mdi-monitor-screenshot</v-icon>
    <v-progress-circular v-else class="mr-3" indeterminate color="warning"/>
    <v-list-item-content>
      <v-list-item-title class="primary--text">Take a screenshot</v-list-item-title>
      <v-list-item-subtitle>Download panel as .png file</v-list-item-subtitle>
      <div v-if="downloadLoading" class="text-body-4 warning--text font-weight-medium">
        Please wait. Download in progress...
      </div>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import {mapGetters} from "vuex";
import {getFileName} from "@/utils/parserService";
import {toPng} from 'html-to-image';

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
      const sectionToPrint = document.getElementById('to-print')
      const ratio = sectionToPrint.clientHeight / sectionToPrint.clientWidth
      const width = 2500
      const height = width * ratio

      toPng(sectionToPrint, {canvasWidth: width, canvasHeight: height, pixelRatio: ratio})
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