<!--
  Component:    ResultView
  Description:  Container of the data table, heatmap and a barchart

  Props:
  ├── queryResult:  Array of raw data fetched from the server
  ├── queryParams:  Object storing the query parameters {granularity, location, date, [lineage]}
  ├── querySupport: Object storing additional info such as total number of sequences collected per week and characterizing muts
  ├── queryCustOpt: Object storing the custom preselection for the filtering/selection options
  └── withLineages: Lineages flag. True if the data refers to a lineage specific analysis.

  Events:
  ├── askAnalysis:  Emitted whenever a next/prev button is pressed
  └── error:        Emitted on server errors
-->

<template>
  <v-layout :ref='fileName' justify-center row class='panel-container' wrap>

    <!-- Filtering options -->
    <v-flex class=' xs12 d-flex filter-container' justify-center>
      <v-container>
        <v-layout justify-center row wrap>
          <v-flex justify-center class='xs12 sm12 md5 d-flex filter-heading'>
            <h3>
              <v-icon color='white' left>mdi-filter-outline</v-icon>
              FILTERING OPTIONS
            </h3>
          </v-flex>
          <!-- Protein filter -->
          <v-flex justify-center class='xs12 sm4 md3 d-flex '>
            <FieldSelector v-model='selectedProtein' label='Protein' placeholder='All'
                           :possible-values='possibleProteins' autocomplete solo />
          </v-flex>

          <!-- Mutation filter -->
          <v-flex justify-center class='xs12 sm7 md4 d-flex '>
            <MutationSelector v-model='selectedMutation' :possible-values='possibleMutations'
                              :queryParams='queryParams' :characterizing-muts='querySupport.characterizingMuts'/>
          </v-flex>
        </v-layout>
      </v-container>
    </v-flex>

    <!-- MUTATIONS TABLE SECTION  --------------------------------------------->
    <SectionElement icon='mdi-table-multiple' title='MUTATIONS TABLE'>
      <v-data-table v-model='selectedRows' :custom-sort='customSort' :headers='tableHeaders'
                    :items='processedQueryResult' :sort-by.sync='sortingIndexes' :sort-desc.sync='isDescSorting'
                    :footer-props='footerProps' :show-expand='!withLineages' @item-expanded='loadLineageDetails'
                    :loading='isLoadingDetails' :single-expand='true' class='table-element' item-key='item_key'
                    :expanded.sync='expandedRows' multi-sort show-select mobile-breakpoint='0'
                    @toggle-select-all='handleToggleSelection'>

        <!---- Table controls ---->
        <template v-slot:top>
          <TableControls :show-p-values='showPValues' :download-loading='downloadLoading'
                         @showPValues='(flag) => showPValues=flag' @downloadAll='downloadAll'
                         @downloadData='downloadData' />
        </template>

        <!---- Table super headers ---->
        <template v-slot:header>
          <TableSuperHeader :with-lineages='withLineages' :show-p-values='showPValues' />
        </template>

        <!-- Customized mutation column style for lineage specific search -->
        <template v-if="withLineages" v-slot:item.mut="{ item }">
          <div :class="isCharacterizingMut(item)? 'char-mut':''">{{ item.mut }}</div>
        </template>

        <!---- Expanded table element ---->
        <template v-if='!withLineages && !isLoadingDetails' v-slot:expanded-item='{ headers, item }'>
          <td :colspan='5' class='expanded-item-title'>
            <div>Lineages</div>
          </td>
          <td class='expanded-td'>
            <v-simple-table>
              <tbody>
              <tr v-for='(lineage, lineage_index) in item.lineages' v-bind:key='lineage_index'>
                <td>{{ lineage.name }}</td>
              </tr>
              </tbody>
            </v-simple-table>
          </td>
          <td class='expanded-td' v-for='week in [1, 2, 3, 4]' v-bind:key='week'>
            <v-simple-table>
              <tbody>
              <tr v-for='(lineage, lineage_index) in item.lineages' v-bind:key='lineage_index'>
                <td>
                  {{ lineage['f' + week].toPrecision(3) + '% (' + lineage['w' + week] + ')' }}
                </td>
              </tr>
              </tbody>
            </v-simple-table>
          </td>
        </template>
        <template v-slot:body.append>
          <td :colspan='withLineages? 5: 6' class='table-append' />
          <td v-for='week in [1,2,3,4]' v-bind:key='week' class='table-append' >
            Tot. seq.: {{querySupport.totSeq[week-1]}}
          </td>
        </template>
      </v-data-table>
    </SectionElement>

    <!-- HEATMAP SECTION  ----------------------------------------------------->
    <SectionElement icon='mdi-chart-gantt' title='DIFFUSION HEATMAP'>
      <HeatMap :dateLabel='computeDateLabels()' :plotData='plotsInfo.data' :plotTitle='plotsInfo.title' />
    </SectionElement>

    <!-- CHART SECTION  ------------------------------------------------------->
    <SectionElement icon='mdi-chart-line' title='DIFFUSION TREND CHART'>
      <LineChart :dateLabel='computeDateLabels()' :plotData='plotsInfo.data' :plotTitle='plotsInfo.title'
                 :weekSeq='plotsInfo.support' />
    </SectionElement>

    <!-- ODD RATIO SECTION  --------------------------------------------------->
    <SectionElement icon='mdi-align-vertical-bottom' title='DIFFUSION ODD RATIO' collapsed
                    :tabs='["Week-by-week","Week-to-first-week","All"]' @tabChange='(selected) => oddRatioType=selected'>
      <OddRatioChart :dateLabel='computeDateLabels()' :plotData='plotsInfo.data' :plotTitle='plotsInfo.title' :type='oddRatioType'/>
    </SectionElement>

    <!-- Next/prev week button ------------------------------------------------>
    <v-flex class='xs12 d-flex'>
      <v-btn class='white--text' color='#011936' @click="$emit('askAnalysis', -7,status)">
        <v-icon left>mdi-chevron-left</v-icon>
        PREV WEEK
      </v-btn>
      <v-spacer></v-spacer>
      <v-btn class='white--text' color='#011936' @click="$emit('askAnalysis', +7,status)">
        NEXT WEEK
        <v-icon right>mdi-chevron-right</v-icon>
      </v-btn>
    </v-flex>
  </v-layout>
