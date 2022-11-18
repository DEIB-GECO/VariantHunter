<template>
  <v-container class="view-sizing">

    <v-row id="top" class="px-5">
      <v-col>
        <div class="text-right text-body-4 font-weight-medium py-3 compact-text-3 success--text">
          <span v-if="lastUpdate"><v-icon left small
                                          color="success">mdi-clock-outline</v-icon>Last dataset update: <span
              class="font-weight-regular d-block d-md-inline-block">{{ lastUpdate }}</span></span>
          <span v-else><v-progress-circular class="mr-2" indeterminate
                                            size="15"/> Fetching last dataset update...</span>
        </div>

        <div class="text-h4 font-weight-black primary--text pb-2">Define new analysis</div>
        <div class="text-body-3 compact-text-2">VariantHunter analyzes the frequencies of amino acid mutations of
          SARS-CoV-2 in order to observe interesting variant trends or identify novel emerging variants.
        </div>
        <div class="text-body-3 compact-text-2 pt-3">Choose the type of analysis you want to perform, then define the
          required parameters.
        </div>
      </v-col>
    </v-row>
    <v-row>
      <v-tabs background-color="transparent" centered active-class="font-weight-black">
        <v-tabs-slider color="primary"></v-tabs-slider>
        <v-tab v-for="[value,title] in Object.entries(modeOptions)" :key="value" @click="mode=value">
          {{ title }}
        </v-tab>
      </v-tabs>
      <v-container class="pt-5 definition-container">
        <v-row>
          <location-selector/>
        </v-row>
        <v-row>
          <date-picker/>
        </v-row>
        <v-expand-transition>
          <v-row v-if="mode==='ls'">
            <lineage-selector/>
          </v-row>
        </v-expand-transition>

        <v-row class='my-4'>
          <v-col>
            <v-btn class='delete-action mr-2 text_var2--text' color='primary' @click='clearForm' depressed small
                   rounded>
              <v-icon left>mdi-backspace-outline</v-icon>
              CLEAR
            </v-btn>
            <v-btn class='float-right text_var2--text' color='primary' @click="sendAnalysis" depressed small rounded
                   :disabled="formError">
              ANALYSE
              <v-icon right>mdi-magnify</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-row>
    <v-row class="px-5">
      <v-container>
        <v-row>
          <v-col>
            <div class="text-h5 font-weight-black primary--text pb-2">
              Dataset Explorer
            </div>
            <v-expand-transition>
              <div v-if="!showExplorer" class="text-body-3 compact-text-2 pb-3">
                The Dataset Explorer allows you to examine the availability of sequences over time, enabling proper
                selection of the analysis period.
                It also provides information on the prevalence of lineages over time.
              </div>
            </v-expand-transition>
            <!-- Show/hide Explorer controls -->
            <div>
              <v-btn depressed rounded small color='primary' class="text_var2--text"
                     @click='showExplorer = !showExplorer'>
                <v-icon left>{{ showExplorer ? 'mdi-close-circle-outline' : 'mdi-compass' }}</v-icon>
                {{ showExplorer ? 'Hide' : 'Show dataset explorer' }}
              </v-btn>
            </div>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-scroll-y-reverse-transition>
            <dataset-explorer v-if="showExplorer" :with-lineages='mode==="ls"' @weekSelection='onWeekSelection'/>
          </v-scroll-y-reverse-transition>
        </v-row>
      </v-container>
    </v-row>

    <loading-sticker :is-loading="isLoading" :error="error"
                     :loading-messages="[{text:'Analyzing sequence data',time:3000},{text:'This may take some time',time:6000},{text:'Almost done! Hang in there',time:9000}]"/>

    <no-data-alert v-model="noDataWarning" @update:modelValue="v=>noDataWarning=v"/>

  </v-container>
</template>

<script>
import LocationSelector from "@/components/form/LocationSelector";
import DatePicker from "@/components/form/DatePicker";
import LineageSelector from "@/components/form/LineageSelector";
import DatasetExplorer from "@/components/explorer/DatasetExplorer";
import {mapMutations, mapState} from "vuex";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import NoDataAlert from "@/components/general/NoDataAlert";

export default {
  name: "NewSearchView",
  components: {NoDataAlert, LoadingSticker, DatasetExplorer, LineageSelector, DatePicker, LocationSelector},
  data() {
    return {
      mode: 'li',
      modeOptions: {li: 'Lineage independent', ls: 'Lineage specific'},

      isLoading: false,
      error: undefined,
      noDataWarning: false,

      showExplorer: false
    }
  },
  computed: {
    ...mapState(['selectedLineage', 'selectedLocation', 'selectedDate', 'lastUpdate']),

    /** Form error flag: true if the form cannot be sent */
    formError() {
      return !this.selectedLocation || !this.selectedDate || (!this.selectedLineage && this.mode === 'ls')
    }
  },
  methods: {
    ...mapMutations(['setDate', 'setLineage', 'setLocation', 'setLocations', 'setLineages', 'addAnalysis', 'setCurrentAnalysis']),

    clearForm() {
      this.setLineage(null)
      this.setLineages([])
      this.setDate(null)
      this.setLocation(null)
      this.setLocations([])
    },

    /**
     * Triggers the analysis request to the server
     */
    sendAnalysis() {
      this.isLoading = true
      this.error = undefined
      const url = (this.mode === 'li') ? "/lineage_independent/getStatistics" : "/lineage_specific/getStatistics"
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

    /**
     * Handler for weekSelection event from Dataset Explorer
     * @param range The selected range
     */
    onWeekSelection(range) {
      this.showExplorer = false
      document.getElementById('top').scrollIntoView({behavior: 'smooth'})
      this.setDate(range)
      if (!this.formError) {
        this.sendAnalysis()
      }
    }
  },
  beforeMount() {
    window.scrollTo({top: 0})
  }
}
</script>

<style scoped>
.delete-action:hover {
  background-color: red !important;
  border-color: red !important;
}

.definition-container {
  max-width: 800px !important;
  justify-content: center;
}
</style>