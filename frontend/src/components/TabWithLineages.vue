<!--
  Component:    TabWithLineages
  Description:  Tab to perform lineage specific analyses.

  Props:
  ├── allLocations: list of all the possible locations. Required.
  └── allLineages: list of all the possible lineages. Required.
-->

<template>
  <div>

    <!-- Analysis definition form -->
    <v-container class="root-container">
      <v-container class="child-container">
        <div class="card-container">

          <v-card :color="secondary_color">
            <v-layout class="card-content" justify-center row wrap>

              <!-- Form header -->
              <v-flex class="xs12 d-flex form-header">
                <h2>DEFINE ANALYSIS</h2>
              </v-flex>

              <!-- Form fields -->
              <!---- Granularity -->
              <v-flex class="xs12 sm6 md3 d-flex">
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
              <v-flex v-if="selectedGranularity!=='world'" class="xs12 sm6 md3 d-flex">
                <v-layout row wrap>
                  <v-flex class="xs12 d-flex field-label">
                    <span>Location</span>
                  </v-flex>

                  <v-flex class="xs12 d-flex field-element">
                    <v-autocomplete v-model="selectedLocation"
                                    :disabled="selectedGranularity === null || selectedGranularity === 'world'"
                                    :items="possibleLocations"
                                    hide-details
                                    label="Location"
                                    solo>
                      <template slot="item" slot-scope="data">
                        <span>{{ getFieldText(data.item) }}</span>
                      </template>
                    </v-autocomplete>
                  </v-flex>
                </v-layout>
              </v-flex>

              <!---- Date -->
              <v-flex class="xs12 sm6 md3 d-flex">
                <v-layout justify-center row wrap>
                  <v-flex class="xs12 d-flex field-label">
                    <span>Date</span>
                  </v-flex>

                  <v-flex class="xs12 d-flex field-element">
                    <v-menu v-model="menuVisibility"
                            :close-on-content-click="false"
                            min-width="auto"
                            offset-y
                            transition="scale-transition">
                      <template v-slot:activator="{ on, attrs }">
                        <v-text-field v-model="selectedDate"
                                      append-icon="mdi-calendar"
                                      hide-details
                                      label="Date"
                                      readonly
                                      solo
                                      v-bind="attrs"
                                      v-on="on"
                                      @click:append="menuVisibility=true"
                        />
                      </template>
                      <v-date-picker v-model="selectedDate"
                                     :max="today"
                                     first-day-of-week="1"
                                     no-title
                                     scrollable
                                     @input="menuVisibility = false"
                      />
                    </v-menu>
                  </v-flex>
                </v-layout>
              </v-flex>

              <!---- Lineage -->
              <v-flex v-if="selectedGranularity!=='world'" class="xs12 sm6 md3 d-flex">
                <v-layout row wrap>
                  <v-flex class="xs12 d-flex field-label">
                    <span>Lineage</span>
                  </v-flex>

                  <v-flex class="xs12 d-flex field-element">
                    <v-autocomplete
                        v-model="selectedLineage"
                        :disabled="selectedGranularity === null || (selectedLocation === null && selectedGranularity !== 'world') || selectedDate === null"
                        :items="possibleLineages"
                        clearable
                        hide-details
                        label="Lineage"
                        solo
                    >
                    </v-autocomplete>
                  </v-flex>
                </v-layout>
              </v-flex>

              <!-- Send button -->
              <v-flex class="xs12 sm6 md12 d-flex form-controls">
                <v-btn :disabled="formError"
                       class="white--text"
                       color="#011936"
                       @click="doAnalysis();"
                >
                  <v-icon left>mdi-magnify</v-icon>  START ANALYSIS
                </v-btn>
              </v-flex>
            </v-layout>
          </v-card>
        </div>

      </v-container>
    </v-container>

    <!-- Analysis results -->
    <v-container ref="result" class="root-container">
      <v-container v-if="rowsTable.length > 0" class="child-container">
        <div class="card-container">

          <!-- Panels list -->
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
                  {{ expansionPanelsSingleInfo[index]['date'] }} /
                  {{ expansionPanelsSingleInfo[index]['lineage'] }}
                </span>
              </v-expansion-panel-header>

              <!-- Panel content -->
              <v-expansion-panel-content :color="secondary_color">
                <AnalysisResult
                    v-if="rowsTable[index].length > 0"
                    :queryResult="rowsTable[index]"
                    :queryParams=expansionPanelsSingleInfo[index]
                    :withLineages="true"
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

        </div>
      </v-container>
    </v-container>


    <!-- Progress circle -->
    <v-overlay :value="isLoading">
      <v-progress-circular
          indeterminate
          size="64"
      ></v-progress-circular>
    </v-overlay>

    <!-- Error message -->
    <v-overlay :value="errorOccurred">
      <v-container>
        <v-alert dismissible elevation="24" type="error" @input="errorOccurred=false; isLoading=false">
          <b>The server is temporarily unreachable</b><br/>
          An error occurred while contacting the server. Please try again later.
        </v-alert>
      </v-container>
    </v-overlay>

  </div>
