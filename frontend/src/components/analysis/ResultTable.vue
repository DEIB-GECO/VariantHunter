<template>
  <section-element icon='mdi-table-multiple' title="Mutations table">
    <v-col cols="12" class="pa-0 table-container">
      <v-data-table v-model='selectedRows' :custom-sort='customSort' :headers='tableHeaders'
                    :items='processedQueryResult' :sort-by.sync='sortingIndexes' :sort-desc.sync='isDescSorting'
                    :footer-props='footerProps' :show-expand='!withLineages' @item-expanded='loadLineageDetails'
                    :loading='isLoadingDetails' single-expand class='table-element' item-key='item_key'
                    :expanded.sync='expandedRows' multi-sort show-select mobile-breakpoint='0'
                    @toggle-select-all='handleToggleSelection'>

        <!---- Table controls ---->
        <template v-slot:top>
          <table-controls @showPValues='(flag) => showPValues=flag'/>
        </template>

        <!---- Table super headers ---->
        <template v-slot:header>
          <table-super-header :with-lineages='withLineages' :show-p-values='showPValues'/>
        </template>

        <!-- Customized mutation column style for lineage specific search -->
        <template v-if='withLineages' v-slot:item.mut='{ item }'>
          <div :class="isCharacterizingMut(item)? 'char-mut':''">{{ item.mut }}</div>
        </template>

        <!---- Expanded table element ---->
        <template v-if='!withLineages && !isLoadingDetails' v-slot:expanded-item='{ item }'>
          <td :colspan='4' class='expanded-item-title'>
            <expansion-mode-menu @changeNotationMode="e=>notationMode=e" @changeExapnsionMode="e=>expansionMode=e"/>
            <div class="row-name">Lineages</div>
          </td>
          <td class='expanded-td'>
            <v-simple-table>
              <tbody>
              <tr v-for='(lineage, lineage_index) in formatBreakdown(item.lineages)' v-bind:key='lineage_index'>
                <td>{{ lineage.name }}</td>
              </tr>
              </tbody>
            </v-simple-table>
          </td>
          <td class='expanded-td' v-for='week in [1, 2, 3, 4]' v-bind:key='week'>
            <v-simple-table>
              <tbody>
              <tr v-for='(lineage, lineage_index) in formatBreakdown(item.lineages)' v-bind:key='lineage_index'>
                <td>
                  {{ lineage['f' + week].toPrecision(3) + '% (' + lineage['w' + week] + ')' }}
                </td>
              </tr>
              </tbody>
            </v-simple-table>
          </td>
        </template>
        <template v-else-if="isLoadingDetails" v-slot:expanded-item>
          <td colspan="9" class="py-5">
            <v-progress-circular indeterminate color="primary"/>
            <span class="pl-4">Loading...</span></td>
        </template>

        <template v-slot:body.append>
          <td :colspan='withLineages? 4: 5' class='table-append'/>
          <td v-for='week in [1,2,3,4]' v-bind:key='week' class='table-append text-center'>
            Tot. seq.: {{ getCurrentAnalysis.totSeq['w' + week] }}
          </td>
        </template>

        <template v-slot:footer.prepend>
          <go-to-cov-spectrum/>
        </template>
      </v-data-table>
    </v-col>
  </section-element>
</template>

