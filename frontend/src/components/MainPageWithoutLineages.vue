<template>
  <div>
    <v-card width="100%" color="white" style="padding: 50px; min-height: 90.5vh">
        <v-row justify="center" align="center">
          <v-card width="95%" style="padding: 50px; margin-top: 50px; margin-bottom: 50px" :color="background_card_color">
             <v-card-text>
               <v-layout row wrap justify-center style="padding: 30px;">
                 <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                   <v-card width="95%" :color="menu_color">
                     <v-layout row wrap justify-center style="padding: 30px;">
                       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 10px">
                       <h2 style="color: white">DEFINE ANALYSIS:</h2>
                      </v-flex>
                      <v-flex class="no-horizontal-padding xs12 md4 d-flex" style="justify-content: center;">
                        <v-layout row wrap justify-center>
                          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding-top: 0; padding-bottom: 0">
                            <span style="color: white">Granularity:</span>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding-top: 0; padding-bottom: 0">
                            <v-select
                              v-model="selectedGeo"
                              :items="possibleGeo"
                              label="Granularity"
                              solo
                              hide-details
                            ></v-select>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                      <v-flex class="no-horizontal-padding xs12 md4 d-flex" style="justify-content: center;">
                        <v-layout row wrap justify-center>
                          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding-top: 0; padding-bottom: 0">
                            <span style="color: white">Location:</span>
                          </v-flex>
                          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding-top: 0; padding-bottom: 0">
                            <v-autocomplete
                              v-model="selectedSpecificGeo"
                              :items="possibleSpecificGeo"
                              label="Place"
                              solo
                              hide-details
                              :disabled="selectedGeo === null || selectedGeo === 'world'"
                            >
                              <template slot="item" slot-scope="data">
                                  <span>{{getFieldText(data.item)}}</span>
                              </template>
                            </v-autocomplete>
                          </v-flex>
                        </v-layout>
                      </v-flex>
                       <v-flex class="no-horizontal-padding xs12 md12 d-flex" style="justify-content: center;">
                       </v-flex>
                       <v-flex class="no-horizontal-padding xs12 md4 d-flex" style="justify-content: center;">
                         <v-layout row wrap justify-center>
                          <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding-top: 0; padding-bottom: 0">
                            <span style="color: white">Date:</span>
                          </v-flex>
                           <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; padding-top: 0; padding-bottom: 0">
                             <v-menu
                                ref="menu"
                                v-model="menu"
                                :close-on-content-click="false"
                                :return-value.sync="selectedDate"
                                transition="scale-transition"
                                offset-y
                                min-width="auto"
                              >
                                <template v-slot:activator="{ on, attrs }">
                                  <v-text-field
                                    v-model="selectedDate"
                                    label="Choose a date"
                                    readonly
                                    solo
                                    hide-details
                                    v-bind="attrs"
                                    v-on="on"
                                    append-icon="mdi-calendar"
                                    @click:append="menu=true"
                                  ></v-text-field>
                                </template>
                                <v-date-picker
                                  v-model="selectedDate"
                                  first-day-of-week="1"
                                  no-title
                                  scrollable
                                >
                                  <v-spacer></v-spacer>
                                  <v-btn
                                    text
                                    color="primary"
                                    @click="menu = false"
                                  >
                                    Cancel
                                  </v-btn>
                                  <v-btn
                                    text
                                    color="primary"
                                    @click="$refs.menu.save(selectedDate)"
                                  >
                                    OK
                                  </v-btn>
                                </v-date-picker>
                              </v-menu>
                           </v-flex>
                         </v-layout>
                       </v-flex>
                       <v-flex class="no-horizontal-padding xs12 md4 d-flex" style="justify-content: center;">
                         <v-layout row wrap justify-center>
                         </v-layout>
                       </v-flex>
                       <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                       <v-btn
                               @click="doAnalysis();"
                               color="#011936"
                               class="white--text"
                               :disabled="selectedGeo !== 'world' && (selectedGeo === null || selectedSpecificGeo === null)"
                        >
                            START ANALYSIS
                        </v-btn>
                     </v-flex>
                     </v-layout>
                   </v-card>
                 </v-flex>

                 <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center; margin-top: 50px" v-if="rowsTable.length > 0">
                   <h2 style="color: white">RESULTS: </h2>
                  </v-flex>
                 <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
                   <v-expansion-panels
                    v-model="expansionPanels"
                    :value="expansionPanels"
                    multiple focusable>
                      <v-expansion-panel style="margin-bottom: 10px" v-for="(array_rows, index) in rowsTable" v-bind:key="index">
                        <v-expansion-panel-header :color="menu_color">
                            <span style="width: 80%; color: black;">{{expansionPanelsSingleInfo[index]['location']}} /
                                              {{expansionPanelsSingleInfo[index]['date']}} /
                                              {{expansionPanelsSingleInfo[index]['weekNum']}} weeks
                            </span>
                        </v-expansion-panel-header>
                        <v-expansion-panel-content :color="menu_color">
                          <TablesComponentWithoutLineages
                            :rowsTable="rowsTable[index]"
                            :singleInfo = expansionPanelsSingleInfo[index]
                            :nameHeatmap="'heatmapWithoutLineage' + index"
                            :timeName="'timeDistributionWithoutLineage'+index"
                            :withLineages="false"
                            :tableIndex="'wo_l_' + index"
                            v-if="rowsTable[index].length > 0">
                          </TablesComponentWithoutLineages>
                          <div v-else style="text-align: center; margin-top: 20px">
                            <h2 style="color: white"> Not enough data for this location </h2>
                          </div>
                        </v-expansion-panel-content>
                      </v-expansion-panel>
                   </v-expansion-panels>
                 </v-flex>
               </v-layout>
             </v-card-text>
          </v-card>
        </v-row>
    </v-card>

    <v-overlay :value="overlay">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>

  </div>
