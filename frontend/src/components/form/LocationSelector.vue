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
          <v-autocomplete v-model='selectedContinent' :items='possibleContinents'
                          :disabled='disableContinentSelection' :loading='isLoading'
                          placeholder='Continent' hide-details attach solo persistent-placeholder
                          @input="updateSelectedLocation('continent')">
            <template v-slot:item='data'>
              <span>{{ getFieldText(data.item) }}</span>
            </template>
          </v-autocomplete>
        </v-col>

        <!-- Country selector-->
        <v-col v-if='showCountrySelector' class='complex-field-element'>
          <v-autocomplete v-model='selectedCountry' :items='possibleCountries'
                          :disabled='disableCountrySelection' :loading='isLoading'
                          placeholder='Country' hide-details attach solo persistent-placeholder
                          @input="updateSelectedLocation('country')">
            <template v-slot:item='data'>
              <span>{{ getFieldText(data.item) }}</span>
            </template>
          </v-autocomplete>
        </v-col>

        <!-- Region selector -->
        <v-col v-if='showRegionSelector' class='complex-field-element'>
          <v-autocomplete v-model='selectedRegion' :items='possibleRegions'
                          :disabled='disableRegionSelection' :loading='isLoading'
                          placeholder='Region' hide-details attach solo persistent-placeholder
                          @input="updateSelectedLocation('region')">
            <template v-slot:item='data'>
              <span>{{ getFieldText(data.item) }}</span>
            </template>
          </v-autocomplete>
        </v-col>
      </v-row>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import { mapStateTwoWay } from '@/utils/bindService'

export default {
  name: 'LocationSelector',
  data () {
    return {
      /** Loading progress */
      isLoading: false
    }
  },
  computed: {
    ...mapState(['selectedGranularity']),
    ...mapStateTwoWay({
      possibleContinents: 'SET_ALL_CONTINENTS',
      selectedContinent: 'SET_CONTINENT',

      possibleCountries: 'SET_ALL_COUNTRIES',
      selectedCountry: 'SET_COUNTRY',

      possibleRegions: 'SET_ALL_REGIONS',
      selectedRegion: 'SET_REGION',

      selectedLocation: 'SET_LOCATION'
    }),

    /** Condition to disable the continent selection. If true is disabled */
    disableContinentSelection () {
      return (
        this.selectedGranularity === null || this.selectedGranularity === 'world'
      )
    },

    /** Condition to disable the country selection. If true is disabled */
    disableCountrySelection () {
      return this.disableContinentSelection || this.selectedContinent === null
    },

    /** Condition to disable the region selection. If true is disabled */
    disableRegionSelection () {
      return this.disableCountrySelection || this.selectedCountry === null
    },

    /** Condition to show the country selector. If true is shown */
    showCountrySelector () {
      return this.selectedGranularity === 'region' || this.selectedGranularity === 'country'
    },

    /** Condition to show the region selector. If true is shown */
    showRegionSelector () {
      return this.selectedGranularity === 'region'
    }
  },
  methods: {
    /** Update the selected location whenever a new field is filled in
     * @param source  The field that has been filled in
     */
    updateSelectedLocation (source) {
      switch (source) {
        case 'continent':
          this.selectedLocation = this.selectedGranularity === 'continent' ? this.selectedContinent : null
          break
        case 'country':
          this.selectedLocation = this.selectedGranularity === 'country' ? this.selectedCountry : null
          break
        case 'region':
          this.selectedLocation = this.selectedGranularity === 'region' ? this.selectedRegion : null
      }
      this.clearFormFrom(source)
    },

    /** Returns the hint for the field completion */
    getFieldText (item) {
      let name
      if (item === null) {
        name = 'N/D'
      } else {
        name = item
      }
      return name
    },

    /** Fetch all possible values for continents */
    fetchContinents () {
      if (!this.disableContinentSelection) {
        this.isLoading = true
        const locationsAPI = `/locations/getContinents`
        axios
          .get(locationsAPI)
          .then(res => {
            return res.data
          })
          .then(res => {
            this.isLoading = false
            this.possibleContinents = res
          }).catch((e) => {
            this.$emit('error', e)
          })
      }
    },

    /** Fetch all possible values for countries */
    fetchCountries () {
      if (!this.disableCountrySelection && this.showCountrySelector) {
        this.isLoading = true
        const locationsAPI = `/locations/getCountries`
        const toSend = {
          continent: this.selectedContinent
        }
        axios
          .post(locationsAPI, toSend)
          .then(res => {
            return res.data
          })
          .then(res => {
            this.isLoading = false
            this.possibleCountries = res
          }).catch((e) => {
            this.$emit('error', e)
          })
      }
    },

    /** Fetch all possible values for regions */
    fetchRegions () {
      if (!this.disableRegionSelection && this.showRegionSelector) {
        this.isLoading = true
        const locationsAPI = `/locations/getRegions`
        const toSend = {
          country: this.selectedCountry
        }
        axios
          .post(locationsAPI, toSend)
          .then(res => {
            return res.data
          })
          .then(res => {
            this.isLoading = false
            this.possibleRegions = res
          }).catch((e) => {
            this.$emit('error', e)
          })
      }
    },

    /**
     * Clear the form from a field on
     * @param from  Starting point for the cleaning action
     */
    clearFormFrom (from) {
      switch (from) {
        case 'granularity':
          this.selectedLocation = null
          this.selectedContinent = null
          this.selectedCountry = null
          this.selectedRegion = null
          this.possibleCountries = []
          this.possibleRegions = []
          break
        case 'continent':
          this.selectedCountry = null
          this.selectedRegion = null
          this.possibleRegions = []
          break
        case 'country':
          this.selectedRegion = null
          break
      }
    }
  },
  watch: {
    /** Adjust the possible continents according to the selected granularity */
    selectedGranularity () {
      this.fetchContinents()
      this.clearFormFrom('granularity')
    },

    /** Adjust the possible countries according to the selected continent */
    selectedContinent () {
      this.fetchCountries()
    },

    /** Adjust the possible countries according to the selected continent  */
    selectedCountry () {
      this.fetchRegions()
    }
  }
}
</script>

<style scoped>
/* Form labels styling */
.field-label {
  justify-content: center;
  padding-top: 8px !important;
  padding-bottom: 5px !important;
  color: white;
}

/* Form elements styling */
.field-element {
  padding-top: 0 !important;
  padding-bottom: 4px !important;
  text-transform: capitalize;
}

.complex-field-element {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
  text-transform: capitalize;
}

</style>
