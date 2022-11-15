<template>
  <v-app-bar dense hide-on-scroll scroll-threshold="50" app flat fixed class="result-bar primary--text" color="bg_var1">
    <v-toolbar-title class="text-body-1 font-weight-black compact-text-2 primary--text">
      {{
        query.location[query.granularity] + " / " +
        query.endDate +
        (query.lineage ? " / " + query.lineage : "")
      }}
    </v-toolbar-title>

    <v-spacer/>
    <icon-with-tooltip hover-color="success" icon="mdi-clock-minus-outline" tip="Shift the analysis period one week backward" bottom
                       :click-handler="()=>$emit('moveBackward',-7)" color="primary"/>
    <icon-with-tooltip hover-color="success" icon="mdi-clock-plus-outline" tip="Shift the analysis period one week forward"  bottom
                       :click-handler="()=>$emit('moveForward',+7)" color="primary"/>

    <icon-with-tooltip v-if="isStarred" color="#C2AD07" hover-color="primary" icon="mdi-star"
                       tip="Mark as not relevant" bottom
                       :click-handler="()=>setStarredAnalysis({id:currentAnalysisId,starred:false})" />
    <icon-with-tooltip v-else hover-color="#C2AD07" color="primary" icon="mdi-star-outline" tip="Mark as relevant"
                       bottom :click-handler="()=>setStarredAnalysis({id:currentAnalysisId,starred:true})"/>

    <icon-with-tooltip hover-color="error" icon="mdi-trash-can-outline" tip="Delete analysis" bottom
                       :click-handler="()=>removeAnalysis(currentAnalysis)" color="primary"/>

  </v-app-bar>
</template>

<script>
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import {mapGetters, mapMutations, mapState} from "vuex";

export default {
  name: "ResultNavbar",
  components: {IconWithTooltip},
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