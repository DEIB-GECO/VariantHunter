<template>
  <section-element icon='mdi-table-multiple' title="Mutations table">
    <v-col cols="12" class="pa-0 table-container">
      <v-data-table :headers='tableHeaders' :custom-sort="customSort"
                    :items='getCurrentFilteredRows' :sort-by.sync='sortingIndexes' :sort-desc.sync='isDescSorting'
                    :footer-props='footerProps' :loading='isLoadingDetails' single-expand class='table-element'
                    item-key='item_key' :custom-filter="()=>true"
                    :expanded.sync='expandedRows' multi-sort show-select mobile-breakpoint='0'
                    @item-expanded='loadLineageDetails' show-expand>

        <!---- TABLE CONTROLS --------------------------------------------->
        <template v-slot:top>
          <table-controls @showPValues='(flag) => showPValues=flag'/>
        </template>


        <!---- TABLE SUPER HEADERS ---------------------------------------->
        <template v-slot:header>
          <table-super-header :with-lineages='withLineages' :show-p-values='showPValues'/>
        </template>

        <!---- TABLE SELECT ALL OPT  -------------------------------------->
        <template v-slot:header.data-table-select>
          <v-tooltip :disabled="showSelectOptions" bottom nudge-bottom="-3" allow-overflow z-index="10"
                     max-width="400px" close-delay="0">
            <template v-slot:activator="{ on }">
              <div class="select-all-opt" v-on="on"  >
                <v-simple-checkbox  :value="selectedRows.length>0" ref="selectToggle"  @click.capture="manageSelectAll"
                                   :indeterminate="selectedRows.length>0 && !hasSelectedAll"/>
              </div>
              <v-menu v-model="showSelectOptions" :attach="$refs.selectToggle" offset-y min-width="fit-content">
                <v-list color="bg_var1" rounded dense width="auto">
                  <v-list-item link dense @click="selectAllRows">
                    <v-icon class="pr-3" color="primary">mdi-checkbox-marked</v-icon>
                    <v-list-item-content>
                      <v-list-item-title class="primary--text">Select all</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                  <v-list-item link dense @click="deselectAllRows">
                    <v-icon class="pr-3" color="primary">mdi-checkbox-blank-outline</v-icon>
                    <v-list-item-content>
                      <v-list-item-title class="primary--text">Clear selection</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-menu>
            </template>
            <span v-if="hasSelectedAll">Deselect all mutations</span>
            <span v-else-if="selectedRows.length===0">
              Select all {{ getCurrentFilteredRows.length }} mutations <br/>Previously selected rows will be cleared
            </span>
            <span v-else>
              Click to see select/deselect options
            </span>
          </v-tooltip>

        </template>

        <!---- TABLE EXPAND/INFO PANEL CONTROLS --------------------------->
        <template v-slot:item.data-table-expand="{expand,item,isExpanded}">
          <row-options :expandable="!withLineages" :item="item" :isExpanded="isExpanded" :expand="expand"/>
        </template>

        <!---- TABLE ROW SELECT CONTROL --------------------------->
        <template v-slot:item.data-table-select="{item}">
          <v-tooltip bottom content-class="rounded-xl tooltip" allow-overflow z-index="10" max-width="400px">
            <template v-slot:activator='{ on, attrs }'>
              <v-simple-checkbox :value="selectedRows.includes(item.item_key)" v-bind="attrs" v-on="on"
                                 @click="manageRowSelect(item.item_key)"/>
            </template>
            Select to view this mutation in the plots below
          </v-tooltip>
        </template>

        <!---- CUSTOMIZED CELLS ------------------------------------------->
        <!-- Mutation column -->
        <template v-if='withLineages' v-slot:item.mut='{ item }'>
          <div :class="isCharacterizingMut(item)? 'char-mut':''">{{ item.mut }}</div>
        </template>

        <!-- Slope column -->
        <template v-slot:item.slope='{ item }'>
          <div :class="(item.slope===0?'warning--text':(item.slope<=0?'error--text':'success--text'))">
            <v-icon :color="(item.slope===0?'warning':(item.slope<=0?'error':'success'))">
              {{ item.slope === 0 ? 'mdi-circle-small' : (item.slope < 0 ? 'mdi-menu-down' : 'mdi-menu-up') }}
            </v-icon>
            {{ item.slope.toPrecision(4).replace(/\.0+$/, '') }}
          </div>
        </template>

        <!-- PValueWithMut column -->
        <template v-if='showPValues' v-slot:item.p_value_with_mut='{ item }'>
          <div v-if="item.p_value_with_mut===-1">N / A</div>
          <div v-else>{{ item.p_value_with_mut.toExponential(3) }}</div>
        </template>

        <!-- PValueWithoutMut column -->
        <template v-if='showPValues' v-slot:item.p_value_without_mut='{ item }'>
          <div v-if="item.p_value_without_mut===-1">N / A</div>
          <div v-else>{{ item.p_value_without_mut.toExponential(3) }}</div>
        </template>

        <!-- PValueComp column -->
        <template v-if='showPValues' v-slot:item.p_value_comp='{ item }'>
          <div v-if="item.p_value_comp===-1">N / A</div>
          <div v-else>{{ item.p_value_comp.toExponential(3) }}</div>
        </template>

        <!-- W1 column -->
        <template v-slot:item.w1='{ item }'>
          <span>{{ (item.f1 === 0 ? 0 : item.f1.toPrecision(3)) + '% ' }}</span>
          <span class="text-body-4">{{ '(' + item.w1 + ')' }}</span>
        </template>

        <!-- W2 column -->
        <template v-slot:item.w2='{ item }'>
          <span>{{ (item.f2 === 0 ? 0 : item.f2.toPrecision(3)) + '% ' }}</span>
          <span class="text-body-4">{{ '(' + item.w2 + ')' }}</span>
        </template>

        <!-- W3 column -->
        <template v-slot:item.w3='{ item }'>
          <span>{{ (item.f3 === 0 ? 0 : item.f3.toPrecision(3)) + '% ' }}</span>
          <span class="text-body-4">{{ '(' + item.w3 + ')' }}</span>
        </template>

        <!-- W4 column -->
        <template v-slot:item.w4='{ item }'>
          <span>{{ (item.f4 === 0 ? 0 : item.f4.toPrecision(3)) + '% ' }}</span>
          <span class="text-body-4">{{ '(' + item.w4 + ')' }}</span>
        </template>

        <!---- EXPANDED TABLE ELEMENT ------------------------------------>
        <template v-if='!withLineages && !isLoadingDetails' v-slot:expanded-item='{ item }'>
          <td :colspan='4' class='expanded-item-title'>
            <expansion-mode-menu v-model="notationMode"/>
            <div class="row-name">Lineages</div>
          </td>
          <td class='expanded-td'>
            <v-simple-table>
              <tbody>
              <tr v-for='(lineage, lineage_index) in formatBreakdown' v-bind:key='lineage_index'>
                <td>{{ lineage.name }}</td>
              </tr>
              </tbody>
            </v-simple-table>
          </td>
          <td class='expanded-td' v-for='week in [1, 2, 3, 4]' v-bind:key='week'>
            <v-simple-table>
              <tbody>
              <tr v-for='(lineage, lineage_index) in formatBreakdown' v-bind:key='lineage_index'>
                <td>
                  <span>{{ (lineage['f' + week] === 0 ? 0 : lineage['f' + week].toPrecision(3)) + '% ' }}</span>
                  <span class="text-body-4">{{ '(' + lineage['w' + week] + ')' }}</span>
                </td>
              </tr>
              </tbody>
            </v-simple-table>
          </td>
        </template>
        <template v-else-if="isLoadingDetails" v-slot:expanded-item>
          <td colspan="9" class="py-5 text-center secondary--text font-weight-medium">
            <loading-sticker :standalone="true" :is-loading="true" no-overlay
                             :loading-messages="[{text:'Analyzing lineages data',time:3000},{text:'This may take some time',time:6000},{text:'Almost done! Hang in there',time:9000}]"/>
          </td>
        </template>

        <!-- TOT SEQ COUNTS --------------------------------------------->
        <template v-slot:body.append>
          <td colspan='5' class='table-append'/>
          <td v-for='week in [1,2,3,4]' v-bind:key='week' class='table-append text-body-4 text-center'>
            Tot. seq: {{ getCurrentAnalysis.totSeq['w' + week] }}
          </td>
        </template>

        <!-- GO TO COVSPECTURM  ----------------------------------------->
        <template v-slot:footer.prepend>
          <go-to-cov-spectrum/>
        </template>

        <template v-slot:no-data>
          <empty-table/>
        </template>

      </v-data-table>
    </v-col>
  </section-element>
