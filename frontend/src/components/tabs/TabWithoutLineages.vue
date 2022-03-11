<!--
  Component:    TabWithoutLineages
  Description:  Tab to perform lineage independent analyses.
-->

<template>
  <Tab :error-occurred="errorOccurred"
       :form-error="formError"
       :is-loading="isLoading"
       :result-length="rowsTable.length"
       @send="doAnalysis()"
       @close-error-alert="onCloseErrorAlert()"
  >

    <!-- Form fields -->
    <template v-slot:form>

      <!---- Granularity -->
      <v-flex class="xs12 sm4 md3 d-flex">
        <v-layout row wrap>
          <v-flex class="xs12 d-flex field-label">
            <span>Granularity</span>
          </v-flex>

          <v-flex class="xs12 d-flex field-element">
            <v-select v-model="selectedGranularity"
                      :items="possibleGranularity"
                      hide-details
                      label="Granularity"
                      solo/>
          </v-flex>
        </v-layout>
      </v-flex>

      <!---- Location -->
      <v-flex v-if="selectedGranularity!=='world'" class="xs12 sm8 md5 d-flex">
        <LocationSelector v-model="selectedLocation" :selectedGranularity="selectedGranularity"/>
      </v-flex>

      <!---- Date -->
      <v-flex class="xs12 sm6 md3 d-flex">
        <DatePicker v-model="selectedDate"/>
      </v-flex>

    </template>

    <!-- Dataset Explorer-->
    <template v-slot:explorer>
      <v-flex class="xs12 d-flex">
        <DatasetExplorer :granularity="selectedGranularity" :location="selectedLocation"/>
      </v-flex>
    </template>

    <!-- Panels list -->
    <template v-slot:results>

      <v-expansion-panels
          v-model="expansionPanels"
          :value="expansionPanels"
          focusable multiple>
        <v-expansion-panel v-for="(array_rows, index) in rowsTable" v-bind:key="index" class="result-list">

          <!-- Panel header -->
          <v-expansion-panel-header :color="secondary_color">
            <span>
              <b>Results for:</b>
              {{ expansionPanelsSingleInfo[index]['granularity'] }} /
              {{ expansionPanelsSingleInfo[index]['location'] }} /
              {{ expansionPanelsSingleInfo[index]['date'] }}
            </span>
            <v-spacer></v-spacer>

            <!-- Panel delete action -->
            <span class="delete-action">
              <v-btn outlined rounded small @click.native.stop="deleteQuery(index)">
                 <v-icon small>mdi-trash-can-outline</v-icon>
                <div class="hidden-md-and-down">Delete</div>
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
          <v-expansion-panel-content :color="secondary_color">
            <ResultView
                v-if="rowsTable[index].length > 0"
                :queryParams="expansionPanelsSingleInfo[index]"
                :queryResult="rowsTable[index]"
                :weekSeq="weekSeq[index]"
                :withLineages="false"
                @askAnalysis="(delay) => handleAnalysisRequest(index,delay)"
            />
            <div v-else class="empty-result-alert">
              <h4>
                <v-icon color="white" left>mdi-alert-circle-outline</v-icon>
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

import {mapState} from "vuex";
import axios from "axios";
import ResultView from "@/components/ResultView";
import Tab from "@/components/tabs/Tab";
import DatePicker from "@/components/form/DatePicker";
import LocationSelector from "@/components/form/LocationSelector";
import DatasetExplorer from "@/components/DatasetExplorer";

