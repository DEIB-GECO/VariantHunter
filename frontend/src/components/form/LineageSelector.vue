<!--

  Component:    LineageSelector
  Description:  Select input element for lineage

-->

<template>
  <v-col>

    <!-- Headings -->
    <v-row class="px-5 pb-2">
      <v-col>
        <span class="text-body-3 compact-text-3 primary--text d-block">
          <span class="compact-text-5 font-weight-black">Lineages</span>:
          select the lineages you want to analyze.
        </span>
      </v-col>
    </v-row>

    <!-- Input element -->
    <v-row dense class="px-5">
      <v-col @keypress.delete.stop="()=>{}" @keydown.delete.stop="()=>{}" @keyup.delete.stop="()=>{}">
        <v-autocomplete :value='getSelectedLineageValues' :items='possibleLineages' :disabled="!selectedLocation"
                        multiple
                        :loading='isLoading' placeholder='Select a lineage from the list' persistent-hint flat
                        :hint="(!selectedLocation)?'You must select at least a location first':'You can select one or more specific lineages, or select entire lineage trees like BA.1.*'"
                        :hide-details="selectedLocation!==null && selectedLineage.count>1" attach solo
                        :search-input.sync="searchQuery"
                        persistent-placeholder clearable clear-icon="mdi-backspace-outline"
                        :class="'lineage-selector '+((!selectedLocation)?'warning--text cursor-forbidden':'')"
                        @click:clear="clearLineages">
          <!-- Hide current selection -->
          <template v-slot:selection="{index}"></template>

          <!-- Current selection as prepend -->
          <template v-slot:prepend-inner>
            <div v-if="getSelectedLineageValues.length>0">
              <div class="d-flex width-100 mt-3 flex-wrap flex-row">
                <v-chip v-for="el in getSelectedLineage" small :key="el" class="ma-0 mr-1 mb-1">{{ el }}
                  <v-icon x-small right class="cursor-pointer" @click="removeLineage(el)">mdi-close</v-icon>
                </v-chip>
              </div>
            </div>
          </template>

          <template v-slot:no-data>
            <div class="pa-5 py-4">Lineage not found</div>
          </template>

          <!-- Hint about lineages list -->
          <template v-slot:prepend-item>
            <slot name='prepend-item'>
              <div class='hint'>{{ hint }}</div>
            </slot>
          </template>

          <!-- Item element -->
          <template v-slot:item="{item}">
            <div class="lineage-item width-100" @click.stop="onLineageItemClick(item)">
              <span class="font-weight-bold">
                {{ item }}
              </span>
              <v-spacer/>
              <div class="text-right py-1">
                <span v-if="(item.match(/\./g)|| []).length<3">
                  <btn-with-tooltip icon="mdi-arrow-top-right" :text="'Select as '+ item+'.*' " outlined
                                    :tip="'Select '+item+' and all its sub-lineages '" bottom color="#4caf50"
                                    content-class="hidden-xs-only" size="x-small"
                                    :click-handler="()=>onLineageSetClick(item)"/>
                <icon-with-tooltip icon="mdi-arrow-top-right" content-class="hidden-sm-and-up"
                                   :tip="'Select this and all its sub-lineages as '+ item+'.*'" bottom color="#4caf50"
                                   size="small" :click-handler="()=>onLineageSetClick(item)"/>
                </span>
                <!-- Sample count -->
                <div v-if="possibleLineagesInfo" class="mt-1 hidden-xs-only d-inline d-sm-block ">
                  <btn-with-tooltip outlined bottom color="text_var1" size="x-small"
                                    :text="possibleLineagesInfo[item] + ' sample' + (possibleLineagesInfo[item] > 1 ? 's' : '')"
                                    :tip="'Number of sequences associated with '+item+' available in the selected location and period'"/>
                </div>
              </div>
            </div>
          </template>

        </v-autocomplete>
      </v-col>
    </v-row>

    <loading-sticker :error="error"/>

  </v-col>
</template>

<script>
import {mapGetters, mapMutations, mapState} from 'vuex'
import {mapStateTwoWay} from '@/utils/bindService'
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip.vue";
import {extractLineages} from "@/utils/formatterService";
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip.vue";

