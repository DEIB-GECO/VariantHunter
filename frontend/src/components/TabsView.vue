<!--
  Component:    TabView
  Description:  Component to switch between the analysis tabs.
                It also fetches all possible locations and lineages values.
-->

<template>
  <v-container id="top" class="tabs-container " fluid grid-list-xl>
    <v-tabs v-model="selectedTab"
            :background-color="secondary_color" :slider-color="primary_color"
            active-class="active-tab"
            dark
            height="60"
            centered
            show-arrows
            slider-size="6">

      <v-tab id="tab0" class="tab">
        LINEAGE INDEPENDENT
      </v-tab>

      <v-tab id="tab1" class="tab">
        LINEAGE SPECIFIC
      </v-tab>

      <v-tab-item class="tab-content">
        <TabWithoutLineages/>
      </v-tab-item>

      <v-tab-item class="tab-content">
        <TabWithLineages :allLineages="allLineages"/>
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
import {mapState} from "vuex";
import TabWithLineages from "@/components/tabs/TabWithLineages";
import TabWithoutLineages from "@/components/tabs/TabWithoutLineages";

export default {
  name: "TabView",
  components: {TabWithoutLineages, TabWithLineages},
  data() {
    return {
      /** Currently selected tab */
      selectedTab: 0,

      /** Progress circe flag: true if the progress circle is displayed */
      isLoading: true,

      /** Progress status */
      progressStatus: 0,

      /** Server error flag */
      errorOccurred: false,

      /** Lineages fetched from server*/
      allLineages: []
    }
  },
  computed: {
    ...mapState(['primary_color', 'secondary_color']),
  },
  watch: {
    /** Progress watcher */
    progressStatus() {
      this.isLoading = this.progressStatus !== 100
    }
  },
  mounted() {

    /** Fetch all possible values for lineages */
    let lineageAPI = `/analyse_mutations/getAllLineage`;
    axios.get(lineageAPI)
        .then((res) => {
          return res.data;
        })
        .then((res) => {
          this.progressStatus = this.progressStatus + 100;
          this.allLineages = res;
        })
        .catch(() => {
          if(!this.errorOccurred)
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
  width: 100%;
}

/* Styling for (inactive) tabs */
.tab {
  font-size: 16px;
  font-weight: normal;
  width: 33%;
  border-bottom: var(--primary-color) solid 1px;
}

/* Styling for active tabs */
.active-tab {
  font-weight: bold;
}

</style>