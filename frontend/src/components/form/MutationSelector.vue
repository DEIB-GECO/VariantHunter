<!--
  Component:    MutationSelector
  Description:  Advanced filter for the mutations

  Props:
  ├── value:              Value variable for binding of the value
  ├── possibleValues:     Possible values for the selector
  └── characterizingMuts: Object storing the characterizing mutations (lin.spec. only)

  Events:
  └── error:    Emitted on server errors
-->

<template>
  <!-- Decorated Field Selector -->
  <FieldSelector v-model='selectedValue' label='Mutations' placeholder='All'
                 :possible-values='possibleValues' autocomplete small-chips
                 multiple solo combobox>

    <template v-slot:prepend-item>

      <!-- List uploader opener -->
      <div class='uploader-opener text-body-3 text_var3--text font-weight-bold' @click='showListUploader=true'>
        <v-icon left>mdi-file-edit-outline</v-icon>
        Open advanced editor
      </div>

      <!-- Lineage selector opener -->
      <div class='uploader-opener text-body-3 text_var3--text font-weight-bold' @click='showLineageSelector=true'>
        <v-icon left>mdi-shape-outline</v-icon>
        Select from lineages
      </div>

      <!-- Non characterizing mutation selector -->
      <div v-if="characterizingMuts && characterizingMuts.length!==possibleValues.length"
           class='uploader-opener text-body-3 text_var3--text font-weight-bold' @click='selectNonCharMuts()'>
        <v-icon left>mdi-star-off-outline</v-icon>
        All non-characterizing mutations
      </div>

      <!-- List uploader element-->
      <v-dialog v-model='showListUploader' max-width='850' transition='dialog-bottom-transition'>
        <v-card>
          <!-- Dialog title -->
          <v-toolbar color='f_primary' class='dialog-title' dark flat>
            <v-icon left large>mdi-file-upload-outline</v-icon>
            Select mutations from list
          </v-toolbar>

          <!-- Dialog content -->
          <v-card-text class='text-s-center dialog-text'>
            <v-container fluid>
              <v-row>

                <!-- Help info -->
                <v-col cols='12'>
                  Please, write here the list of mutations to be filtered.
                  The list will be automatically parsed to fill in the filter. See the example below.
                </v-col>

                <!-- Separator selector -->
                <v-col cols='12'>
                  <v-text-field v-model='selectedSeparator' label='Separator' :rules='rules' hide-details='auto'
                                :loading='processing' outlined dense @input='parseMutationList'/>
                </v-col>

                <!-- List uploader -->
                <v-col cols='12'>
                  <v-textarea v-model='uploadedList' label='List content' auto-grow outlined rows='4' row-height='20'
                              clearable dense :loading='processing' hide-details='auto' :error-messages='errorMessages'
                              :success-messages='successMessages' @input='parseMutationList'/>
                </v-col>

                <v-col cols="12">
                  <v-checkbox v-model="excludeAbsent" dense @click="parseMutationList">
                    <template v-slot:label>
                      <v-tooltip bottom max-width="400px" allow-overflow>
                        <template v-slot:activator="{on, attrs}">
                          <span v-on="on" v-bind="attrs" class="text-body-5 text-uppercase">
                            Exclude absent mutations</span>
                        </template>
                        <div class="mb-2">
                          If active, mutations not present in the current analysis will not be considered.
                        </div>
                        <span class="text-decoration-underline">In case of global scope filtering</span> this implies
                        that only mutations present in this analysis will be considered for the other analyses too.
                        Disable to consider them all.
                      </v-tooltip>
                    </template>
                  </v-checkbox>
                </v-col>

                <!-- Examples section -->
                <v-col cols='12'>
                  Example:
                  <code>M_A63T {{ selectedSeparator ? selectedSeparator : ';' }} M_D3G
                    {{ selectedSeparator ? selectedSeparator : ';' }} M_I76V</code> or
                  <code>M:A63T {{ selectedSeparator ? selectedSeparator : ';' }} M:D3G
                    {{ selectedSeparator ? selectedSeparator : ';' }} M:I76V</code>
                </v-col>

                <!-- Parsed result -->
                <v-col v-if='parsedList.length>0' cols='12'>

                  <v-chip v-for='elem in parsedList' :key='elem' class="mr-1 mb-1"
                          :text-color='possibleValues.includes(elem)?"green":"red"'
                          :color='possibleValues.includes(elem)?"green lighten-5":"red lighten-5"'>{{ elem }}
                  </v-chip>

                </v-col>
              </v-row>
            </v-container>
          </v-card-text>

          <!-- Dialog actions -->
          <v-card-actions class='justify-end'>
            <v-btn text @click='showListUploader = false'>
              Done
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Lineage selector element-->
      <v-dialog v-model='showLineageSelector' max-width='850' transition='dialog-bottom-transition'>
        <v-card>
          <!-- Dialog title -->
          <v-toolbar color='f_primary' class='dialog-title' dark flat>
            <v-icon left large>mdi-shape-outline</v-icon>
            Select mutations from lineages
          </v-toolbar>

          <!-- Dialog content -->
          <v-card-text class='text-s-center dialog-text lineage-selector-dialog'>
            <v-container fluid>
              <v-row>

                <!-- Help info -->
                <v-col cols='12'>
                  Please, select the lineages to filter the mutations.
                </v-col>

                <!-- Lineage selector -->
                <v-col cols="12" class="my-0 py-0">
                  <field-selector v-model='selectedLineages' :possible-values='possibleLineages' placeholder='Lineages'
                                  :loading='processing' solo autocomplete multiple small-chips
                                  @input='manageLineageSelection'/>
                </v-col>
                <v-col cols="12">
                  <v-checkbox v-model="excludeAbsent" dense @click="manageLineageSelection">
                    <template v-slot:label>
                      <v-tooltip bottom max-width="400px" allow-overflow>
                        <template v-slot:activator="{on, attrs}">
                          <span v-on="on" v-bind="attrs" class="text-body-5 text-uppercase">
                            Exclude absent mutations</span>
                        </template>
                        <div class="mb-2">
                          If active, mutations not present in the current analysis will not be considered.
                        </div>
                        <span class="text-decoration-underline">In case of global scope filtering</span> this implies
                        that only mutations present in this analysis will be considered for the other analyses too.
                        Disable to consider them all.
                      </v-tooltip>
                    </template>
                  </v-checkbox>
                </v-col>

                <!-- Result -->
                <v-col cols='12' v-if='allLinMuts.length>0'>
                  <div class="text-body-3 my-2"> Mutation report:</div>
                  <v-chip x-small class="mb-5 mr-2" text-color='green' color='green lighten-5'>PRESENT MUTATION</v-chip>
                  <v-chip x-small class="mb-5 mr-2" text-color='red' color='red lighten-5'>ABSENT MUTATION</v-chip>
                  <br/>
                  <v-chip v-for='elem in allLinMuts' :key='elem' class="mr-1 mb-1"
                          :text-color='possibleValues.includes(elem)?"green":"red"'
                          :color='possibleValues.includes(elem)?"green lighten-5":"red lighten-5"'>
                    {{ elem }}
                  </v-chip>
                </v-col>

                <!-- Additional info -->
                <v-col cols="12">
                  <v-row no-gutters>
                    <v-col cols='1' class='mt-4'>
                      <v-icon small left>mdi-information-outline</v-icon>
                    </v-col>
                    <v-col cols='11' class='mt-4'>
                      <span>
                        The characterizing mutations are identified as those that are
                        present in at least 50% of the lineage sequences.
                      </span>
                    </v-col>
                  </v-row>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>

          <!-- Dialog actions -->
          <v-card-actions class='justify-end'>
            <v-btn text @click='showLineageSelector = false'>
              Apply
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </template>

    <template v-slot:no-data>
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="break-spaces mt-2 error--text">
            Mutation not present in the current analysis. <br/>
            Press <kbd>enter</kbd> to add anyway.
          </v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </template>
  </FieldSelector>
