<!--
  Component:    ResultView
  Description:  Container of the data table, heatmap and a barchart

  Props:
  ├── queryResult:  Array of raw data fetched from the server
  ├── queryParams:  Object storing the query parameters {granularity, location, date, [lineage]}
  ├── querySupport: Object storing additional info such as total number of sequences collected per week and characterizing muts
  ├── queryCustOpt: Object storing the custom preselection for the filtering/selection options
  └── withLineages: Lineages flag. True if the data refers to a lineage specific analysis.

  Events:
  ├── askAnalysis:  Emitted whenever a next/prev button is pressed
  └── error:        Emitted on server errors
-->

<template>
  <div>
    <result-navbar @shiftPeriod="d => shiftPeriod(d)" @shiftArea="a => shiftArea(a)" @shiftType="shiftType"/>
    <v-container class="view-sizing">

      <!-- Filtering options -->
      <result-filters/>

      <!-- Table -->
      <result-table :with-lineages="withLineages"/>

      <!-- Diffusion Heatmap -->
      <diffusion-heatmap/>

      <!-- Diffusion Trend -->
      <diffusion-trend/>

      <!-- Diffusion Trend -->
      <diffusion-odd-ratio/>

      <!-- Next/prev week button -->
      <week-slider @shiftPeriod="d => shiftPeriod(d)"/>

      <!-- Info -->
      <result-info/>

      <loading-sticker :is-loading="isLoading" :error="error"
                       :loading-messages="[{text:'Analyzing sequence data',time:3000},{text:'This may take some time',time:6000},{text:'Almost done! Hang in there',time:9000}]"/>

      <no-data-alert v-model="noDataWarning"/>


      <div v-if="false">
        <v-layout>
          GF: {{ $store.state.globalFilteringOpt }} <br/>
          <hr/>
          LF: {{ $store.state.localFilteringOpt }} <br/>
          <hr/>
          GO: {{ $store.state.globalOrderingOpt }} <br/>
          <hr/>
          LO: {{ $store.state.localOrderingOpt }} <br/>
          <hr/>
        </v-layout>
      </div>
    </v-container>
  </div>
</template>

<script>
import {mapGetters, mapMutations, mapState} from 'vuex'
import WeekSlider from '@/components/form/WeekSlider'
import ResultNavbar from "@/components/analysis/navbar/ResultNavbar";
import ResultTable from "@/components/analysis/table/ResultTable";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import DiffusionHeatmap from "@/components/analysis/DiffusionHeatmap";
import DiffusionTrend from "@/components/analysis/DiffusionTrend";
import DiffusionOddRatio from "@/components/analysis/DiffusionOddRatio";
import NoDataAlert from "@/components/general/NoDataAlert";
import ResultInfo from "@/components/analysis/ResultInfo";
import ResultFilters from "@/components/analysis/ResultFilters";

export default {
  name: 'ResultView',
  components: {
    ResultFilters,
    ResultInfo,
    NoDataAlert,
    DiffusionOddRatio,
    DiffusionTrend,
    DiffusionHeatmap,
    LoadingSticker,
    ResultTable,
    ResultNavbar,
    WeekSlider,
  },
  data() {
    return {
      noDataWarning: false,
      isLoading: false,
      error: undefined,
    }
  },
  computed: {
    ...mapState(['selectedLocation', 'selectedDate', 'selectedLineage']),
    ...mapGetters(['getCurrentAnalysis']),

    withLineages() {
      return this.getCurrentAnalysis.query.lineage !== null
    },
  },
  methods: {
    ...mapMutations(['setLocations', 'setLocation', 'setLineages', 'setLineage', 'setDate', 'addAnalysis']),

    /**
     * Restore the current analysis parameters
     */
    restoreCurrentAnalysis() {
      const {location, granularity, lineage, endDate} = this.getCurrentAnalysis.query
      this.setLocation(location[granularity])
      if (this.withLineages) {
        this.setLineage(lineage)
      }
      const referenceDate = new Date(endDate)
      this.setDate([null, referenceDate.toISOString().slice(0, 10)])
    },

    /**
     * Handle next/prev analysis requests
     * @param requestDelay  Delay in days for the new analysis
     */
    shiftPeriod(requestDelay) {
      this.restoreCurrentAnalysis()
      const {endDate} = this.getCurrentAnalysis.query
      const referenceDate = new Date(endDate)
      referenceDate.setDate(referenceDate.getDate() + requestDelay)
      this.setDate([null, referenceDate.toISOString().slice(0, 10)])
      this.sendAnalysis()
    },

    /**
     * Handle shift type requests
     */
    shiftType() {
      this.restoreCurrentAnalysis()
      this.setLineage(null)
      this.sendAnalysis()
    },

    /**
     * Handle shift area requests
     * @param locationName  Name of the location
     */
    shiftArea(locationName) {
      this.restoreCurrentAnalysis()
      this.setLocation(locationName)
      this.sendAnalysis()
    },

    /**
     * Triggers the analysis request to the server
     */
    sendAnalysis() {
      this.isLoading = true
      this.error = undefined
      const url = (this.selectedLineage) ? "/lineage_specific/getStatistics" : "/lineage_independent/getStatistics"
      const queryParams = {
        location: this.selectedLocation,
        date: this.selectedDate[1],
        lineage: this.selectedLineage
      }

      this.$axios
          .get(url, {params: queryParams}).then(({data}) => data)
          .then(({rows, tot_seq, characterizing_muts = null, metadata}) => {
            if (rows.length > 0) {
              // Save the search parameters and results
              this.addAnalysis({rows, tot_seq, characterizing_muts, metadata})
            } else {
              this.noDataWarning = true
            }
          })
          .catch((e) => {
            this.error = e
          })
          .finally(() => {
            this.isLoading = false
          })
    },

  },
  beforeMount() {
    window.scrollTo({top: 0})
  }
}
</script>

<style scoped>

</style>

