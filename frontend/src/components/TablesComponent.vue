<template>
  <v-layout row wrap justify-center style="padding-top: 30px;">
    <v-flex class="no-horizontal-padding xs12 md4 lg2 d-flex" style="justify-content: center;" v-if="withLineages">
      <v-autocomplete
        v-model="selectedLineage"
        :items="possibleLineage"
        label="Lineage"
        solo
        hide-details
        clearable
      ></v-autocomplete>
    </v-flex>
    <v-flex class="no-horizontal-padding xs12 md4 lg2 d-flex" style="justify-content: center;">
      <v-autocomplete
        v-model="selectedProtein"
        :items="possibleProtein"
        label="Protein"
        solo
        hide-details
        clearable
      ></v-autocomplete>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 md12 lg12 d-flex" style="justify-content: center;">
       <v-layout row wrap justify-center style="padding-top: 30px;">
         <v-flex class="no-horizontal-padding xs6 md4 lg2 d-flex" style="justify-content: center;">
<!--          <v-switch-->
<!--            v-model="switch_alert"-->
<!--            label="Only Important Mutation"-->
<!--          >-->
<!--            <template v-slot:label>-->
<!--              <span style="color: white">Only Important Mutation</span>-->
<!--           </template>-->
<!--          </v-switch>-->
         </v-flex>
         <v-flex class="no-horizontal-padding xs6 md2 lg1 d-flex" style="justify-content: center;">
          <v-text-field
            v-model="maxNumberOfImportantMuts"
            label="Protein"
            solo
            min="0"
            hide-details
            type="number"
            style="width: 10%"
          ></v-text-field>
         </v-flex>
       </v-layout>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 md4 lg4 d-flex" style="justify-content: center;">
      <v-switch
        v-model="switch_show_perc"
      >
        <template v-slot:label>
          <span style="color: white">Show Percentage</span>
       </template>
      </v-switch>
    </v-flex>
    <v-flex class="no-horizontal-padding xs12 md4 lg4 d-flex" style="justify-content: center;">
    </v-flex>
    <v-flex class="no-horizontal-padding xs12 md4 lg4 d-flex" style="justify-content: center;">
      <v-btn @click="dialogTableHeaders = true" color="primary">
        INFO TABLE'S HEADERS
      </v-btn>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
        <h2 style="color: white">TABLE<v-btn @click="downloadTable()" x-small icon
                style="margin-left: 20px; margin-bottom: 5px; color: white">
                  <v-icon size="23">
                    mdi-download-circle-outline
                  </v-icon>
              </v-btn>
        </h2>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 md12 lg12 d-flex" style="justify-content: center;">
          <v-data-table
                :headers="headerTable"
                :items="filteredResults"
                :id = "nameHeatmap + 'table'"
                class="data-table table_prov_reg"
                style="width: 98%; border: grey solid 1px"
                multi-sort
                :sort-by.sync="sortByTable"
                :sort-desc.sync="sortDescTable"
                :custom-sort="customSort"
          >
              <template v-slot:item ="{ item }">
                <tr>
                  <td style="white-space:pre-wrap; word-wrap:break-word; text-align: center" v-for="header in headerTableSubPlaces"
                          :key="header.value" v-show="header.show">
                           <span v-if="header.value === 'info'">
                                <v-btn
                                  class="info-button"
                                  x-small
                                  text icon color="blue"
                                   @click.stop="handleClickRow(item)">
                                  <v-icon class="info-icon">mdi-information</v-icon>
                                </v-btn>
                            </span>
                            <span v-else-if="header.value !== 'location' && header.value !== 'lineage'
                            && header.value !== 'protein' && header.value !== 'mut' && item[header.value] !== null
                            && item[header.value] !== undefined && !header.value.includes('perc')"
                                  style="white-space: pre-line">{{Number.parseFloat(item[header.value]).toPrecision(2)}}
                            </span>
                            <span v-else style="white-space: pre-line"> {{item[header.value]}}</span>
                      </td>
                </tr>
              </template>
          </v-data-table>
    </v-flex>


    <v-dialog
      persistent
      v-model="dialogTableHeaders"
      width="1300"
      >
        <v-card>
          <v-card-title class="white--text" v-bind:style="{ backgroundColor: 'grey' }">
            INFO TABLE'S HEADERS
            <v-spacer></v-spacer>
            <v-btn
                style="background-color: red"
                slot="activator"
                icon
                small
                color="white"
                @click="dialogTableHeaders = false"
            >
              X
            </v-btn>
          </v-card-title>

          <v-card-text class="text-xs-center" style="padding: 20px">
            <li><b>P value with mut: </b>  shows if the population «lineage + mutation» is growing differently compared to everything else. </li><br>
            <li><b>P value without mut: </b>  shows if the population «lineage without mutation» is growing differently compared to everything else. </li><br>
            <li><b>P value comparative: </b>  shows if the population «lineage + mutation» is growing differently compared to the population «lineage without mutation». </li><br>
            <li><b>Slope: </b> is calculated through a linear interpolation of the diffusion (percentage).  (y=<b>m</b>x + q)</li><br>
            <li><b>Y-intercept: </b> is calculated through a linear interpolation of the diffusion (percentage).  (y=mx + <b>q</b>)</li><br>
          </v-card-text>

        </v-card>
      </v-dialog>


    <v-dialog
      persistent
      v-model="dialogSelectedItem"
      width="1300"
      >
        <v-card>
          <v-card-title class="white--text" v-bind:style="{ backgroundColor: 'grey' }">
            MORE INFO
            <v-spacer></v-spacer>
            <v-btn
                style="background-color: red"
                slot="activator"
                icon
                small
                color="white"
                @click="closeDialogSelectedItem()"
            >
              X
            </v-btn>
          </v-card-title>

          <v-card-text class="text-xs-center">
            <div v-if="selectedItem !== null">
              <span v-for="(item, key, index) in selectedItem['important_info']" v-bind:key="key + index">
                <b>{{key}}:</b> {{item}} <br>
              </span>

              <br><br>

              <span v-for="(item, key, index) in selectedItem['dates_info']" v-bind:key="key + index">
                <b>{{key}}:</b> {{item}} <br>
              </span>
            </div>
          </v-card-text>

        </v-card>
      </v-dialog>

    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center" v-if="showCharts">
        <h2 style="color: white; margin-top: 80px;">
          HEATMAP (Diffusion)
        </h2>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="showCharts">
      <HeatmapMuts
        :nameHeatmap="nameHeatmap"
        :mutsData="filteredResults"
        :singleInfo= "singleInfo"
        :sortColumn="sortByTable"
        :descColumn="sortDescTable"
        :withLineages="false">
      </HeatmapMuts>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center" v-if="showCharts">
        <h2 style="color: white; margin-top: 80px;">
          DIFFUSION BAR CHART
        </h2>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;" v-if="showCharts">
      <BarChartPrevalence
        :time-name="timeName"
        :time-distribution="filteredResults"
        :singleInfo = "singleInfo"
        :sortColumn="sortByTable"
        :descColumn="sortDescTable"
        :withLineages="withLineages"
        style="padding: 0; width: 100%;  margin-top: 50px;">
      </BarChartPrevalence>
    </v-flex>

  </v-layout>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import HeatmapMuts from "@/components/HeatmapMuts";