<script>
import SectionElement from "@/components/general/SectionElement";
import TableControls from "@/components/tables/TableControls";
import TableSuperHeader from "@/components/tables/TableSuperHeader";
import ExpansionModeMenu from "@/components/form/menus/ExpansionModeMenu";
import {mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import {compactLineagesData} from "@/utils/formatterService";
import GoToCovSpectrum from "@/components/tables/GoToCovSpectrum";

export default {
  name: "ResultTable",
  components: {GoToCovSpectrum, ExpansionModeMenu, TableSuperHeader, TableControls, SectionElement},
  props: {
    withLineages: {},
  },
  data() {
    return {

      /** Array of expanded rows (relevant for lineage-indep only )*/
      expandedRows: [],

      /** Mode of the breakdown view. 0=consider the expanded line only; 1= consider the whole dataset */
      expansionMode: 0,

      /** Notation mode of the breakdown view.  0=full notation; 1,2= start notation (level)  */
      notationMode: 0,

      /** Default sorting options */
      defaultSorting: {indexes: ['slope'], isDescSorting: [true]},

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
      }
  },
  computed: {
    ...mapState(['globalFilteringOpt','globalOrderingOpt']),
    ...mapGetters(['getCurrentAnalysis','getCurrentLocalFilteringOpt','getCurrentLocalOrderingOpt',
      'getCurrentFilteredRows','getCurrentSelectedRows']),

    characterizingMuts() {
      console.log("# characterizingMuts=" + this.getCurrentAnalysis.characterizingMuts)
      return this.withLineages ? this.getCurrentAnalysis.characterizingMuts : null
    },

    useGlobalFilters() {
      console.log("# useGlobalFilters=" + this.getCurrentLocalFilteringOpt.useGlobalFilters)
      return this.getCurrentLocalFilteringOpt.useGlobalFilters
    },

    filteringOpt() {
      console.log("# filters=" + JSON.stringify((this.useGlobalFilters ? this.globalFilteringOpt : this.getCurrentLocalFilteringOpt)))
      return (this.useGlobalFilters ? this.globalFilteringOpt : this.getCurrentLocalFilteringOpt)
    },

     orderingOpt() {
      console.log("# order=" + JSON.stringify((this.useGlobalFilters ? this.globalOrderingOpt : this.getCurrentLocalOrderingOpt)))
      return (this.useGlobalFilters ? this.globalOrderingOpt : this.getCurrentLocalOrderingOpt)
    },

    /** Array of selected rows */
    selectedRows: {
      set(newVal) {
        const keys = newVal.map(({item_key})=>item_key)
        this.setFilterOpt({global: this.useGlobalFilters, opt: 'rowKeys', value: keys})
      },
      get() {
        console.log("# selectedRows=" + this.getCurrentSelectedRows)
        return this.getCurrentSelectedRows
      }
    },


    /** Array of columns selected for sorting data */
    sortingIndexes: {
      set(newVal) {
        console.log("# set sortingIndexes")
        this.setOrderOpt({global: this.useGlobalFilters, opt: 'sortingIndexes', value: newVal})
      },
      get() {
        console.log("# sortingIndexes=" + this.orderingOpt.sortingIndexes)
        return this.orderingOpt.sortingIndexes
      }
    },

    /** Array defining asc(true)/desc(false) order for each column selected for sorting in sortingIndexes */
    isDescSorting: {
      set(newVal) {
        console.log("# set isDescSorting")
        this.setOrderOpt({global: this.useGlobalFilters, opt: 'isDescSorting', value: newVal})
      },
      get() {
        console.log("# isDescSorting=" + this.orderingOpt.isDescSorting)
        return this.orderingOpt.isDescSorting
      }
    },

    query() {
      return this.getCurrentAnalysis.query
    },

    /** Array of objects describing header columns */
    tableHeaders() {
      const {w1,w2,w3,w4}=this.query.weeks
      let headers = [
        {text: 'Protein', value: 'protein', divider: true, align: 'center'},
        {text: 'Mut', value: 'mut', divider: true, align: 'center'},
        {text: 'Slope', value: 'slope', divider: true, align: 'center'},
        {text: w1, value: 'f_w1', divider: true, align: 'center'},
        {text: w2, value: 'f_w2', divider: true, align: 'center'},
        {text: w3, value: 'f_w3', divider: true, align: 'center'},
        {text: w4, value: 'f_w4', divider: true, align: 'center'}
      ]

      if (this.showPValues) {
        const extendedHeaders = [
          {text: 'P-value with mut', value: 'p_value_with_mut', divider: true, align: 'center'},
          {text: 'P-value without mut', value: 'p_value_without_mut', divider: true, align: 'center'},
          {text: 'P-value comparative', value: 'p_value_comp', divider: false, align: 'center'}
        ]
        headers = headers.concat(extendedHeaders)
      }
      return headers
    },

    /** Array of (formatted) data actually displayed in the tables  */
    processedQueryResult() {
      const rows = []
      console.log(this.getCurrentFilteredRows)
      this.getCurrentFilteredRows.forEach(rawRow => {
        const row = {}

        row['item_key'] = rawRow['protein'] + '_' + rawRow['mut']
        row['protein'] = rawRow['protein']
        row['mut'] = rawRow['mut']
        row['location'] = rawRow['location']

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

  },
  methods: {
    ...mapMutations(['setFilterOpt','setOrderOpt']),

    /**
     * Custom sort function for data table
     * @param items           Array of (processed) rows to be sorted
     * @param sortingIndexes  Array of field names selected for sorting
     * @param isDescSorting   Array of boolean values. Element i is true iff index[i] needs to be desc ordered
     * @returns {Array}       Array of sorted items
     */
    customSort(items, sortingIndexes, isDescSorting) {
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
     * Fetch lineages data when a row of the table is expanded. Lineage independent search only.
     * @param item
     */
    loadLineageDetails(item) {
      console.log("EXPANDED "+JSON.stringify(item))
      // Catch row expansion only
      if (item.value) {
        this.error = undefined
        this.isLoadingDetails = true
        const url = `/lineage_independent/getLineagesStatistics`
        const toSend = {
          location: item.item.location,
          date: this.query.endDate,
          prot: item.item.protein,
          mut: item.item.mut,
          mode: this.expansionMode === 0 ? 'line' : 'full'
        }

        axios
            .post(url, toSend)
            .then(({data}) => item.item.lineages = data)
            .catch((e) => this.error = e)
            .finally(() => this.isLoadingDetails = false)
      }
    },

    /**
     * Reformat breakdown data based on the notation mode selected. Either using full notation or star notation.
     * @param lineagesData  The lineages data in full notation
     * @returns {*}         Lineages data in the correct notation
     */
    formatBreakdown(lineagesData){
      return (this.notationMode===0 || !lineagesData)? lineagesData : compactLineagesData(lineagesData,this.notationMode)
    },

    /**
     * Determines whether a mutation is characterizing the lineage or not
     * @param item   The item to be considered
     * @returns {boolean}   True iff the mutation is characterizing the lineage
     */
    isCharacterizingMut(item) {
      return this.getCurrentAnalysis.characterizingMuts.includes(item.protein + '_' + item.mut)
    },

    /**
     * Clear all the selected rows on deselect-all table event
     * @param toggleStatus  Status of the toggle from v-data-table event
     */
    handleToggleSelection(toggleStatus) {
      if (!toggleStatus.value) {
        this.selectedRows = []
      }
    }
  }
}
</script>

<style>

.table-container{
  border: solid 1px var(--primary-color);
  border-radius: 4px;
}

/* Table size */
.table-element {
  width: 100% !important;
}

/* Special formatting for characterizing muts*/
.char-mut {
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
  position: relative;
  text-align: -webkit-right;
  background: var(--tertiary-color-light);
  border-right: thin solid var(--primary-color);
}

.expanded-item-title .row-name {
  color: rgba(0, 0, 0, 0.6);
  font-weight: bold;
  font-size: 12px;
  letter-spacing: 0.019em;
  display: inherit;
  width: 110px;
  height: 110px;
  text-align: center;
  vertical-align: bottom;
  rotate: -90deg;
  padding-bottom: 4px;
}

td.table-append {
  padding: 6px;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.87);
  border-right: thin solid rgba(0, 0, 0, 0.12);
}

/* Additional global rules to overwrite the vuetify styling fot table*/
.section-container .v-data-table-header th {
  border-top: none !important;
  border-bottom: white solid 1px !important;
  padding-top: 17px !important;
  padding-bottom: 3px !important;
}

.v-data-table-header .v-input--selection-controls__input {
  padding-bottom: 15px !important;
}

.section-container .v-data-table,
.section-container .v-data-table-header {
  border-radius: 4px;
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