</template>

<script>
import LineChart from './plots/LineChart'
import HeatMap from './plots/HeatMap'
import { mapState } from 'vuex'
import html2canvas from 'html2canvas'
import axios from 'axios'
import FieldSelector from '@/components/form/FieldSelector'
import TableControls from '@/components/tables/TableControls'
import TableSuperHeader from '@/components/tables/TableSuperHeader'
import OddRatioChart from '@/components/plots/OddRatioChart'
import SectionElement from '@/components/general/SectionElement'
import MutationSelector from '@/components/form/MutationSelector'
import { json2csv } from '@/utils/parserService'

export default {
  name: 'ResultView',
  components: { MutationSelector, SectionElement, OddRatioChart, TableSuperHeader, TableControls, FieldSelector, HeatMap, LineChart },
  props: {
    /**
     * Array of raw data fetched from the server of the form:
     *  [{  location, protein, [lineage,] mut, slope, w[1-4], f[1-4],
     *      p_value_with_mut, p_value_without_mut, p_value_comp}, ...      ]
     */
    queryResult: { required: true },

    /** Object storing the query parameters {granularity, location, date, [lineage]} */
    queryParams: { required: true },

    /** Object storing additional info such as total number of sequences collected per week and characterizing muts */
    querySupport: { required: true },

    /** Object storing the custom preselection for the filtering/selection options */
    queryCustOpt: { required: false },

    /** Lineages flag. True if the data refers to a lineage specific analysis.*/
    withLineages: Boolean
  },
  data () {
    return {
      /** Selected protein to further filter the data */
      selectedProtein: null,

      /** Selected mutation to further filter the data. Takes the form <PROTEIN>_<MUT> */
      selectedMutation: null,

      /** Array of selected rows */
      selectedRows: [],

      /** Array of expanded rows (relevant for lineage-indep only)*/
      expandedRows: [],

      /** Array of columns selected for sorting data */
      sortingIndexes: [],

      /** Array defining asc(true)/desc(false) order for each column selected for sorting in sortingIndexes */
      isDescSorting: [],

      /** Default sorting options */
      defaultSorting: { indexes: ['slope'], isDescSorting: [true] },

      /** Footer options for the data table */
      footerProps: {
        'items-per-page-options': [-1, 10, 20, 50, 100, 150, 200, 500]
      },

      /** Flag to show the p_values in the table */
      showPValues: false,

      /** Loading flag for the table */
      isLoadingDetails: false,

      /** Download flag: true if a file download is in progress */
      downloadLoading: false,

      /** Type of odd ratio to be displayed. 0: week-by-week; 1: week-to-first-week; 2: all*/
      oddRatioType: 0
    }
  },
  computed: {
    ...mapState(['secondary_color']),

    /** The current customization status */
    status () {
      return {
        'selectedRowsKeys': this.selectedRows.map(row => row.item_key),
        'selectedProtein': this.selectedProtein,
        'selectedMutation': this.selectedMutation
      }
    },

    /** Array of objects describing header columns */
    tableHeaders () {
      let headers = [
        { text: 'Location', value: 'location', divider: true, align: 'center' },
        { text: 'Protein', value: 'protein', divider: true, align: 'center' },
        { text: 'Mut', value: 'mut', divider: true, align: 'center' },
        { text: 'Slope', value: 'slope', divider: true, align: 'center' },
        { text: this.computeDateLabel(27, 21), value: 'f_w1', divider: true, align: 'center' },
        { text: this.computeDateLabel(20, 14), value: 'f_w2', divider: true, align: 'center' },
        { text: this.computeDateLabel(13, 7), value: 'f_w3', divider: true, align: 'center' },
        { text: this.computeDateLabel(6, 0), value: 'f_w4', divider: true, align: 'center' }
      ]

      if (this.showPValues) {
        const extendedHeaders = [
          { text: 'P-value with mut', value: 'p_value_with_mut', divider: true, align: 'center' },
          { text: 'P-value without mut', value: 'p_value_without_mut', divider: true, align: 'center' },
          { text: 'P-value comparative', value: 'p_value_comp', divider: false, align: 'center' }
        ]
        headers = headers.concat(extendedHeaders)
      }

      return headers
    },

    /** Array of raw data fetched from the server filtered by protein and mut, if set */
    filteredQueryResult () {
      const that = this
      return this.queryResult.filter(function (row) {
        const proteinCheck = that.selectedProtein === null || row.protein === that.selectedProtein
        const mutationCheck = that.selectedMutation === null || that.selectedMutation.length === 0 || that.selectedMutation.includes(row.protein + '_' + row.mut)
        return proteinCheck && mutationCheck
      })
    },

    /** Array of (formatted) data actually displayed in the tables  */
    processedQueryResult () {
      const rows = []
      this.filteredQueryResult.forEach(rawRow => {
        const row = {}

        row['item_key'] = rawRow['protein'] + '_' + rawRow['mut']
        row['location'] = rawRow['location']
        row['protein'] = rawRow['protein']
        row['mut'] = rawRow['mut']

        // Convert numeric slope and p-values into a formatted string
        row['slope'] = rawRow['slope'].toPrecision(4)
        if (!isNaN(rawRow['p_value_with_mut'])) {
          row['p_value_with_mut'] = rawRow['p_value_with_mut'].toExponential(3)
        }
        if (!isNaN(rawRow['p_value_without_mut'])) {
          row['p_value_without_mut'] = rawRow['p_value_without_mut'].toExponential(3)
        }
        if (!isNaN(rawRow['p_value_comp'])) {
          row['p_value_comp'] = rawRow['p_value_comp'].toExponential(3)
        }

        for (let i = 1; i <= 4; i++) {
          row['f_w' + i] = rawRow['f' + i].toPrecision(3) + '% (' + rawRow['w' + i] + ')'
          row['f' + i] = rawRow['f' + i] // numeric value for sorting and plots
          row['w' + i] = rawRow['w' + i] // numeric value for plots
        }

        rows.push(row)
      })
      return rows
    },

    /** Possible proteins values computed based on data results */
    possibleProteins () {
      const set = new Set(this.queryResult.map(row => row['protein']))
      return [...set].sort()
    },

    /** Possible mutations values computed based on data results */
    possibleMutations () {
      const set = new Set(
        this.queryResult.map(row => row['protein'] + '_' + row['mut'])
      )
      return [...set].sort()
    },

    /** Array of data to be plotted */
    plotsInfo () {
      let plotsTitle
      let plotsData

      if (this.selectedRows.length > 0) {
        plotsTitle = `Selected mutations (${this.selectedRows.length})`
        plotsData = this.customSort([...this.selectedRows], this.sortingIndexes, this.isDescSorting).reverse()
      } else {
        const sortedData = this.customSort([...this.processedQueryResult], ['slope'], [false])
        // Get first 5 and last 5
        if (sortedData.length >= 10) {
          plotsTitle = 'Top 5 decreasing + Top 5 increasing mutations'
          plotsData = sortedData.slice(0, 5).concat(sortedData.slice(-5))
        } else {
          plotsTitle = `All mutations (${sortedData.length})`
          plotsData = sortedData
        }
      }

      return { title: plotsTitle, data: plotsData, support: this.querySupport.totSeq }
    },

    /** Name for downloaded files:  Lin[<LINEAGE>|"Indep"]_<GRANULARITY>_[<LOCATION>]_<DATE> */
    fileName () {
      return (
        'Lin' + (this.withLineages ? this.queryParams['lineage'] : 'Indep') + '_' +
        this.queryParams['granularity'] + '_' +
        (this.queryParams['granularity'] !== 'world' ? this.queryParams['location'] : '') + '_' +
        this.queryParams['date']
      )
    }
  },
  methods: {
    /**
     * Downloads the data of the table
     */
    downloadData () {
      this.downloadLoading = true
      const sortedData = this.customSort(this.processedQueryResult, this.sortingIndexes, this.isDescSorting)
      const csv = json2csv(sortedData, this.tableHeaders)

      // Anchor element to download the file
      const anchor = document.createElement('a')
      anchor.setAttribute('download', this.fileName + '.csv')
      const data = new Blob([csv])
      anchor.href = URL.createObjectURL(data)
      document.body.appendChild(anchor)

      // Simulate click and remove element
      anchor.click()
      document.body.removeChild(anchor)
      this.downloadLoading = false
    },

    /**
     * Downloads a screenshot of the table, heatmap and line chart
     */
    downloadAll () {
      this.downloadLoading = true
      // Ref value of the section to be printed
      const sectionToPrint = this.$refs[this.fileName]
      const that = this

      async function downloadImage () {
        (await html2canvas(sectionToPrint)).toBlob(data => {
          // Anchor element to download the file
          const anchor = document.createElement('a')
          anchor.setAttribute('download', that.fileName + '.png')
          anchor.href = URL.createObjectURL(data)
          document.body.appendChild(anchor)

          // Simulate click and remove element
          anchor.click()
          document.body.removeChild(anchor)
          that.downloadLoading = false
        })
      }

      downloadImage()
    },

    /**
     * Custom sort function for data table
     * @param items           Array of (processed) rows to be sorted
     * @param sortingIndexes  Array of field names selected for sorting
     * @param isDescSorting   Array of boolean values. Element i is true iff index[i] needs to be desc ordered
     * @returns {Array}       Array of sorted items
     */
    customSort (items, sortingIndexes, isDescSorting) {
      // Num of index selected
      const len = sortingIndexes.length

      // No elements to be sorted? Nothing to do
      if (items.length === 0) {
        return items
      }

      // No indexes selected to be sort on? Apply default ones
      if (len === 0) {
        return this.customSort(
          items,
          this.defaultSorting.indexes,
          this.defaultSorting.isDescSorting
        )
      }

      const i = 0
      const positionOfLastIndex = len - 1

      // Sort via custom cmp fn (returning 0 if A==B equal; 1 if A must appear before B; -1 otherwise)
      items.sort(function (a, b) {
        let iLocal = i
        const consideredIndex = sortingIndexes[iLocal]
        while (iLocal <= positionOfLastIndex) {
          // res is computed as follows: 0 if A==B, 1 if A<B, -1 if A>B
          let res

          if (consideredIndex.startsWith('f_w')) {
            // Mutation diffusion data must consider only the percentage value
            const weekNum = consideredIndex[3]
            res = a['f' + weekNum] - b['f' + weekNum]
          } else {
            if (
              consideredIndex.startsWith('p_value') ||
              consideredIndex.startsWith('slope')
            ) {
              // P_values (possibly NaN valued) and slope must be converted back into numbers to sort them
              if (!isNaN(a[consideredIndex]) && !isNaN(b[consideredIndex])) {
                res = Number(a[consideredIndex]) - Number(b[consideredIndex])
              } else {
                res = isNaN(a[consideredIndex]) ? 1 : -1
              }
            } else {
              // String are compared as usual
              res = String(a[consideredIndex]).localeCompare(b[consideredIndex])
            }
          }

          // A<B on the current attribute? No need to check the others.
          if (res > 0) {
            return isDescSorting[iLocal] ? -1 : 1
          }

          // A>B on the current attribute. No need to check the others.
          if (res < 0) {
            return isDescSorting[iLocal] ? 1 : -1
          }

          // A==B on the current attribute. Decide on the basis of the other indexes.
          iLocal++
        }
        // No other indexes selected to be sort on? Then, A==B
        if (iLocal === positionOfLastIndex) {
          return 0
        }
      })
      return items
    },

    /**
     * Compute all the table labels for the week
     * @returns {Array} List of all the table labels for the week
     */
    computeDateLabels () {
      const dateLabels = []
      dateLabels['w1'] = this.computeDateLabel(27, 21)
      dateLabels['w2'] = this.computeDateLabel(20, 14)
      dateLabels['w3'] = this.computeDateLabel(13, 7)
      dateLabels['w4'] = this.computeDateLabel(6, 0)
      return dateLabels
    },

    /**
     * Compute the table label for the week based on the day difference from the reference date
     * @param from        Difference from the reference date for the start date of the label
     * @param to          Difference from the reference date for the ending date of the label
     * @returns {string}  A string of the form "YYYY/mm/dd - YYYY/mm/dd"
     */
    computeDateLabel (from, to) {
      const referenceDate = new Date(this.queryParams.date)
      const fromDate = new Date(referenceDate)
      const toDate = new Date(referenceDate)

      fromDate.setDate(referenceDate.getDate() - from)
      toDate.setDate(referenceDate.getDate() - to)
      return (
        fromDate
          .toISOString()
          .slice(0, 10)
          .replaceAll('-', '/') +
        ' - ' +
        toDate
          .toISOString()
          .slice(0, 10)
          .replaceAll('-', '/')
      )
    },

    /**
     * Fetch lineages data when a row of the table is expanded. Lineage independent search only.
     * @param item
     */
    loadLineageDetails (item) {
      // Catch row expansion only
      if (item.value) {
        this.isLoadingDetails = true
        const url = `/lineage_independent/getLineagesStatistics`
        const toSend = {
          location: item.item.location,
          date: this.queryParams.date,
          prot: item.item.protein,
          mut: item.item.mut
        }

        axios
          .post(url, toSend)
          .then(res => {
            return res.data
          })
          .then(res => {
            item.item.lineages = res
            this.isLoadingDetails = false
          })
          .catch((e) => {
            this.$emit('error', e)
          })
      }
    },

    /**
     * Determines whether a mutation is characterizing the lineage or not
     * @param item   The item to be considered
     * @returns {boolean}   True iff the mutation is characterizing the lineage
     */
    isCharacterizingMut (item) {
      return this.querySupport.characterizingMuts.includes(item.protein + '_' + item.mut)
    },

    /**
     * Clear all the selected rows on deselect-all table event
     * @param toggleStatus  Status of the toggle from v-data-table event
     */
    handleToggleSelection (toggleStatus) {
      if (!toggleStatus.value) {
        this.selectedRows = []
      }
    }
  },
  mounted () {
    // Apply customization options: restore filters and selection but only if applicable
    if (this.queryCustOpt) {
      const presMut = this.queryCustOpt.selectedMutation
      const presProt = this.queryCustOpt.selectedProtein
      const presKeys = this.queryCustOpt.selectedRowsKeys

      this.selectedProtein = this.possibleProteins.includes(presProt)
        ? presProt
        : null
      this.selectedMutation = presMut
        ? presMut.filter((m) => this.possibleMutations.includes(m))
        : null
      this.selectedRows = presKeys
        ? this.processedQueryResult.filter(row => presKeys.includes(row.item_key))
        : []
    }
  },
  watch: {
    /** Force closing expanded rows (relevant for lineage-indep only) on data update */
    processedQueryResult () {
      this.expandedRows = []
    }
  }
}
</script>