</template>

<script>
import SectionElement from "@/components/analysis/SectionElement";
import TableControls from "@/components/analysis/table/TableControls";
import TableSuperHeader from "@/components/analysis/table/TableSuperHeader";
import ExpansionModeMenu from "@/components/menus/ExpansionModeMenu";
import {mapGetters, mapMutations} from "vuex";
import {compactLineagesData} from "@/utils/formatterService";
import {sortItems} from "@/utils/sorterService";
import GoToCovSpectrum from "@/components/analysis/table/GoToCovSpectrum";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import RowOptions from "@/components/analysis/table/RowOptions";
import EmptyTable from "@/components/analysis/table/EmptyTable";

export default {
  name: "ResultTable",
  components: {
    EmptyTable,
    RowOptions,
    LoadingSticker, GoToCovSpectrum, ExpansionModeMenu, TableSuperHeader, TableControls, SectionElement
  },
  props: {
    withLineages: Boolean,
  },
  data() {
    return {
      /** Array of keys of expanded rows (relevant for li only )*/
      expandedRows: [],

      showSelectOptions: false,

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
    }
  },
  computed: {
    ...mapGetters(['getCurrentAnalysis', 'getCurrentOpt', 'useLocalOpt',
      'getCurrentFilteredRows', 'getCurrentSelectedRows']),

    /** query: query value of the current analysis */
    query() {
      return this.getCurrentAnalysis.query
    },

    /** characterizingMuts: characterizing muts for the current analysis */
    characterizingMuts() {
      return this.withLineages ? this.getCurrentAnalysis.characterizingMuts : null
    },

    hasSelectedAll() {
      return this.selectedRows.length >= this.getCurrentFilteredRows.length &&
          this.getCurrentFilteredRows.every(({item_key}) => this.selectedRows.includes(item_key))
    },


    /** Array of selected rows */
    selectedRows: {
      set(newVal) {
        this.setOpt({local: this.useLocalOpt, opt: 'rowKeys', value: newVal})
      },
      get() {
        return this.getCurrentOpt.rowKeys
      }
    },

    /** Array of columns selected for sorting data */
    sortingIndexes: {
      set(newVal) {
        this.setOpt({local: this.useLocalOpt, opt: 'sortingIndexes', value: newVal})
      },
      get() {
        return this.getCurrentOpt.sortingIndexes
      }
    },

    /** Array defining asc(true)/desc(false) order for each column selected for sorting in sortingIndexes */
    isDescSorting: {
      set(newVal) {
        console.log("SET to " + newVal)
        this.setOpt({local: this.useLocalOpt, opt: 'isDescSorting', value: newVal})
      },
      get() {
        return this.getCurrentOpt.isDescSorting
      }
    },

    /** Array of objects describing header columns */
    tableHeaders() {
      const {w1, w2, w3, w4} = this.query.weeks
      let headers = [
        {text: 'Protein', value: 'protein', divider: true, align: 'center'},
        {text: 'Mut', value: 'mut', divider: true, align: 'center'},
        {text: 'Slope', value: 'slope', divider: true, align: 'center'},
        {text: w1, value: 'w1', divider: true, align: 'center'},
        {text: w2, value: 'w2', divider: true, align: 'center'},
        {text: w3, value: 'w3', divider: true, align: 'center'},
        {text: w4, value: 'w4', divider: true, align: 'center'}
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

    /**
     * Reformat breakdown data based on the notation mode selected. Either using full notation or star notation.
     */
    formatBreakdown() {
      if (this.expandedRows.length === 0) return []

      const lineagesData = this.expandedRows[0].lineages // lineages data in full notation
      return (this.notationMode === 0 || !lineagesData) ? lineagesData : compactLineagesData(lineagesData, this.notationMode)
    },

  },
  methods: {
    ...mapMutations(['setOpt']),

    manageRowSelect(rowKey) {
      console.log(rowKey)
      if (this.selectedRows.includes(rowKey)) {
        // deselect this row only  (keep all the others)
        this.selectedRows = this.selectedRows.filter(rk => rk !== rowKey)
      } else {
        //select this row only (keep all the others)
        this.selectedRows = [...this.selectedRows, rowKey]
      }
    },


    /**
     * Clear all the selected rows on deselect-all table event
     */
    manageSelectAll() {
      console.log("MANAGER ")
      const isIndeterminate = this.selectedRows.length > 0 && !this.hasSelectedAll
      if (isIndeterminate) {
        // Two viable options. Ask.
        this.showSelectOptions = true
      } else if (this.hasSelectedAll) {
        this.deselectAllRows()
      } else {
        this.selectAllRows()
      }
    },

    deselectAllRows() {
      console.log("DESELECT ALL")
      this.selectedRows = []  // clear selected rows
    },

    selectAllRows() {
      console.log("SELECT ALL")
      this.selectedRows = this.getCurrentFilteredRows.map(({item_key}) => item_key) // select all and only these mutations
    },

    /** Custom sorter mapping */
    customSort(items, sortingIndexes, isDescSorting) {
      return sortItems(items, sortingIndexes, isDescSorting)
    },

    /**
     * Fetch lineages data when a row of the table is expanded. Lineage independent search only.
     * @param item
     */
    loadLineageDetails(item) {
      // Catch row expansion only
      if (item.value) {
        this.error = undefined
        this.isLoadingDetails = true
        const url = `/lineage_independent/getLineagesStatistics`
        const queryParams = {
          location: this.query.location[this.query.granularity],
          date: this.query.endDate,
          prot: item.item.protein,
          mut: item.item.mut,
        }

        this.$axios
            .get(url, {params: queryParams})
            .then(({data}) => item.item.lineages = data)
            .catch((e) => this.error = e)
            .finally(() => this.isLoadingDetails = false)
      }
    },

    /**
     * Determines whether a mutation is characterizing the lineage or not
     * @param item   The item to be considered
     * @returns {boolean}   True iff the mutation is characterizing the lineage
     */
    isCharacterizingMut(item) {
      return this.getCurrentAnalysis.characterizingMuts.includes(item.item_key)
    },
  }
}
</script>

<style>

.table-container {
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
  color: var(--v-text_var1-base);
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
  color: var(--v-text_var1-base);
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
  background: var(--v-bg_var2-base) !important;
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

/** Fix wrong placement of toggle all */
.select-all-opt i::before {
  margin-bottom: auto;
}
</style>
