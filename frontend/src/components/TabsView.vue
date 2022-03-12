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

  </v-container>
</template>

<script>
import { mapState } from 'vuex'
import TabWithLineages from '@/components/tabs/TabWithLineages'
import TabWithoutLineages from '@/components/tabs/TabWithoutLineages'
import ErrorAlert from '@/components/general/ErrorAlert'

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
      errorMessage: null
    }
  },
  computed: {
    ...mapState(['primary_color', 'secondary_color'])
  },
  methods: {
    /**
     * Handler for server errors
     * @param e The error event
     */
    handleError (e) {
      this.errorOccurred = true
      this.errorMessage = e
    }
  }
}
</script>

<style scoped>

/* Container of the tabs */
.tabs-container {
  justify-content: center;
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
