<!--
  Component:    LineageSelector
  Description:  Select input element for lineage

  Props:
  ├── selectedGranularity: Value of the selected granularity
  ├── selectedLocation: Value of the selected location
  ├── selectedDate: Value of the selected date
  └── value: Value variable for binding of the date

  Events:
  └── error:    Emitted on server errors
-->

<template>
  <v-layout row wrap>
    <v-flex class='xs12 d-flex field-label'>
      <span>Lineage</span>
    </v-flex>

    <v-flex class='xs12 d-flex field-element'>
      <v-autocomplete v-model='selectedLineage' :loading='isLoading'
                      :disabled="selectedGranularity === null || (selectedLocation === null && selectedGranularity !== 'world')"
                      :items='possibleLineages' clearable hide-details label='Lineage' attach solo />
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios'

export default {
  name: 'LineageSelector',
  props: {
    /** Value of the selected granularity */
    selectedGranularity: { required: true },

    /** Value of the selected location */
    selectedLocation: { required: true },

    /** Value of the selected date */
    selectedDate: { required: true },

    /** Value variable for binding of the location */
    value: {}
  },
  data () {
    return {
      /** Lineage: available options (wrt to other params) */
      possibleLineages: [],

      /** All possible values for lineage */
      allLineages: null,

      /** Loading flag  */
      isLoading: false
    }
  },
  computed: {
    /** Selected lineage */
    selectedLineage: {
      /**
       * Getter for the string representing the selected lineage
       * @returns {string}  The selected lineage
       */
      get () {
        return this.value
      },

      /**
       * Setter for the lineage
       * @param val The new value
       */
      set (val) {
        this.$emit('input', val)
      }
    }
  },
  methods: {
    /** Fetch all possible values for lineages (given the other params) */
    getPossibleLineages () {
      this.isLoading = true

      // Avoid fetching all lineages if already cached
      if (!this.allLineages || this.selectedLocation || this.selectedDate) {
        const url = `/lineage_specific/getLineages`
        const toSend = {
          location: this.selectedLocation ? this.selectedLocation : null,
          date: this.selectedDate ? this.selectedDate[1] : null
        }
        axios
          .post(url, toSend)
          .then(res => {
            this.possibleLineages = res.data

            // Cache if all lineages and not already cached
            if (!this.allLineages && !this.selectedLocation && !this.selectedDate) {
              this.allLineages = res.data
            }

            // Keep selected lineage if included in the possible ones
            if (this.selectedLineage && !this.possibleLineages.includes(this.selectedLineage)) {
              this.selectedLineage = null
            }
          })
          .catch((e) => {
            this.$emit('error', e)
          })
      } else {
        this.possibleLineages = this.allLineages
      }

      this.isLoading = false
    }
  },
  watch: {
  /** Adjust the possible lineages according to the selected granularity */
    selectedGranularity (newVal) {
      if (newVal === 'world') { this.getPossibleLineages() }
    },

    /** Adjust the possible lineages according to the selected location */
    selectedLocation (newVal) {
      if (newVal) { this.getPossibleLineages() }
    },

    /** Adjust the possible lineages according to the selected date */
    selectedDate (newVal) {
      this.getPossibleLineages()
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
</style>
