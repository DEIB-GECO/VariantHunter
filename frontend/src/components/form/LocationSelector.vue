<!--
  Component:    LocationSelector
  Description:  Select input element for location
                It transfers the location value to the $store

  Events:
  └── error:    Emitted on server errors
-->

<template>
  <v-layout row wrap>

    <!-- Label -->
    <v-flex class='xs12 d-flex field-label'>
      <span>Location</span>
    </v-flex>

    <v-flex class='xs12 d-flex field-element'>
      <v-row dense>

        <!-- Continent selector -->
        <v-col class='complex-field-element'>
          <v-autocomplete v-model='selectedLocation' :items='possibleLocations' :search-input.sync="searchQuery"
                          :loading='isLoading' placeholder='Start typing the location' attach solo hide-details
                          persistent-placeholder :hide-no-data="(!searchQuery || searchQuery.length<1)"
                          :no-data-text="(isLoading?'Loading locations...':(searchQuery && searchQuery.length<3?'Continue typing...':'Location not found'))"
                          clearable @update:search-input="fetchLocations">
            <template v-slot:selection="{item}">
              <v-chip dark small class="text-uppercase mr-3 hidden-xs-only" :color="getLocationColor(item)">granularity:
                {{ possibleLocationsInfo[item].type }}
              </v-chip>
              <span class="text-uppercase">{{ item }}</span>
            </template>
            <template v-slot:item="{item}">
              <span class="text-uppercase">
                <span v-if="possibleLocationsInfo[item].continent">{{ possibleLocationsInfo[item].continent }}&nbsp;/&nbsp;</span>
                <span
                    v-if="possibleLocationsInfo[item].country">{{
                    possibleLocationsInfo[item].country
                  }}&nbsp;/&nbsp;</span>
                <span class="font-weight-bold">{{ item }}</span>
              </span>
              <v-spacer/>
              <v-chip dark small class="text-uppercase hidden-xs-only" :color="getLocationColor(item)">
                {{ possibleLocationsInfo[item].type }}
              </v-chip>
            </template>
          </v-autocomplete>
        </v-col>

      </v-row>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios'
import {mapStateTwoWay} from '@/utils/bindService'

export default {
  name: 'LocationSelector',
  data() {
    return {
      /** Loading progress */
      isLoading: false,
      /** Location query */
      searchQuery: ''
    }
  },
  computed: {
    ...mapStateTwoWay({
      selectedGranularity: 'SET_GRANULARITY',
      possibleLocationsInfo: 'SET_ALL_LOCATIONS_INFO',
      possibleLocations: 'SET_ALL_LOCATIONS',
      selectedLocation: 'SET_LOCATION'
    })
  },
  methods: {
    /** Fetch all possible values for locations */
    fetchLocations() {
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
                this.possibleLocationsInfo[value] = {type, country, continent}
              })
            })
            .catch((e) => {
              this.error = e
            })
      } else {
        if (!this.selectedLocation)
          this.possibleLocations = []
      }
    },

    getLocationColor(item) {
      return (this.possibleLocationsInfo[item].type === 'region'
          ? '#88c287'
          : this.possibleLocationsInfo[item].type === 'country'
              ? '#ff6e3e'
              : '#bc7fbf')
    }
  },
  watch:{
    selectedLocation(newVal){
      if(newVal!==null){
        this.selectedGranularity=this.possibleLocationsInfo[newVal].type
      }
    }
  }
}
</script>

<style scoped>
/* Form labels styling */
.field-label {
  padding-left:24px !important;
  padding-top: 8px !important;
  padding-bottom: 5px !important;
  color: white;
}

/* Form elements styling */
.field-element {
  padding-top: 0 !important;
  padding-bottom: 4px !important;
}

.complex-field-element {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

</style>
