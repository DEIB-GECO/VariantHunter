<!--
  Component:    LineageSelector
  Description:  Select input element for lineage
                It transfers the lineage value to the $store

  Events:
  └── error:    Emitted on server errors
-->

<template>
  <v-layout row wrap>
    <v-flex class='xs12 d-flex field-label'>
      <span>Lineage</span>
    </v-flex>

    <v-flex class='xs12 d-flex field-element'>
      <v-autocomplete v-model='selectedLineage' :items='possibleLineages' :loading='isLoading'
                      :disabled="selectedGranularity === null || (selectedLocation === null && selectedGranularity !== 'world')"
                      label='Lineage' clearable hide-details attach solo>
        <template v-slot:prepend-item>
          <slot name='prepend-item'>
            <div class='hint'>{{ hint }}</div>
          </slot>
        </template>
      </v-autocomplete>
    </v-flex>
  </v-layout>
</template>

<script>
import axios from 'axios'
import { mapState } from 'vuex'
import { mapStateTwoWay } from '@/utils/bindService'

export default {
  name: 'LineageSelector',
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
    ...mapState(['selectedGranularity', 'selectedLocation', 'selectedDate']),
    ...mapStateTwoWay({ selectedLineage: 'SET_LINEAGE' }),

    /** Hint for the selector  */
    hint () {
      return (this.selectedLocation)
        ? 'Lineages in ' + this.selectedLocation + (this.selectedDate ? ' for the last week of the selected analysis period:' : ':')
        : 'All available lineages:'
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
      if (newVal === 'world') {
        this.getPossibleLineages()
      }
    },

    /** Adjust the possible lineages according to the selected location */
    selectedLocation (newVal) {
      if (newVal) {
        this.getPossibleLineages()
      }
    },

    /** Adjust the possible lineages according to the selected date */
    selectedDate (newVal) {
      this.getPossibleLineages()
    }
  },
  mounted () {
    if (this.selectedDate !== null || this.selectedLocation !== null) {
      this.getPossibleLineages()
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
  text-transform: capitalize;
}

/* Hint */
.hint {
  color: rgba(0, 0, 0, 0.54);
  text-align: center;
  padding: 10px 14px;
  line-height: 17px;
  line-break: loose;
  text-transform: initial !important;
}
</style>
