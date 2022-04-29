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
                        clearable solo v-bind='attrs' v-on='on' @click:append='menuVisibility = true' />
        </template>
        <div class='hint'>Select the end date for the 4 weeks analysis period
          <v-row class='tip'>
            <v-col class='col-2 tip-icon'><v-icon>mdi-lightbulb-on-outline</v-icon></v-col>
            <v-col class='col-10 tip-text'> use the &nbsp;
            <v-icon small>mdi-compass</v-icon>
            DATASET EXPLORER &nbsp; to choose the best analysis period
              </v-col>
          </v-row>
        </div>
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
        const startDate = new Date(new Date(endDate).setDate(new Date(endDate).getDate() - 27)).toISOString().slice(0, 10)
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
        this.$emit('input', null)
      }
    }
  },
  watch: {
    /** Auto adjust the date range if not appropriately set*/
    selectedDate (newRange) {
      if (newRange && newRange[0] == null) {
        const startDate = new Date(new Date(newRange[1]).setDate(new Date(newRange[1]).getDate() - 27)).toISOString().slice(0, 10)
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
  color: rgba(0, 0, 0, 0.54);
  background: white;
  text-align: center;
  max-width: 290px;
  padding: 10px 14px 0;
  line-height: 17px;
  line-break: loose;
  text-transform: initial !important;
}
.tip{
  margin-top: 15px;
  margin-bottom: 0;
  text-align: left;
  text-transform: uppercase;
  font-size: 11px;
  line-height: 12px;
  color:  #000;
}
.tip-icon{
  padding-top: 0;
  padding-bottom: 0;
  margin: auto;
  text-align: right;
  border-right: solid 1px #000;
}
.tip-icon *{
  color:  #000;
  font-size: 18px !important;
}
.tip-text .v-icon::before{
  color:  #000;
  font-size: 14px !important;
}
.tip-text{
  padding-top: 0;
  padding-bottom: 0;
}

/* Menu container style */
.menu-container {
  background: white !important;
}

</style>
