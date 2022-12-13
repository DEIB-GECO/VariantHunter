<!--

  Component:    DatePicker
  Description:  Select input element with embedded date picker for the analysis period

-->

<template>
  <v-col>

    <!-- Headings -->
    <v-row class="px-5 pb-2">
      <v-col>
        <span class="text-body-3 compact-text-3 primary--text d-block">
          <span class="compact-text-5 font-weight-black">Analysis period</span>:
          select the 4-weeks analysis period.
        </span>
      </v-col>
    </v-row>

    <!-- Input element -->
    <v-row dense class="px-5">
      <v-col>
        <v-menu v-model='menuVisibility' :close-on-content-click='false' min-width='auto' offset-y
                transition='scale-transition' content-class='menu-container' attach nudge-bottom="-30px">

          <template v-slot:activator='{ on, attrs }'>
            <v-text-field v-model='selectedDateText' append-icon='mdi-calendar' :hide-details="false"
                          persistent-hint flat
                          hint="Not sure which period to select? Analyze the sequences over time using the Dataset Explorer below."
                          placeholder='Select the end date of the period' readonly
                          clearable clear-icon="mdi-backspace-outline" solo v-bind='attrs' v-on='on' @click:append='menuVisibility = true'
                          persistent-placeholder/>
          </template>
          <v-date-picker v-model='selectedDate' :max='lastUpdate' first-day-of-week='1' no-title range :show-current="lastUpdate"
                          @input='menuVisibility = false' header-color="f_primary" color="f_primary" class="rounded-t-0"/>
        </v-menu>
      </v-col>
    </v-row>

  </v-col>
</template>

<script>
import {mapStateTwoWay} from '@/utils/bindService'
import {mapState} from "vuex";

export default {
  name: 'DatePicker',

  data() {
    return {
      /** Visibility flag of date picker menu */
      menuVisibility: false,
    }
  },

  computed: {
    ...mapState(['lastUpdate']),
    ...mapStateTwoWay({
      selectedDate: 'setDate'
    }),

    /** Selected analysis period label */
    selectedDateText: {
      /**
       * Getter for the label
       * @returns {Array}  The label date
       */
      get() {
        return this.selectedDate ? this.selectedDate.join(' ⏐ ') : null
      },

      /**
       * Setter for the label.
       */
      set() {
        this.selectedDate = null
      }
    }
  }
}
</script>

<style scoped>

/* Menu container style */
.menu-container {
  background: white !important;
}

</style>
