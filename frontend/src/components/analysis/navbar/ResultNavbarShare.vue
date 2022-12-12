<!--

  Component:    ResultNavbarShare
  Description:  Share the current analysis as link

-->

<template>
  <!-- Action button -->
  <v-list-item link dense @click='onDownloadClick'>
    <v-icon class="pr-3" color="primary">mdi-share-variant-outline</v-icon>
    <v-list-item-content>
      <v-list-item-title class="primary--text">Share analysis</v-list-item-title>
      <v-list-item-subtitle>Generate a link to the current analysis</v-list-item-subtitle>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import {mapGetters} from "vuex";
import {getFileName} from "@/utils/parserService";
import domtoimage from "dom-to-image-more";

export default {
  name: "ResultNavbarShare",

  data() {
    return {

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
    }
  }
}
</script>

<style scoped>

</style>