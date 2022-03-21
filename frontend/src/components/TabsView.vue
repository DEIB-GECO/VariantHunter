<!--
  Component:    TabsView
  Description:  Component to switch between the analysis tabs.
-->

<template>
  <v-container id='top' class='tabs-container ' fluid grid-list-xl>

    <!-- Tabs -->
    <v-tabs v-model='selectedTab' :background-color='secondary_color' :slider-color='primary_color'
            active-class='active-tab' dark height='60' centered show-arrows slider-size='6'>
      <v-tab id='tab0' class='tab'>
        LINEAGE INDEPENDENT
      </v-tab>

      <v-tab id='tab1' class='tab'>
        LINEAGE SPECIFIC
      </v-tab>

      <v-tab-item class='tab-content'>
        <TabWithoutLineages @error='handleError' />
      </v-tab-item>

      <v-tab-item class='tab-content'>
        <TabWithLineages @error='handleError' />
      </v-tab-item>
    </v-tabs>

    <!-- Global error alert -->
    <ErrorAlert v-model='errorOccurred' :errorMessage='errorMessage' />

    <!-- Last update snackbar -->
    <v-snackbar v-model='showSnackbar' timeout='10000' height='10' color='green' transition='scroll-y-transition'>
      <v-icon left>mdi-clock</v-icon>
      <span><b>Last dataset update: &nbsp;</b>{{ lastUpdate }}</span>
    </v-snackbar>
    <v-chip v-if='!showSnackbar' color='green' class='last-update' text-color='white'>
      <v-icon left>mdi-clock</v-icon>
      <span><b>Last dataset update: &nbsp;</b>{{ lastUpdate }}</span>
    </v-chip>
  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import TabWithLineages from '@/components/tabs/TabWithLineages'
import TabWithoutLineages from '@/components/tabs/TabWithoutLineages'
import ErrorAlert from '@/components/general/ErrorAlert'
import axios from 'axios'

export default {
  name: 'TabView',
  components: { ErrorAlert, TabWithoutLineages, TabWithLineages },
  data () {
    return {
      /** Currently selected tab */
      selectedTab: 0,

      /** Error flag. True iff an error has occurred */
      errorOccurred: false,

      /** Error message */
      errorMessage: null,

      /** Last update snackbar visibility flag */
      showSnackbar: false,

      /** Last update date */
      lastUpdate: null
    }
  },
  computed: {
    ...mapState(['primary_color', 'secondary_color'])
  },
  mounted () {
    // Fetch the last update date on page load
    this.fetchLastUpdate()
  },
  methods: {
    /**
     * Handler for server errors
     * @param e The error event
     */
    handleError (e) {
      this.errorOccurred = true
      this.errorMessage = e
    },

    /** Fetch the last update date of the dataset */
    fetchLastUpdate () {
      const urlAPI = `/explorer/getLastUpdate`

      axios
        .get(urlAPI)
        .then(res => {
          return res.data
        })
        .then(res => {
          this.lastUpdate = res
          this.showSnackbar = true
        })
        .catch((e) => {
          this.handleError(e)
        })
    }
  }
}
</script>

<style scoped>

/* Container of the tabs */
.tabs-container {
  justify-content: center;
  text-align: center;
  padding: 0;
}

/* Content of the tabs */
.tab-content {
  width: 100%;
}

/* Inactive tab style */
.tab {
  font-size: 16px;
  font-weight: normal;
  width: 33%;
  border-bottom: var(--primary-color) solid 1px;
}

/* Active tab style */
.active-tab {
  font-weight: bold;
}

</style>
<style>

/* Overwrite default styling for v-snackbars */
.v-snack__wrapper {
  border-radius: 28px 28px 0 0 !important;
  margin-bottom: 0 !important;
}

.last-update{
  padding: 25px;
  margin-bottom: 10px;
}

.v-snack__content {
  text-align: center !important;
}
</style>
