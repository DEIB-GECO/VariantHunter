<!--

  View:         HomeView
  Description:  View container for the tool home

-->

<template>
  <div class="height-100">
    <!-- Tool sidebar -->
    <sidebar/>

    <!-- Main sub-view -->
    <div id="to-print">
      <div class="tool-views-container height-100">
        <v-fade-transition hide-on-leave>
          <new-search-view v-if="currentView==='new-search'"/>
          <result-view v-if="currentView==='result'"/>
        </v-fade-transition>
      </div>
    </div>

    <loading-sticker :error="error"/>

    <!-- Screen size alert -->
    <screen-size-alert/>

  </div>
</template>

<script>
import Sidebar from "@/components/general/Sidebar";
import NewSearchView from "@/components/views/NewSearchView";
import ResultView from "@/components/views/ResultView";
import {mapMutations, mapState} from "vuex";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import ScreenSizeAlert from "@/components/general/ScreenSizeAlert.vue";

export default {
  name: "HomeView",
  components: {ScreenSizeAlert, LoadingSticker, ResultView, NewSearchView, Sidebar},

  data() {
    return {
      /** Error data for the table and expansion. Undefined if no error. */
      error: undefined,
    }
  },

  computed: {
    ...mapState(['currentAnalysisId', 'loading']),

    /** Current type of main sub-view */
    currentView() {
      return this.currentAnalysisId !== null ? 'result' : 'new-search'
    }
  },

  methods: {
    ...mapMutations(['setLastUpdate', 'setDatasetInfo']),

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
            setTimeout(this.fetchDatasetInfo, 10000)
            this.error = e
          })
    }
  },

  watch: {
    /** After storage restore has been completed */
    loading(newVal) {
      if (!newVal) {
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