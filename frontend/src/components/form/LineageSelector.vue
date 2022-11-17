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
                        :loading='isLoading' placeholder='Select a lineage from the list' persistent-hint flat
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

    <loading-sticker :error="error" />

  </v-col>
</template>

<script>
import {mapState} from 'vuex'
import {mapStateTwoWay} from '@/utils/bindService'
import LoadingSticker from "@/components/general/basic/LoadingSticker";

export default {
  name: 'LineageSelector',
  components: {LoadingSticker},
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
      if (this.selectedLocation !== null) {
        this.isLoading = true
        this.error = undefined

        const url = `/lineage_specific/getLineages`
        const queryParams = {
          location: this.selectedLocation,
          date: this.selectedDate ? this.selectedDate[1] : undefined
        }

        this.$axios
            .get(url, {params: queryParams})
            .then(({data}) => {
              this.possibleLineages = data

              // Keep selected lineage if included in the possible ones
              if (this.selectedLineage && !this.possibleLineages.includes(this.selectedLineage)) {
                this.selectedLineage = null
              }
            })
            .catch((e) => {
              this.error = e
              this.possibleLineages = []
              this.selectedLineage = null
            })
            .finally(() => {
              this.isLoading = false
            })
      }
    }
  },
  watch: {
    /** Adjust the possible lineages according to the selected location */
    selectedLocation() {
        this.getPossibleLineages()
    },

    /** Adjust the possible lineages according to the selected date */
    selectedDate() {
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
  color: var(--v-text_var1-base);
  text-align: center;
  padding: 10px 14px;
  line-height: 17px;
  line-break: loose;
  text-transform: initial !important;
}
</style>
