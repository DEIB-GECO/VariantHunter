<template>
  <v-navigation-drawer class="sidebar-sizing no-border" :mini-variant="isCollapsed" clipped permanent expand-on-hover touchless
                       absolute dark color="primary" width="500px" height="100vh">
    <v-list rounded nav dense>
      <list-item icon="mdi-plus" title="New analysis" link subtitle="Perform a new analysis" expand-on-hover
                 :class="currentView==='new-search'?'v-list-item--active':''" @click.native="newAnalysisHandler()"/>
      <v-divider/>

      <list-item icon="mdi-history" title="Recent analysis" subtitle="Your recent analysis" with-actions>
        <template v-slot:actions>
          <icon-with-tooltip v-if="showHistory" icon="mdi-chevron-up" tip="Collapse" bottom
                             :click-handler="()=>{showHistory=false}"/>
          <icon-with-tooltip v-else icon="mdi-chevron-down" tip="Expand" bottom
                             :click-handler="()=>{showHistory=true}"/>
        </template>
      </list-item>
      <v-expand-transition>
        <search-history v-if="showHistory" type="all" @select="currentView='result'"/>
      </v-expand-transition>

    </v-list>
  </v-navigation-drawer>
</template>

<script>
import ListItem from "@/components/general/basic/ListItem";
import SearchHistory from "@/components/general/SearchHistory";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import {mapMutations, mapState} from "vuex";

export default {
  name: "Sidebar",
  components: {IconWithTooltip, SearchHistory, ListItem},
  data() {
    return {
      showSidebar: true,
      isCollapsed: true,
      showHistory: true,
      currentView: 'new-search'
    }
  },
  computed:{
    ...mapState(['currentAnalysis'])
  },
  watch: {
    currentAnalysis(newVal){
      if(newVal)
        this.currentView='result'
    }
  },
  methods: {
    ...mapMutations(['setCurrentAnalysis']),

    newAnalysisHandler() {
      this.currentView = 'new-search'
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