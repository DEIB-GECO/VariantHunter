<!--

  Component:    ResultNavbar
  Description:  Results section toolbar containing options to adjust analysis parameters
                and other options

  Events:
  ├── shiftPeriod:  Emitted on period shift together with the delay
  ├── shiftType:    Emitted on type switch from ls to li
  └── shiftArea:    Emitted on location switch together with the new location data (id and text)

-->

<template>
  <v-app-bar dense hide-on-scroll scroll-threshold="50" app flat fixed class="result-bar primary--text" color="bg_var1">

    <!-- Current analysis parameters -->
    <v-toolbar-title class="text-body-1 font-weight-black compact-text-2 primary--text">
      {{
        query.location[query.granularity].text + " / " +
        query.endDate +
        (query.lineage ? " / " + lineagesToText(query.lineage) : "")
      }}
    </v-toolbar-title>

    <v-spacer/>

    <!-- Week slider option -->
    <result-navbar-week-slider @shiftPeriod="d => $emit('shiftPeriod',d)"/>

    <!-- Location switcher option -->
    <result-navbar-location-switcher @shiftArea="a => $emit('shiftArea',a)"/>

    <!-- Analysis type switcher option -->
    <icon-with-tooltip v-if="query.lineage" hover-color="warning" icon="mdi-source-branch-minus"
                       tip="Switch to lineage independent analysis" bottom :delay="0"
                       :click-handler="()=>$emit('shiftType')" color="primary"/>

    <!-- Mark as favourite option -->
    <icon-with-tooltip v-if="isStarred" color="#C2AD07" hover-color="primary" icon="mdi-star"
                       tip="Mark as not relevant" bottom
                       :click-handler="()=>setStarredAnalysis({id:currentAnalysisId,starred:false})"/>
    <icon-with-tooltip v-else hover-color="#C2AD07" color="primary" icon="mdi-star-outline" tip="Mark as relevant"
                       bottom :click-handler="()=>setStarredAnalysis({id:currentAnalysisId,starred:true})"/>

    <!-- Remove analysis option -->
    <icon-with-tooltip hover-color="error" icon="mdi-trash-can-outline" tip="Delete analysis" bottom
                       :click-handler="()=>removeAnalysis(currentAnalysisId)" color="primary"/>

    <!-- Other result navbar options under 3 dots -->
    <result-navbar-menu/>

  </v-app-bar>
</template>

<script>
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import {mapGetters, mapMutations, mapState} from "vuex";
import ResultNavbarMenu from "@/components/analysis/navbar/ResultNavbarMenu";
import ResultNavbarWeekSlider from "@/components/analysis/navbar/ResultNavbarWeekSlider";
import ResultNavbarLocationSwitcher from "@/components/analysis/navbar/ResultNavbarLocationSwitcher";
import {toText} from "@/utils/formatterService";

export default {
  name: "ResultNavbar",
  components: {ResultNavbarLocationSwitcher, ResultNavbarWeekSlider, ResultNavbarMenu, IconWithTooltip},

  computed: {
    ...mapState(['currentAnalysisId']),
    ...mapGetters(['getCurrentAnalysis']),

    /** Flag set to true if current analysis is in favorites */
    isStarred() {
      return this.getCurrentAnalysis.starred
    },

    /** Shortcut to query params */
    query() {
      return this.getCurrentAnalysis.query
    },
  },

  methods: {
    ...mapMutations(['removeAnalysis', 'setStarredAnalysis']),

    /** Mapping lineage toText */
    lineagesToText(arg) {
      return toText(arg)
    },
  }
}
</script>

<style scoped>
.result-bar {
  border-radius: 4px 0 !important;
  margin-top: 56px !important;
  margin-left: 56px !important;
}
</style>
<style>
.result-bar .v-toolbar__content {
  border-bottom: 2px solid var(--v-primary-base) !important;
}
</style>