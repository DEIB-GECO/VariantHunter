<!--

  Component:    FieldSelector
  Description:  Custom select input element

  Props:
  ├── value: Value variable for binding of the value
  ├── label: Label for the field
  ├── placeholder: Placeholder for the selector
  ├── possibleValues: Possible values for the selector
  ├── autocomplete: Autocomplete flag. If true, the selector is a v-autocomplete
  ├── combobox: Combobox flag. If true, the selector is a v-combobox
  ├── highlightPossibleValues: Color flag for the chips. If true, possible values are green and others are red
  ├── multiple: Multiple selector flag. If true, the selector allows multiple selection
  ├── solo: Solo selector flag. If true, changes the style of the input
  ├── loading: Loading selector flag. If true, it displays linear progress bar
  ├── assignId: Id to be assigned to the select element
  └── smallChips: smallChips flag. If true, the selector shows small chips for selected items

  Slots:
  ├── no-data: no-data slot for v-combobox
  └── prepend-item: prepend-item slot for v-combobox or v-autocomplete

-->

<template>
  <v-row>

    <!-- Headings -->
    <v-col v-if='label' cols="12" sm="4">
       <span class="text-body-3 compact-text-3 primary--text d-block text-left text-sm-right align-center">
          <span class="compact-text-5 font-weight-bold">{{ label }}</span>
       </span>
    </v-col>

    <!-- Input element -->
    <v-col cols="12" sm="8" class='field-element'>
      <!-- Manual selector -->
      <v-select v-if='!autocomplete' v-model='selectedValue' :items='possibleValues' no-data-text="Not found"
                hide-details :placeholder='placeholder' solo='solo' :loading='loading'
                attach persistent-placeholder dense flat :id="assignId"/>

      <!-- Combobox selector -->
      <v-combobox v-else-if="combobox" v-model='selectedValue' :items='possibleValues' clearable
                  clear-icon="mdi-backspace-outline" :multiple='multiple'
                  :small-chips='smallChips' hide-details :label='placeholder' :placeholder='placeholder' :solo='solo'
                  :loading='loading' attach dense no-data-text="Not found" flat :id="assignId">

        <template v-slot:prepend-item>
          <slot name='prepend-item'></slot>
        </template>

        <!-- Selection summary -->
        <template v-if='smallChips && multiple' v-slot:selection="{ item, index }">
          <v-chip v-if="index<5" class="mr-1 my-1 font-weight-medium" small :color="getChipColor(item)"
                  :text-color="getTextColor(item)">{{ item }}
          </v-chip>
          <v-tooltip v-else-if="index===5" bottom content-class="rounded-xl" allow-overflow z-index="999"
                     max-width="80vw">
            <template v-slot:activator="{ on, attrs }">
              <v-chip v-on="on" v-bind="attrs" class="mr-1 my-1" small outlined>
                +{{ value.length - 5 }} others
              </v-chip>
            </template>
            Selected values: <br/>
            <v-chip v-for="(value,idx) in selectedValue" :key="idx" class="mr-1 my-1 font-weight-medium" small
                    :color="getChipColor(value)" :text-color="getTextColor(value)">{{ value }}
            </v-chip>
            <div class="mt-5">
              <v-chip x-small class="mr-2 font-weight-medium" text-color='success darken-3' color='success lighten-5'>F O U N D
              </v-chip>
              <v-chip x-small class="mr-2 font-weight-medium" text-color='error darken-3' color='error lighten-5'>A B S E N T
              </v-chip>
            </div>
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
                      :solo='solo' :loading='loading' attach dense no-data-text="Not found" flat :id="assignId">

        <template v-slot:prepend-item>
          <slot name='prepend-item'></slot>
        </template>

        <!-- Selection summary-->
        <template v-if='smallChips && multiple' v-slot:selection="{ item, index }">
          <v-chip v-if="index<5" class="mr-1 my-1 font-weight-medium" small :color="getChipColor(item)"
                  :text-color="getTextColor(item)">{{ item }}
          </v-chip>
          <v-tooltip v-else-if="index===5" bottom content-class="rounded-xl" allow-overflow z-index="999"
                     max-width="80vw">
            <template v-slot:activator="{ on, attrs }">
              <v-chip v-on="on" v-bind="attrs" class="mr-1 my-1" small outlined>
                +{{ value.length - 5 }} others
              </v-chip>
            </template>
            Selected values: <br/>
            <v-chip v-for="(value,idx) in selectedValue" :key="idx" class="mr-1 my-1 font-weight-medium" small
                    :color="getChipColor(value)" :text-color="getTextColor(value)">{{ value }}
            </v-chip>
            <div class="mt-5">
              <v-chip x-small class="mr-2 font-weight-medium" text-color='success darken-3' color='success lighten-5'>F O U N D
              </v-chip>
              <v-chip x-small class="mr-2 font-weight-medium" text-color='error darken-3' color='error lighten-5'>A B S E N T
              </v-chip>
            </div>
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
    label: {},

    /** Placeholder for the selector */
    placeholder: {},

    /** Possible values for the selector */
    possibleValues: {},

    /** Autocomplete flag. If true, the selector is a v-autocomplete */
    autocomplete: Boolean,

    /** Combobox flag. If true, the selector is a v-combobox */
    combobox: Boolean,

    /** Color flag for the chips. If true, possible values are green and others are red */
    highlightPossibleValues: Boolean,

    /** Multiple selector flag. If true, the selector allows multiple selection */
    multiple: Boolean,

    /** Solo flag. If true, the selector has solo style */
    solo: Boolean,

    /** Small-chips flag. If true, the selector shows small chips for selected items */
    smallChips: Boolean,

    /** Boolean loading flag. If true, the selector is loading data */
    loading: Boolean,

    /** Id to be assigned to the select element */
    assignId: undefined,
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
  },

  methods: {
    /** Get chip bg color for the selector */
    getChipColor(value) {
      return this.highlightPossibleValues
          ? this.possibleValues.includes(value) ? "success lighten-5" : "error lighten-5"
          : undefined
    },

    /** Get chip text color for the selector */
    getTextColor(value) {
      return this.highlightPossibleValues
          ? this.possibleValues.includes(value) ? "success darken-3" : "error darken-3"
          : undefined
    }
  }
}
</script>

<style scoped>

/* Form elements styling */
.field-element {
  padding-top: 0 !important;
  padding-bottom: 4px !important;
  text-transform: capitalize;
}
</style>
