<template>
  <div class="filter-area">
    <div id="filtering-area" class="text-body-3 mb-2">
      <chip-menu attach="#filtering-area" :close-on-content-click="false" small activator-icon="mdi-filter" activator-text="Filter by"
                 :color="(isFiltering?'f_secondary':'f_tertiary')" :activator-outlined="!isFiltering" :closable="isFiltering"
                 :activator-close-action="clearFilters">
        <div id="filtering-menu" class="text-body-4 pb-2 text-center f_text_dark--text">
          <v-icon small left>mdi-eye</v-icon>
          Showing:
        </div>
        <!-- Filtering options -->
        <v-row class="pb-2" no-gutters>
          <v-col>
            <!-- Analysis mode filtering -->
            <chip-menu attach="#filtering-area" color="#bc7fbf" small activator-icon="mdi-shape"
                       :activator-text="filteredMode?modeOptions[filteredMode]:modeOptions['null']"
                       :activator-outlined="!filteredMode" hide-on-leave>
              <v-list color="transparent">
                <v-list-item link v-for="([value, title], index) in Object.entries(modeOptions)" :key="index">
                  <v-list-item-title @click="filteredMode=(value==='null'?null:value)">{{ title }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </chip-menu>
          </v-col>
        </v-row>
        <v-row class="pb-2" no-gutters>
          <v-col>
            <!-- Analysis granularity filtering -->
            <chip-menu attach="#filtering-area" absolute color="#ff6e3e" small activator-icon="mdi-map-outline"
                       :activator-text="filteredGranularity?granularityOptions[filteredGranularity]:granularityOptions['null']"
                       :activator-outlined="!filteredGranularity" hide-on-leave>
              <v-list color="transparent">
                <v-list-item link v-for="([value, title], index) in Object.entries(granularityOptions)" :key="index">
                  <v-list-item-title @click="filteredGranularity=(value==='null'?null:value)">
                    {{ title }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </chip-menu>
          </v-col>
        </v-row>
        <v-row class="pb-2" no-gutters>
          <v-col>
            <!-- Starred analysis filtering -->
            <chip-menu attach="#filtering-area" absolute color="#C2AD07" small activator-icon="mdi-star"
                       :activator-text="filteredStarred?starredOptions[filteredStarred]:starredOptions['null']"
                       :activator-outlined="!filteredStarred" hide-on-leave>
              <v-list color="transparent">
                <v-list-item link v-for="([value, title], index) in Object.entries(starredOptions)" :key="index">
                  <v-list-item-title @click="filteredStarred=(value==='null'?null:value)">
                    {{ title }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </chip-menu>
          </v-col>
        </v-row>
        <v-row class="pt-3 text-center" v-if="isFiltering" no-gutters>
          <v-col>
            <!-- Clear filtering -->
            <v-chip small color="error" outlined class="text-uppercase" @click="clearFilters()">
              <v-icon left small>mdi-close-thick</v-icon>
              Clear filters
            </v-chip>
          </v-col>
        </v-row>
      </chip-menu>
      <icon-with-tooltip v-if="isFiltering" bottom size="small" class="ml-1" icon="mdi-close" tip="Clear filters"
                         :click-handler="clearFilters"></icon-with-tooltip>
    </div>

    <!-- Actual filtered history-->
    <v-list-item v-for="{id, starred, query} in getAnalysesSummary(filters)" :key="id" link
                 @click="elementClickHandler(id)" :class="'pl-7 '+(currentAnalysisId===id?'v-list-item--active':'')">

      <v-list-item-content>
        <v-list-item-title class="text-body-3 font-weight-medium">
          {{
            query.location[query.granularity] + " / " +
            query.endDate +
            (query.lineage ? " / " + query.lineage : "")
          }}
        </v-list-item-title>

        <!-- Analysis categories -->
        <v-list-item-subtitle class="break-spaces pt-1">
          <v-chip x-small color="#ff6e3e" class="text-uppercase mr-1 mb-1 text-body-5">
            {{ query.granularity }}
          </v-chip>
          <v-chip x-small color="#bc7fbf" class="text-uppercase mb-1 text-body-5">
            {{ query.lineage ? "lineage-specific" : "lineage-independent" }}
          </v-chip>
        </v-list-item-subtitle>
      </v-list-item-content>

      <!-- Analysis actions -->
      <v-list-item-action class="pr-4 d-block">
        <icon-with-tooltip hover-color="error" icon="mdi-close" size="medium" tip="Delete analysis" bottom
                           :click-handler="()=>removeAnalysis(id)"/>
        <icon-with-tooltip v-if="starred" color="#C2AD07" hover-color="white" icon="mdi-star" size="medium"
                           tip="Mark as not relevant" bottom
                           :click-handler="()=>setStarredAnalysis({id,starred:false})"/>
        <icon-with-tooltip v-else hover-color="#C2AD07" icon="mdi-star-outline" size="medium" tip="Mark as relevant"
                           bottom :click-handler="()=>setStarredAnalysis({id,starred:true})"/>
      </v-list-item-action>
    </v-list-item>
    <div class="filter-area text-body-4 pt-2" v-if="getAnalysesSummary(filters).length<1">No recent analysis yet</div>

  </div>
</template>

<script>
import {mapGetters, mapMutations, mapState} from "vuex";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import ChipMenu from "@/components/general/basic/ChipMenu";

export default {
  name: "SearchHistory",
  components: {ChipMenu, IconWithTooltip},
  data() {
    return {
      filteredMode: null,
      modeOptions: {null: 'All analysis types', ls: 'Lineage specific only', li: 'Lineage independent only'},

      filteredGranularity: null,
      granularityOptions: {
        null: ' All granularities',
        continent: 'Continent only',
        country: 'Country only',
        region: 'Region only'
      },

      filteredStarred: null,
      starredOptions: {null: 'Both starred and not', starred: 'Starred only'},
    }
  },
  computed: {
    ...mapState(['currentAnalysisId']),
    ...mapGetters(['getAnalysesSummary']),

    filters() {
      return {mode: this.filteredMode, granularity: this.filteredGranularity, starred: this.filteredStarred}
    },

    isFiltering() {
      return this.filteredMode !== null || this.filteredStarred !== null || this.filteredGranularity !== null
    }
  },
  methods: {
    ...mapMutations(["setCurrentAnalysis", "setStarredAnalysis", "removeAnalysis"]),

    clearFilters() {
      this.filteredMode = null
      this.filteredStarred = null
      this.filteredGranularity = null
    },

    elementClickHandler(id){
      this.setCurrentAnalysis(id)
      this.$emit('select',id)
    }
  }
}
</script>

<style scoped>
.filter-area {
  margin-left: 60px;
}

.break-spaces {
  white-space: break-spaces;
}

</style>