<!--
  Component:    DatePicker
  Description:  Select input element with embedded date picker

  Props:
  └── value: Value variable for binding of the date
-->

<template>
  <v-layout justify-center row wrap>
    <!-- Label -->
    <v-flex class='xs12 d-flex field-label'>
      <span>Analysis period</span>
    </v-flex>

    <!-- Picker -->

    <v-flex class='xs12 d-flex field-element'>
      <v-menu v-model='menuVisibility' :close-on-content-click='false' min-width='auto' offset-y
              transition='scale-transition' content-class='menu-container' attach>

        <template v-slot:activator='{ on, attrs }'>
          <v-text-field v-model='selectedDateText' append-icon='mdi-calendar' hide-details label='Date' readonly
                        clearable
                        solo v-bind='attrs' v-on='on' @click:append='menuVisibility = true' />
        </template>
        <div class='hint'>Select the end date for the 4 weeks analysis period</div>
        <v-date-picker v-model='selectedDate' :max='today' first-day-of-week='1' no-title range
                       show-adjacent-months @input='menuVisibility = false' />
      </v-menu>
    </v-flex>

  </v-layout>
</template>

<script>
export default {
  name: 'DatePicker',
  props: {
    /** Value variable for binding of the date */
    value: { type: Array }
  },
  data () {
    return {
      /** Visibility flag of date picker menu */
      menuVisibility: false,

      /** Today date */
      today: new Date().toISOString().slice(0, 10)
    }
  },
  computed: {
    /** Selected date */
    selectedDate: {
      /**
       * Getter for the string representing the selected date
       * @returns {Array}  The selected date
       */
      get () {
        return this.value
      },

      /**
       * Setter for the date. Automatically select the analysis period starting from the ending date selection
       * @param endDate The new value
       */
      set ([endDate]) {
        const startDate = new Date(new Date(endDate).setDate(new Date(endDate).getDate() - 28)).toISOString().slice(0, 10)
        this.$emit('input', [startDate, endDate])
      }
    },

    /** Selected analysis period label */
    selectedDateText: {
      /**
       * Getter for the label
       * @returns {Array}  The label date
       */
      get () {
        return this.value ? this.value.join(' ⏐ ') : null
      },

      /**
       * Setter for the label.
       * @param label The new label
       */
      set (label) {
        // Ignore change requests
      }
    }
  },
  watch: {
    /** Auto adjust the date range if not appropriately set*/
    selectedDate (newRange) {
      if (newRange && newRange[0] == null) {
        const startDate = new Date(new Date(newRange[1]).setDate(new Date(newRange[1]).getDate() - 28)).toISOString().slice(0, 10)
        this.$emit('input', [startDate, newRange[1]])
      }
    }
  }
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

/* Hint for date-picker */
.hint {
  background: white;
  text-align: center;
  max-width: fit-content;
  padding: 10px 14px;
  line-height: 17px;
  line-break: loose;
  text-transform: initial !important;
}

/* Menu container style */
.menu-container {
  background: white !important;
}

</style>
