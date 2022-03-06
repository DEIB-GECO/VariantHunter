<!--
  Component:    LocationSelector
  Description:  Select input element for location

  Props:
  ├── allLocations: List of all the possible locations.
  ├── selectedGranularity: Value of the selected granularity
  └── value: Value variable for binding of the date
-->

<template>
  <v-layout row wrap>
    <v-flex class="xs12 d-flex field-label">
      <span>Location</span>
    </v-flex>

    <v-flex class="xs12 d-flex field-element">
      <v-autocomplete v-model="selectedLocation"
                      :disabled="selectedGranularity === null || selectedGranularity === 'world'"
                      :items="possibleLocations"
                      hide-details
                      label="Location"
                      solo>
        <template slot="item" slot-scope="data">
          <span>{{ getFieldText(data.item) }}</span>
        </template>
      </v-autocomplete>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  name: "LocationSelector",
  props: {

    /** List of all the possible locations. */
    allLocations: {required: true},

    /** Value of the selected granularity */
    selectedGranularity: {required: true},

    /** Value variable for binding of the location */
    value: {}
  },
  data() {
    return {

      /** Location: available options (wrt to other params) */
      possibleLocations: [],

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
        return this.value
      },

      /**
       * Setter for the location
       * @param val The new value
       */
      set(val) {
        this.$emit('input', val)
      }
    }
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

    /** Compute the possible locations based on the other parameters of the form*/
    computePossibleLocations() {
      this.possibleLocations = [];
      this.selectedLocation = null;
      let i = 0;
      if (this.allLocations !== null && this.selectedGranularity != null) {
        if (this.selectedGranularity !== 'world') {
          while (i < this.allLocations[this.selectedGranularity].length) {
            if (this.allLocations[this.selectedGranularity][i] != null) {
              this.possibleLocations.push(this.allLocations[this.selectedGranularity][i]);
            } else {
              this.possibleLocations.push('N/D');
            }
            i = i + 1;
          }
        } else {
          this.selectedLocation = 'all'
        }
      }
      this.possibleLocations.sort();
    },

  },
  watch: {

    /** Adjust the possible locations according to the selected granularity */
    selectedGranularity() {
      this.computePossibleLocations()
    },

  },
}
</script>

<style scoped>

/* Form labels styling */
.field-label {
  justify-content: center;
  padding-top: 5px !important;
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