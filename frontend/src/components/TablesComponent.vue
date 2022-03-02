<!--
  Component:    TablesComponent
  Description:  Container of the raw data table, heatmap and a barchart

  Props:
  ├──
  └──
-->

<template>
  <v-layout justify-center row class="panel-container" wrap>

    <!-- Filtering options -->
    <v-flex class=" xs12 d-flex filter-container" justify-center>
      <v-container>
        <v-layout justify-center row wrap>

          <v-flex justify-center class="xs12 sm6 d-flex filter-heading">
            <h3>
              <v-icon color="white" left>mdi-filter-outline</v-icon>
              FILTERING OPTIONS
            </h3>
          </v-flex>

          <!-- Protein filter -->
          <v-flex justify-center class="xs12 sm6 d-flex ">
            <v-layout row wrap>
              <v-flex class="xs12 d-flex field-label">
                <span>Protein</span>
              </v-flex>

              <v-flex class="xs12 d-flex field-element">
                <v-autocomplete v-model="selectedProtein"
                                :items="possibleProteins"
                                clearable
                                hide-details
                                label="All"
                                solo
                />
              </v-flex>
            </v-layout>
          </v-flex>

        </v-layout>
      </v-container>
    </v-flex>

    <!-- MUTATIONS TABLE SECTION -->
    <!---- Heading ---->
    <v-flex class="xs12 d-flex" justify-center>
      <h2 class="result-heading">
        <v-icon left color="white">mdi-table-multiple</v-icon>
        MUTATIONS TABLE
        <hr/>
      </h2>
    </v-flex>

    <!---- Table ---->
    <v-flex justify-center class="xs12 d-flex">
      <v-data-table :id="nameHeatmap + 'table'"
                    v-model="selectedRows"
                    :custom-sort="customSort"
                    :headers="headerTable"
                    :items="filteredResults"
                    :sort-by.sync="sortByTable"
                    :sort-desc.sync="sortDescTable"
                    :footer-props="footerProps"
                    class="table-element"
                    item-key="mut"
                    multi-sort
                    show-select
      >

        <!---- Table controls ---->
        <template v-slot:top>
          <v-container class="table-controls">
            <v-layout justify-center row wrap >

              <!---- Show/hide p-values info button ---->
              <v-flex justify-center class="xs12 sm6 md4 d-flex">
                <v-btn v-if="!showP_values" outlined depressed rounded small color="primary" @click="showP_values=true">
                  <v-icon left>mdi-plus-circle-outline</v-icon>
                  Show p-values
                </v-btn>
                <v-btn v-else depressed rounded small color="primary" @click="showP_values=false">
                  <v-icon left>mdi-minus-circle-outline</v-icon>
                  Hide p-values
                </v-btn>
              </v-flex>

              <!---- Show/hide columns descriptions button ---->
              <v-flex justify-center class="xs12 sm6 md4 d-flex">
                <v-btn outlined depressed rounded small color="primary" @click="dialogTableHeaders = true">
                  <v-icon left>mdi-help-circle-outline</v-icon>
                  Columns description
                </v-btn>
              </v-flex>

              <!---- Download data button ---->
              <v-flex justify-center class="xs12 sm6 md4 d-flex">
                <v-btn outlined depressed rounded small color="primary" @click="downloadTable()">
                  <v-icon left>mdi-download-circle-outline</v-icon>
                  Download data
                </v-btn>
              </v-flex>
            </v-layout>

          </v-container>
        </template>

      </v-data-table>
    </v-flex>

    <v-dialog
        v-model="dialogTableHeaders"
        persistent
        width="1300"
    >
      <v-card>
        <v-card-title class="white--text" v-bind:style="{ backgroundColor: 'grey' }">
          INFO TABLE'S HEADERS
          <v-spacer></v-spacer>
          <v-btn
              slot="activator"
              color="white"
              icon
              small
              style="background-color: red"
              @click="dialogTableHeaders = false"
          >
            X
          </v-btn>
        </v-card-title>

        <v-card-text class="text-xs-center" style="padding: 20px">
          <li><b>P value with mut: </b> shows if the population «with mutation» is growing differently compared to
            everything.
          </li>
          <br>
          <li><b>P value without mut: </b> shows if the population «without mutation» is growing differently compared to
            everything.
          </li>
          <br>
          <li><b>P value comparative: </b> shows if the population «with mutation» is growing differently compared to
            the population «without mutation».
          </li>
          <br>
          <li><b>Slope: </b> is calculated through a linear interpolation of the diffusion (percentage). (y=<b>m</b>x +
            q)
          </li>
          <br>
          <li><b>Y-intercept: </b> is calculated through a linear interpolation of the diffusion (percentage). (y=mx +
            <b>q</b>)
          </li>
          <br>
        </v-card-text>

      </v-card>
    </v-dialog>


    <v-flex class="xs12 d-flex" justify-center>
      <h2 class="result-heading">
        <v-icon left color="white">mdi-chart-gantt</v-icon>
        HEATMAP (Diffusion)
        <hr/>
      </h2>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
      <HeatMap :plotlyId="tableIndex"
               :referenceDate="singleInfo.date"
               :tableForHeatMap="tableForLinePlot"
               :title="plotsTitles"
               style="justify-content: center;"
      />
    </v-flex>


    <v-flex class="xs12 d-flex" justify-center>
      <h2 class="result-heading">
        <v-icon left color="white">mdi-chart-line</v-icon>
        DIFFUSION TREND CHART
        <hr/>
      </h2>
    </v-flex>

    <v-flex class="no-horizontal-padding xs12 d-flex" style="justify-content: center;">
      <BarChart :plotlyId="tableIndex"
                :referenceDate="singleInfo.date"
                :tableForLinePlot="tableForLinePlot"
                :title="plotsTitles"
                style="justify-content: center;"
      />
    </v-flex>

  </v-layout>
