<!--

  View:         NewSearchView
  Description:  Sub-view container for the new analysis form

-->

<template>
  <v-container class="view-sizing">


    <v-row id="top" class="px-5 pt-3">
      <!-- Main introduction to the app-tour-->
      <tour-intro/>

      <v-col>
        <!-- Dataset info summary -->
        <dataset-info/>

        <!-- Headings -->
        <div class="text-h4 font-weight-black primary--text pb-2">Define new analysis</div>
        <div class="text-body-3 compact-text-2">VariantHunter analyzes the frequencies of amino acid mutations of
          SARS-CoV-2 in order to observe interesting variant trends or identify novel emerging variants.
          <router-link :to="{name:'About'}" class="primary--text text-body-6 text-uppercase">More info...</router-link>
        </div>
        <div class="text-body-3 compact-text-2 pt-3">Choose the type of analysis you want to perform, then define the
          required parameters.
        </div>
      </v-col>
    </v-row>

    <!-- Definition form -------------------------------------------->
    <v-row>
      <!-- Definition step of the app-tour -->
      <definition-intro @selectMode="mode='li'" @showExplorer="showExplorer? {} : showExplorer=true"/>

      <!-- Analysis type selector -->
      <v-tabs id="type-tabs" background-color="transparent" centered active-class="font-weight-black">
        <v-tabs-slider color="primary"></v-tabs-slider>
        <v-tab v-for="[value,title] in Object.entries(modeOptions)" :key="value" @click="mode=value">
          {{ title }}
        </v-tab>
      </v-tabs>

      <v-container class="pt-5 definition-container">
        <!-- Location selector -->
        <v-row>
          <location-selector/>
        </v-row>

        <!-- Period selector -->
        <v-row>
          <date-picker/>
        </v-row>

        <!-- Lineage selector -->
        <v-expand-transition>
          <v-row v-if="mode==='ls'">
            <lineage-selector/>
          </v-row>
        </v-expand-transition>

        <!-- Tag selector -->
        <v-row>
          <quick-tag-selector v-model="tag"/>
        </v-row>

        <!-- Controls -->
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

    <!-- Dataset explorer ------------------------------------------->
    <v-row class="px-5">
      <v-container>

        <!-- Intro text -->
        <v-row>
          <v-col>
            <div class="text-h5 font-weight-black primary--text pb-2" id="explorer">
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

        <!-- Plots -->
        <v-row no-gutters>
          <!-- Explorer step of the app-tour -->
          <explorer-intro/>
          <v-scroll-y-reverse-transition>
            <dataset-explorer v-if="showExplorer" :with-lineages='mode==="ls"' @weekSelection='onWeekSelection'/>
          </v-scroll-y-reverse-transition>
        </v-row>
      </v-container>
    </v-row>

    <!-- QuickStart ------------------------------------------->
    <quick-start v-if="isPublicEndpoint && datasetInfo?.fileType==='nextstrain'"/>

    <loading-sticker :is-loading="isLoading" :error="error"
                     :loading-messages="[{text:'Analyzing sequence data',time:3000},{text:'This may take some time',time:6000},{text:'Almost done! Hang in there',time:9000}]"/>

    <!-- No data alert -->
    <no-data-alert v-model="noDataWarning"/>

  </v-container>
</template>

<script>
import LocationSelector from "@/components/form/LocationSelector";
import DatePicker from "@/components/form/DatePicker";
import LineageSelector from "@/components/form/LineageSelector";
import DatasetExplorer from "@/components/explorer/DatasetExplorer";
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import NoDataAlert from "@/components/general/NoDataAlert";
import QuickTagSelector from "@/components/form/QuickTagSelector";
import TourIntro from "@/components/intros/TourIntro";
import DefinitionIntro from "@/components/intros/DefinitionIntro";
import ExplorerIntro from "@/components/intros/ExplorerIntro";
import DatasetInfo from "../general/DatasetInfo";
import QuickStart from "@/components/general/QuickStart.vue";

export default {
  name: "NewSearchView",
  components: {
    QuickStart,
    DatasetInfo, ExplorerIntro, DefinitionIntro, TourIntro, QuickTagSelector, NoDataAlert,
    LoadingSticker, DatasetExplorer, LineageSelector, DatePicker, LocationSelector
  },
  data() {
    return {
      /** Currently selected mode. Either 'li' or 'ls'*/
      mode: 'li',
      /** Available modes */
      modeOptions: {li: 'Lineage independent', ls: 'Lineage specific'},

      /** Current tag. Possibly null. */
      tag: null,

      /** Boolean loading flag for the table and expansion */
      isLoading: false,
      /** Error data for the table and expansion. Undefined if no error. */
      error: undefined,

      /** Boolean visibility flag for the no data warning popup*/
      noDataWarning: false,
      /** Boolean visibility flag for the dataset explore */
      showExplorer: false
    }
  },

  computed: {
    ...mapState(['selectedLineage', 'selectedLocation', 'selectedDate','isPublicEndpoint','datasetInfo']),
    ...mapGetters(['getSelectedLineage']),

    /** Form error flag: true if the form cannot be sent */
    formError() {
      return !this.selectedLocation || !this.selectedDate ||
          (this.selectedLineage.count < 1 && this.mode === 'ls')
    }
  },

  methods: {
    ...mapActions(['addAnalysis']),
    ...mapMutations(['setDate', 'setLineage', 'setLocation', 'setLocations', 'setLineages', 'setCurrentAnalysis']),

    /** Clear the form completely */
    clearForm() {
      this.setLineage({'groups':{},'items':[]})
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
      const queryParams = new URLSearchParams();
      queryParams.append('location', this.selectedLocation.id)
      queryParams.append('date', this.selectedDate[1])
      // Add lineages data
      if (this.selectedLineage.count > 0) {
        this.getSelectedLineage.forEach(name => queryParams.append("lineages", name))
      }

      this.$axios
          .get(url, {params: queryParams}).then(({data}) => data)
          .then(({rows, tot_seq, characterizing_muts = null, metadata}) => {
            if (rows.length > 0) {
              // Save the search parameters and results
              this.addAnalysis({rows, tot_seq, characterizing_muts, metadata, tag: this.tag})
            } else {
              this.noDataWarning = true
            }
          })
          .catch((e) => this.error = e)
          .finally(() => this.isLoading = false)
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

  /** Always scroll to top */
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