import BarChartPrevalence from "@/components/BarChartPrevalence";

export default {
  name: "TablesComponent",
  components: {BarChartPrevalence, HeatmapMuts},
  props: {
    rowsTable: {required: true,},
    singleInfo: {required: true},
    nameHeatmap: {required: true},
    timeName: {required: true},
    withLineages: {required: true}
  },
  data() {
    return {
      switch_alert: false,
      filteredResults: [],
      showCharts: false,
      maxNumberOfImportantMuts: 20,
      switch_show_perc: false,

      selectedRows: [],

      headerTable: [],
      headerTableSubPlaces: [],
      sortByTable: [],
      sortDescTable: [],
      sortByTableSubPlaces: [],
      sortDescTableSubPlaces: [],

      selectedLineage: null,
      possibleLineage: [],
      selectedProtein: null,
      possibleProtein: [],
      selectedLocation: null,
      possibleLocation: [],
      selectedLocationFirstTable: null,
      possibleLocationFirstTable: [],

      dialogSelectedItem: false,
      selectedItem: null,
      dialogTableHeaders: false,
    }
  },
  computed: {
    ...mapState(['toolbar_color']),
    ...mapGetters({}),
  },
  methods: {
    ...mapMutations([]),
    ...mapActions([]),
    downloadTable(){
      let result_sorted = this.customSort(this.filteredResults, this.sortByTable, this.sortDescTable);
      let text = this.json2csv(result_sorted, this.headerTable);
      let filename = "LinSpec_" + this.singleInfo['location'] + '_';
      if(this.singleInfo['lineage'] !== null && this.singleInfo['lineage'] !== undefined){
        filename += this.singleInfo['lineage'] + '_';
      }
      filename += this.singleInfo['date'] + '_' + this.singleInfo['weekNum'] + 'week.csv'
      let element = document.createElement('a');
      element.setAttribute('download', filename);
      var data = new Blob([text]);
      element.href = URL.createObjectURL(data);
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    },
    json2csv(input, selected_headers) {
        var json = input;
        var fields = [];
        var fields2 = [];
        selected_headers.forEach(function (el) {
            fields.push(el.text.replaceAll("\n", ""));
        });
        selected_headers.forEach(function (el) {
            fields2.push(el.value.replaceAll("\n", ""));
        });
        var csv = json.map(function (row) {
            return fields2.map(function (fieldName) {
                let string_val;
                string_val = String(row[fieldName]);
                string_val = string_val.replaceAll("\n", " ");
                return JSON.stringify(string_val);
            }).join(',')
        });
        csv.unshift(fields.join(','));
        return csv.join('\r\n')
    },
        customSort(items, index, isDesc) {
        if(index !== null && index !== undefined){
          let i = 0;
          let len = index.length - 1;
          let idx = index[i];
          let desc = isDesc[i];
          if(idx !== null && idx !== undefined) {
            items.sort((a, b) => {
              if (!idx.includes('p_value') && !idx.includes('polyfit')) {
                if (idx === 'mut') {
                  if (desc) {
                    let pos_a = a['muts'][0]['loc'];
                    let pos_b = b['muts'][0]['loc'];
                    if (pos_a !== pos_b || i >= len) {
                      return pos_b < pos_a ? -1 : 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  } else {
                    let pos_a = a['muts'][0]['loc'];
                    let pos_b = b['muts'][0]['loc'];
                    if (pos_a !== pos_b || i >= len) {
                      return pos_b > pos_a ? -1 : 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                }
                else if(idx.includes('perc')){
                  let date = idx.replace('perc_with_absolute_number','');
                  let realKey = 'perc_with_mut_this_week' + date;
                  if (desc) {
                    if(a[idx] === null || a[idx] === undefined){
                      if (b[idx] !== a[idx] || i >= len) {
                        return 1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                    if(b[idx] === null || b[idx] === undefined){
                      if (b[idx] !== a[idx] || i >= len) {
                        return -1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                    if (b[realKey] !== a[realKey] || i >= len) {
                      return Number(b[realKey]) < Number(a[realKey]) ? -1 : 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  } else {
                    if(a[idx] === null || a[idx] === undefined){
                      if (b[idx] !== a[idx] || i >= len) {
                        return 1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                    if(b[idx] === null || b[idx] === undefined){
                      if (b[idx] !== a[idx] || i >= len) {
                        return -1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                    if (b[realKey] !== a[realKey] || i >= len) {
                      return Number(b[realKey]) > Number(a[realKey]) ? -1 : 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                }
                else{
                  if (desc) {
                      if (b[idx] !== a[idx] || i >= len) {
                        return b[idx] < a[idx] ? -1 : 1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    } else {
                      if (b[idx] !== a[idx] || i >= len) {
                        return b[idx] > a[idx] ? -1 : 1;
                      }
                      else{
                        return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                      }
                    }
                }
              }
              else{
                if (desc) {
                  if(a[idx] === null || a[idx] === undefined){
                    if (b[idx] !== a[idx] || i >= len) {
                      return 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                  if(b[idx] === null || b[idx] === undefined){
                    if (b[idx] !== a[idx] || i >= len) {
                      return -1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                  if (b[idx] !== a[idx] || i >= len) {
                    return Number(b[idx]) < Number(a[idx]) ? -1 : 1;
                  }
                  else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                } else {
                  if(a[idx] === null || a[idx] === undefined){
                    if (b[idx] !== a[idx] || i >= len) {
                      return 1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                  if(b[idx] === null || b[idx] === undefined){
                    if (b[idx] !== a[idx] || i >= len) {
                      return -1;
                    }
                    else{
                      return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                    }
                  }
                  if (b[idx] !== a[idx] || i >= len) {
                    return Number(b[idx]) > Number(a[idx]) ? -1 : 1;
                  }
                  else{
                    return this.singleCustomSort(a, b, i+1, len, index, isDesc);
                  }
                }
              }
            });
          }
          return items;
        }
    },
    singleCustomSort(a, b, i, len, index, isDesc) {
      let idx = index[i];
      let desc = isDesc[i];
      if (!idx.includes('p_value') && !idx.includes('polyfit')) {
        if (idx === 'mut') {
          if (desc) {
            let pos_a = a['muts'][0]['loc'];
            let pos_b = b['muts'][0]['loc'];
            if (pos_a !== pos_b || i >= len) {
              return pos_b < pos_a ? -1 : 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          } else {
            let pos_a = a['muts'][0]['loc'];
            let pos_b = b['muts'][0]['loc'];
            if (pos_a !== pos_b || i >= len) {
              return pos_b > pos_a ? -1 : 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
        }
        else if(idx.includes('perc')){
          let date = idx.replace('perc_with_absolute_number','');
          let realKey = 'perc_with_mut_this_week' + date;
          if (desc) {
            if(a[idx] === null || a[idx] === undefined){
              if (b[idx] !== a[idx] || i >= len) {
                return 1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
            if(b[idx] === null || b[idx] === undefined){
              if (b[idx] !== a[idx] || i >= len) {
                return -1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
            if (b[realKey] !== a[realKey] || i >= len) {
              return Number(b[realKey]) < Number(a[realKey]) ? -1 : 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          } else {
            if(a[idx] === null || a[idx] === undefined){
              if (b[idx] !== a[idx] || i >= len) {
                return 1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
            if(b[idx] === null || b[idx] === undefined){
              if (b[idx] !== a[idx] || i >= len) {
                return -1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
            if (b[realKey] !== a[realKey] || i >= len) {
              return Number(b[realKey]) > Number(a[realKey]) ? -1 : 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
        }
        else{
          if (desc) {
              if (b[idx] !== a[idx] || i >= len) {
                return b[idx] < a[idx] ? -1 : 1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            } else {
              if (b[idx] !== a[idx] || i >= len) {
                return b[idx] > a[idx] ? -1 : 1;
              }
              else{
                return this.singleCustomSort(a, b, i+1, len, index, isDesc);
              }
            }
        }
      }
      else{
        if (desc) {
          if(a[idx] === null || a[idx] === undefined){
            if (b[idx] !== a[idx] || i >= len) {
              return 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
          if(b[idx] === null || b[idx] === undefined){
            if (b[idx] !== a[idx] || i >= len) {
              return -1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
          if (b[idx] !== a[idx] || i >= len) {
            return Number(b[idx]) < Number(a[idx]) ? -1 : 1;
          }
          else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
        } else {
          if(a[idx] === null || a[idx] === undefined){
            if (b[idx] !== a[idx] || i >= len) {
              return 1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
          if(b[idx] === null || b[idx] === undefined){
            if (b[idx] !== a[idx] || i >= len) {
              return -1;
            }
            else{
              return this.singleCustomSort(a, b, i+1, len, index, isDesc);
            }
          }
          if (b[idx] !== a[idx] || i >= len) {
            return Number(b[idx]) > Number(a[idx]) ? -1 : 1;
          }
          else{
            return this.singleCustomSort(a, b, i+1, len, index, isDesc);
          }
        }
      }

    },
    handleClickRow(item){
      let new_obj = {'important_info': {}, 'dates_info': {}};
      let array_important_info = [];
      if(this.withLineages) {
        array_important_info = [
          'location',
          'lineage',
          'protein',
          'mut',
        ]
      }
      else{
        array_important_info = [
          'location',
          'protein',
          'mut',
        ]
      }
      let array_dates_info = [
          'p_value_comparative_mut',
          'p_value_without_mut',
          //diff_perc_without_mut',
          'perc_without_mut_this_week',
          'perc_without_mut_prev_week',
          'count_without_mut_this_week',
          'count_without_mut_prev_week',
          'p_value_with_mut',
          //'diff_perc',
          // 'diff_perc_with_mut',
          'perc_with_mut_this_week',
          'perc_with_mut_prev_week',
          'count_with_mut_this_week',
          'count_with_mut_prev_week',
          'total_seq_lineage_this_week',
          'total_seq_lineage_prev_week',
          'total_seq_pop_this_week',
          'total_seq_pop_prev_week'
      ]

      Object.keys(item).forEach(elem => {
        array_important_info.find(element => {
          if (elem === element) {
            new_obj['important_info'][elem] = item[elem];
          }
        });
        array_dates_info.find(element => {
          if (elem.includes(element)) {
            new_obj['dates_info'][elem] = item[elem];
          }
        });
      })

      this.selectedItem = new_obj;
      this.dialogSelectedItem = true;
    },
    closeDialogSelectedItem(){
      this.selectedItem = null;
      this.dialogSelectedItem = false;
    },
    loadTables(){
      let predefined_headers = [];
      if(this.withLineages) {
        predefined_headers = [
          //{text: 'Info', value: 'info', sortable: false, show: true, align: 'center', width: '3vh'},
          {text: 'Location', value: 'location', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Lineage', value: 'lineage', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Protein', value: 'protein', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Mut', value: 'mut', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Slope', value: 'polyfit_slope', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Y-intercept', value: 'polyfit_intercept', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'P-value with mut', value: 'p_value_with_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'P-value without mut', value: 'p_value_without_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'P-value comparative', value: 'p_value_comparative_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},
        ]
      }
      else{
        predefined_headers = [
          //{text: 'Info', value: 'info', sortable: false, show: true, align: 'center', width: '3vh'},
          {text: 'Location', value: 'location', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Protein', value: 'protein', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Mut', value: 'mut', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Slope', value: 'polyfit_slope', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Y-intercept', value: 'polyfit_intercept', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'P-value with mut', value: 'p_value_with_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'P-value without mut', value: 'p_value_without_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'P-value comparative', value: 'p_value_comparative_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},

        ]
      }

      let additional_headers = [];
      // let array_possible_header = ['diff_perc', 'perc_this_week', 'perc_prev_week', 'count_this_week',
      //   'count_prev_week']
      let array_possible_header = [
      ]

      if(!this.withLineages){
        array_possible_header.unshift('perc_with_mut_this_week');
      }

      let analysis_date = this.singleInfo['date'];
      for(let i = 0; i < array_possible_header.length; i++){
        let value = array_possible_header[i] + '_' + analysis_date;
        let text = array_possible_header[i] + '_' + analysis_date + '\n';
        // let text = i.toString();
        text = text.replaceAll('_', ' ');
        text = text.charAt(0).toUpperCase() + text.slice(1);
        let single_header = {text: text, value: value, sortable: true, show: true, align: 'center', width: '10vh'};
        additional_headers.unshift(single_header);
      }

      let max = this.singleInfo['weekNum'] - 1;

      for(let j=0; j<max; j=j+1){
        let this_date = new Date(analysis_date);
        let days = 7 ;
        // if(j === 0) {
        //   days = 7;
        // }
        // else{
        //   days = 6;
        // }
        let previous_date = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
        analysis_date = previous_date.toISOString().split('T')[0]
        for(let i = 0; i < array_possible_header.length; i++){
          let value = array_possible_header[i] + '_' + analysis_date;
          let text = array_possible_header[i] + '_' + analysis_date + '\n';
          // let text = i.toString();
          text = text.replaceAll('_', ' ');
          text = text.charAt(0).toUpperCase() + text.slice(1);
          let single_header = {text: text, value: value, sortable: true, show: true, align: 'center', width: '10vh'};
          additional_headers.unshift(single_header);
        }
      }

      predefined_headers = predefined_headers.concat(additional_headers);

      let array_to_add = []
      if(this.switch_show_perc){
        let array_added_headers = ['perc_with_absolute_number'];
        max = this.singleInfo['weekNum'];
        analysis_date = this.singleInfo['date'];
        for(let j=0; j<max; j=j+1){
          let this_date = new Date(analysis_date);
          for(let i = 0; i < array_added_headers.length; i++){
            let value = array_added_headers[i] + '_' + analysis_date;
            let text = array_added_headers[i] + '_' + analysis_date + '\n';
            text = text.replaceAll('_', ' ');
            text = text.charAt(0).toUpperCase() + text.slice(1);
            if(array_added_headers[i] === 'perc_with_absolute_number'){
              text = 'Presence (%) ' + analysis_date + '\n';
            }
            let single_header = {text: text, value: value, sortable: true, show: true, align: 'center', width: '15vh'};
            array_to_add.unshift(single_header);
          }
          let days = 7 ;
          let previous_date = new Date(this_date.getTime() - (days * 24 * 60 * 60 * 1000));
          analysis_date = previous_date.toISOString().split('T')[0]
        }
        predefined_headers = predefined_headers.concat(array_to_add);
      }

      this.headerTable = predefined_headers;
      this.headerTableSubPlaces = predefined_headers;

      this.filteredResults.forEach(elem => {
        if(this.withLineages) {
          let lineage = elem['lineage'];
          if (!this.possibleLineage.includes(lineage)){
            this.possibleLineage.push(lineage);
          }
          this.possibleLineage.sort();
        }
        let protein = elem['muts'][0]['pro'];

        if (!this.possibleProtein.includes(protein)){
          this.possibleProtein.push(protein);
        }
        this.possibleProtein.sort();

        // eslint-disable-next-line no-prototype-builtins
        if(elem.hasOwnProperty(elem['granularity'])){
          let location = elem[elem['granularity']];
          if (!this.possibleLocationFirstTable.includes(location)) {
            if(location !== null) {
              this.possibleLocationFirstTable.push(location);
            }
            // else{
            //   this.possibleLocationFirstTable.push('N/D');
            // }
          }
        }
        // else{
        //   this.possibleLocationFirstTable.push('World');
        // }
        this.possibleLocationFirstTable.sort();

      });

    },
    doFilterOnResults(){
      let that = this;
      let partially_filtered = JSON.parse(JSON.stringify(this.rowsTable)).filter(function (el) {
        return (
            (that.selectedLineage === null || el['lineage'] ===  that.selectedLineage)
            &&
            (that.selectedProtein === null || el['muts'][0]['pro'] ===  that.selectedProtein)
            &&
            (that.selectedLocationFirstTable === null || el[that.rowsTable[0]['granularity']] ===  that.selectedLocationFirstTable)
        )
      });
      if(this.switch_alert){
        let copyResults = JSON.parse(JSON.stringify(partially_filtered));
        let copyResults2 = this.customSort(copyResults, ['polyfit_slope'], [true]);
        this.filteredResults = JSON.parse(JSON.stringify(copyResults2.slice(0, this.maxNumberOfImportantMuts)));
      }
      else{
        this.filteredResults = JSON.parse(JSON.stringify(partially_filtered));
      }
      if(this.switch_alert){
        this.showCharts = true;
      }
      else{
        if(this.filteredResults.length <= 50){
          this.showCharts = true;
        }
        else{
          this.showCharts = false;
        }
      }
    },
  },
  mounted() {
    this.doFilterOnResults();
    if(this.filteredResults.length > 0) {
      this.loadTables();
    }
  },
  watch: {
    switch_show_perc(){
      if(this.filteredResults.length > 0) {
        this.loadTables();
      }
    },
    switch_alert(){
      this.doFilterOnResults();
    },
    selectedLineage(){
      this.doFilterOnResults();
    },
    selectedProtein(){
      this.doFilterOnResults();
    },
    selectedLocation(){
      this.doFilterOnResults();
    },
    selectedLocationFirstTable(){
      this.doFilterOnResults();
    },
    maxNumberOfImportantMuts(){
      this.doFilterOnResults();
    },
    filteredResults(){
      if(this.filteredResults.length > 0) {
        this.loadTables();
      }
    }
  },
}
</script>

<style scoped>

.provaprova {
  color:red
}

</style>