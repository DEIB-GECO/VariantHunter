<!--

  Component:    ResultNavbarShare
  Description:  Share the current analysis as link

-->

<template>
  <!-- Action button -->
  <v-list-item link dense @click='onShareClick'>
    <v-icon class="pr-3" color="primary">mdi-share-variant-outline</v-icon>
    <v-list-item-content>
      <v-list-item-title class="primary--text">Share analysis</v-list-item-title>
      <v-list-item-subtitle>Generate a link to the current analysis</v-list-item-subtitle>
      <div v-if="showDialog" class="text-body-4 success--text font-weight-medium">
        <span v-if="!error">Link has been copied to clipboard!</span>
        <span v-else>{{ error }}</span>
      </div>
    </v-list-item-content>
  </v-list-item>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "ResultNavbarShare",

  data() {
    return {
      /** Boolean flag set to true iff copy dialog is shown */
      showDialog: false,

      /** Error flag. Undefined if no error. */
      error: undefined
    }
  },

  computed: {
    ...mapGetters(['getCurrentAnalysis']),
  },

  methods: {

    /**
     * Click manager for the share option
     */
    onShareClick() {
      // Generate the url string
      const {lineage, endDate, location: locationData, granularity} = this.getCurrentAnalysis.query
      const type = lineage ? 'ls' : 'li'
      const locationId = locationData[granularity].id

      let url = location.origin + '/variant_hunter/linkTo?type=' + type + '&location=' + locationId + '&date=' + endDate
      if (lineage) {
        const lineages = [...lineage.items]
        lineages.push(...Object.keys(lineage.groups))
        lineages.forEach(name => url += '&lineages=' + name)
        url = url.replaceAll('*', '%2a')
      }

      console.log(url)
      this.error = undefined
      this.$copyText(url).then(() => {
        this.showDialog = true
        setTimeout(() => this.showDialog = false, 5000)
      })

    }
  }
}
</script>

<style scoped>

</style>