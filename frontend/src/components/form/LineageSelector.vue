<!--
  Component:    LineageSelector
  Description:  Select input element for lineage

  Props:
  ├── allLineages: List of all the possible lineages.
  ├── selectedGranularity: Value of the selected granularity
  ├── selectedLocation: Value of the selected location
  ├── selectedDate: Value of the selected date
  └── value: Value variable for binding of the date
-->

<template>
    <v-layout row wrap>
      <v-flex class="xs12 d-flex field-label">
        <span>Lineage</span>
      </v-flex>

      <v-flex class="xs12 d-flex field-element">
        <v-autocomplete
            v-model="selectedLineage"
            :disabled="selectedGranularity === null || (selectedLocation === null && selectedGranularity !== 'world')"
            :items="possibleLineages"
            clearable
            hide-details
            label="Lineage"
            solo
        >
        </v-autocomplete>
      </v-flex>
    </v-layout>
</template>

<script>

import axios from "axios";

export default {
  name: "LineageSelector",
  props: {

    /** Value of the selected granularity */
    selectedGranularity: {required: true},

    /** Value of the selected location */
    selectedLocation: {required: true},

    /** Value of the selected date */
    selectedDate: {required: true},

    /** All values of lineages */
    allLineages: {reduired: true}, // TODO move fetch inside the component

    /** Value variable for binding of the location */
    value: {}
  },
  data() {
    return {

      /** Lineage: available options (wrt to other params) */
      possibleLineages: this.allLineages,

    }
  },
  computed: {

    /** Selected lineage */
    selectedLineage: {
      /**
       * Getter for the string representing the selected lineage
       * @returns {string}  The selected lineage
       */
      get() {
        return this.value
      },

      /**
       * Setter for the lineage
       * @param val The new value
       */
      set(val) {
        this.$emit('input', val)
      }
    }
  },
  methods: {

    /** Fetch all possible values for lineages (given the other params) */
    getPossibleLineages() {
      if (this.selectedLocation !== null && this.selectedLocation !== 'world' && this.selectedDate !== null) {
        let url = `/lineage_specific/getGeoLineages`;
        let to_send = {
          'geo': this.selectedLocation,
          'date': this.selectedDate
        };
        axios.post(url, to_send)
            .then((res) => {
              this.possibleLineages = res.data;
              if (!this.possibleLineages.includes(this.selectedLineage))
                this.selectedLineage = null;
            })
      }
    },

  },
  watch: {

    /** Adjust the possible lineages according to the selected location */
    selectedLocation() {
      if (this.selectedDate)
        this.getPossibleLineages()
      else
        this.possibleLineages = this.allLineages
    },

    /** Adjust the possible lineages according to the selected date */
    selectedDate() {
      if (this.selectedDate)
        this.getPossibleLineages()
      else
        this.possibleLineages = this.allLineages
    },

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

</style>