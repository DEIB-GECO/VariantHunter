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

          <!-- Fake hidden input area to trigger outside click -->
          <input style="width: 0; height: 0" id="outside"/>
        </span>
      </v-col>
    </v-row>
    <v-row dense class="px-5">
      <v-col>
        <v-autocomplete v-model='selectedLocation' :items='possibleLocations' :search-input.sync="searchQuery"
                        :loading='isLoading' placeholder='Start typing the location' attach solo hide-details
                        persistent-placeholder :hide-no-data="(!searchQuery || searchQuery.length<1)" flat
                        :filter="customFilter"
                        @click.capture="onBoxClick" :menu-props="{closeOnClick: true,closeOnContentClick: true}"
                        :no-data-text="(isLoading?'Loading locations...':(searchQuery && searchQuery.length<2?'Continue typing...':'This location seems not to exist'))"
                        clearable clear-icon="mdi-backspace-outline" v-click-outside="onClickOutside"
                        @click:clear.stop="onClear" @change="onChange">
          <!-- Current selection -->
          <template v-slot:selection="{item}">
            <div @click="onBoxClick">
              <v-chip dark small class="text-uppercase mr-3 hidden-xs-only" :color="getLocationColor(item)">
                granularity: {{ possibleLocationsInfo[item].type }}
              </v-chip>
              <span class="text-uppercase">{{ item }}</span>
            </div>
          </template>

          <!-- Item element -->
          <template v-slot:item="{item}">
              <span class="text-uppercase">
                <span v-if="possibleLocationsInfo[item].continent">{{ possibleLocationsInfo[item].continent }}&nbsp;/&nbsp;</span>
                <span v-if="possibleLocationsInfo[item].country">{{
                    possibleLocationsInfo[item].country
                  }}&nbsp;/&nbsp;</span>
                <span class="font-weight-bold">{{ item }}</span>
              </span>
            <v-spacer/>
            <icon-with-tooltip v-if="possibleLocationsInfo[item].type!=='region'" icon="mdi-arrow-top-right"
                               :tip="'Browse locations of '+ item" bottom color="secondary" class="ml-1" size="medium"
                               :click-handler="()=>fillWith(item)" />

            <v-chip dark small class="text-uppercase hidden-xs-only" :color="getLocationColor(item)">
              {{ possibleLocationsInfo[item].type }}
            </v-chip>
          </template>
        </v-autocomplete>
      </v-col>
    </v-row>

    <loading-sticker :error="error" />

  </v-col>
</template>

<script>
import {mapStateTwoWay} from "@/utils/bindService";
import Vue from "vue";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import LoadingSticker from "@/components/general/basic/LoadingSticker";

export default {
  name: 'LocationSelector',
  components: {LoadingSticker, IconWithTooltip},
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
      error: undefined,
      searchQuery: undefined,
    }
  },
  computed: {
    ...mapStateTwoWay({
      selectedLocation: 'setLocation',
      possibleLocations: 'setLocations',
      possibleLocationsInfo: 'setLocationsInfo'
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

    fillWith(item) {
      this.searchQuery = item + '/'
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
      this.error = undefined
      const locationsAPI = `/locations/getLocations`
      this.$axios
          .get(locationsAPI, {params: {string: queryString}})
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
            this.isLoading = false
            this.error = e
          })

    },

    getLocationColor(item) {
      return this.possibleLocationsInfo[item].type === 'region'
          ? '#7CB17B'
          : this.possibleLocationsInfo[item].type === 'country'
              ? '#ff6e3e'
              : '#90177d'
    }
  },
  watch: {
    selectedLocation(newVal) {
      if (newVal !== null && this.possibleLocationsInfo[newVal] ) {
        this.selectedGranularity = this.possibleLocationsInfo[newVal].type
      }
    },
    searchQuery(newVal, oldVal) {
      // If the new query extends the previous one ('Eu'->'Eur') prevent fetch
      if (newVal?.length >= 2 && (oldVal?.length < 2 || oldVal?.slice(0, 2) !== newVal?.slice(0, 2)))
        this.fetchLocations()
      else if (newVal?.length < 2 && oldVal?.length >= 2 && newVal !== '') {
        this.possibleLocations = [] // reset locations when query string is less than 2 characters
      } else if(newVal?.length >= 2 && this.error){
        this.fetchLocations()
      }
    }
  }
}
</script>

<style scoped>

</style>
