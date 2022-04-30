import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  primary_color: '#014878',
  secondary_color: '#35B1ECFF',
  tertiary_color_light: '#D2ECF8FF',
  tertiary_color_dark: '#1976D2FF',

  /** Granularity: available options */
  possibleGranularity: [/* 'world',*/'continent', 'country', 'region'],
  /** Granularity: selected option */
  selectedGranularity: null,

  /** Selectable continents */
  possibleContinents: [],
  /** Selected continent */
  selectedContinent: null,

  /** Selectable countries */
  possibleCountries: [],
  /** Selected country */
  selectedCountry: null,

  /** Selectable regions */
  possibleRegions: [],
  /** Selected region */
  selectedRegion: null,

  /** Selected location (continent, country or region based on granularity) */
  selectedLocation: null,

  /** Date: selected date */
  selectedDate: null,

  /** Lineage: selected lineage */
  selectedLineage: null
}

const mutations = {
  SET_GRANULARITY: (state, newValue) => {
    state.selectedGranularity = newValue
  },

  SET_ALL_CONTINENTS: (state, newValue) => {
    state.possibleContinents = newValue
  },
  SET_CONTINENT: (state, newValue) => {
    state.selectedContinent = newValue
  },

  SET_ALL_COUNTRIES: (state, newValue) => {
    state.possibleCountries = newValue
  },
  SET_COUNTRY: (state, newValue) => {
    state.selectedCountry = newValue
  },

  SET_ALL_REGIONS: (state, newValue) => {
    state.possibleRegions = newValue
  },
  SET_REGION: (state, newValue) => {
    state.selectedRegion = newValue
  },

  SET_LOCATION: (state, newValue) => {
    state.selectedLocation = newValue
  },

  SET_END_DATE: (state, newValue) => {
    if (newValue !== null && newValue.length === 1) {
      // Date has been set from the picker (and has the form [endDate])
      const endDate = newValue[0]
      const startDate = new Date(new Date(endDate).setDate(new Date(endDate).getDate() - 27)).toISOString().slice(0, 10)
      state.selectedDate = [startDate, endDate]
    } else {
      if (newValue !== null && newValue.length === 2 && newValue[0] === null) {
        // Date has been set indirectly (and has the form [null,endDate])
        const endDate = newValue[1]
        const startDate = new Date(new Date(endDate).setDate(new Date(endDate).getDate() - 27)).toISOString().slice(0, 10)
        state.selectedDate = [startDate, endDate]
      } else {
        // Date has been set in another way (either null or [startDate,endDate])
        state.selectedDate = newValue
      }
    }
  },

  SET_LINEAGE: (state, newValue) => {
    state.selectedLineage = newValue
  }
}

export default new Vuex.Store({
  state,
  mutations
})
