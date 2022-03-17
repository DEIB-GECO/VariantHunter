<!--
  Component:    FieldSelector
  Description:  Custom select input element

  Props:
  ├── value: Value variable for binding of the value
  ├── label: Label for the field
  ├── placeholder: Placeholder for the selector
  ├── possibleValues: Possible values for the selector
  ├── autocomplete: Autocomplete flag. If true, the selector is a v-autocomplete
  ├── multiple: Multiple selector flag. If true, the selector allows multiple selection
  └── smallChips: smallChips flag. If true, the selector shows small chips for selected items

  Slots:
  └── prepend-item: prepend-item slot for v-autocomplete. Only if autocomplete flag is true.
-->

<template>
  <v-layout row wrap>
    <v-flex class='xs12 d-flex field-label'>
      <span>{{ label }}</span>
    </v-flex>

    <v-flex class='xs12 d-flex field-element'>
      <!-- Manual selector -->
      <v-select v-if='!autocomplete' v-model='selectedValue' :items='possibleValues' hide-details :label='placeholder'
                attach solo />

      <!-- Autocomplete selector -->
      <v-autocomplete v-else v-model='selectedValue' :items='possibleValues' clearable :multiple='multiple'
                      :small-chips='smallChips' hide-details :label='placeholder' attach solo>
        <template v-slot:prepend-item>
          <slot name='prepend-item'></slot>
        </template>
      </v-autocomplete>

    </v-flex>
  </v-layout>
</template>

<script>
export default {
  name: 'FieldSelector',
  props: {
    /** Value variable for binding of the value */
    value: {},

    /** Label for the field */
    label: { required: true },

    /** Placeholder for the selector */
    placeholder: { required: true },

    /** Possible values for the selector */
    possibleValues: { required: true },

    /** Autocomplete flag. If true, the selector is a v-autocomplete */
    autocomplete: { default: false },

    /** Multiple selector flag. If true, the selector allows multiple selection */
    multiple: { default: false },

    /** smallChips flag. If true, the selector shows small chips for selected items */
    smallChips: { default: false }
  },
  computed: {
    /** Selected value */
    selectedValue: {
      /**
       * Getter for the string representing the selected value
       * @returns {string}  The selected value
       */
      get () {
        return this.value
      },

      /**
       * Setter for the value
       * @param val The new value
       */
      set (val) {
        this.$emit('input', val)
      }
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
