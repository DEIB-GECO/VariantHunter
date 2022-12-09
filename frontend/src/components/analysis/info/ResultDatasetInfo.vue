<!--

  Component:    ResultDatasetInfo
  Description:  Dataset info summary of the result panel

-->

<template>
  <v-list color="transparent">
    <v-list-item>

      <v-list-item-icon>
        <v-icon left large color="primary">mdi-database-outline</v-icon>
      </v-list-item-icon>

      <v-tooltip top right allow-overflow z-index="999" :close-delay="0" max-width="400px">
        <!-- Activator: section name-->
        <template v-slot:activator="{ on, attrs }">
          <v-list-item-content v-on="on" v-bind="attrs">
            <v-list-item-title>{{ datasetInfo['file_type'].toUpperCase() }} dataset
            </v-list-item-title>
            <v-list-item-subtitle>updated on {{ datasetInfo['last_update'] }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </template>

        <!-- Dataset info on hover -->
        <div class="pa-3">
          <div class="text-body-3 font-weight-bold mb-3">
            <v-icon left color="f_text_light">mdi-database-outline</v-icon>
            Dataset used
          </div>
          <div class="mb-3">
            <div>
              <v-icon small left color="f_text_light">mdi-connection</v-icon>
              Metadata provider
            </div>
            <span class="text-uppercase font-weight-bold ml-6">{{ datasetInfo['file_type'] }}</span>
          </div>
          <div class="mb-3" v-if="!(noBegin && noEnd)">
            <div>
              <v-icon small left color="f_text_light">mdi-clock-outline</v-icon>
              Available period
            </div>
            <div class="text-body-5 ml-6">The data set was limited to the following time period:</div>
            <span class="text-uppercase font-weight-bold ml-6">[ {{ begin }} &nbsp;;&nbsp; {{ end }} ]</span>
          </div>
          <div class="mb-3" v-if="!(noCountryFilter)">
            <div>
              <v-icon small left color="f_text_light">mdi-map-marker-outline</v-icon>
              Available countries
            </div>
            <div class="text-body-5 ml-6">The dataset was limited to the following countries:</div>
            <span class="text-uppercase font-weight-bold ml-6">{{ datasetInfo['filtered_countries'] }}</span>
          </div>
        </div>

      </v-tooltip>

    </v-list-item>
  </v-list>
</template>

<script>
import {mapGetters} from "vuex";

export default {
  name: "ResultDatasetInfo",

  computed: {
    ...mapGetters(['getCurrentAnalysis']),

    /** Dataset info for the current analysis */
    datasetInfo() {
      return this.getCurrentAnalysis.query.datasetInfo
    },

    /** Boolean flag set to true if no upper bound was defined on the dataset */
    noBegin() {
      return this.datasetInfo['begin_date'] === 'beginning'
    },
    /** Boolean flag set to true if no lower bound was defined on the dataset */
    noEnd() {
      return this.datasetInfo['end_date'] === 'end'
    },
    /** Boolean flag set to true if no country-based filtering was performed on the dataset */
    noCountryFilter() {
      return this.datasetInfo['filtered_countries'] === 'all'
    },

    /** Dataset begin date */
    begin() {
      return this.noBegin ? 'N.A.' : this.datasetInfo['begin_date']
    },
    /** Dataset end date */
    end() {
      return this.noEnd ? 'N.A.' : this.datasetInfo['end_date']
    }
  }
}
</script>

<style scoped>

</style>