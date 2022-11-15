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
import NewSearchView from "@/components/views/NewSearchView";
import ResultView from "@/components/views/ResultView";
import {mapState} from "vuex";
import {mapStateTwoWay} from "@/utils/bindService";

export default {
  name: "HomeView",
  components: {ResultView, NewSearchView, Sidebar},
  data() {
    return {
      currentView: 'new-search'
    }
  },
  methods:{
    /** Fetch the last update date of the dataset */
    fetchLastUpdate () {
      const urlAPI = `/explorer/getLastUpdate`

      this.$axios
        .get(urlAPI)
        .then(({data})=> { this.lastUpdate = data})
        .catch(() => {})
    }
  },
  computed:{
    ...mapState(['currentAnalysisId']),
    ...mapStateTwoWay({'lastUpdate':'setLastUpdate'}),
  },
  watch: {
    currentAnalysisId(newVal){
      if(newVal!==null)
        this.currentView='result'
      else
        this.currentView='new-search'
    }
  },
  mounted() {
    this.fetchLastUpdate()
  }
}
</script>

<style scoped>
.tool-views-container {
  background: var(--v-bg_var1-base);
  margin-left: 55px;
  padding-bottom:200px;
}
</style>