<!--

  View:         ResultView
  Description:  Sub-view container for the result panel

-->

<template>
  <div>
    <!-- Result toolbar with various options -->
    <result-navbar @shiftPeriod="d => shiftPeriod(d)" @shiftArea="a => shiftArea(a)" @shiftType="shiftType"/>

    <!-- Actual result panel -->
    <v-container class="view-sizing" id="result-top">
      <!-- Steps of the app-tour -->
      <result-intro/>
      <sidebar-intro/>

      <!-- Filtering options -->
      <v-slide-y-reverse-transition hide-on-leave>
        <result-filters v-if="sections?.filters"/>
        <v-skeleton-loader v-else type="card" height="110" class="mt-5"/>
      </v-slide-y-reverse-transition>

      <!-- Table -->
      <v-slide-y-reverse-transition hide-on-leave>
        <result-table v-if="sections?.table" :with-lineages="withLineages"/>
        <v-skeleton-loader v-else type="table" height="500" class="mt-8"/>
      </v-slide-y-reverse-transition>

      <!-- Diffusion Heatmap -->
      <v-slide-y-reverse-transition hide-on-leave>
        <diffusion-heatmap v-if="sections?.heatmap"/>
        <v-skeleton-loader v-else type="image" height="200" class="mt-8"/>
      </v-slide-y-reverse-transition>

      <!-- Diffusion Trend -->
      <v-slide-y-reverse-transition hide-on-leave>
        <diffusion-trend v-if="sections?.trend"/>
        <v-skeleton-loader v-else type="image" height="200" class="mt-8"/>
      </v-slide-y-reverse-transition>

      <!-- Diffusion Odd ratio -->
      <v-slide-y-reverse-transition hide-on-leave>
        <diffusion-odd-ratio v-if="sections?.ratio"/>
        <v-skeleton-loader v-else type="image" height="200" class="mt-8"/>
      </v-slide-y-reverse-transition>


      <!-- Next/prev week button -->
      <v-slide-y-reverse-transition hide-on-leave>
        <week-slider v-if="sections?.append" @shiftPeriod="d => shiftPeriod(d)"/>
      </v-slide-y-reverse-transition>

      <!-- Info -->
      <v-slide-y-reverse-transition hide-on-leave>
        <result-info v-if="sections?.append"/>
        <v-skeleton-loader v-else type="list-item" height="200" class="mt-8"/>
      </v-slide-y-reverse-transition>

      <!-- Local processing loading element -->
      <loading-sticker :is-loading="Object.values(sections).some(x=>!x)" no-overlay
                       :loading-messages="[{text:'Processing',time:3000}]"/>
      <!-- Server-side processing loading/error element -->
      <loading-sticker :is-loading="isLoading" :error="error"
                       :loading-messages="[{text:'Analyzing sequence data',time:3000},{text:'This may take some time',time:6000},{text:'Almost done! Hang in there',time:9000}]"/>

      <no-data-alert v-model="noDataWarning"/>

    </v-container>
  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from 'vuex'
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
import ResultIntro from "@/components/intros/ResultIntro";
import SidebarIntro from "../intros/SidebarIntro";

export default {
  name: 'ResultView',
  components: {
    SidebarIntro, ResultIntro, ResultFilters, ResultInfo, NoDataAlert, DiffusionOddRatio,
    DiffusionTrend, DiffusionHeatmap, LoadingSticker, ResultTable, ResultNavbar, WeekSlider,
  },

  data() {
    return {
      /** Visibility flags for the sections */
      sections: {
        'filters': false,
        'table': false,
        'heatmap': false,
        'trend': false,
        'ratio': false,
        'append': false
      },

      /** Boolean visibility flag for the no data warning popup*/
      noDataWarning: false,
      /** Boolean loading flag for the table and expansion */
      isLoading: false,
      /** Error data for the table and expansion. Undefined if no error. */
      error: undefined,
    }
  },

  computed: {
    ...mapState(['selectedLocation', 'selectedDate', 'selectedLineage']),
    ...mapGetters(['getCurrentAnalysis']),

  /** Boolean flag set to true iff the current analysis is lineage specific */
    withLineages() {
      return this.getCurrentAnalysis.query.lineage !== null
    },
  },

  methods: {
    ...mapActions(['addGroupAnalysis']),
    ...mapMutations(['setLocations', 'setLocation', 'setLineages', 'setLineage', 'setDate']),

    /**
     * Restore the current analysis parameters
     */
    restoreCurrentAnalysis() {
      const {location, granularity, lineage, endDate} = this.getCurrentAnalysis.query
      this.setLocation(location[granularity])
      this.setLineage(lineage)

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
     * @param location  Data of the location
     */
    shiftArea(location) {
      this.restoreCurrentAnalysis()
      this.setLocation(location)
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
        location: this.selectedLocation.id,
        date: this.selectedDate[1],
        lineage: this.selectedLineage
      }

      this.$axios
          .get(url, {params: queryParams}).then(({data}) => data)
          .then(({rows, tot_seq, characterizing_muts = null, metadata}) => {
            if (rows.length > 0) {
              // Save the search parameters and results
              this.addGroupAnalysis({rows, tot_seq, characterizing_muts, metadata})
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

  /** Always scroll to top */
  beforeMount() {
    window.scrollTo({top: 0})
  },

  /** Allow faster page rendering */
  mounted() {
    Object.keys(this.sections).forEach((section) => {
      setTimeout(() => {
        this.sections[section] = !this.sections[section]
      }, 1)
    })
  }
}
</script>

<style scoped>

</style>

