<!--
  Component:    LineageSelector
  Description:  Select input element for lineage
                It transfers the lineage value to the $store

  Events:
  └── error:    Emitted on server errors
-->

<template>
  <v-col>
    <v-row class="px-5 pb-2">
      <v-col>
        <span class="text-body-3 compact-text-3 primary--text d-block">
          <span class="compact-text-5 font-weight-black">Lineage</span>:
          select the lineage you want to analyze.
        </span>
      </v-col>
    </v-row>
    <v-row dense class="px-5">
      <v-col>
        <v-autocomplete v-model='selectedLineage' :items='possibleLineages' :disabled="!selectedLocation"
                        :loading='isLoading' placeholder='Select a lineage from the list' persistent-hint
                        :hint="(!selectedLocation)?'You must select at least a location first':''" :hide-details="selectedLocation!==null" attach solo
                        persistent-placeholder clearable clear-icon="mdi-backspace-outline" :class="(!selectedLocation)?'warning--text cursor-forbidden':''">
          <template v-slot:prepend-item>
            <slot name='prepend-item'>
              <div class='hint'>{{ hint }}</div>
            </slot>
          </template>
        </v-autocomplete>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import axios from 'axios'
import {mapState} from 'vuex'
import {mapStateTwoWay} from '@/utils/bindService'

export default {
  name: 'LineageSelector',
  data() {
    return {
      isLoading: false,
      error: undefined,
    }
  },
  computed: {
    ...mapState(['selectedLocation', 'selectedDate']),
    ...mapStateTwoWay({selectedLineage: 'setLineage', possibleLineages: 'setLineages'}),

    /** Hint for the selector  */
    hint() {
      return (this.selectedLocation)
          ? 'Lineages in ' + this.selectedLocation + (this.selectedDate ? ' for the selected analysis period:' : ':')
          : 'All available lineages:'
    }
  },
  methods: {
    /** Fetch all possible values for lineages (given the other params) */
    getPossibleLineages() {
      if (this.selectedDate !== null || this.selectedLocation !== null) {
        this.isLoading = true

        const url = `/lineage_specific/getLineages`
        const toSend = {
          location: this.selectedLocation ? this.selectedLocation : null,
          date: this.selectedDate ? this.selectedDate[1] : null
        }

        axios
            .post(url, toSend)
            .then(({data}) => {
              this.possibleLineages = data

              // Keep selected lineage if included in the possible ones
              if (this.selectedLineage && !this.possibleLineages.includes(this.selectedLineage)) {
                this.selectedLineage = null
              }
            })
            .catch((e) => {
              this.error = e
            })
            .finally(() => {
              this.isLoading = false
            })
      }
    }
  },
  watch: {
    /** Adjust the possible lineages according to the selected location */
    selectedLocation(newVal) {
        this.getPossibleLineages()
    },

    /** Adjust the possible lineages according to the selected date */
    selectedDate(newVal) {
      this.getPossibleLineages()
    }
  },
  mounted() {
    this.getPossibleLineages()
  }
}
</script>

<style scoped>
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
