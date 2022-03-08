<!--
  Component:    AnalysisResult
  Description:  Container of the raw data table, heatmap and a barchart

  Props:
  ├── queryResult:  Array of objects, each of which represents a row
  ├── queryParams:  Object containing all the query parameters {granularity, location, date, [lineage]}
  └── withLineages: Lineages flag. True if the data refers to a lineage specific analysis. Required.

-->

<template>
  <v-layout :ref="fileName" justify-center row class="panel-container" wrap>

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
    <v-flex justify-center class="xs12 d-flex table-container">
      <v-data-table v-model="selectedRows"
                    :custom-sort="customSort"
                    :headers="tableHeaders"
                    :items="processedQueryResult"
                    :sort-by.sync="sortingIndexes"
                    :sort-desc.sync="isDescSorting"
                    :footer-props="footerProps"
                    class="table-element"
                    item-key="mut"

                    multi-sort
                    show-select
                    mobile-breakpoint="0"
      >

        <!---- Table controls ---->
        <template v-slot:top>
          <v-container class="table-controls">
            <v-layout justify-center row wrap>

              <!---- Show/hide p-values info button ---->
              <v-flex justify-center class="xs12 sm6 md3 d-flex">
                <v-btn v-if="!showPValues" outlined depressed rounded small color="primary" @click="showPValues=true">
                  <v-icon left>mdi-plus-circle-outline</v-icon>
                  Show p-values
                </v-btn>
                <v-btn v-else depressed rounded small color="primary" @click="showPValues=false">
                  <v-icon left>mdi-minus-circle-outline</v-icon>
                  Hide p-values
                </v-btn>
              </v-flex>

              <!---- Show/hide columns descriptions button ---->
              <DialogOpener :button-prefix="false" title="Columns description">
                <ul>
                  <li>
                    <b>P value with mut: </b>
                    shows if the population «with mutation» is growing differently compared to everything.
                  </li>
                  <li>
                    <b>P value without mut: </b>
                    shows if the population «without mutation» is growing differently compared to everything.
                  </li>
                  <li>
                    <b>P value comparative: </b>
                    shows if the population «with mutation» is growing differently compared to the population «without
                    mutation».
                  </li>
                  <li>
                    <b>Slope: </b>
                    is calculated through a linear interpolation of the diffusion (percentage). (y=<b>m</b>x + q)
                  </li>
                </ul>
              </DialogOpener>

              <!---- Download data button ---->
              <v-flex justify-center class="xs12 sm6 md3 d-flex">
                <v-btn :loading="downloadLoading" outlined depressed rounded small color="primary"
                       @click="downloadData()">
                  <v-icon left>mdi-download-circle-outline</v-icon>
                  Download data
                </v-btn>
              </v-flex>

              <!---- Print result button ---->
              <v-flex justify-center class="xs12 sm6 md3 d-flex">
                <v-btn :loading="downloadLoading" outlined depressed rounded small color="primary"
                       @click="downloadAll()">
                  <v-icon left>mdi-printer</v-icon>
                  Download all
                </v-btn>
              </v-flex>
            </v-layout>

          </v-container>
        </template>

        <!---- Table top headers ---->
        <template v-slot:header>
          <thead class="main-headers">
          <tr>
            <th colspan="2" class="empty-main-header"/>
            <th colspan="1" class="empty-main-header"/>
            <th colspan="1" class="empty-main-header"/>
            <th colspan="1" class="empty-main-header"/>
            <th colspan="4">Mutation diffusion in % &nbsp;&nbsp; (num of affected sequences)</th>
            <th v-if="showPValues" colspan="3">P-values</th>
          </tr>
          </thead>
        </template>

      </v-data-table>
    </v-flex>

    <!-- HEATMAP SECTION -->
    <!---- Heading ---->
    <v-flex class="xs12 d-flex" justify-center>
      <h2 class="result-heading">
        <v-icon left color="white">mdi-chart-gantt</v-icon>
        DIFFUSION HEATMAP
        <hr/>
      </h2>
    </v-flex>

    <!---- Heatmap ---->
    <v-flex class="xs12 d-flex" justify-center>
      <HeatMap
          :dateLabel="computeDateLabels()"
          :plotData="plotsInfo.data"
          :plotTitle="plotsInfo.title"
      />
    </v-flex>

    <!-- CHART SECTION -->
    <!---- Heading ---->
    <v-flex class="xs12 d-flex" justify-center>
      <h2 class="result-heading">
        <v-icon left color="white">mdi-chart-line</v-icon>
        DIFFUSION TREND CHART
        <hr/>
      </h2>
    </v-flex>

    <!---- Chart ---->
    <v-flex class="xs12 d-flex" justify-center>
      <BarChart :dateLabel="computeDateLabels()"
                :plotData="plotsInfo.data"
                :plotTitle="plotsInfo.title"
                :weekSeq="plotsInfo.weekSeq"
      />
    </v-flex>

  </v-layout>