</template>

<script>
import BarChart from "./BarChart";
import HeatMap from "./HeatMap";
import {mapState} from "vuex";

export default {
  name: "TablesComponent",
  components: {HeatMap, BarChart},
  props: {
    /** Array of objects, each of which represents a row as follows:
     *  [{location, protein, [lineage,] mut, polyfit_slope, polifit_intercept,
     *  w4,w3,w2,w1,f1,f2,f3,f4,p_value_with_mut_total,p_value_without_mut_total,
     *  p_value_comparative_mut_total}]
     */
    rowsTable: {required: true,},

    /** Object containing all the query parameters {granularity, location, date, [lineage]} */
    singleInfo: {required: true},

    /** Heatmap name used as id. Required. */
    nameHeatmap: {required: true}, //TODO: remove, it's useless.

    /** Heatmap name used as id. Required. */
    timeName: {required: true}, //TODO: remove, it's useless

    /** Lineages flag. True if the data refers to a lineage specific analysis. Required.*/
    withLineages: {required: true},

    /** Analysis index. */
    tableIndex: {required: true}, //TODO: change usage
  },
  data() {
    return {
      /** Title for the plots */
      plotsTitles: 'Top 5 decreasing + Top 5 increasing mutations',

      /** Flag to show the p_values in the table */
      showP_values: false,

      /** Flag to show table header descriptions */
      dialogTableHeaders: false,

      /** Array of data to display in the table */
      filteredResults: [],

      /** Array of data to be plotted */
      tableForLinePlot: [],

      /** Array of selected rows */
      selectedRows: [],

      /** Array of objects describing header columns */
      headerTable: [],

      /** Array of columns selected for sorting data */
      sortByTable: [],

      /** Array defining asc(true)/desc(false) order for each column selected for sorting in sortByTable */
      sortDescTable: [],

      /** Footer options for the data table */
      footerProps: {'items-per-page-options': [5, 10, 20, 50, 100, -1]},

      /** Selected protein to further filter the data */
      selectedProtein: null,

      /** Possible proteins values */
      possibleProteins: []
    }
  },
  computed: {
    ...mapState(['primary_color', 'secondary_color']),
  },
  methods: {
    downloadTable() {
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
      if (index !== null && index !== undefined) {
        let i = 0;
        let len = index.length - 1;
        let idx = index[i];
        let desc = isDesc[i];
        if (idx !== null && idx !== undefined) {
          items.sort((a, b) => {
            if (!idx.includes('p_value') && !idx.includes('polyfit')) {
              if (idx === 'mut') {
                if (desc) {
                  let pos_a = a['muts'][0]['loc'];
                  let pos_b = b['muts'][0]['loc'];
                  if (pos_a !== pos_b || i >= len) {
                    return pos_b < pos_a ? -1 : 1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                } else {
                  let pos_a = a['muts'][0]['loc'];
                  let pos_b = b['muts'][0]['loc'];
                  if (pos_a !== pos_b || i >= len) {
                    return pos_b > pos_a ? -1 : 1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                }
              } else if (idx.includes('perc')) {
                let date = idx.replace('perc_with_absolute_number', '');
                let realKey = 'perc_with_mut_this_week' + date;
                if (desc) {
                  if (a[idx] === null || a[idx] === undefined) {
                    if (b[idx] !== a[idx] || i >= len) {
                      return 1;
                    } else {
                      return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                    }
                  }
                  if (b[idx] === null || b[idx] === undefined) {
                    if (b[idx] !== a[idx] || i >= len) {
                      return -1;
                    } else {
                      return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                    }
                  }
                  if (b[realKey] !== a[realKey] || i >= len) {
                    return Number(b[realKey]) < Number(a[realKey]) ? -1 : 1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                } else {
                  if (a[idx] === null || a[idx] === undefined) {
                    if (b[idx] !== a[idx] || i >= len) {
                      return 1;
                    } else {
                      return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                    }
                  }
                  if (b[idx] === null || b[idx] === undefined) {
                    if (b[idx] !== a[idx] || i >= len) {
                      return -1;
                    } else {
                      return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                    }
                  }
                  if (b[realKey] !== a[realKey] || i >= len) {
                    return Number(b[realKey]) > Number(a[realKey]) ? -1 : 1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                }
              } else {
                if (desc) {
                  if (b[idx] !== a[idx] || i >= len) {
                    return b[idx] < a[idx] ? -1 : 1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                } else {
                  if (b[idx] !== a[idx] || i >= len) {
                    return b[idx] > a[idx] ? -1 : 1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                }
              }
            } else {
              if (desc) {
                if (a[idx] === null || a[idx] === undefined) {
                  if (b[idx] !== a[idx] || i >= len) {
                    return 1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                }
                if (b[idx] === null || b[idx] === undefined) {
                  if (b[idx] !== a[idx] || i >= len) {
                    return -1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                }
                if (b[idx] !== a[idx] || i >= len) {
                  return Number(b[idx]) < Number(a[idx]) ? -1 : 1;
                } else {
                  return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                }
              } else {
                if (a[idx] === null || a[idx] === undefined) {
                  if (b[idx] !== a[idx] || i >= len) {
                    return 1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                }
                if (b[idx] === null || b[idx] === undefined) {
                  if (b[idx] !== a[idx] || i >= len) {
                    return -1;
                  } else {
                    return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
                  }
                }
                if (b[idx] !== a[idx] || i >= len) {
                  return Number(b[idx]) > Number(a[idx]) ? -1 : 1;
                } else {
                  return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
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
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          } else {
            let pos_a = a['muts'][0]['loc'];
            let pos_b = b['muts'][0]['loc'];
            if (pos_a !== pos_b || i >= len) {
              return pos_b > pos_a ? -1 : 1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          }
        } else if (idx.includes('perc')) {
          let date = idx.replace('perc_with_absolute_number', '');
          let realKey = 'perc_with_mut_this_week' + date;
          if (desc) {
            if (a[idx] === null || a[idx] === undefined) {
              if (b[idx] !== a[idx] || i >= len) {
                return 1;
              } else {
                return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
              }
            }
            if (b[idx] === null || b[idx] === undefined) {
              if (b[idx] !== a[idx] || i >= len) {
                return -1;
              } else {
                return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
              }
            }
            if (b[realKey] !== a[realKey] || i >= len) {
              return Number(b[realKey]) < Number(a[realKey]) ? -1 : 1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          } else {
            if (a[idx] === null || a[idx] === undefined) {
              if (b[idx] !== a[idx] || i >= len) {
                return 1;
              } else {
                return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
              }
            }
            if (b[idx] === null || b[idx] === undefined) {
              if (b[idx] !== a[idx] || i >= len) {
                return -1;
              } else {
                return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
              }
            }
            if (b[realKey] !== a[realKey] || i >= len) {
              return Number(b[realKey]) > Number(a[realKey]) ? -1 : 1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          }
        } else {
          if (desc) {
            if (b[idx] !== a[idx] || i >= len) {
              return b[idx] < a[idx] ? -1 : 1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          } else {
            if (b[idx] !== a[idx] || i >= len) {
              return b[idx] > a[idx] ? -1 : 1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          }
        }
      } else {
        if (desc) {
          if (a[idx] === null || a[idx] === undefined) {
            if (b[idx] !== a[idx] || i >= len) {
              return 1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          }
          if (b[idx] === null || b[idx] === undefined) {
            if (b[idx] !== a[idx] || i >= len) {
              return -1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          }
          if (b[idx] !== a[idx] || i >= len) {
            return Number(b[idx]) < Number(a[idx]) ? -1 : 1;
          } else {
            return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
          }
        } else {
          if (a[idx] === null || a[idx] === undefined) {
            if (b[idx] !== a[idx] || i >= len) {
              return 1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          }
          if (b[idx] === null || b[idx] === undefined) {
            if (b[idx] !== a[idx] || i >= len) {
              return -1;
            } else {
              return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
            }
          }
          if (b[idx] !== a[idx] || i >= len) {
            return Number(b[idx]) > Number(a[idx]) ? -1 : 1;
          } else {
            return this.singleCustomSort(a, b, i + 1, len, index, isDesc);
          }
        }
      }

    },
    loadTables() {
      console.log("loadTables");
      let predefined_headers = [];
      if (this.withLineages) {
        predefined_headers = [
          {text: 'Location', value: 'location', sortable: true, show: true, align: 'center'},
          {text: 'Lineage', value: 'lineage', sortable: true, show: true, align: 'center'},
          {text: 'Protein', value: 'protein', sortable: true, show: true, align: 'center'},
          {text: 'Mut', value: 'mut', sortable: true, show: true, align: 'center'},
          {text: 'Slope', value: 'polyfit_slope', sortable: true, show: true, align: 'center'},
          {text: this.computeDateLabel(28, 22), value: 'w1', sortable: true, show: true, align: 'center'}, //'28-22 days before'
          {text: this.computeDateLabel(21, 15), value: 'w2', sortable: true, show: true, align: 'center'}, // '21-15 days before'
          {text: this.computeDateLabel(14, 8), value: 'w3', sortable: true, show: true, align: 'center'}, // '14-8 days before'
          {text: this.computeDateLabel(7, 0), value: 'w4', sortable: true, show: true, align: 'center'} // '7-0 days before'
        ]
      } else {

        predefined_headers = [
          {text: 'Location', value: 'location', sortable: true, show: true, align: 'center'},
          {text: 'Protein', value: 'protein', sortable: true, show: true, align: 'center'},
          {text: 'Mut', value: 'mut', sortable: true, show: true, align: 'center'},
          {text: 'Slope', value: 'polyfit_slope', sortable: true, show: true, align: 'center'},
          {text: this.computeDateLabel(28, 22), value: 'w1', sortable: true, show: true, align: 'center'}, //'28-22 days before'
          {text: this.computeDateLabel(21, 15), value: 'w2', sortable: true, show: true, align: 'center'}, // '21-15 days before'
          {text: this.computeDateLabel(14, 8), value: 'w3', sortable: true, show: true, align: 'center'}, // '14-8 days before'
          {text: this.computeDateLabel(7, 0), value: 'w4', sortable: true, show: true, align: 'center'} // '7-0 days before'
        ]
      }

      // let array_possible_header = ['diff_perc', 'perc_this_week', 'perc_prev_week', 'count_this_week',
      //   'count_prev_week']
      let array_possible_header = [];

      if (!this.withLineages) {
        // array_possible_header.unshift('perc_with_mut_this_week');
        array_possible_header.unshift('perc_with_absolute_number');
      }

      if (this.showP_values) {
        let total_p_value_headers = [
          {
            text: 'P-value with mut',
            value: 'p_value_with_mut_total',
            sortable: true,
            show: true,
            align: 'center',


          },
          {
            text: 'P-value without mut',
            value: 'p_value_without_mut_total',
            sortable: true,
            show: true,
            align: 'center'
          },
          {
            text: 'P-value comparative',
            value: 'p_value_comparative_mut_total',
            sortable: true,
            show: true,
            align: 'center'
          },
        ]
        predefined_headers = predefined_headers.concat(total_p_value_headers);
      }
      this.headerTable = predefined_headers;
      // let i = 0;
      this.filteredResults.forEach(elem => {
        // PROBABLY USELESS CODE
        // if (this.withLineages) {
        //   let lineage = elem['lineage'];
        //   if (!this.possibleLineage.includes(lineage)) {
        //     this.possibleLineage.push(lineage);
        //   }
        //   this.possibleLineage.sort();
        // }
        // END PROBABLY USELESS CODE

        let protein = elem.protein;
        if (!this.possibleProteins.includes(protein)) {
          this.possibleProteins.push(protein);
        }
        this.possibleProteins.sort();

        // PROBABLY USELESS CODE
        // eslint-disable-next-line no-prototype-builtins
        // if (elem.hasOwnProperty(elem['granularity'])) {
        //   let location = elem[elem['granularity']];
        //   if (!this.possibleLocationFirstTable.includes(location)) {
        //     if (location !== null) {
        //       this.possibleLocationFirstTable.push(location);
        //     }
        //   }
        //
        // }
        // this.possibleLocationFirstTable.sort();
        // END PROBABLY USELESS CODE

      });

    },
    doFilterOnResults() {
      this.filteredResults = this.rowsTable
      if (this.selectedProtein != null) {
        this.filteredResults = this.filteredResults.filter((item) => item.protein == this.selectedProtein)
      }
    },
    doTableForLinePlot() {
      // console.log("doTableForLinePlot");
      // array.sort() sorts the array inline, so it starts the watch function of filteredResults
      // [...this.filteredResults]=> makes a shallow copy of the array

      let selected;
      if (this.selectedRows.length > 0) {
        this.plotsTitles = `Selected mutations (${this.selectedRows.length})`;
        selected = [...this.selectedRows];
      } else {
        this.plotsTitles = 'Top 5 decreasing + Top 5 increasing mutations';
        let sorted = [...this.filteredResults].sort(function (b, a) {
          return a.polyfit_slope - b.polyfit_slope
        });
        // get first 5 and last 5
        selected = sorted.slice(0, 5).concat(sorted.slice(-5));
      }
      selected = [...new Set(selected)];
      //sort again
      selected = selected.sort(function (b, a) {
        return a.polyfit_slope - b.polyfit_slope
      });
      this.tableForLinePlot = selected
      console.log(this.tableForLinePlot)
    },
    computeDateLabel(from, to) {
      const referenceDate = new Date(this.singleInfo.date);
      const fromDate = new Date(referenceDate);
      const toDate = new Date(referenceDate);

      fromDate.setDate(referenceDate.getDate() - from);
      toDate.setDate(referenceDate.getDate() - to);
      return fromDate.toISOString().slice(0, 10).replaceAll('-', '/') + " - " + toDate.toISOString().slice(0, 10).replaceAll('-', '/');
    },
  },
  mounted() {
    this.doFilterOnResults();
    this.loadTables();
    this.doTableForLinePlot();
  },
  watch: {
    selectedRows(newVal, oldVal) {
      this.doTableForLinePlot();
    },
    selectedProtein() {
      this.doFilterOnResults();
      this.selectedRows = []
    },
    filteredResults(newVal, oldVal) {
      // if nothing has been changed, then not run the code below.
      if (JSON.stringify(newVal) !== JSON.stringify(oldVal)) {
        console.log("filteredResults");
        if (this.filteredResults.length > 0) {
          this.loadTables();
          this.doTableForLinePlot();
        }
      }
    },
    showP_values() {
      if (this.filteredResults.length > 0) {
        this.loadTables();
      }
    }
  },
}
</script>

<style scoped>

/* Panel container styling */
.panel-container {
  padding-top: 30px;
  margin: 0;
}

/* Filter container styling */
.filter-container {
  border: #014878 solid 1px;
  border-radius: 4px;
  justify-content: center;
  margin: 0 12px;
  padding: 30px;
}

/* Filter heading styling */
.filter-heading {
  text-align: center;
  margin: auto;
  color: white;
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

/* Heading of table and graphs */
.result-heading {
  color: white;
  font-weight: 800;
  margin-top: 30px;
}

/* Table options */
.table-controls{
  padding-top: 25px;
  padding-bottom: 18px;
}

.table-controlsXX{
  background: rgba(53, 177, 236, 0.21) !important;
}
.table-controls .d-flex{
  padding-bottom:7px !important;
  padding-top: 0 !important;
}



.table-element {
  width: 100%;
}

</style>
<style>
/* Additional global rules to overwrite the vuetify styling fot table*/
.v-data-table-header th{
  border-top: #1976D2FF solid 1px !important;
  border-bottom: #1976D2FF solid 1px !important;
  padding-top:8px !important;
  padding-bottom: 8px !important;
}
.v-data-table,.v-data-table-header{
  background: #D2ECF8FF !important;
}
table{
  background: white !important;
}
</style>