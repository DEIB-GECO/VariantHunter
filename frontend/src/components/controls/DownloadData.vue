<template>
  <v-tooltip bottom max-width='400'>
    <template v-slot:activator='{ on, attrs }'>
      <v-btn v-if="controlType==='button'" v-bind='attrs' v-on='on' :loading='downloadLoading' color='primary'
             outlined depressed rounded small @click='downloadData'>
        <v-icon left class="hidden-xs-only">mdi-download-circle-outline</v-icon>
        Download&nbsp;<span class='hidden-sm-and-down'>data</span>
      </v-btn>
      <v-list-item v-else link dense @click='downloadData'>
        <v-icon v-if="!downloadLoading" class="pr-3" color="primary">mdi-download</v-icon>
        <v-progress-circular v-else indeterminate color="warning"/>
        <v-list-item-content>
        <v-list-item-title class="primary--text">Download data</v-list-item-title>
        <v-list-item-subtitle>Download table data as a .csv file</v-list-item-subtitle>
          </v-list-item-content>
      </v-list-item>
    </template>
    <span>Download table data as a .csv file</span>
  </v-tooltip>
</template>

<script>
import {getFileName, json2csv} from "@/utils/parserService";
import {mapGetters, mapState} from "vuex";
import {sortItems} from "@/utils/sorterService";

export default {
  name: "DownloadData",
  props: {
    /** controlType: type of activator. Either 'button' or 'icon'. */
    controlType: {}
  },
  data() {
    return {
      downloadLoading: false
    }
  },
  computed: {
    ...mapGetters(['getCurrentAnalysis', 'getCurrentFilteredRows', 'getCurrentOpt'])
  },
  methods: {

    /**
     * Download the current view of the data (keep filtering and ordering options)
     */
    downloadData() {
      this.downloadLoading = true

      // Sort data
      const {sortingIndexes, isDescSorting} = this.getCurrentOpt
      const sortedData = sortItems(this.getCurrentFilteredRows, sortingIndexes, isDescSorting)

      // Columns to download
      const {w1, w2, w3, w4} = this.getCurrentAnalysis.query.weeks
      const tableHeaders = [
        {text: 'Protein', value: 'protein'},
        {text: 'Mut', value: 'mut',},
        {text: 'Slope', value: 'slope',},
        {text: w1+' (freq)', value: 'f1',},
        {text: w1+' (abs)', value: 'w1',},
        {text: w2+' (freq)', value: 'f2',},
        {text: w2+' (abs)', value: 'w2',},
        {text: w3+' (freq)', value: 'f3',},
        {text: w3+' (abs)', value: 'w3',},
        {text: w4+' (freq)', value: 'f4',},
        {text: w4+' (abs)', value: 'w4',},
        {text: 'P-value with mut', value: 'p_value_with_mut',},
        {text: 'P-value without mut', value: 'p_value_without_mut',},
        {text: 'P-value comparative', value: 'p_value_comp'}
      ]
      const csv = json2csv(sortedData, tableHeaders)

      // Anchor element to download the file
      const anchor = document.createElement('a')
      anchor.setAttribute('download', getFileName(this.getCurrentAnalysis.query) + '.csv')
      const data = new Blob([csv])
      anchor.href = URL.createObjectURL(data)
      document.body.appendChild(anchor)

      // Simulate click and remove element
      anchor.click()
      document.body.removeChild(anchor)
      this.downloadLoading = false
    },
  }
}
</script>

<style scoped>

</style>