</template>

<script>
import FieldSelector from '@/components/form/FieldSelector'

export default {
  name: 'MutationSelector',
  components: {FieldSelector},
  props: {
    /** Value variable for binding of the value */
    value: {},

    /** Possible values for the selector */
    possibleValues: {required: true},

    /** Object storing the characterizing mutations (lin.spec. only) */
    characterizingMuts: {required: false}
  },
  data() {
    return {
      /** List uploader visibility */
      showListUploader: false,

      /** excludeAbsent: true iff absent muts must be excluded */
      excludeAbsent: false,

      /** Processing flag. If true, the list is being parsed. */
      processing: false,

      /** Error messages for the parsing */
      errorMessages: [],

      /** Success messages for the parsing */
      successMessages: [],

      /** Currently selected separator */
      selectedSeparator: ',',

      /** Rules for the separators */
      rules: [
        value => !!value || 'Required.',
        value => (value && value[0] !== '_' && value[0] !== ':') || 'This separator is not allowed',
        value => (value && !(value[0] <= 9 && value[0] >= 0)) || 'The separator cannot be a number',
        value => (value && !(value[0] <= 'Z' && value[0] >= 'A')) || 'The separator cannot be a letter',
        value => (value && !(value[0] <= 'z' && value[0] >= 'a')) || 'The separator cannot be a letter'
      ],

      /** Value for the uploaded list content*/
      uploadedList: '',

      /** Array representing the parsed list content*/
      parsedList: [],

      /** Lineage uploader visibility */
      showLineageSelector: false,

      /** The selectable lineages */
      possibleLineages: [],

      /** The selected lineages */
      selectedLineages: [],

      /** The mutations that correspond to the selected lineages */
      allLinMuts: [],

      /** The mutations that correspond to the selected lineages and are allowed values */
      selectedLinMuts: []
    }
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
    /**
     * Perform the parsing of the uploadedList
     */
    parseMutationList() {
      let count = 0
      this.errorMessages = []
      this.successMessages = []

      if (this.selectedSeparator !== '' && this.uploadedList !== null) {
        try {
          this.processing = true

          // Split, trim, remove duplicates and eventually replace _ with : as separator between prot and mut
          let values = this.uploadedList.split(this.selectedSeparator).map(x => x.trim()).map(x => x.replace(/:/, '_'))
          values = values.filter((x, index) => x !== '' && values.indexOf(x) === index)

          // Eventually filter the possible ones in the context only.
          this.parsedList = this.excludeAbsent
              ? this.possibleValues.filter((x) => values.includes(x))
              : values

          count = this.parsedList.length
          this.successMessages = ['Parsing completed. Found ' + (count) + ' valid mutations.']
          this.$emit('input', this.parsedList)

        } catch (e) {
          this.errorMessages = ['Invalid input. (Details – ' + e.toString() + ')']
        } finally {
          this.processing = false
        }
      } else {
        this.parsedList = []
      }
    },

    /** Fetch the possible lineages*/
    fetchLineages() {
      if (this.possibleLineages.length === 0) {
        this.processing = true
        const url = `/lineage_specific/getLineages`
        this.$axios
            .get(url, {params: {location: undefined, date: undefined}})
            .then(res => {
              this.possibleLineages = res.data
            })
            .catch((e) => {
              this.$emit('error', e)
            })
            .finally(() => {
              this.processing = false
            })
      }
    },

    /**
     * Perform the selection of the mutations based on the lineages
     */
    manageLineageSelection() {
      this.allLinMuts = []
      this.selectedLinMuts = []

      if (this.selectedLineages.length > 0) {
        this.processing = true
        const classificationAPI = `/explorer/getLineagesCharacteristics`
        const queryParams = new URLSearchParams(); // avoid [] conversion of parameter
        this.selectedLineages.forEach(name => queryParams.append("lineages", name))

        this.$axios
            .get(classificationAPI, {params: queryParams})
            .then(res => {
              this.allLinMuts = res.data

              //  Eventually filter and emit update
              this.selectedLinMuts = this.excludeAbsent
                  ? this.possibleValues.filter((x) => this.allLinMuts.includes(x))
                  : this.allLinMuts
              this.$emit('input', this.selectedLinMuts)
            })
            .catch((e) => {
              this.$emit('error', e)
            })
            .finally(() => {
              this.processing = false
            })
      }
    },

    /**
     * Select the non characterizing mutations
     */
    selectNonCharMuts() {
      const nonCharMuts = this.possibleValues.filter((x) => !this.characterizingMuts.includes(x))
      this.$emit('input', nonCharMuts)
    }
  },
  watch: {
    /** On uploader close apply filter parsing */
    showListUploader(newVal) {
      if (!newVal) {
        this.parseMutationList()
      }
    },

    /** On uploader open fetch the lineages */
    showLineageSelector(newVal) {
      if (newVal) {
        this.fetchLineages()
      }
    }
  }
}
</script>

<style scoped>
.uploader-opener {
  color: rgba(0, 0, 0, 0.54);
  padding: 5px 14px;
  text-transform: initial;
  cursor: pointer;
}

.uploader-opener:hover {
  background-color: rgba(0, 0, 0, 0.04);
}

.lineage-selector-dialog {
  min-height: 400px;
}
</style>
