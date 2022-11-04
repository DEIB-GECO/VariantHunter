<!--
  View:         HomeView
  Description:  View container for the tool home
-->
<template>
  <div class="height-100">
    <sidebar />
    <div class="tool-views-container height-100">
      <v-scroll-y-reverse-transition>
        <new-search-view v-if="currentView==='new-search'"/>
        <result-view v-if="currentView==='result'"/>
      </v-scroll-y-reverse-transition>
    </div>
  </div>
</template>

<script>
import Sidebar from "@/components/general/Sidebar";
import NewSearchView from "@/views/NewSearchView";
import ResultView from "@/views/ResultView";
import {mapState} from "vuex";

export default {
  name: "HomeView",
  components: {ResultView, NewSearchView, Sidebar},
  data() {
    return {
      currentView: 'result'//'new-search'
    }
  },
  computed:{
    ...mapState(['currentAnalysisId']),
  },
  watch: {
    currentAnalysisId(newVal){
      if(newVal!==null)
        this.currentView='result'
      else
        this.currentView='new-search'
    }
  },
}
</script>

<style scoped>
.tool-views-container {
  background: var(--tertiary-color-light);
  margin-left: 55px;
  padding-bottom:200px;
}
</style>