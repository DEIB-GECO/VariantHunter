<!--

  Component:    Sidebar
  Description:  Sidebar app element with history

-->

<template>
  <v-navigation-drawer class="sidebar-sizing hide-scrollbar" :mini-variant="isCollapsed" clipped permanent expand-on-hover touchless
                       absolute dark color="f_primary" width="500px" height="100vh" floating>
    <!-- Sidebar body -->
    <v-list rounded nav dense>

      <!-- New analysis -->
      <list-item icon="mdi-plus" title="New analysis" link subtitle="Perform a new analysis" expand-on-hover
                 :class="currentView==='new-search'?'v-list-item--active':''" @click.native="newAnalysisHandler()"/>

      <v-divider/>

      <!-- Analysis history -->
      <list-item icon="mdi-history" title="Recent analyses" subtitle="Your recent analyses" with-actions>
        <template v-slot:actions>
          <icon-with-tooltip v-if="showHistory" icon="mdi-chevron-up" tip="Collapse" bottom
                             :click-handler="()=>{showHistory=false}"/>
          <icon-with-tooltip v-else icon="mdi-chevron-down" tip="Expand" bottom
                             :click-handler="()=>{showHistory=true}"/>
        </template>
      </list-item>
      <v-expand-transition>
        <search-history v-if="showHistory" type="all"/>
      </v-expand-transition>

    </v-list>

    <!-- Sidebar append -->
    <template v-slot:append>
      <app-preferences/>
    </template>

  </v-navigation-drawer>
</template>

<script>
import ListItem from "@/components/general/basic/ListItem";
import SearchHistory from "@/components/general/SearchHistory";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import {mapMutations, mapState} from "vuex";
import AppPreferences from "@/components/general/AppPreferences";

export default {
  name: "Sidebar",
  components: {AppPreferences, IconWithTooltip, SearchHistory, ListItem},

  data() {
    return {
      /** Boolean flag set to true if the bar is collapsed */
      isCollapsed: true,

      /** Boolean visibility flag set to true if the history is visible */
      showHistory: true,
    }
  },

  computed: {
    ...mapState(['currentAnalysisId']),

    /** Currently displayed mode */
    currentView() {
      return this.currentAnalysisId !== null ? 'result' : 'new-search'
    }
  },

  methods: {
    ...mapMutations(['setCurrentAnalysis']),

    /** Show new analysis tab */
    newAnalysisHandler() {
      this.setCurrentAnalysis(null)
    }
  }
}
</script>

<style scoped>
.sidebar-sizing {
  padding-top: 56px;
  max-width: 90vw !important;
  z-index: 10 !important;
  position: fixed !important;
}
</style>