</template>

<script>
import BarChart from "./plots/LineChart";
import HeatMap from "./plots/HeatMap";
import {mapState} from "vuex";
import html2canvas from "html2canvas";
import DialogOpener from "@/components/general/DialogOpener";

export default {
  name: "AnalysisResult",
  components: {DialogOpener, HeatMap, BarChart},
  props: {
    /** Array of raw data, of the form:
     *  [{location, protein, [lineage,] mut, polyfit_slope,w4,w3,w2,w1,f1,f2,f3,f4,
     *  p_value_with_mut, p_value_without_mut, p_value_comparative_mut}]
     */
    queryResult: {required: true,},

    /** Object containing all the query parameters {granularity, location, date, [lineage]} */
    queryParams: {required: true},

    /** Total number of sequences collected per week */
    weekSeq: {required: true},

    /** Lineages flag. True if the data refers to a lineage specific analysis. Required.*/
    withLineages: {required: true}
  },
  data() {
    return {

      /** Flag to show the p_values in the table */
      showPValues: false,

      /** Array of selected rows */
      selectedRows: [],

      /** Array of columns selected for sorting data */
      sortingIndexes: [],

      /** Array defining asc(true)/desc(false) order for each column selected for sorting in sortingIndexes */
      isDescSorting: [],

      /** Default sorting options */
      defaultSorting: {indexes: ['polyfit_slope'], isDescSorting: [true]},

      /** Footer options for the data table */
      footerProps: {'items-per-page-options': [-1, 5, 10, 20, 50, 100, 150, 200, 500]},

      /** Selected protein to further filter the data */
      selectedProtein: null,

      /* Download flag: true if a file download is in progress */
      downloadLoading: false
    }
  },
  computed: {
    ...mapState(['primary_color', 'secondary_color']),

    /** Array of objects describing header columns */
    tableHeaders() {
      let headers =
          [
            {text: 'Location', value: 'location', divider: true, align: 'center'},
            {text: 'Protein', value: 'protein', divider: true, align: 'center'},
            {text: 'Mut', value: 'mut', divider: true, align: 'center'},
            {text: 'Slope', value: 'polyfit_slope', divider: true, align: 'center'},
            {text: this.computeDateLabel(28, 22), value: 'f_w1', divider: true, align: 'center'}, //'28-22 days before'
            {text: this.computeDateLabel(21, 15), value: 'f_w2', divider: true, align: 'center'}, //'21-15 days before'
            {text: this.computeDateLabel(14, 8), value: 'f_w3', divider: true, align: 'center'},  //'14-8  days before'
            {text: this.computeDateLabel(7, 0), value: 'f_w4', divider: true, align: 'center'}    //'7-0   days before'
          ]

      if (this.showPValues) {
        const extendedHeaders =
            [
              {text: 'P-value with mut', value: 'p_value_with_mut', divider: true, align: 'center'},
              {text: 'P-value without mut', value: 'p_value_without_mut', divider: true, align: 'center'},
              {text: 'P-value comparative', value: 'p_value_comparative', divider: false, align: 'center'}
            ]
        headers = headers.concat(extendedHeaders);
      }

      return headers;
    },

    /** Array of (raw) data to display in the table (filtered by protein, if set) */
    filteredQueryResult() {
      if (this.selectedProtein !== null)
        return this.queryResult.filter((row) => row.protein === this.selectedProtein)
      else
        return this.queryResult
    },

    /** Array of (formatted) data actually displayed  */
    processedQueryResult() {
      const labelledRows = []
      this.filteredQueryResult.forEach((row) => {
        const labelledRow = {};
        // Notice: all the numeric values are converted into string
        labelledRow["location"] = row["location"];
        labelledRow["protein"] = row["protein"];
        labelledRow["mut"] = row["mut"];
        labelledRow["polyfit_slope"] = row["polyfit_slope"].toPrecision(4);
        if (!isNaN(row["p_value_with_mut"]))
          labelledRow["p_value_with_mut"] = row["p_value_with_mut"].toExponential(3);
        if (!isNaN(row["p_value_without_mut"]))
          labelledRow["p_value_without_mut"] = row["p_value_without_mut"].toExponential(3);
        if (!isNaN(row["p_value_comparative_mut"]))
          labelledRow["p_value_comparative"] = row["p_value_comparative_mut"].toExponential(3);
        for (let i = 1; i <= 4; i++) {
          labelledRow["f_w" + i] = row["f" + i].toPrecision(3) + "% (" + row["w" + i] + ")"
          labelledRow["f" + i] = row["f" + i]; // numeric value for sorting and plots
          labelledRow["w" + i] = row["w" + i]; // numeric value for plots
        }
        labelledRows.push(labelledRow)
      })
      return labelledRows;
    },

    /** Possible proteins values computed based on data results */
    possibleProteins() {
      const set = new Set(this.queryResult.map(row => row["protein"]));
      return [...set].sort();
    },

    /** Array of data to be plotted */
    plotsInfo() {
      let plotsTitle;
      let plotsData;

      if (this.selectedRows.length > 0) {
        plotsTitle = `Selected mutations (${this.selectedRows.length})`;
        plotsData = this.customSort([...this.selectedRows], this.sortingIndexes, this.isDescSorting).reverse();
      } else {
        plotsTitle = "Top 5 decreasing + Top 5 increasing mutations";
        const sortedData = this.customSort([...this.processedQueryResult], ['polyfit_slope'], [false])
        // Get first 5 and last 5
        if (sortedData.length >= 10)
          plotsData = sortedData.slice(0, 5).concat(sortedData.slice(-5));
        else
          plotsData = sortedData;
      }

      return {title: plotsTitle, data: plotsData, weekSeq: this.weekSeq};
    },

    /** Name for downloaded files:  Lin[<LINEAGE>|"Indep"]_<GRANULARITY>_[<LOCATION>]_<DATE> */
    fileName() {
      return "Lin" + (this.withLineages ? this.queryParams["lineage"] : "Indep") + "_" + this.queryParams['granularity'] + "_" + (this.queryParams['granularity'] !== 'world' ? this.queryParams['location'] : "") + "_" + this.queryParams['date'];
    }
  },
  methods: {

    /**
     * Downloads the data of the table
     */
    downloadData() {
      this.downloadLoading = true;
      const sortedData = this.customSort(this.processedQueryResult, this.sortingIndexes, this.isDescSorting);
      const csv = this.json2csv(sortedData, this.tableHeaders);

      // Anchor element to download the file
      const anchorElement = document.createElement('a');
      anchorElement.setAttribute('download', this.fileName + ".csv");
      const data = new Blob([csv]);
      anchorElement.href = URL.createObjectURL(data);
      document.body.appendChild(anchorElement);

      // Simulate click and remove element
      anchorElement.click();
      document.body.removeChild(anchorElement);
      this.downloadLoading = false;
    },


    /**
     * Downloads a screenshot of the table, heatmap and line chart
     */
    downloadAll() {
      this.downloadLoading = true;
      // Ref value of the section to be printed
      const sectionToPrint = this.$refs[this.fileName];

      const that = this

      async function downloadImage() {
        (await html2canvas(sectionToPrint)).toBlob((data) => {
          // Anchor element to download the file
          const anchorElement = document.createElement('a');
          anchorElement.setAttribute('download', that.fileName + ".png");
          anchorElement.href = URL.createObjectURL(data);
          document.body.appendChild(anchorElement);

          // Simulate click and remove element
          anchorElement.click();
          document.body.removeChild(anchorElement);
          that.downloadLoading = false;
        });
      }

      downloadImage();
    },


    /**
     * Converter utility json to csv
     * @param jsonData    The json data to be converted
     * @param headersInfo The headers info for the file to be generated
     * @returns {String}  A string representing the csv file
     */
    json2csv(jsonData, headersInfo) {
      // Names for the headers of the csv file (es. "Location","Slope",..)
      const fieldsHeaders = [];
      // Names of the fields of the jsonData element (es. "location","polyfit_slope",..)
      const fieldsNames = [];

      headersInfo.forEach(function (headerInfo) {
        fieldsHeaders.push(headerInfo.text);
        fieldsNames.push(headerInfo.value);
      });

      const csv = jsonData.map(function (jsonRow) {
        return fieldsNames.map(function (fieldName) {
          return JSON.stringify(String(jsonRow[fieldName]));
        }).join(',')
      });
      csv.unshift(fieldsHeaders.join(','));
      return csv.join('\r\n')
    },


    /**
     * Custom sort function for data table
     * @param items           Array of (processed) rows to be sorted
     * @param sortingIndexes  Array of field names selected for sorting
     * @param isDescSorting   Array of boolean values. Element i is true iff index[i] needs to be desc ordered
     * @returns {Array}       Array of sorted items
     */
    customSort(items, sortingIndexes, isDescSorting) {
      // Num of index selected
      const len = sortingIndexes.length;

      // No elements to be sorted? Nothing to do
      if (items.length === 0)
        return items;

      // No indexes selected to be sort on? Apply default ones
      if (len === 0)
        return this.customSort(items, this.defaultSorting.indexes, this.defaultSorting.isDescSorting);

      let i = 0;
      let positionOfLastIndex = len - 1;

      // Sort via custom cmp fn (returning 0 if A==B equal; 1 if A must appear before B; -1 otherwise)
      items.sort(function (a, b) {
        let i_local = i;
        let consideredIndex = sortingIndexes[i_local];
        while (i_local <= positionOfLastIndex) {
          // res is computed as follows: 0 if A==B, 1 if A<B, -1 if A>B
          let res;

          if (consideredIndex.startsWith("f_w")) {
            // Mutation diffusion data must consider only the percentage value
            let weekNum = consideredIndex[3];
            res = a["f" + weekNum] - b["f" + weekNum]
          } else {
            if (consideredIndex.startsWith("p_value") || consideredIndex.startsWith("polyfit_slope")) {
              // P_values (possibly NaN valued) and slope must be converted back into numbers to sort them
              if (!isNaN(a[consideredIndex]) && !isNaN(b[consideredIndex]))
                res = Number(a[consideredIndex]) - Number(b[consideredIndex])
              else
                res = isNaN(a[consideredIndex]) ? 1 : -1
            } else {
              // String are compared as usual
              res = String(a[consideredIndex]).localeCompare(b[consideredIndex]);
            }
          }

          // A<B on the current attribute? No need to check the others.
          if (res > 0)
            return (isDescSorting[i_local]) ? -1 : 1;

          // A>B on the current attribute. No need to check the others.
          if (res < 0)
            return (isDescSorting[i_local]) ? 1 : -1

          // A==B on the current attribute. Decide on the basis of the other indexes.
          i_local++;
        }
        // No other indexes selected to be sort on? Then, A==B
        if (i_local === positionOfLastIndex)
          return 0;
      })
      return items;
    },

    /**
     * Compute all the table labels for the week
     * @returns {Array} List of all the table labels for the week
     */
    computeDateLabels() {
      const dateLabels = [];
      dateLabels['w1'] = this.computeDateLabel(28, 22)
      dateLabels['w2'] = this.computeDateLabel(21, 15)
      dateLabels['w3'] = this.computeDateLabel(14, 8)
      dateLabels['w4'] = this.computeDateLabel(7, 0)
      return dateLabels;
    },

    /**
     * Compute the table label for the week based on the day difference from the reference date
     * @param from        Difference from the reference date for the start date of the label
     * @param to          Difference from the reference date for the ending date of the label
     * @returns {string}  A string of the form "YYYY/mm/dd - YYYY/mm/dd"
     */
    computeDateLabel(from, to) {
      const referenceDate = new Date(this.queryParams.date);
      const fromDate = new Date(referenceDate);
      const toDate = new Date(referenceDate);

      fromDate.setDate(referenceDate.getDate() - from);
      toDate.setDate(referenceDate.getDate() - to);
      return fromDate.toISOString().slice(0, 10).replaceAll('-', '/') + " - " + toDate.toISOString().slice(0, 10).replaceAll('-', '/');
    },
  }
}
</script>