export default {
  name: 'LineageSelector',
  components: {BtnWithTooltip, IconWithTooltip, LoadingSticker},

  data() {
    return {
      /** Current search query */
      searchQuery: undefined,

      /** Boolean loading flag for the table and expansion */
      isLoading: false,

      /** Error data for the table and expansion. Undefined if no error. */
      error: undefined,
    }
  },

  computed: {
    ...mapState(['selectedLocation', 'selectedDate', 'selectedLineage']),
    ...mapGetters(['getSelectedLineageValues', 'getSelectedLineage']),
    ...mapStateTwoWay({possibleLineages: 'setLineages', possibleLineagesInfo: 'setLineagesInfo'}),

    /** Hint for the selector  */
    hint() {
      return (this.selectedLocation)
          ? 'Lineages in ' + this.selectedLocation.text + (this.selectedDate ? ' for the selected analysis period:' : ':')
          : 'All available lineages:'
    }
  },

  methods: {
    ...mapMutations(['setLineage']),

    /**
     * Manager for lineage item (simple) select
     * @param lineage   Name of the lineage item
     */
    onLineageItemClick(lineage) {
      const lineageObj = structuredClone(this.selectedLineage)

      // If already selected as single element, remove
      const index = lineageObj.items.indexOf(lineage)
      if (index > -1) {
        lineageObj.items.splice(index, 1)
      } else {
        // If already selected inside some groups, convert group into items and remove
        const group = Object.entries(lineageObj.groups).find(([, gContent]) => gContent.indexOf(lineage) > -1)
        if (group) {
          const gName = group[0]
          lineageObj.items.push(...lineageObj.groups[gName].filter(name => name !== lineage))
          delete lineageObj.groups[gName]
        } else {
          // Not already selected: add as single item
          lineageObj.items.push(lineage)
        }
      }

      this.setLineage(lineageObj) // actually update the value
      this.searchQuery = ''
    },

    /**
     * Manager for lineage group select
     * @param lineageSet  Name of the parent lineage selected
     */
    onLineageSetClick(lineageSet) {
      const lineageObj = structuredClone(this.selectedLineage)

      // Compute lineages to be selected
      const lineagesToAdd = extractLineages(this.possibleLineages, lineageSet)

      // Manage conflicts
      lineagesToAdd.forEach(lta => {
        // If already selected as single element, remove
        const index = lineageObj.items.indexOf(lta)
        if (index > -1) {
          lineageObj.items.splice(index, 1)
        } else {
          // If already selected inside some groups, remove group
          const group = Object.entries(lineageObj.groups).find(([, gContent]) => gContent.indexOf(lta) > -1)
          if (group) {
            delete lineageObj.groups[group[0]]
          }
        }
      })

      lineageObj.groups[lineageSet + '.*'] = lineagesToAdd
      this.setLineage(lineageObj) // actually update the value
      this.searchQuery = ''
    },

    /**
     * Remove a lineage
     * @param element Element to be removed. Either specific lineage or lineage group
     */
    removeLineage(element) {
      const lineageObj = structuredClone(this.selectedLineage)
      if (element.at(-1) === '*') {
        // deselect group
        delete lineageObj.groups[element]
      } else {
        // deselect item
        const index = lineageObj.items.indexOf(element)
        if (index > -1) {
          lineageObj.items.splice(index, 1)
        }
      }
      this.setLineage(lineageObj) // actually update the value
    },

    /** Clear lineage selection */
    clearLineages() {
      this.setLineage({'groups': {}, 'items': []})
    },

    /** Fetch all possible values for lineages (given the other params) */
    getPossibleLineages() {
      if (this.selectedLocation !== null) {
        this.isLoading = true
        this.error = undefined

        const url = `/lineage_specific/getLineages`
        const queryParams = {
          location: this.selectedLocation.id,
          date: this.selectedDate ? this.selectedDate[1] : undefined
        }

        this.$axios
            .get(url, {params: queryParams})
            .then(({data}) => {
              this.possibleLineages = data['possible_lineages']
              this.possibleLineagesInfo = data['availability']

              // Keep selected lineage if included in the possible ones.
              // Discard in any case if * notation is in use
               if ((this.selectedLineage.count > 1) ||
                   (this.selectedLineage.count === 1 && !this.possibleLineages.includes(this.selectedLineage.items[0]))) {
                 this.clearLineages()
               }
            })

            .catch((e) => {
              this.error = e
              this.possibleLineages = []
              this.possibleLineagesInfo = null
              this.clearLineages()
            })
            .finally(() => {
              this.isLoading = false
            })
      } else {
        this.possibleLineages = []
        this.possibleLineagesInfo = null
      }
    }
  },

  watch: {
    /** Adjust the possible lineages according to the selected location */
    selectedLocation() {
      this.getPossibleLineages()
    }
    ,

    /** Adjust the possible lineages according to the selected date */
    selectedDate() {
      this.getPossibleLineages()
    }
  }
  ,

  /** Get possible lineages */
  mounted() {
    this.getPossibleLineages()
  }
}
</script>

<style scoped>
/* Hint */
.hint {
  color: var(--v-text_var1-base);
  text-align: center;
  padding: 10px 14px;
  line-height: 17px;
  line-break: loose;
  text-transform: initial !important;
}

/* Lineage select item */
.lineage-item {
  display: flex;
  align-content: center;
  align-items: center;
  justify-content: center;
  padding: 6px 22px;
}
</style>

<style>
/* Lineage selector styling: remove padding to disable internal selection mechanism*/
.lineage-selector .v-list-item {
  padding: 0 !important;
}

/** Display for prepend slot chips*/
.lineage-selector .v-input__prepend-inner {
  color: var(--v-text_var1-base);
  display: flex !important;
}

/** Move prepend slot above */
.lineage-selector .v-input__slot {
  flex-wrap: wrap !important;
}
</style>