<style>

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

/* Table size */
.table-element {
  width: 100%;
}

/* Special formatting for characterizing muts*/
.char-mut{
  background: rgba(255, 255, 0, 0.45);
}

/* Expanded element style */
td.expanded-td {
  text-align: center;
  border-right: thin solid rgba(0, 0, 0, 0.12);
}

td.expanded-td tr:hover {
  background: none !important;
}

.expanded-item-title {
  text-align: -webkit-right;
  background: var(--tertiary-color-light);
  border-right: thin solid var(--tertiary-color-dark);
}

.expanded-item-title div {
  color: rgba(0, 0, 0, 0.6);
  font-weight: bold;
  font-size: 12px;
  letter-spacing: 0.019em;
  display: inherit;
}

td.table-append{
  padding: 6px;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.87);
  border-right: thin solid rgba(0, 0, 0, 0.12);
}

/* Additional global rules to overwrite the vuetify styling fot table*/
.section-container .v-data-table-header th {
  border-top: none !important;
  border-bottom: var(--tertiary-color-dark) solid 1px !important;
  padding-top: 17px !important;
  padding-bottom: 3px !important;
}

.v-data-table-header .v-input--selection-controls__input {
  padding-bottom: 15px !important;
}

.section-container .v-data-table,
.section-container .v-data-table-header {
  border-radius: 4px 0 4px 4px;
  background: var(--tertiary-color-light) !important;
}

.section-container table {
  background: white !important;
}

.section-container th span:first-child {
  display: block !important;
}

/* Avoid breaking table content across multiple lines */
.section-container tbody {
  white-space: nowrap !important;
}

/* Overwrite the default ordering icon with a more intuitive one */
.v-data-table-header__icon::before {
  content: '\F04BC' !important;
}

/* Avoid box shadow for expanded table element */
tr.v-data-table__expanded__content {
  box-shadow: none !important;
}

/* Reduce excessive padding to the right icons of the tables*/
.v-application .text-start {
  padding-left: 11px !important;
  padding-right: 2px !important;
}
</style>
