<template>
  <section-element icon='mdi-table-multiple' title="Mutations table">
    <v-col cols="12" class="pa-0 table-container">
      <v-data-table v-model='selectedRows' :headers='tableHeaders' :custom-sort="customSort" col
                    :items='getCurrentFilteredRows' :sort-by.sync='sortingIndexes' :sort-desc.sync='isDescSorting'
                    :footer-props='footerProps' :loading='isLoadingDetails' single-expand class='table-element'
                    item-key='item_key'
                    :expanded.sync='expandedRows' multi-sort show-select mobile-breakpoint='0'
                    @item-expanded='loadLineageDetails' show-expand
                    @toggle-select-all='handleToggleSelection'>

        <!---- TABLE CONTROLS --------------------------------------------->
        <template v-slot:top>
          <table-controls @showPValues='(flag) => showPValues=flag'/>
        </template>

        <!---- TABLE SUPER HEADERS ---------------------------------------->
        <template v-slot:header>
          <table-super-header :with-lineages='withLineages' :show-p-values='showPValues'/>
        </template>

        <!---- TABLE EXPAND/INFO PANEL CONTROLS --------------------------->
        <template v-slot:item.data-table-expand="{expand,item,isExpanded}">
          <row-options :expandable="!withLineages" :item="item" :isExpanded="isExpanded" :expand="expand"/>
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
            <expansion-mode-menu @changeNotationMode="e=>notationMode=e"/>
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
                  <span>{{ (item['f' + week] === 0 ? 0 : item['f' + week].toPrecision(3)) + '% ' }}</span>
                  <span class="text-body-4">{{ '(' + item['w' + week] + ')' }}</span>
                </td>
              </tr>
              </tbody>
            </v-simple-table>
          </td>
        </template>
        <template v-else-if="isLoadingDetails" v-slot:expanded-item>
          <td colspan="9" class="py-5 text-center secondary--text font-weight-medium">
            <loading-sticker :standalone="true" :is-loading="true"
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
import TableControls from "@/components/analysis/tables/TableControls";
import TableSuperHeader from "@/components/analysis/tables/TableSuperHeader";
import ExpansionModeMenu from "@/components/menus/ExpansionModeMenu";
import {mapGetters, mapMutations, mapState} from "vuex";
import axios from "axios";
import {compactLineagesData} from "@/utils/formatterService";
import {sortItems} from "@/utils/sorterService";
import GoToCovSpectrum from "@/components/analysis/tables/GoToCovSpectrum";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import RowOptions from "@/components/analysis/tables/RowOptions";
import EmptyTable from "@/components/analysis/tables/EmptyTable";

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
      /** Array of expanded rows (relevant for li only )*/
      expandedRows: [],

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
    ...mapState(['globalFilteringOpt', 'globalOrderingOpt']),
    ...mapGetters(['getCurrentAnalysis', 'getCurrentLocalFilteringOpt', 'getCurrentLocalOrderingOpt',
      'getCurrentFilteredRows', 'getCurrentSelectedRows']),

    /** query: query value of the current analysis */
    query() {
      return this.getCurrentAnalysis.query
    },

    /** characterizingMuts: characterizing muts for the current analysis */
    characterizingMuts() {
      return this.withLineages ? this.getCurrentAnalysis.characterizingMuts : null
    },

    /** useGlobalFilters: flag for global filter for the current analysis */
    useGlobalFilters() {
      return this.getCurrentLocalFilteringOpt.useGlobalFilters
    },

    /** filteringOpt: filtering options for the current analysis (either global or local based on preference) */
    filteringOpt() {
      return this.useGlobalFilters ? this.globalFilteringOpt : this.getCurrentLocalFilteringOpt
    },

    /** orderingOpt: ordering options for the current analysis (either global or local based on preference) */
    orderingOpt() {
      return this.useGlobalFilters ? this.globalOrderingOpt : this.getCurrentLocalOrderingOpt
    },

    /** Array of selected rows */
    selectedRows: {
      set(newVal) {
        const keys = newVal.map(({item_key}) => item_key)
        this.setFilterOpt({global: this.useGlobalFilters, opt: 'rowKeys', value: keys})
      },
      get() {
        return this.getCurrentSelectedRows
      }
    },

    /** Array of columns selected for sorting data */
    sortingIndexes: {
      set(newVal) {
        this.setOrderOpt({global: this.useGlobalFilters, opt: 'sortingIndexes', value: newVal})
      },
      get() {
        return this.orderingOpt.sortingIndexes
      }
    },

    /** Array defining asc(true)/desc(false) order for each column selected for sorting in sortingIndexes */
    isDescSorting: {
      set(newVal) {
        this.setOrderOpt({global: this.useGlobalFilters, opt: 'isDescSorting', value: newVal})
      },
      get() {
        return this.orderingOpt.isDescSorting
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
    }

  },
  methods: {
    ...mapMutations(['setFilterOpt', 'setOrderOpt']),

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

        axios
            .get(url, {params: queryParams})
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
    formatBreakdown(lineagesData) {
      return (this.notationMode === 0 || !lineagesData) ? lineagesData : compactLineagesData(lineagesData, this.notationMode)
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
</style>
