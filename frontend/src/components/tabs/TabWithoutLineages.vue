<!--
  Component:    TabWithoutLineages
  Description:  Tab to perform lineage independent analyses.

  Props:
  └── allLocations: list of all the possible locations. Required.
-->

<template>
  <Tab :is-loading="isLoading"
       :error-occurred="errorOccurred"
       :result-length="rowsTable.length"
       :form-error="formError"
       @send="doAnalysis()"
       @close-error-alert="onCloseErrorAlert()"
  >

    <!-- Form fields -->
    <template v-slot:form>

      <!---- Granularity -->
      <v-flex class="xs12 sm6 md4 d-flex">
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
      <v-flex v-if="selectedGranularity!=='world'" class="xs12 sm6 md4 d-flex">
        <LocationSelector :allLocations="allLocations" :selectedGranularity="selectedGranularity" v-model="selectedLocation"/>
      </v-flex>

      <!---- Date -->
      <v-flex class="xs12 sm6 md4 d-flex">
        <DatePicker v-model="selectedDate"/>
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
          </v-expansion-panel-header>

          <!-- Panel content -->
          <v-expansion-panel-content :color="secondary_color">
            <AnalysisResult
                v-if="rowsTable[index].length > 0"
                :queryResult="rowsTable[index]"
                :queryParams="expansionPanelsSingleInfo[index]"
                :weekSeq="weekSeq[index]"
                :withLineages="false"
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
import AnalysisResult from "@/components/ResultView";
import Tab from "@/components/tabs/Tab";
import DatePicker from "@/components/form/DatePicker";
import LocationSelector from "@/components/form/LocationSelector";

export default {
  name: "TabWithoutLineages",
  components: {LocationSelector, DatePicker, Tab, AnalysisResult},
  props: {
    /** List of all the possible locations. Required. */
    allLocations: {required: true}
  },
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
      weekSeq: []
    }
  },
  computed: {
    ...mapState(['secondary_color']),

    /** Form error flag: true if the form cannot be sent */
    formError() {
      return !((this.selectedGranularity === 'world' && this.selectedDate != null) ||
          (this.selectedGranularity !== null && this.selectedLocation !== null && this.selectedDate !== null)
      )
    },
  },
  methods: {

    /** Clears the form */
    clearForm(){
      this.selectedDate=null;
      this.selectedLocation=null;
      this.selectedGranularity=null;
    },

    /** Triggers the analysis request to the server */
    doAnalysis() {
      this.isLoading = true;
      let countNumAnalysis = this.rowsTable.length;
      let url = `/analyse_mutations_without_lineages/getStatistics`;
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
              'location': to_send.value? to_send.value : 'all' ,
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

    /** Handle error alert close */
    onCloseErrorAlert(){
      this.errorOccurred=false;
      this.isLoading=false;
    }
  },
  mounted() {
    // Default values (test purposes only)
    // setTimeout(() => {
    //   this.selectedGranularity = 'country';
    //   this.selectedDate = '2022-02-01';
    //   this.selectedLocation = 'Italy';
    //   this.doAnalysis();
    // }, 1000);
  },
}
</script>

<style scoped>

/* Root tab container styling */
.root-container {
  margin: 0 auto auto auto;
  min-width: 97vw;
  height: 100%;
}

/* Child tab container styling */
.child-container {
  background-color: var(--primary-color);
  border-radius: 8px;
  margin-top: 15px;
  margin-bottom: 0;
  min-width: 96vw;
}

/* Form container styling */
.card-container {
  margin: 15px auto;
  justify-content: center;
  padding: 15px 1vw 15px 1vw;
}

/* Form content styling */
.card-content {
  padding: 30px;
  margin: auto;
}

/* Headings */
.form-header, .result-header {
  color: white;
  justify-content: center;
  text-align: center;
}

.result-header {
  margin-bottom: 20px;
}

/* Form labels styling */
.field-label {
  justify-content: center;
  padding-top: 5px !important;
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
  border-radius: 4px;
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


</style>