<template>
  <v-app-bar dense hide-on-scroll scroll-threshold="50" app flat fixed class="result-bar primary--text" color="bg_var1">
    <v-toolbar-title class="text-body-1 font-weight-black compact-text-2 primary--text">
      {{
        query.location[query.granularity].text + " / " +
        query.endDate +
        (query.lineage ? " / " + query.lineage : "")
      }}
    </v-toolbar-title>

    <v-spacer/>
    <result-navbar-week-slider @shiftPeriod="d => $emit('shiftPeriod',d)"/>

    <result-navbar-location-switcher @shiftArea="a => $emit('shiftArea',a)"/>

    <icon-with-tooltip v-if="query.lineage" hover-color="warning" icon="mdi-source-branch-minus" tip="Switch to lineage independent analysis"  bottom
                       :click-handler="()=>$emit('shiftType')" color="primary"/>

    <icon-with-tooltip v-if="isStarred" color="#C2AD07" hover-color="primary" icon="mdi-star"
                       tip="Mark as not relevant" bottom
                       :click-handler="()=>setStarredAnalysis({id:currentAnalysisId,starred:false})" />
    <icon-with-tooltip v-else hover-color="#C2AD07" color="primary" icon="mdi-star-outline" tip="Mark as relevant"
                       bottom :click-handler="()=>setStarredAnalysis({id:currentAnalysisId,starred:true})"/>

    <icon-with-tooltip hover-color="error" icon="mdi-trash-can-outline" tip="Delete analysis" bottom
                       :click-handler="()=>removeAnalysis(currentAnalysisId)" color="primary"/>
    <result-navbar-menu/>

  </v-app-bar>
</template>

<script>
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import {mapGetters, mapMutations, mapState} from "vuex";
import ResultNavbarMenu from "@/components/analysis/navbar/ResultNavbarMenu";
import ResultNavbarWeekSlider from "@/components/analysis/navbar/ResultNavbarWeekSlider";
import ResultNavbarLocationSwitcher from "@/components/analysis/navbar/ResultNavbarLocationSwitcher";

export default {
  name: "ResultNavbar",
  components: {ResultNavbarLocationSwitcher, ResultNavbarWeekSlider, ResultNavbarMenu, IconWithTooltip},
  computed: {
    ...mapState(['currentAnalysisId']),
    ...mapGetters(['getCurrentAnalysis']),

    isStarred() {
      return this.getCurrentAnalysis.starred
    },
    query(){
      return this.getCurrentAnalysis.query
    },
  },
  methods: {
    ...mapMutations(['removeAnalysis', 'setStarredAnalysis'])
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
  border-bottom: 2px solid var(--primary-color) !important;
}
</style>