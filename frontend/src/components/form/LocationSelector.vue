<!--

  Component:    LocationSelector
  Description:  Select input element for location

-->

<template>
  <v-col>

    <!-- Headings -->
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

    <!-- Input element -->
    <v-row dense class="px-5">
      <v-col>
        <v-autocomplete v-model='selectedLocation' :items='possibleLocations' :search-input.sync="searchQuery"
                        :loading='isLoading' placeholder='Start typing the location' attach solo hide-details
                        persistent-placeholder :hide-no-data="(!searchQuery || searchQuery.length<1)" flat
                        :filter="customFilter" return-object item-text="text" item-value="id"
                        @click.capture="onBoxClick" :menu-props="{closeOnClick: true,closeOnContentClick: true}"
                        :no-data-text="(isLoading?'Loading locations...':(searchQuery && searchQuery.length<2?'Continue typing...':'This location seems not to exist'))"
                        clearable clear-icon="mdi-backspace-outline" v-click-outside="onClickOutside"
                        @click:clear.stop="onClear" @change="onChange">

          <!-- Current selection -->
          <template v-slot:selection="{item}">
            <div @click="onBoxClick">
              <v-chip dark small class="text-uppercase mr-3 hidden-xs-only" :color="locationColor(item.id)">
                granularity: {{ possibleLocationsInfo[item.id].type }}
              </v-chip>
              <span class="text-uppercase">{{ item.text }}</span>
            </div>
          </template>

          <!-- Item element -->
          <template v-slot:item="{item}">
              <span class="text-uppercase">
                <span v-if="possibleLocationsInfo[item.id].continent">
                  {{ possibleLocationsInfo[item.id].continent.text }}&nbsp;/&nbsp;
                </span>
                <span v-if="possibleLocationsInfo[item.id].country">
                  {{ possibleLocationsInfo[item.id].country.text }}&nbsp;/&nbsp;
                </span>
                <span class="font-weight-bold">{{ item.text }}</span>
              </span>
            <v-spacer/>
            <icon-with-tooltip v-if="possibleLocationsInfo[item.id].type!=='region'" icon="mdi-arrow-top-right"
                               :tip="'Browse locations of '+ item.text" bottom color="secondary" class="ml-1"
                               size="medium" :click-handler="()=>fillWith(item.text)"/>

            <v-chip dark small class="text-uppercase hidden-xs-only" :color="locationColor(item.id)">
              {{ possibleLocationsInfo[item.id].type }}
            </v-chip>
          </template>

        </v-autocomplete>
      </v-col>
    </v-row>

    <loading-sticker :error="error"/>

  </v-col>
</template>

<script>
import {mapStateTwoWay} from "@/utils/bindService";
import Vue from "vue";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import {getLocationColor} from "@/utils/colorService";

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

      /** Boolean loading flag for the table and expansion */
      isLoading: false,
      /** Error data for the table and expansion. Undefined if no error. */
      error: undefined,

      /** Current search query */
      searchQuery: undefined,

      /** Boolean flag set to true when the data are fetched not because of user input */
      externalTriggering: false,
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

    /**
     * Manager for the input element click
     */
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
        this.searchQuery = this.previousValues.selectedLocation ? this.previousValues.selectedLocation.text : null
      });
    },

    /**
     * Manager for the click outside the input element
     */
    onClickOutside() {
      // Restore previous values if set
      if (this.previousValues.selectedLocation) {
        this.possibleLocationsInfo = this.previousValues.possibleLocationsInfo
        this.possibleLocations = this.previousValues.possibleLocations
        this.selectedLocation = this.previousValues.selectedLocation
      }
    },

    /**
     * Manager of the clear form action
     */
    onClear() {
      this.possibleLocationsInfo = []
      this.possibleLocations = []
      this.selectedLocation = null
      this.previousValues.possibleLocationsInfo = []
      this.previousValues.possibleLocations = []
      this.previousValues.selectedLocation = null
    },

    /**
     * Manager for the selection of a new value
     */
    onChange() {
      this.previousValues.possibleLocationsInfo = []
      this.previousValues.possibleLocations = []
      this.previousValues.selectedLocation = null
      this.searchQuery = ""
      Vue.nextTick(() => {
        document.getElementById('outside').focus()
      });
    },

    /** Fill the search text with a certain string followed by '/'
     * @param itemText  The string to be considered
     */
    fillWith(itemText) {
      this.searchQuery = itemText + '/'
    },

    /**
     * Custom filter for the autocomplete items
     * @param item        Item to be considered
     * @param queryText   Current query text
     * @param itemText    Text value of the item to be considered
     * @returns {boolean} True iff item has to be shown in the list or not
     */
    customFilter(item, queryText, itemText) {
      const {type, continent, country} = this.possibleLocationsInfo[item.id]
      queryText = queryText.trim().toLowerCase() // clean the query string
      itemText = itemText.toLowerCase()

      // If continent direct comparison only
      if (type === 'continent') return itemText.indexOf(queryText) > -1

      // Otherwise check for indirect search
      const indirect = (type === 'country')
          ? continent.text.toLowerCase() + '/' + itemText
          : continent.text.toLowerCase() + '/' + country.text.toLowerCase() + '/' + itemText

      // Trim spaces near '/'
      const indirectQueryText = queryText.replaceAll(' /', '/').replaceAll('/ ', '/')
      return itemText.indexOf(queryText) > -1 || indirect.indexOf(indirectQueryText) > -1
    },

    /** Fetch all possible values for locations */
    fetchLocations() {
      const fullQueryString = this.searchQuery
      const queryString = fullQueryString.match(/[^/][^/]/m)[0]
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
              this.possibleLocationsInfo[value.id] = {type, country, continent}
            })

            // If the fetch was caused by external triggering, then select the corresponding value
            if (this.externalTriggering) {
              this.externalTriggering = false
              this.selectedLocation = this.possibleLocations.find(({text}) => fullQueryString.toUpperCase() === text.toUpperCase())
            }
          })
          .catch((e) => {
            this.isLoading = false
            this.error = e
          })

    },

    /**
     * Mapping for getLocationColor
     */
    locationColor(itemId) {
      return getLocationColor(itemId)
    }
  },

  watch: {
    /**
     * On selected location changes
     */
    selectedLocation(newVal) {
      if (newVal !== null && this.possibleLocationsInfo[newVal.id]) {
        // new value selected, update corresponding granularity value
        this.selectedGranularity = this.possibleLocationsInfo[newVal.id].type
      } else if (newVal !== null && this.possibleLocations.length === 0) {
        // location has been set manually (not through user input): trigger fetch
        this.searchQuery = newVal
        this.externalTriggering = true
      }
    },

    /**
     * On search query changes, triggers the fetch
     */
    searchQuery(newVal, oldVal) {
      // If the new query extends the previous one ('Eu'->'Eur') prevent fetch
      if (newVal?.length >= 2 && (oldVal?.length < 2 || oldVal?.slice(0, 2) !== newVal?.slice(0, 2)))
        this.fetchLocations()
      else if (newVal?.length < 2 && oldVal?.length >= 2 && newVal !== '') {
        this.possibleLocations = [] // reset locations when query string is less than 2 characters
      } else if (newVal?.length >= 2 && this.error) {
        this.fetchLocations() // an error occurred previously, fetch anyway
      }
    }
  }
}
</script>

<style scoped>

</style>