export default {
  name: "TabWithoutLineages",
  components: {DatasetExplorer, LocationSelector, DatePicker, Tab, ResultView},
  data() {
    return {
      /** Progress circe flag: true if the progress circle is displayed */
      isLoading: false,

      /** Server error flag */
      errorOccurred: false,

      /** Granularity: available options */
      possibleGranularity: [/*'world',*/ 'continent', 'country', 'region'],
      /** Granularity: selected option */
      selectedGranularity: null,

      /** Location: selected option */
      selectedLocation: null,

      /** Date: selected date */
      selectedDate: null,

      /** Panel expansion status array */
      expansionPanels: [],

      /** Panel search parameters array */
      expansionPanelsSingleInfo: [],

      /** Panel data array */
      rowsTable: [],

      /** Array of total number of sequences collected per week for each tab */
      weekSeq: [],

      /** Automatically clear the form after submit */
      autoclear: false
    }
  },
  computed: {
    ...mapState(['secondary_color', 'debug_mode']),

    /** Form error flag: true if the form cannot be sent */
    formError() {
      return !((this.selectedGranularity === 'world' && this.selectedDate != null) ||
          (this.selectedGranularity !== null && this.selectedLocation !== null && this.selectedDate !== null)
      )
    },
  },
  methods: {

    /** Clears the form */
    clearForm() {
      if (this.autoclear) {
        this.selectedDate = null;
        this.selectedLocation = null;
        this.selectedGranularity = null;
      }
    },

    /** Triggers the analysis request to the server */
    doAnalysis() {
      this.isLoading = true;
      let countNumAnalysis = this.rowsTable.length;
      let url = `/lineage_independent/getStatistics`;
      let to_send = {
        'granularity': this.selectedGranularity,
        'value': this.selectedLocation,
        'date': this.selectedDate
      };
      this.clearForm();

      axios.post(url, to_send)
          .then((res) => {
            return res.data;
          })
          .then((res) => {
            // Save the search parameters
            this.expansionPanelsSingleInfo[countNumAnalysis] = {
              'granularity': to_send.granularity,
              'location': to_send.value ? to_send.value : 'all',
              'date': to_send.date,
            };

            // Save the result data
            this.rowsTable[countNumAnalysis] = JSON.parse(JSON.stringify(res))['rows'];
            this.weekSeq[countNumAnalysis] = JSON.parse(JSON.stringify(res))['tot_seq'];
            this.isLoading = false;

            // Open the new panel and jump to the result container
            this.expansionPanels = [countNumAnalysis];
          })
          .catch(() => {
            this.errorOccurred = true
          });
    },

    /**
     * Handle next/prev analysis requests
     * @param index         Reference search
     * @param requestDelay  Delay for the new analysis
     */
    handleAnalysisRequest(index, requestDelay) {
      this.selectedGranularity = this.expansionPanelsSingleInfo[index].granularity;
      this.selectedLocation = this.expansionPanelsSingleInfo[index].location;
      const referenceDate = new Date(this.expansionPanelsSingleInfo[index].date);
      referenceDate.setDate(referenceDate.getDate() + requestDelay);
      this.selectedDate = referenceDate.toISOString().slice(0, 10);

      this.doAnalysis();
    },

    /** Handle error alert close */
    onCloseErrorAlert() {
      this.errorOccurred = false;
      this.isLoading = false;
    },

    /**
     * Removes the query from the result list
     * @param queryIndex  The index of the expansion panel to be removed
     */
    deleteQuery(queryIndex) {
      this.expansionPanelsSingleInfo.splice(queryIndex, 1)
      this.rowsTable.splice(queryIndex, 1)
      this.weekSeq.splice(queryIndex, 1)
    }
  },
  mounted() {
    // Default values (test purposes only)
    if (this.debug_mode)
      setTimeout(() => {
        this.selectedGranularity = 'country';
        this.selectedDate = '2022-02-01';
        this.selectedLocation = 'Italy';
        this.doAnalysis();
      }, 1000);
  },
}
</script>

<style scoped>

/* Form labels styling */
.field-label {
  justify-content: center;
  padding-top: 8px !important;
  padding-bottom: 5px !important;
  color: white;
}

/* Form elements styling */
.field-element {
  padding-top: 0 !important;
  padding-bottom: 4px !important;
  text-transform: capitalize;
}

/* Form controls styling */
.form-controls {
  margin-top: 26px !important;
  justify-content: center !important;
}

/* Result list styling */
.result-list {
  margin-bottom: 20px;
}

.result-list span {
  text-transform: capitalize;
  font-size: 17px;
  color: white;
  letter-spacing: 1px;
}

.result-list span b {
  text-transform: none;
}

v-expansion-panel-header {
  border-radius: var(--border-radius);
}

/* No result message styling */
.empty-result-alert {
  text-align: center;
  margin-top: 40px;
  margin-bottom: 20px;
  font-size: 17px;
  color: white !important;
  letter-spacing: 1px;
  line-height: 10px;
}

/* Panel action styling*/
.delete-action > * {
  float: right;
  margin-right: 5px;
  color: rgba(0, 0, 0, 0.54) !important;
}

.delete-action button:hover {
  background: #da3f3f !important;
  color: white !important;
}

</style>