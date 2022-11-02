<!--
  Component:    TabWithLineages
  Description:  Tab to perform lineage specific analyses.

  Props:
  └── visible:      Visibility flag for the tab: true iff this is the current tab

  Events:
  └── error:    Emitted on server errors
-->

<template>
  <Tab :is-loading='isLoading' :result-length='queriesResults.length' :visible='visible' with-lineages
       @send='startAnalysis(null)' @error='e=> $emit("error",e)'>

    <!-- Panels list -->
    <template v-slot:results>
      <v-expansion-panels v-model='expandedPanels' :value='expandedPanels' focusable multiple tile>
        <v-expansion-panel v-for='(element, index) in queriesResults' v-bind:key='index' :ref='"L"+index'
                           :class="'expansion-panel-result '+(deletedIndexes.includes(index)?' d-none':'')">

          <!-- Panel header -->
          <v-expansion-panel-header :color='secondary_color' v-if="!deletedIndexes.includes(index)">
            <span :ref='"WL"+index' class='panel-header'>
              <b>Results for:</b>
              {{ queriesParams[index]['granularity'] }} /
              {{ queriesParams[index]['location'] }} /
              {{ queriesParams[index]['date'] }} /
              {{ queriesParams[index]['lineage'] }}
            </span>
            <v-spacer></v-spacer>

            <!-- Panel delete action -->
            <span class='delete-action'>
              <v-btn outlined rounded small @click.native.stop='deleteQuery(index)'>
                <v-icon small>mdi-trash-can-outline</v-icon>
                <div class='hidden-md-and-down'>Delete</div>
              </v-btn>
            </span>

            <!-- Panel collapse/expand action -->
            <template v-slot:actions>
              <v-btn icon outlined small>
                <v-icon small>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
          </v-expansion-panel-header>

          <!-- Panel content -->
          <v-expansion-panel-content :color='secondary_color' v-if="!deletedIndexes.includes(index)">
            <ResultView v-if='queriesResults[index].length > 0' :queryResult='queriesResults[index]'
                        :queryParams='queriesParams[index]' :querySupport='queriesSupport[index]'
                        :queryCustOpt='queriesCustomOptions[index]' withLineages
                        @askAnalysis='(delay,status) => requestStartAnalysis(index, delay, status)'
                        @error='e => $emit("error",e)' />

            <div v-else class='empty-result-alert'>
              <h4>
                <v-icon color='white' left>mdi-alert-circle-outline</v-icon>
                Insufficient data to perform the analysis
              </h4>
            </div>

          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </template>
  </Tab>
</template>

<script>
import { mapState } from 'vuex'
import axios from 'axios'
import ResultView from '../ResultView'
import Tab from '@/components/tabs/Tab'
import { mapStateTwoWay } from '@/utils/bindService'

export default {
  name: 'TabWithLineages',
  components: {
    Tab,
    ResultView
  },
  props: {
    /** Visibility flag for the Tab */
    visible: Boolean
  },
  data () {
    return {
      /** Progress circe flag: true if the progress circle is displayed */
      isLoading: false,

      /** Panel expansion status array */
      expandedPanels: [],

      /** Array storing the search parameters for each query */
      queriesParams: [],

      /** Array storing the search results for each query */
      queriesResults: [],

      /**
       * Array storing additional queries info such as the total number of sequences collected
       * per week for each query and the characterizing mutations for the lineage
       */
      queriesSupport: [],

      /** Array storing the customization options (filter values, selections) for each query */
      queriesCustomOptions: [],

      /** Deleted indexes */
      deletedIndexes: [],
    }
  },
  computed: {
    ...mapState(['secondary_color']),
    ...mapStateTwoWay({
      selectedGranularity: 'SET_GRANULARITY',
      selectedLocation: 'SET_LOCATION',
      selectedDate: 'SET_END_DATE',
      selectedLineage: 'SET_LINEAGE'
    })
  },
  methods: {
    /**
     * Triggers the analysis request to the server
     * @param customOptions   The customization options (filter values, selections) for the new tab
     */
    startAnalysis (customOptions) {
      this.isLoading = true
      const url = `/lineage_specific/getStatistics`
      const toSend = {
        granularity: this.selectedGranularity,
        location: this.selectedLocation ? this.selectedLocation : 'all',
        date: this.selectedDate[1],
        lineage: this.selectedLineage
      }

      axios
        .post(url, toSend)
        .then(res => {
          return res.data
        })
        .then(res => {
          // Save the search parameters and results
          this.queriesParams.push(toSend)
          this.queriesCustomOptions.push(customOptions)
          this.queriesResults.push(res['rows'])
          const supportInfo = {
            totSeq: res['tot_seq'],
            characterizingMuts: res['characterizing_muts'],
            locationData: res['location']
          }
          const panelIndex = this.queriesSupport.push(supportInfo) - 1

          // Open the new panel and jump to the result container
          this.expandedPanels = [panelIndex]
          const that = this
          setTimeout(() => {
            that.$refs['WL' + (panelIndex)][0].scrollIntoView(true)
          }, 1000)
        })
        .catch((e) => {
          this.$emit('error', e)
        })
        .finally(() => {
          this.isLoading = false
        })
    },

    /**
     * Handle next/prev analysis requests
     * @param index         Reference search
     * @param requestDelay  Delay in days for the new analysis
     * @param customOptions The customization options (filter values, selections)
     */
    requestStartAnalysis (index, requestDelay, customOptions) {
      this.selectedGranularity = this.queriesParams[index].granularity
      this.selectedLocation = this.queriesParams[index].location
      this.selectedLineage = this.queriesParams[index].lineage
      const referenceDate = new Date(this.queriesParams[index].date)
      referenceDate.setDate(referenceDate.getDate() + requestDelay)
      this.selectedDate = [null, referenceDate.toISOString().slice(0, 10)]

      this.startAnalysis(customOptions)
    },

    /**
     * Removes a query from the result list
     * @param queryIndex  The index of the expansion panel to be removed
     */
    deleteQuery (queryIndex) {
      this.deletedIndexes.push(queryIndex)
    }
  }
}
</script>

<style scoped>

/* Result list styling */
.expansion-panel-result {
  margin-bottom: 20px;
}

.expansion-panel-result span {
  text-transform: capitalize;
  font-size: 17px;
  color: white;
  letter-spacing: 1px;
}

.expansion-panel-result span b {
  text-transform: none;
}

/* No result message styling */
.expansion-panel-result .empty-result-alert {
  text-align: center;
  margin-top: 40px;
  margin-bottom: 20px;
  font-size: 17px;
  color: white !important;
  letter-spacing: 1px;
  line-height: 10px;
}

/* Panel action styling*/
.expansion-panel-result .delete-action > * {
  float: right;
  margin-right: 5px;
  color: rgba(0, 0, 0, 0.54) !important;
}

.expansion-panel-result .delete-action button:hover {
  background: #da3f3f !important;
  color: white !important;
}

.panel-header {
  scroll-margin-top: 60px;
}
</style>
