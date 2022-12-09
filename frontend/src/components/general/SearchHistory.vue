<!--

  Component:    SearchHistory
  Description:  Search history list

-->

<template>
  <div class="filter-area">

    <!-- Filtering options container -------------------------------------------->
    <div id="filtering-area" class="text-body-3 mb-2 d-flex text-center">
      <chip-menu attach="#filtering-area" :close-on-content-click="false" small activator-icon="mdi-filter"
                 :activator-text="(isFiltering?'Filtering by':'Filter by')"
                 :color="(isFiltering?'f_secondary':'f_tertiary')" :activator-outlined="!isFiltering"
                 :closable="isFiltering" :activator-close-action="clearFilters">
        <div id="filtering-menu" class="text-body-4 pb-2 text-center f_text_dark--text">
          <v-icon small left color="f_text_dark">mdi-eye</v-icon>
          Showing:
        </div>

        <!-- Analysis mode filtering -->
        <v-row class="pb-2" no-gutters>
          <v-col>
            <chip-menu attach="#filtering-area" color="#bc7fbf" small activator-icon="mdi-shape"
                       :activator-text="filteredMode?modeOptions[filteredMode]:modeOptions['null']"
                       :activator-outlined="!filteredMode" hide-on-leave>
              <v-list color="transparent" light>
                <v-list-item link v-for="([value, title], index) in Object.entries(modeOptions)" :key="index">
                  <v-list-item-title @click="filteredMode=(value==='null'?null:value)">{{ title }}</v-list-item-title>
                </v-list-item>
              </v-list>
            </chip-menu>
          </v-col>
        </v-row>

        <!-- Analysis granularity filtering -->
        <v-row class="pb-2" no-gutters>
          <v-col>
            <chip-menu attach="#filtering-area" absolute color="#ff6e3e" small activator-icon="mdi-map-outline"
                       :activator-text="filteredGranularity?granularityOptions[filteredGranularity]:granularityOptions['null']"
                       :activator-outlined="!filteredGranularity" hide-on-leave class="rounded-xl">
              <v-list color="transparent" light>
                <v-list-item link v-for="([value, title], index) in Object.entries(granularityOptions)" :key="index">
                  <v-list-item-title @click="filteredGranularity=(value==='null'?null:value)">
                    {{ title }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </chip-menu>
          </v-col>
        </v-row>

        <!-- Starred analysis filtering -->
        <v-row class="pb-2" no-gutters>
          <v-col>
            <chip-menu attach="#filtering-area" absolute color="#C2AD07" small activator-icon="mdi-star"
                       :activator-text="filteredStarred?starredOptions[filteredStarred]:starredOptions['null']"
                       :activator-outlined="!filteredStarred" hide-on-leave>
              <v-list color="transparent" light class="rounded-xl">
                <v-list-item link v-for="([value, title], index) in Object.entries(starredOptions)" :key="index">
                  <v-list-item-title @click="filteredStarred=(value==='null'?null:value)">
                    {{ title }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </chip-menu>
          </v-col>
        </v-row>

        <!-- Tag analysis filtering -->
        <v-row class="pb-2" no-gutters>
          <v-col>
            <chip-menu attach="#filtering-area" absolute color="#4252d9" small activator-icon="mdi-tag"
                       :activator-text="filteredTag?tagOptions[filteredTag]:tagOptions['null']"
                       :activator-outlined="!filteredTag" hide-on-leave>
              <v-list color="transparent" light>
                <v-list-item link v-for="([value, title], index) in Object.entries(tagOptions)" :key="index">
                  <v-list-item-title @click="filteredTag=(value==='null'?null:value)">
                    {{ title }}
                  </v-list-item-title>
                </v-list-item>
              </v-list>
            </chip-menu>
          </v-col>
        </v-row>

        <!-- Clear filtering -->
        <v-row class="pt-3 text-center" v-if="isFiltering" no-gutters>
          <v-col>
            <v-chip small color="error" outlined class="text-uppercase" @click="clearFilters()">
              <v-icon left small>mdi-close-thick</v-icon>
              Clear filters
            </v-chip>
          </v-col>
        </v-row>

      </chip-menu>

      <!-- Additional filtering options-->
      <icon-with-tooltip v-if="isFiltering" bottom size="small" class="ml-1 mr-2" icon="mdi-close" tip="Clear filters"
                         :click-handler="clearFilters"/>
      <v-spacer/>
      <data-manager mode="icon" class="mr-2"/>
    </div>

    <!-- Actual filtered history ----------------------------------------------->
    <div v-for="[date,analysesGroup] in groupedAnalysesSummary" :key="date">
      <!-- Group date -->
      <div class="text-body-5 f_tertiary--text text-uppercase text-right mr-4 mb-1 mt-2">
        {{ date === today ? 'Today' : date === yesterday ? 'Yesterday' : date.slice(0, 6) }}
      </div>

      <!-- List of elements -->
      <v-list-item v-for="{id, starred, query, tag} in analysesGroup" :key="id" link
                   @click="elementClickHandler(id)" :class="'pl-7 '+(currentAnalysisId===id?'v-list-item--active':'')">

        <!-- Params -->
        <v-list-item-content>
          <v-list-item-title class="text-body-3 font-weight-medium break-spaces">{{
              query.location[query.granularity].text + " / " +
              query.endDate +
              (query.lineage ? " / " + lineagesToText(query.lineage) : "")
            }}
          </v-list-item-title>

          <!-- Analysis categories -->
          <v-list-item-subtitle class="break-spaces pt-1">
            <v-chip x-small :color="getLocationColor(query.granularity)" class="text-uppercase mr-1 mb-1 text-body-5">
              {{ query.granularity }}
            </v-chip>
            <v-chip x-small :color="query.lineage?'#1f2215':'#3398DC'" class="text-uppercase mr-1 mb-1 text-body-5">
              {{ query.lineage ? "lineage-specific" : "lineage-independent" }}
            </v-chip>
            <v-chip v-if="tag" x-small :color="tags[tag]?.tagColor.color" :light="!tags[tag]?.tagColor.isDark"
                    :dark="tags[tag]?.tagColor.isDark" class="text-uppercase mb-1 text-body-5">
              {{ tag }}
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
    </div>

    <div class="filter-area text-body-4 pt-2" v-if="filteredAnalysesSummary.length<1">No recent analyses yet</div>

    <keyboard-shortcuts :filtered-analyses="filteredAnalysesSummary.map(({id})=>id)"/>

  </div>
</template>

<script>
import {mapGetters, mapMutations, mapState} from "vuex";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import ChipMenu from "@/components/general/basic/ChipMenu";
import KeyboardShortcuts from "@/components/controls/KeyboardShortcuts";
import DataManager from "@/components/controls/DataManager";
import {toText} from "@/utils/formatterService";

export default {
  name: "SearchHistory",
  components: {DataManager, KeyboardShortcuts, ChipMenu, IconWithTooltip},

  data() {
    return {
      /** Today date */
      today: undefined,
      /** Yesterday date */
      yesterday: undefined,

      /** Filtered mode */
      filteredMode: null,
      /** Filtered mode options */
      modeOptions: {null: 'All analysis types', ls: 'Lineage specific only', li: 'Lineage independent only'},

      /** Filtered granularity */
      filteredGranularity: null,
      /** Filtered granularity options */
      granularityOptions: {
        null: ' All granularities',
        continent: 'Continent only',
        country: 'Country only',
        region: 'Region only'
      },

      /** Filtered starred */
      filteredStarred: null,
      /** Filtered starred options */
      starredOptions: {null: 'Both starred and not', starred: 'Starred only'},

      /** Filtered tag */
      filteredTag: null,
    }
  },

  computed: {
    ...mapState(['currentAnalysisId', 'tags']),
    ...mapGetters(['getAnalysesSummary']),

    /** Filtered tag otpions */
    tagOptions() {
      const opts = {null: 'All tags'}
      Object.keys(this.tags).forEach(tag => opts[tag] = tag)
      return opts
    },

    /** Flag set to true iff filters are in use */
    isFiltering() {
      return this.filteredMode !== null || this.filteredStarred !== null ||
          this.filteredGranularity !== null || this.filteredTag !== null
    },

    /** Summary of analysis filtered */
    filteredAnalysesSummary() {
      const mode = this.filteredMode
      const granularity = this.filteredGranularity
      const starred = this.filteredStarred
      const tag = this.filteredTag

      let analyses = this.getAnalysesSummary

      // Apply filtering parameters
      if (tag)
        analyses = analyses.filter(({tag: aTag}) => tag === aTag)
      if (starred)
        analyses = analyses.filter(({starred}) => starred)
      if (mode)
        analyses = analyses.filter(({query}) => (mode === 'li' && !query.lineage) || (mode === 'ls' && query.lineage))
      if (granularity)
        analyses = analyses.filter(({query}) => granularity === query.granularity)

      return analyses
    },

    /** Summary of analysis grouped by date */
    groupedAnalysesSummary() {
      const groups = {}
      this.filteredAnalysesSummary.forEach(data => {
        const date = data.query.performedOn.slice(4, 15)

        if (!groups[date])
          groups[date] = [data]
        else
          groups[date].push(data)
      })
      return Object.entries(groups)
    },
  },

  methods: {
    ...mapMutations(["setCurrentAnalysis", "setStarredAnalysis", "removeAnalysis"]),

    /** Mapping lineage toText */
    lineagesToText(arg) {
      return toText(arg)
    },

    /** Clear all filters */
    clearFilters() {
      this.filteredMode = null
      this.filteredStarred = null
      this.filteredGranularity = null
    },

    /**
     * Switcher
     * @param id Analysis id
     */
    elementClickHandler(id) {
      this.setCurrentAnalysis(id)
    },

    /**
     * Get location color based on granularity
     * @param granularity Granularity value
     * @returns {string}  Color code
     */
    getLocationColor(granularity) {
      return granularity === 'region'
          ? '#7CB17B'
          : granularity === 'country'
              ? '#ff6e3e'
              : '#90177d'
    }
  },

  /** On mounted gets dates */
  mounted() {
    this.today = new Date().toDateString().slice(4, 15)
    this.yesterday = new Date(Date.now() - 86400000).toDateString().slice(4, 15)
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