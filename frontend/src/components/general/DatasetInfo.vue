<template>
  <div class="text-right text-body-4 font-weight-medium pb-3 compact-text-3 success--text">
    <div v-if="lastUpdate">
      <v-tooltip bottom right allow-overflow z-index="999" :close-delay="0" max-width="400px">
        <template v-slot:activator="{ on, attrs }">
          <span v-bind="attrs" v-on="on"><v-icon small color="success">mdi-database-outline</v-icon>
          &nbsp;<span class="text-uppercase">{{ datasetInfo.fileType }}</span> dataset updated on <span
                class="font-weight-regular d-block d-md-inline-block">{{ lastUpdate }}</span>
          </span>
        </template>
        <div class="pa-3">
          <div class="text-body-3 font-weight-bold mb-3">
            <v-icon left color="f_text_light">mdi-database-outline</v-icon>
            Dataset currently in use
          </div>
          <div class="mb-3">
            <div><v-icon small left color="f_text_light">mdi-connection</v-icon>Metadata provider</div>
            <span class="text-uppercase font-weight-bold ml-6">{{ datasetInfo.fileType }}</span>
          </div>
           <div class="mb-3" v-if="!(noBegin && noEnd)">
            <div><v-icon small left color="f_text_light">mdi-clock-outline</v-icon>Available period</div>
             <div class="text-body-5 ml-6">The data set was limited to the following time period:</div>
            <span class="text-uppercase font-weight-bold ml-6">[ {{ begin }} &nbsp;;&nbsp; {{ end }} ]</span>
          </div>
          <div class="mb-3" v-if="!(noCountryFilter)">
            <div><v-icon small left color="f_text_light">mdi-map-marker-outline</v-icon>Available countries</div>
            <div class="text-body-5 ml-6">The dataset was limited to the following countries:</div>
            <span class="text-uppercase font-weight-bold ml-6">{{ datasetInfo.filteredCountries }}</span>
          </div>
        </div>
      </v-tooltip>
    </div>

    <div v-else>
      <v-progress-circular class="mr-2" indeterminate
                           size="15"/>
      Fetching last dataset update...
    </div>
  </div>
</template>

<script>
import {mapState} from "vuex";

export default {
  name: "DatasetInfo",
  computed: {
    ...mapState(['lastUpdate', 'datasetInfo']),
    noBegin(){
      return this.datasetInfo.beginDate==='beginning'
    },
    noEnd(){
      return this.datasetInfo.endDate==='end'
    },
    noCountryFilter(){
      return this.datasetInfo.filteredCountries==='all'
    },

    begin(){
      return this.noBegin?'N.A.':this.datasetInfo.beginDate
    },
    end(){
      return this.noEnd?'N.A.':this.datasetInfo.endDate
    }
  }
}
</script>

<style scoped>

</style>