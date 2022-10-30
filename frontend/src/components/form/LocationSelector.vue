<!--
  Component:    LocationSelector
  Description:  Select input element for location
                It transfers the location value to the $store

  Events:
  └── error:    Emitted on server errors
-->

<template>
  <v-col>
    <v-row class="px-5 pb-2">
      <v-col>
        <span class="text-body-3 compact-text-3 primary--text d-block">
          <span class="compact-text-5 font-weight-black">Location</span>:
          select the continent, country, or region you want to analyze.
        </span>
      </v-col>
    </v-row>
    <v-row dense class="px-5">
      <v-col>
        <v-autocomplete v-model='selectedLocation' :items='possibleLocations' :search-input.sync="searchQuery"
                        :loading='isLoading' placeholder='Start typing the location' attach solo hide-details
                        persistent-placeholder :hide-no-data="(!searchQuery || searchQuery.length<1)"
                        :no-data-text="(isLoading?'Loading locations...':(searchQuery?.length<3?'Continue typing':'Location not found'))"
                        clearable clear-icon="mdi-backspace-outline" @update:search-input="fetchLocations">
          <template v-slot:selection="{item}">
              <v-chip dark small class="text-uppercase mr-3 hidden-xs-only" :color="getLocationColor(item)">granularity: {{ possibleLocationsInfo[item].type }}</v-chip>
              <span class="text-uppercase">{{ item }}</span>
              </template>
          <template v-slot:item="{item}">
              <span class="text-uppercase">
                <span v-if="possibleLocationsInfo[item].continent">{{possibleLocationsInfo[item].continent}}&nbsp;/&nbsp;</span>
                <span v-if="possibleLocationsInfo[item].country">{{possibleLocationsInfo[item].country}}&nbsp;/&nbsp;</span>
                <span class="font-weight-bold">{{ item }}</span>
              </span>
              <v-spacer/>
              <v-chip dark small class="text-uppercase hidden-xs-only" :color="getLocationColor(item)">{{ possibleLocationsInfo[item].type }}</v-chip>
          </template>
        </v-autocomplete>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import axios from 'axios'
import {mapStateTwoWay} from "@/utils/bindService";

export default {
  name: 'LocationSelector',
  data() {
    return {
      /** Loading progress */
      isLoading: false,
      error: undefined,
      searchQuery: undefined,
    }
  },
  computed: {
    ...mapStateTwoWay({
      selectedLocation: 'setLocation',
      possibleLocations:'setLocations',
      possibleLocationsInfo:'setLocationsInfo'
    })
  },
  methods: {

    /** Fetch all possible values for locations */
    fetchLocations() {
      console.log(this.searchQuery)
      if (this.searchQuery?.length >= 3) {
        this.isLoading = true
        const locationsAPI = `/locations/getLocations`
        axios
            .get(locationsAPI, {params: {string: this.searchQuery}})
            .then(({data}) => {
              this.isLoading = false
              this.possibleLocations = []
              this.possibleLocationsInfo = {}
              data.forEach(({value, type, country, continent}) => {
                this.possibleLocations.push(value)
                this.possibleLocationsInfo[value] = {type,country,continent}
              })
            })
            .catch((e) => {
              this.error = e
            })
      } else {
        if(!this.selectedLocation)
          this.possibleLocations = []
      }
    },

    getLocationColor(item){
      return this.possibleLocationsInfo[item].type==='region'
          ? '#88c287'
          : this.possibleLocationsInfo[item].type==='country'
              ? '#ff6e3e'
              : '#bc7fbf'
    }
  }
}
</script>

<style scoped>

</style>
