<!--
  Component:    MenuPage
  Description:  Component to switch between the analysis tabs.
                It also fetches all possible locations and lineages values saving them in the store.
-->

<template>
  <v-container class="tabs-container " fluid grid-list-xl>
    <v-tabs v-model="selectedTab"
            :background-color="secondary_color" :slider-color="primary_color"
            active-class="active-tab"
            dark
            height="60"
            show-arrows
            slider-size="6">

      <v-tab id="tab0" class="tab">
        LINEAGE INDEPENDENT
      </v-tab>

      <v-tab id="tab1" class="tab">
        LINEAGE SPECIFIC
      </v-tab>

      <v-tab-item class="tab-content">
        <MainPageWithoutLineages/>
      </v-tab-item>

      <v-tab-item class="tab-content">
        <MainPageWithLineages/>
      </v-tab-item>

    </v-tabs>


    <!-- Progress circle -->
    <v-overlay :value="isLoading">
      <v-progress-circular
          indeterminate
          size="64"
      ></v-progress-circular>
    </v-overlay>

    <!-- Error message -->
    <v-overlay :value="errorOccurred">
      <v-container>
        <v-alert dismissible elevation="24" type="error" @input="errorOccurred=false; isLoading=false">
          <b>The server is temporarily unreachable</b><br/>
          An error occurred while contacting the server. Please try again later.
        </v-alert>
      </v-container>
    </v-overlay>

  </v-container>
</template>

<script>
import axios from "axios";
import {mapMutations, mapState} from "vuex";
import MainPageWithLineages from "@/components/MainPageWithLineages";
import MainPageWithoutLineages from "@/components/MainPageWithoutLineages";

export default {
  name: "MenuPage",
  components: {MainPageWithoutLineages, MainPageWithLineages},
  data() {
    return {
      /** Currently selected tab */
      selectedTab: 0,

      /** Progress circe flag: true if the progress circle is displayed */
      isLoading: true,

      /** Progress status */
      progressStatus: 0,

      /** Server error flag */
      errorOccurred: false
    }
  },
  computed: {
    ...mapState(['primary_color', 'secondary_color']),
  },
  methods: {
    ...mapMutations(['setAllLocations', 'setAllLineages']),
  },
  watch: {
    /** Progress watcher */
    progressStatus() {
      this.isLoading = this.progressStatus !== 100
    }
  },
  mounted() {
    /** Fetch all possible values for locations (continents, countries, regions) */
    // let locationsAPI = `http://localhost:5001/variant_hunter/api/analyse_mutations/getAllGeo`; //TODO development env
    let locationsAPI = `/analyse_mutations/getAllGeo`;
    axios.get(locationsAPI)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          this.progressStatus = this.progressStatus + 50;
          this.setAllLocations(res);
        })
        .catch(() => {
          this.errorOccurred = true
        });

    /** Fetch all possible values for lineages */
    // let lineageAPI = `http://0.0.0.0:5001/variant_hunter/api/analyse_mutations/getAllLineage`; //TODO development env
    let lineageAPI = `/analyse_mutations/getAllLineage`;
    axios.get(lineageAPI)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          this.progressStatus = this.progressStatus + 50;
          this.setAllLineages(res);
        })
        .catch(() => {
          this.errorOccurred = true
        });
  }
}
</script>

<style scoped>

.tabs-container {
  justify-content: center;
  padding: 0;
}
.tab-content {
  height: 84vh;
  width: 100%;
  overflow-y: auto;
  float: left;
  position: relative;
}

/* Styling for (inactive) tabs */
.tab {
  font-size: 16px;
  font-weight: normal;
  border-right: #014878 solid 1px;
  width: 33%;
  border-bottom: #014878 solid 1px;
}

/* Styling for active tabs */
.active-tab {
  font-weight: bold;
}

</style>