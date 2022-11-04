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
  <div :ref='fileName'>
    <result-navbar @moveForward="shiftAnalysis(+7)" @moveBackward="shiftAnalysis(-7)"/>
    <v-container class="view-sizing">

      <!-- Filtering options -->
      <v-row id="top" class="mt-5 px-5">
        <v-col cols="12" class="d-flex">
          <span class="text-h6 compact-h6 font-weight-black primary--text pb-2 mx-n5 spaced-5">
            <v-icon color='primary' left>mdi-filter-outline</v-icon>
            <span>Filters</span>
          </span>
          <v-spacer/>
          <v-icon color="primary">mdi-dots-horizontal</v-icon>
        </v-col>
        <!-- Protein filter -->
        <v-col cols="12" sm="5" md="3">
          <FieldSelector v-model='selectedProtein' label='Protein' placeholder='All'
                         :possible-values='possibleProteins' autocomplete solo/>
        </v-col>

        <!-- Mutation filter -->
        <v-col cols="12" sm="7" md="7">
          <MutationSelector v-model='selectedMutation' :possible-values='possibleMutations'
                            :characterizing-muts='characterizingMuts'/>
        </v-col>
      </v-row>

      <!-- Table -->
      <result-table :with-lineages="withLineages"/>

      <!-- Next/prev week button -->
      <v-row>
        <WeekSlider @moveForward="shiftAnalysis(+7)" @moveBackward="shiftAnalysis(-7)"/>
      </v-row>

      <loading-sticker :is-loading="isLoading" :error="error"
                       :loading-messages="[{text:'Analyzing sequence data',time:3000},{text:'This may take some time',time:6000},{text:'Almost done! Hang in there',time:9000}]"/>
      <div>
        <v-layout style="height: 1800px">
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
import {getFileName} from "@/utils/parserService";
import FieldSelector from '@/components/form/FieldSelector'
import MutationSelector from '@/components/form/MutationSelector'
import WeekSlider from '@/components/form/WeekSlider'
import ResultNavbar from "@/components/general/ResultNavbar";
import ResultTable from "@/components/analysis/ResultTable";
import axios from "axios";
import LoadingSticker from "@/components/general/basic/LoadingSticker";

export default {
  name: 'ResultView',
  components: {
    LoadingSticker,
    ResultTable,
    ResultNavbar,
    WeekSlider, MutationSelector, FieldSelector,
  },
  data() {
    return {
      isLoading: false,
      error: undefined,
    }
  },
  computed: {
    ...mapState(['currentAnalysisId','globalFilteringOpt',]),
    ...mapGetters(['getCurrentAnalysis','getCurrentLocalFilteringOpt']),

    fileName() {
      // TODO: verify if necessary
      return getFileName(this.getCurrentAnalysis.query)
    },

    withLineages() {
      console.log("# withLineages=" + (this.getCurrentAnalysis.query.lineage !== null))
      return this.getCurrentAnalysis.query.lineage !== null
    },

    characterizingMuts() {
      console.log("# characterizingMuts=" + this.getCurrentAnalysis.characterizingMuts)
      return this.withLineages ? this.getCurrentAnalysis.characterizingMuts : null
    },

    useGlobalFilters() {
      return this.getCurrentLocalFilteringOpt.useGlobalFilters
    },

    filteringOpt() {
      return (this.useGlobalFilters ? this.globalFilteringOpt : this.getCurrentLocalFilteringOpt)
    },

    /** Possible proteins values computed based on data results */
    possibleProteins() {
      const set = new Set(this.getCurrentAnalysis.rows.map(({protein}) => protein))
      return [...set].sort()
    },

    /** Possible mutations values computed based on data results */
    possibleMutations() {
      const set = new Set(this.getCurrentAnalysis.rows.map(({protein, mut}) => protein + '_' + mut))
      return [...set].sort()
    },

    /** Selected mutation to further filter the data. Takes the form <PROTEIN>_<MUT> */
    selectedMutation: {
      set(newVal) {
        this.setFilterOpt({global: this.useGlobalFilters, opt: 'muts', value: newVal})
      },
      get() {
        return this.filteringOpt.muts
      }
    },

    /** Selected protein to further filter the data */
    selectedProtein: {
      set(newVal) {
        this.setFilterOpt({global: this.useGlobalFilters, opt: 'protein', value: newVal})
      },
      get() {
        return this.filteringOpt.protein
      }
    },


  },
  methods: {
    ...mapMutations(['setFilterOpt', 'setLocations', 'setLineage', 'setDate']),

    /**
     * Handle next/prev analysis requests
     * @param requestDelay  Delay in days for the new analysis
     */
    shiftAnalysis(requestDelay) {
      const currQuery = this.getCurrentAnalysis.query
      this.setLocations(currQuery.location[currQuery.granularity])
      if (this.withLineages) this.setLineage(currQuery.lineage)

      const referenceDate = new Date(currQuery.endDate)
      referenceDate.setDate(referenceDate.getDate() + requestDelay)
      this.setDate([null, referenceDate.toISOString().slice(0, 10)])

      this.sendAnalysis()
    },

    /**
     * Triggers the analysis request to the server
     */
    sendAnalysis() {
      this.isLoading = true
      this.error = undefined
      const url = (this.withLineages) ? "/lineage_specific/getStatistics" : "/lineage_independent/getStatistics"
      const toSend = {
        location: this.selectedLocation,
        date: this.selectedDate[1],
        lineage: this.selectedLineage
      }

      axios
          .post(url, toSend).then(({data}) => data)
          .then(({rows, tot_seq, characterizing_muts = null}) => {
            // Save the search parameters and results
            this.addAnalysis({rows, tot_seq, characterizing_muts, mode: (this.withLineages ? 'ls' : 'li')})
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

