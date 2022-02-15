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

       </v-layout>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 md4 lg4 d-flex" style="justify-content: center;">
      <v-switch
        v-model="switch_show_p_values"
      >
        <template v-slot:label>
          <span style="color: white">Show P-values</span>
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
                show-select
                :headers="headerTable"
                v-model="selectedRows"
                item-key="mut"
                :items="filteredResults"
                :id = "nameHeatmap + 'table'"
                class="data-table table_prov_reg mytable"
                style="width: 98%; border: grey solid 1px"
                multi-sort
                :sort-by.sync="sortByTable"
                :sort-desc.sync="sortDescTable"
                :custom-sort="customSort"
          >
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
            <li><b>P value with mut: </b>  shows if the population «with mutation» is growing differently compared to everything. </li><br>
            <li><b>P value without mut: </b>  shows if the population «without mutation» is growing differently compared to everything. </li><br>
            <li><b>P value comparative: </b>  shows if the population «with mutation» is growing differently compared to the population «without mutation». </li><br>
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
    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
      <NewHeatMap style="justify-content: center;"
                  :tableForHeatMap="tableForLinePlot"
                  :plotlyId="tableIndex"
      ></NewHeatMap>
    </v-flex>


    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center">
        <h2 style="color: white; margin-top: 80px;">
          DIFFUSION TREND CHART
        </h2>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
      <NewBarChart style="justify-content: center;"
                   :tableForLinePlot="tableForLinePlot"
                   :plotlyId="tableIndex"
      ></NewBarChart>
    </v-flex>

  </v-layout>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
// import DialogAnalyseSelectedMuts from "@/components/DialogAnalyseSelectedMuts";
import NewBarChart from "./NewBarChart";
import NewHeatMap from "./NewHeatMap";

export default {
  name: "TablesComponentWithoutLineages",
  components: {NewHeatMap, /*DialogAnalyseSelectedMuts,*/ NewBarChart},
  props: {
    rowsTable: {required: true,},
    singleInfo: {required: true},
    nameHeatmap: {required: true},
    timeName: {required: true},
    withLineages: {required: true},
    tableIndex: {required: true},
  },
  data() {
    return {
      switch_alert: false,
      switch_show_p_values: false,
      filteredResults: [],
      showCharts: true,
      maxNumberSelectedMuts: 20,

      tableForLinePlot : [],
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
      let filename = "LinIndep_" + this.singleInfo['location'] + '_' + this.singleInfo['date'] + '_' + this.singleInfo['weekNum'] + 'week.csv'
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
      console.log("loadTables");
      let predefined_headers = [];
      if(this.withLineages) {
        predefined_headers = [
          // {text: 'Info', value: 'info', sortable: false, show: true, align: 'center', width: '3vh'},
          {text: 'Location', value: 'location', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Lineage', value: 'lineage', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Protein', value: 'protein', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Mut', value: 'mut', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Slope', value: 'polyfit_slope', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: '28-22 days before', value: 'w1', sortable: true, show: true, align: 'center', width: '13vh' },
          {text: '21-15 days before', value: 'w2', sortable: true, show: true, align: 'center', width: '13vh' },
          {text: '14-8 days before', value: 'w3', sortable: true, show: true, align: 'center', width: '13vh' },
          {text: '7-0 days before', value: 'w4', sortable: true, show: true, align: 'center', width: '13vh' }
        ]
      }
      else{

        predefined_headers = [
          // {text: 'Info', value: 'info', sortable: false, show: true, align: 'center', width: '3vh'},
          {text: 'Location', value: 'location', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Protein', value: 'protein', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Mut', value: 'mut', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'Slope', value: 'polyfit_slope', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: '28-22 days before', value: 'w1', sortable: true, show: true, align: 'center', width: '13vh' },
          {text: '21-15 days before', value: 'w2', sortable: true, show: true, align: 'center', width: '13vh' },
          {text: '14-8 days before', value: 'w3', sortable: true, show: true, align: 'center', width: '13vh' },
          {text: '7-0 days before', value: 'w4', sortable: true, show: true, align: 'center', width: '13vh' }
        ]
      }

      // let array_possible_header = ['diff_perc', 'perc_this_week', 'perc_prev_week', 'count_this_week',
      //   'count_prev_week']
      let array_possible_header = [];

      if(!this.withLineages){
        // array_possible_header.unshift('perc_with_mut_this_week');
        array_possible_header.unshift('perc_with_absolute_number');
      }

      if(this.switch_show_p_values){
        let total_p_value_headers = [
          {text: 'P-value with mut', value: 'p_value_with_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'P-value without mut', value: 'p_value_without_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},
          {text: 'P-value comparative', value: 'p_value_comparative_mut_total', sortable: true, show: true, align: 'center', width: '13vh'},
        ]
        predefined_headers = predefined_headers.concat(total_p_value_headers);
      }
      this.headerTable = predefined_headers;
      this.headerTableSubPlaces = predefined_headers;
      // let i = 0;
      this.filteredResults.forEach(elem => {
        if(this.withLineages) {
          let lineage = elem['lineage'];
          if (!this.possibleLineage.includes(lineage)){
            this.possibleLineage.push(lineage);
          }
          this.possibleLineage.sort();
        }
        let protein = elem.protein;

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
          }

        }
        this.possibleLocationFirstTable.sort();

      });

    },
    doFilterOnResults(){
      this.filteredResults = this.rowsTable
      if ( this.selectedProtein != null ) {
        this.filteredResults = this.filteredResults.filter((item) => item.protein == this.selectedProtein)
      }
    },
    doTableForLinePlot() {
      // console.log("doTableForLinePlot");
      // array.sort() sorts the array inline, so it starts the watch function of filteredResults
      // [...this.filteredResults]=> makes a shallow copy of the array
      let temp_table;
      if (this.selectedRows.length > 0) {
        temp_table = [...this.selectedRows];
      }
      else{
        temp_table = [...this.filteredResults];
      }
      let sorted = temp_table.sort(function (b, a) {
        return a.polyfit_slope - b.polyfit_slope
      })
      // get first 5 and last 5
      let selected = sorted.slice(0, 5).concat(sorted.slice(-5))
      //remove duplicates
      selected = [...new Set(selected)]
      //sort again
      selected = selected.sort(function (b, a) {
        return a.polyfit_slope - b.polyfit_slope
      })
      this.tableForLinePlot = selected
    },
  },
  mounted() {
    this.doFilterOnResults();
    this.loadTables();
    this.doTableForLinePlot();
  },
  watch: {
    selectedRows (newVal, oldVal) {
      this.doTableForLinePlot();
    },
    switch_alert(){
      this.doFilterOnResults();
    },
    selectedLineage(){
      this.doFilterOnResults();
    },
    selectedProtein(){
      this.doFilterOnResults();
      this.selectedRows = []
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
    filteredResults(newVal, oldVal){
      // if nothing has been changed, then not run the code below.
      if(JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
        console.log("filteredResults");
        if (this.filteredResults.length > 0) {
          this.loadTables();
          this.doTableForLinePlot();
        }
      }
    },
    switch_show_p_values(){
      if(this.filteredResults.length > 0) {
        this.loadTables();
      }
    }
  },
}
</script>

<style scoped>


</style>