<!--
  View:         HomeView
  Description:  View container for the tool home
-->
<template>
  <div class="height-100">
    <sidebar/>
    <div class="tool-views-container height-100">
      <v-fade-transition hide-on-leave>
        <new-search-view v-if="currentView==='new-search'"/>
        <result-view v-if="currentView==='result'"/>
      </v-fade-transition>
    </div>

    <loading-sticker :error="error"/>

  </div>
</template>

<script>
import Sidebar from "@/components/general/Sidebar";
import NewSearchView from "@/components/views/NewSearchView";
import ResultView from "@/components/views/ResultView";
import {mapMutations, mapState} from "vuex";
import LoadingSticker from "@/components/general/basic/LoadingSticker";

export default {
  name: "HomeView",
  components: {LoadingSticker, ResultView, NewSearchView, Sidebar},
  data() {
    return {
      error: undefined,
    }
  },
  computed: {
    ...mapState(['currentAnalysisId','loading']),

    currentView() {
      return this.currentAnalysisId !== null ? 'result' : 'new-search'
    }
  },
  methods: {
    ...mapMutations(['setLastUpdate','setDatasetInfo']),

    /** Fetch the last update date of the dataset and other info */
    fetchDatasetInfo() {
      this.error = undefined
      const urlAPI = `/explorer/getDatasetInfo`

      this.$axios
          .get(urlAPI)
          .then(({data}) => {
            this.setLastUpdate(data['last_update'])
            this.setDatasetInfo(data)
          })
          .catch((e) => {
            this.setLastUpdate(null)
            setTimeout(this.fetchDatasetInfo,4000)
            this.error = e
          })
    }
  },
  watch:{
    loading(newVal){
      if(!newVal){
        this.fetchDatasetInfo()
      }
    }
  }
}
</script>

<style scoped>
.tool-views-container {
  background: var(--v-bg_var1-base);
  margin-left: 55px;
  padding-bottom: 200px;
}
</style>