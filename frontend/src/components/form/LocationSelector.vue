<!--
  Component:    LocationSelector
  Description:  Select input element for location

  Props:
  ├── selectedGranularity: Value of the selected granularity
  └── value: Value variable for binding of the date
-->

<template>
  <v-layout row wrap>
    <v-flex class="xs12 d-flex field-label">
      <span>Location</span>
    </v-flex>

    <v-flex class="xs12 d-flex field-element">
      <v-row dense>
        <!-- Continent selector -->
        <v-col class="complex-field-element">
          <v-autocomplete v-model="selectedContinent"
                          :disabled="disableContinentSelection"
                          :items="possibleContinents"
                          :loading="isLoading"
                          hide-details
                          label="Continent"
                          solo>
            <template v-slot:item="data">
              <span>{{ getFieldText(data.item) }}</span>
            </template>
          </v-autocomplete>
        </v-col>

        <!-- Country selector-->
        <v-col v-if="showCountrySelector" class="complex-field-element">
          <v-autocomplete v-model="selectedCountry"
                          :disabled="disableCountrySelection"
                          :items="possibleCountries"
                          :loading="isLoading"
                          hide-details
                          label="Country"
                          solo>
            <template v-slot:item="data">
              <span>{{ getFieldText(data.item) }}</span>
            </template>
          </v-autocomplete>
        </v-col>

        <!-- Region selector -->
        <v-col v-if="showRegionSelector" class="complex-field-element">
          <v-autocomplete v-model="selectedRegion"
                          :disabled="disableRegionSelection"
                          :items="possibleRegions"
                          :loading="isLoading"
                          hide-details
                          label="Region"
                          solo>
            <template v-slot:item="data">
              <span>{{ getFieldText(data.item) }}</span>
            </template>
          </v-autocomplete>
        </v-col>

      </v-row>
    </v-flex>
  </v-layout>
</template>

<script>

import axios from "axios";

export default {
  name: "LocationSelector",
  props: {

    /** Value of the selected granularity */
    selectedGranularity: {required: true},

    /** Value variable for binding of the location */
    value: {}
  },
  data() {
    return {

      /** Selectable continents */
      possibleContinents: [],

      /** Selectable countries */
      possibleCountries: [],

      /** Selectable regions */
      possibleRegions: [],

      /** Selected continent */
      selectedContinent: null,

      /** Selected country */
      selectedCountry: null,

      /** Selected region */
      selectedRegion: null,

      /** Loading progress */
      isLoading: false,

    }
  },
  computed: {

    /** Selected location */
    selectedLocation: {
      /**
       * Getter for the string representing the selected location
       * @returns {string}  The selected location
       */
      get() {
        switch (this.selectedGranularity) {
          case 'continent':
            return this.selectedContinent;
          case 'country':
            return this.selectedCountry;
          case 'region':
            return this.selectedRegion;
          default:
            return null;
        }
      },

      /**
       * Setter for the location
       * @param val The new value
       */
      set(val) {
        this.$emit('input', val)
      }
    },

    /** Condition to disable the continent selection. If true is disabled */
    disableContinentSelection() {
      return this.selectedGranularity === null || this.selectedGranularity === 'world'
    },

    /** Condition to disable the country selection. If true is disabled */
    disableCountrySelection() {
      return this.disableContinentSelection || this.selectedContinent === null
    },

    /** Condition to disable the region selection. If true is disabled */
    disableRegionSelection() {
      return this.disableCountrySelection || this.selectedCountry === null
    },

    /** Condition to show the country selector. If true is shown */
    showCountrySelector() {
      return this.selectedGranularity === 'region' || this.selectedGranularity === 'country'
    },

    /** Condition to show the region selector. If true is shown */
    showRegionSelector() {
      return this.selectedGranularity === 'region'
    },

  },
  methods: {

    /** Returns the hint for the field completion */
    getFieldText(item) {
      let name;
      if (item === null) {
        name = 'N/D'
      } else {
        name = item;
      }
      return name;
    },

    /** Fetch all possible values for continents */
    fetchContinents() {
      if (!this.disableContinentSelection) {
        this.selectedContinent = null;
        this.isLoading = true;
        let locationsAPI = `/locations/getContinents`;
        axios.get(locationsAPI)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.isLoading = false;
              this.possibleContinents = res;
            });
      }
    },

    /** Fetch all possible values for countries */
    fetchCountries() {
      if (!this.disableCountrySelection && this.showCountrySelector) {
        this.selectedCountry = null;
        this.isLoading = true;
        let locationsAPI = `/locations/getCountries`;
        let to_send = {
          'continent': this.selectedContinent,
        };
        axios.post(locationsAPI, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.isLoading = false;
              this.possibleCountries = res;
            });
      }
    },

    /** Fetch all possible values for regions */
    fetchRegions() {
      if (!this.disableRegionSelection && this.showRegionSelector) {
        this.selectedRegion = null;
        this.isLoading = true;
        let locationsAPI = `/locations/getRegions`;
        let to_send = {
          'country': this.selectedCountry,
        };
        axios.post(locationsAPI, to_send)
            .then((res) => {
              return res.data;
            })
            .then((res) => {
              this.isLoading = false;
              this.possibleRegions = res;
            });
      }
    },

  },
  watch: {

    /** Adjust the possible continents according to the selected granularity */
    selectedGranularity(newVal) {
      this.possibleCountries = []
      this.possibleRegions = []
      if (newVal != null)
        this.fetchContinents();
    },

    /** Adjust the possible countries and the binding according to the selected continent */
    selectedContinent(newVal) {
      this.possibleRegions = []
      this.selectedLocation = newVal
      if (newVal != null)
        this.fetchCountries();
    },

    /** Adjust the possible countries and the binding according to the selected continent  */
    selectedCountry(newVal) {
      this.selectedLocation = newVal
      if (newVal != null)
        this.fetchRegions();
    },

    /** Adjust the binding */
    selectedRegion(newVal) {
      this.selectedLocation = newVal
    }

  },
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