</template>

<script>

import {mapState} from "vuex";
import axios from "axios";
import AnalysisResult from "./AnalysisResult";

export default {
  name: "TabWithLineages",
  components: {AnalysisResult},
  props: {
    /** List of all the possible locations. Required. */
    allLocations: {required: true},

    /** List of all the possible lineages. Required. */
    allLineages: {required: true}
  },
  data() {
    return {
      /** Visibility flag of date picker menu */
      menuVisibility: false,

      /** Progress circe flag: true if the progress circle is displayed */
      isLoading: false,

      /** Server error flag */
      errorOccurred: false,

      /** Granularity: available options */
      possibleGranularity: [/*'world',*/ 'continent', 'country', 'region'],
      /** Granularity: selected option */
      selectedGranularity: null,

      /** Location: available options (wrt to other params) */
      possibleLocations: [],
      /** Location: selected option */
      selectedLocation: null,

      /** Date: selected date */
      selectedDate: null,

      /** Lineage: available options (wrt to other params) */
      possibleLineages: this.allLineages,
      /** Lineage: selected option */
      selectedLineage: null,

      /** Today date */
      today: new Date().toISOString().slice(0, 10),

      /** Panel expansion status array */
      expansionPanels: [],

      /** Panel search parameters array */
      expansionPanelsSingleInfo: [],

      /** Panel data array */
      rowsTable: [],
    }
  },
  computed: {
    ...mapState(['secondary_color']),

    /** Form error flag: true if the form cannot be sent */
    formError() {
      return !((this.selectedGranularity === 'world' && this.selectedDate !== null && this.selectedLineage !== null) ||
          (this.selectedGranularity !== null && this.selectedLocation !== null && this.selectedDate !== null && this.selectedLineage !== null)
      )
    },
  },
  methods: {
    /** Returns the hint for the field completion */
    getFieldText(item) {
      let name;
      if (item === null) {
        name = 'N/D'
      } else {
        name = item;
      }
      return name;
    },

    /** Clears the form */
    clearForm(){
      this.selectedLineage=null;
      this.selectedDate=null;
      this.selectedLocation=null;
      this.selectedGranularity=null;
    },

    /** Triggers the analysis request to the server */
    doAnalysis() {
      this.isLoading = true;
      let countNumAnalysis = this.rowsTable.length;
      let url = `/analyse_mutations/getStatistics`;
      let to_send = {
        'granularity': this.selectedGranularity,
        'value': this.selectedLocation,
        'date': this.selectedDate,
        'lineage': this.selectedLineage
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
              'location': to_send.value,
              'date': to_send.date,
              'lineage': to_send.lineage
            };

            // Save the result data
            this.rowsTable[countNumAnalysis] = JSON.parse(JSON.stringify(res));

            this.isLoading = false;

            // Open the new panel and jump to the result container
            this.expansionPanels = [countNumAnalysis];
            this.$refs.result.scrollIntoView();
          })
          .catch(() => {
            this.errorOccurred = true
          });
    },

    /** Compute the possible locations based on the other parameters of the form*/
    computePossibleLocations() {
      this.possibleLocations = [];
      this.selectedLocation = null;
      let i = 0;
      if (this.allLocations !== null) {
        if (this.selectedGranularity !== 'world') {
          while (i < this.allLocations[this.selectedGranularity].length) {
            if (this.allLocations[this.selectedGranularity][i] != null) {
              this.possibleLocations.push(this.allLocations[this.selectedGranularity][i]);
            } else {
              this.possibleLocations.push('N/D');
            }
            i = i + 1;
          }
        } else {
          this.selectedLocation = 'all'
        }
      }
      this.possibleLocations.sort();
    },

    /** Fetch all possible values for lineages (given the other params) */
    getPossibleLineages() {
      if (this.selectedLocation !== null && this.selectedDate !== null) {
        let url = `/analyse_mutations/getGeoLineages`;
        let to_send = {
          'geo': this.selectedLocation,
          'date': this.selectedDate
        };
        axios.post(url, to_send)
            .then((res) => {
              this.possibleLineages = res.data;
            })
      }
    }
  },
  mounted() {
    // Default values (test purposes only)
    // setTimeout(() => {
    //   this.selectedGranularity = 'country';
    //   this.selectedDate = '2022-02-01';
    //   this.selectedLocation = 'Italy';
    //   this.selectedLineage = 'BA.1';
    //   this.doAnalysis();
    // }, 1000);
  },
  watch: {
    /** Adjust the possible locations according to the selected granularity */
    selectedGranularity() {
      this.computePossibleLocations()
    },

    /** Adjust the possible lineages according to the selected location */
    selectedLocation() {
      this.getPossibleLineages()
    },

    /** Adjust the possible lineages according to the selected date */
    selectedDate() {
      this.getPossibleLineages()
    },
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
  background-color: #014878;
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