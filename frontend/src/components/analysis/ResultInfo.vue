<template>
  <v-row class="mt-6" no-gutters>
    <v-col>
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon><v-icon left large color="primary">mdi-map-marker-outline</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Sequences from</v-list-item-title>
            <v-list-item-subtitle>{{ locationData }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>
    <v-col>
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon><v-icon left large color="primary">mdi-calendar-week-outline</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Analysis period</v-list-item-title>
            <v-list-item-subtitle>{{period}}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>
    <v-col>
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon><v-icon left large color="primary">mdi-clock-outline</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Analysis performed on</v-list-item-title>
            <v-list-item-subtitle>{{ getCurrentAnalysis.query.performedOn }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      </v-col>
    <v-col>
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon><v-icon left large color="primary">mdi-database-outline</v-icon></v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ getCurrentAnalysis.query.datasetType.toUpperCase() }} dataset</v-list-item-title>
            <v-list-item-subtitle>updated on {{ getCurrentAnalysis.query.datasetAsOf }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>
  </v-row>
</template>

<script>
import {mapGetters} from "vuex";
import {computeDateLabel} from "@/store/utils/utils";

export default {
  name: "ResultInfo",
  computed: {
    ...mapGetters(['getCurrentAnalysis']),

    locationData() {
      const {granularity, location} = this.getCurrentAnalysis.query
      const {region, country, continent} = location

      switch (granularity){
        case 'region': return region+', '+country+', '+continent
        case 'country': return country+', '+continent
        default: return continent
      }
    },

    period(){
      return computeDateLabel(this.getCurrentAnalysis.query.endDate, 27, 0)
    }
  }
}
</script>

<style scoped>

</style>