</template>

<script>

import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import TablesComponentWithoutLineages from "@/components/TablesComponentWithoutLineages";

export default {
  name: "MainPageWithoutLineages",
  components: {TablesComponentWithoutLineages},
  data() {
    return {
      menu: false,
      overlay: false,
      allGeo: null,
      selectedGeo: 'world',
      possibleGeo: ['world', 'continent', 'country', 'region'],
      selectedSpecificGeo: null,
      possibleSpecificGeo: [],
      selectedDate: null,

      expansionPanels: [],
      expansionPanelsSingleInfo: [],

      rowsTable: [],
    }
  },
  computed: {
    ...mapState(['background_card_color', 'menu_color', 'toolbar_color', 'all_geo']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    getFieldText(item){
      let name;
      if (item === null){
        name = 'N/D'
      }
      else{
        name = item;
      }
      return name;
    },
    doAnalysis(){
      this.loadTables();
    },
    loadTables(){
      this.overlay = true;
      let countNumAnalysis = this.rowsTable.length;
      let url = `/analyse_mutations_without_lineages/getStatistics`;
      let to_send = {
        'granularity': this.selectedGeo,
        'value': this.selectedSpecificGeo,
        'date': this.selectedDate,
        'numWeek': this.selectedWeekNum};

      axios.post(url, to_send)
        .then((res) => {
          return res.data;
        })
        .then((res) => {

          this.expansionPanelsSingleInfo[countNumAnalysis] = {
            'weekNum': this.selectedWeekNum,
            'date': this.selectedDate,
            'granularity': this.selectedGeo,
            'location': this.selectedSpecificGeo,
          };

          this.rowsTable[countNumAnalysis] = JSON.parse(JSON.stringify(res));

          this.selectedWeekNum = 4;
          this.selectedDate = new Date().toISOString().slice(0, 10);
          this.selectedGeo = 'world';
          this.selectedSpecificGeo = null;
          this.overlay = false;
          this.expansionPanels.push(countNumAnalysis);
        });
    },
  },
  mounted() {
      this.selectedDate = new Date().toISOString().slice(0, 10);
      this.selectedSpecificGeo = null;
      this.possibleSpecificGeo = [];
      this.allGeo = this.all_geo;

      // //DEFAULT VALUES
      // setTimeout(() => {
      //   this.selectedGeo = 'country';
      //   this.selectedDate = '2022-02-01';
      //   this.selectedSpecificGeo = 'Italy';
      //   this.doAnalysis();
      // }, 1000);
      // //DEFAULT VALUES
  },
  watch: {
    all_geo(){
      this.allGeo = this.all_geo;
    },
    selectedGeo(){
      this.possibleSpecificGeo = [];
      let i = 0;
      if (this.selectedGeo !== 'world') {
        while (i < this.allGeo[this.selectedGeo].length) {
          if (this.allGeo[this.selectedGeo][i] != null) {
            this.possibleSpecificGeo.push(this.allGeo[this.selectedGeo][i]);
          } else {
            this.possibleSpecificGeo.push('N/D');
          }
          i = i + 1;
        }
      }
      this.possibleSpecificGeo.sort();
    },
  },
}
</script>

<style scoped>

</style>