<style scoped>

/* Panel container styling */
.panel-container {
  background: var(--secondary-color); /* to ensure readable downloadable images */
  padding-top: 30px;
  margin: 0;
}


/* Filter container styling */
.filter-container {
  border-radius: var(--border-radius);
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
  word-spacing: 5px;
  margin-top: 30px;
}


/* Table options */
.table-controls {
  padding-top: 25px;
  padding-bottom: 18px;
}

.table-controls .d-flex {
  padding-bottom: 7px !important;
  padding-top: 0 !important;
}


/* Custom main headers styling*/
.main-headers {
  background: var(--tertiary-color-light);
}

.main-headers th {
  letter-spacing: 0.05em;
  word-spacing: 0.1em;
  text-align: center !important;
  border-top: var(--tertiary-color-dark) solid 1px !important;
  padding-top: 7px !important;
  padding-bottom: 7px !important;
  height: fit-content !important;
}

.main-headers th:not(:last-child) {
  border-right: thin solid rgba(0, 0, 0, 0.12) !important;

}

.empty-main-header {
  border-bottom: none !important;
}

/* Table size */
.table-element {
  width: 100%;
}

</style>

<style>

/* Additional global rules to overwrite the vuetify styling fot table*/
.table-container .v-data-table-header th {
  border-top: none !important;
  border-bottom: var(--tertiary-color-dark) solid 1px !important;
  padding-top: 17px !important;
  padding-bottom: 3px !important;
}

.table-container .v-data-table-header th:first-child {
  padding-bottom: 15px !important;
}

.table-container .v-data-table, .table-container .v-data-table-header {
  background: var(--tertiary-color-light) !important;
}

.table-container table {
  background: white !important;
}

.table-container th span:first-child {
  display: block !important;
}

/* Avoid breaking table content across multiple lines */
.table-container tbody {
  white-space: nowrap !important;
}

/* Overwrite the default ordering icon with a more intuitive one */
.v-data-table-header__icon::before {
  content: "\F04BC" !important;
}
</style>