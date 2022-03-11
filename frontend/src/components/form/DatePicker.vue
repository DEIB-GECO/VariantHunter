<!--
  Component:    DatePicker
  Description:  Select input element with embedded date picker

  Props:
  └── value: Value variable for binding of the date
-->

<template>
  <v-layout justify-center row wrap>

    <!-- Label -->
    <v-flex class="xs12 d-flex field-label">
      <span>Date</span>
    </v-flex>

    <!-- Picker -->
    <v-flex class="xs12 d-flex field-element">
      <v-menu v-model="menuVisibility"
              :close-on-content-click="false"
              min-width="auto"
              offset-y
              transition="scale-transition">
        <template v-slot:activator="{ on, attrs }">
          <v-text-field v-model="selectedDate"
                        append-icon="mdi-calendar"
                        hide-details
                        label="Date"
                        readonly
                        clearable
                        solo
                        v-bind="attrs"
                        v-on="on"
                        @click:append="menuVisibility=true"
          />
        </template>
        <v-date-picker v-model="selectedDate"
                       :max="today"
                       first-day-of-week="1"
                       no-title
                       scrollable
                       @input="menuVisibility=false"
        />
      </v-menu>
    </v-flex>
  </v-layout>
</template>

<script>

export default {
  name: "DatePicker",
  props: {
    /** Value variable for binding of the date */
    value: {type: String}
  },
  data() {
    return {
      /** Visibility flag of date picker menu */
      menuVisibility: false,

      /** Today date */
      today: new Date().toISOString().slice(0, 10),
    }
  },
  computed: {

    /** Selected date */
    selectedDate: {
      /**
       * Getter for the string representing the selected date
       * @returns {string}  The selected date
       */
      get() {
        return this.value
      },

      /**
       * Setter for the date
       * @param val The new value
       */
      set(val) {
        this.$emit('input', val)
      }
    }
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

/* Form controls styling */
.form-controls {
  margin-top: 26px !important;
  justify-content: center !important;
}

/* Result list styling */
.result-list {
  margin-bottom: 20px;
}

.result-list span {
  text-transform: capitalize;
  font-size: 17px;
  color: white;
  letter-spacing: 1px;
}

.result-list span b {
  text-transform: none;
}

v-expansion-panel-header {
  border-radius: var(--border-radius);
}

/* No result message styling */
.empty-result-alert {
  text-align: center;
  margin-top: 40px;
  margin-bottom: 20px;
  font-size: 17px;
  color: white !important;
  letter-spacing: 1px;
  line-height: 10px;
}

</style>