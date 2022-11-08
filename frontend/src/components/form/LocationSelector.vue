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
      <!-- Fake hidden input area to trigger outside click -->
      <input style="width: 0; height: 0" id="outside"/>
    </v-flex>

    <v-flex class='xs12 d-flex field-element'>
      <v-row dense>

        <!-- Continent selector -->
        <v-col class='complex-field-element'>
          <v-autocomplete v-model='selectedLocation' :items='possibleLocations' :search-input.sync="searchQuery"
                          :filter="customFilter"
                          :loading='isLoading' placeholder='A continent, country or region' attach solo hide-details
                          persistent-placeholder :hide-no-data="(!searchQuery || searchQuery.length<1)"
                          @click.capture="onBoxClick" :menu-props="{closeOnClick: true,closeOnContentClick: true}"
                          :no-data-text="(isLoading?'Loading locations...':(searchQuery && searchQuery.length<2?'Continue typing...':'This location seems not to exist'))"
                          clearable v-click-outside="onClickOutside" @click:clear.stop="onClear" @change="onChange">
            <template v-slot:selection="{item}">
              <div @click="onBoxClick">
                <v-chip dark small class="text-uppercase mr-3 hidden-xs-only" :color="getLocationColor(item)">
                  granularity:
                  {{ possibleLocationsInfo[item].type }}
                </v-chip>
                <span class="text-uppercase">{{ item }}</span>
              </div>
            </template>
            <template v-slot:item="{item}">
              <span class="text-uppercase">
                <span v-if="possibleLocationsInfo[item].continent">{{ possibleLocationsInfo[item].continent }}&nbsp;/&nbsp;</span>
                <span v-if="possibleLocationsInfo[item].country">{{possibleLocationsInfo[item].country }}&nbsp;/&nbsp;</span>
                <span class="font-weight-bold">{{ item }}</span>
              </span>
              <v-spacer/>
              <v-tooltip content-class="rounded-xl" bottom v-if="possibleLocationsInfo[item].type!=='region'">
                <template v-slot:activator="{ on }">
                  <v-btn color="secondary" class="ml-1" @click.stop="fillWith(item)" icon v-on="on" >
                    <v-icon small>mdi-arrow-top-right</v-icon>
                  </v-btn>
                </template>
                Explore "{{ item }}"
              </v-tooltip>
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
import Vue from "vue";

export default {
  name: 'LocationSelector',
  components: {},
  data() {
    return {
      /** Values for locations before an edit of the current selection */
      previousValues: {
        possibleLocations: [],
        possibleLocationsInfo: [],
        selectedLocation: null,
      },

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
    onBoxClick() {
      // Store previous values and clear them
      this.previousValues = {
        possibleLocations: this.possibleLocations,
        possibleLocationsInfo: this.possibleLocationsInfo,
        selectedLocation: this.selectedLocation
      }
      this.possibleLocationsInfo = []
      this.possibleLocations = []
      this.selectedLocation = null

      // Fill the search area with the past selection to enable exploring (eg "Europe/", "Italy/")
      Vue.nextTick(() => {
        this.searchQuery = this.previousValues.selectedLocation
      });
    },

    onClickOutside() {
      // Restore previous values if set
      if (this.previousValues.selectedLocation) {
        this.possibleLocationsInfo = this.previousValues.possibleLocationsInfo
        this.possibleLocations = this.previousValues.possibleLocations
        this.selectedLocation = this.previousValues.selectedLocation
      }
    },

    onClear() {
      this.possibleLocationsInfo = []
      this.possibleLocations = []
      this.selectedLocation = null
      this.previousValues.possibleLocationsInfo = []
      this.previousValues.possibleLocations = []
      this.previousValues.selectedLocation = null
    },

    onChange() {
      this.previousValues.possibleLocationsInfo = []
      this.previousValues.possibleLocations = []
      this.previousValues.selectedLocation = null
      this.searchQuery = ""
      Vue.nextTick(() => {
        document.getElementById('outside').focus()
      });
    },

    fillWith(item){
      this.searchQuery=item+'/'
    },

    customFilter(item, queryText, itemText) {
      const {type, continent, country} = this.possibleLocationsInfo[itemText]
      queryText = queryText.trim().toLowerCase() // clean the query string
      itemText = itemText.toLowerCase()

      // If continent direct comparison only
      if (type === 'continent') return itemText.indexOf(queryText) > -1

      // Otherwise check for indirect search
      const indirect = (type === 'country')
          ? continent.toLowerCase() + '/' + itemText
          : continent.toLowerCase() + '/' + country.toLowerCase() + '/' + itemText

      // Trim spaces near '/'
      const indirectQueryText = queryText.replaceAll(' /', '/').replaceAll('/ ', '/')
      return itemText.indexOf(queryText) > -1 || indirect.indexOf(indirectQueryText) > -1
    },


    /** Fetch all possible values for locations */
    fetchLocations() {
      const queryString = this.searchQuery.match(/[^/][^/]/m)[0]
      this.isLoading = true
      const locationsAPI = `/locations/getLocations`
      axios
          .get(locationsAPI, {params: {string: queryString}})
          .then(({data}) => {
            this.isLoading = false
            this.possibleLocations = []
            this.possibleLocationsInfo = {}
            data.forEach(({value, type, country, continent}) => {
              if (value) {
                this.possibleLocations.push(value)
                this.possibleLocationsInfo[value] = {type, country, continent}
              }
            })
          })
          .catch((e) => {
            this.error = e
          })
    },

    getLocationColor(item) {
      return (this.possibleLocationsInfo[item].type === 'region'
          ? '#88c287'
          : this.possibleLocationsInfo[item].type === 'country'
              ? '#ff6e3e'
              : '#bc7fbf')
    }
  },
  watch: {
    selectedLocation(newVal) {
      if (newVal !== null) {
        this.selectedGranularity = this.possibleLocationsInfo[newVal].type
      }
    },
    searchQuery(newVal, oldVal) {
      // If the new query extends the previous one ('Eu'->'Eur') prevent fetch
      if (newVal?.length >= 2 && (oldVal?.length < 2 || oldVal?.slice(0, 2) !== newVal?.slice(0, 2)))
        this.fetchLocations()
      else if (newVal?.length < 2 && oldVal?.length >= 2 && newVal !== '') {
        this.possibleLocations = [] // reset locations when query string is less than 2 characters
      }
    }
  }
}
</script>

<style scoped>
/* Form labels styling */
.field-label {
  padding-left: 24px !important;
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
