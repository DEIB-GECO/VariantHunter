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
  ├── solo: Solo selector flag. If true, changes the style of the input
  ├── loading: Loading selector flag. If true, it displays linear progress bar
  └── smallChips: smallChips flag. If true, the selector shows small chips for selected items

  Slots:
  └── prepend-item: prepend-item slot for v-autocomplete. Only if autocomplete flag is true.
-->

<template>
  <v-row>
    <v-col cols="12" sm="4" v-if='label'>
       <span class="text-body-3 compact-text-3 primary--text d-block text-left text-sm-right align-center">
          <span class="compact-text-5 font-weight-bold">{{ label }}</span>
       </span>
    </v-col>

    <v-col cols="12" sm="8" class='field-element'>
      <!-- Manual selector -->
      <v-select v-if='!autocomplete' v-model='selectedValue' :items='possibleValues' no-data-text="Not found"
                hide-details :placeholder='placeholder' solo='solo' :loading='loading'
                attach persistent-placeholder dense flat/>

      <!-- Combobox selector -->
      <v-combobox v-else-if="combobox" v-model='selectedValue' :items='possibleValues' clearable
                  clear-icon="mdi-backspace-outline" :multiple='multiple'
                  :small-chips='smallChips' hide-details :label='placeholder' :placeholder='placeholder' :solo='solo'
                  :loading='loading' attach dense no-data-text="Not found" flat>

        <template v-slot:prepend-item>
          <slot name='prepend-item'></slot>
        </template>

        <template v-if='smallChips && multiple' v-slot:selection="{ item, index }">
          <v-chip v-if="index<5" class="mr-1 my-1" small>{{ item }}</v-chip>
          <v-tooltip v-else-if="index===5" bottom content-class="rounded-xl" allow-overflow z-index="999" max-width="80vw">
            <template v-slot:activator="{ on, attrs }">
              <v-chip v-on="on" v-bind="attrs"  class="mr-1 my-1" small outlined>
            +{{ value.length - 5 }} others
          </v-chip>
            </template>
            Selected values: <br/>
            <v-chip v-for="(value,idx) in selectedValue" :key="idx" class="mr-1 my-1" small>{{ value }}</v-chip>
          </v-tooltip>
        </template>

        <template v-slot:no-data>
          <slot name="no-data"></slot>
        </template>

      </v-combobox>

      <!-- Autocomplete selector -->
      <v-autocomplete v-else v-model='selectedValue' :items='possibleValues' clearable
                      clear-icon="mdi-backspace-outline" :multiple='multiple'
                      :small-chips='smallChips' hide-details :label='placeholder' :placeholder='placeholder'
                      :solo='solo' :loading='loading' attach dense no-data-text="Not found" flat>

        <template v-slot:prepend-item>
          <slot name='prepend-item'></slot>
        </template>

        <template v-if='smallChips && multiple' v-slot:selection="{ item, index }">
          <v-chip v-if="index<5" class="mr-1 my-1" small>{{ item }}</v-chip>
          <v-tooltip v-else-if="index===5" bottom content-class="rounded-xl" allow-overflow z-index="999" max-width="80vw">
            <template v-slot:activator="{ on, attrs }">
              <v-chip v-on="on" v-bind="attrs"  class="mr-1 my-1" small outlined>
            +{{ value.length - 5 }} others
          </v-chip>
            </template>
            Selected values: <br/>
            <v-chip v-for="(value,idx) in selectedValue" :key="idx" class="mr-1 my-1" small>{{ value }}</v-chip>
          </v-tooltip>
        </template>

      </v-autocomplete>

    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'FieldSelector',
  props: {
    /** Value variable for binding of the value */
    value: {},

    /** Label for the field */
    label: {required: false},

    /** Placeholder for the selector */
    placeholder: {required: true},

    /** Possible values for the selector */
    possibleValues: {required: true},

    /** Autocomplete flag. If true, the selector is a v-autocomplete */
    autocomplete: Boolean,

    combobox: Boolean,

    /** Multiple selector flag. If true, the selector allows multiple selection */
    multiple: Boolean,

    /** Solo flag. If true, the selector has solo style */
    solo: Boolean,

    /** smallChips flag. If true, the selector shows small chips for selected items */
    smallChips: Boolean,

    /** loading flag. If true, the selector is loading data */
    loading: Boolean,
  },
  computed: {
    /** Selected value */
    selectedValue: {
      /**
       * Getter for the string representing the selected value
       * @returns {string}  The selected value
       */
      get() {
        return this.value
      },

      /**
       * Setter for the value
       * @param val The new value
       */
      set(val) {
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
