<template>
  <!-- Decorated Field Selector -->
  <FieldSelector v-model='selectedValue' label='Mutation' placeholder='All'
                 :possible-values='possibleValues' :autocomplete='true' :small-chips='true'
                 :multiple='true'>

    <template v-slot:prepend-item>

      <!-- Uploader opener -->
      <div class='uploader-opener' @click='showUploader=true'>
        <v-icon left>mdi-file-upload-outline</v-icon>
        Upload from file
      </div>

      <!-- Uploader element-->
      <v-dialog v-model='showUploader' max-width='500' transition='dialog-bottom-transition'>
        <v-card>
          <!-- Dialog title -->
          <v-toolbar :color='primary_color' class='dialog-title' dark flat>
            <v-icon left>mdi-file-upload-outline</v-icon>
            Upload mutations from file
          </v-toolbar>

          <!-- Dialog content -->
          <v-card-text class='text-s-center dialog-text'>
            <v-container fluid>
              <v-row>

                <!-- Help info -->
                <v-col cols='12'>
                  Please, paste here the list of mutations to be filtered. <br />
                  The list will be automatically parsed to fill in the filter.
                </v-col>

                <!-- Separator selector -->
                <v-col cols='12'>
                  <v-text-field v-model='selectedSeparator' label='Separator' :rules='rules' hide-details='auto'
                                :loading='processing' outlined dense />
                </v-col>

                <!-- File uploader -->
                <v-col cols='12'>
                  <v-textarea v-model='uploadedFile' label='File content' auto-grow outlined rows='4' row-height='20'
                              clearable dense :loading='processing' hide-details='auto' :error-messages='errorMessages'
                              @input='parseFile' />
                </v-col>

                <!-- Example section -->
                <v-col cols='12'>
                  For example:
                  <code>M_A63T {{ selectedSeparator ? selectedSeparator : ';' }} M_D3G
                    {{ selectedSeparator ? selectedSeparator : ';' }} M_I76V</code>
                </v-col>

                <!-- Parsed result -->
                <v-col v-if='parsedFile' cols='12'>

                  <v-chip v-for='elem in parsedFile' :key='elem'>{{ elem }}</v-chip>

                </v-col>
              </v-row>
            </v-container>
          </v-card-text>

          <!-- Dialog actions -->
          <v-card-actions class='justify-end'>
            <v-btn text @click='showUploader = false'>
              Done
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

    </template>
  </FieldSelector>
</template>

<script>
import FieldSelector from '@/components/form/FieldSelector'
import { mapState } from 'vuex'

export default {
  name: 'MutationSelector',
  components: { FieldSelector },
  props: {
    /** Value variable for binding of the value */
    value: {},

    /** Possible values for the selector */
    possibleValues: { required: true }
  },
  data () {
    return {
      /** Uploader visibility */
      showUploader: false,

      /** Processing flag. If true, the file is being parsed. */
      processing: false,

      /** Error messages for the parsing */
      errorMessages: [],

      /** Currently selected separator */
      selectedSeparator: ',',

      /** Rules for the separators */
      rules: [
        value => !!value || 'Required.',
        value => (value && value.length === 1) || 'The separator must be only one character long',
        value => (value && value[0] !== '_') || 'This separator is not allowed',
        value => (value && !(value[0] <= 9 && value[0] >= 0)) || 'The separator cannot be a number',
        value => (value && !(value[0] <= 'Z' && value[0] >= 'A')) || 'The separator cannot be a letter',
        value => (value && !(value[0] <= 'z' && value[0] >= 'a')) || 'The separator cannot be a letter'
      ],

      /** Value for the uploaded file content*/
      uploadedFile: '',

      /** Array representing the parsed file content*/
      parsedFile: []
    }
  },
  computed: {
    ...mapState(['primary_color']),

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
  },
  methods: {
    /**
     * Perform the parsing of the uploadedFile
     * @returns {number}  Number of elements correctly parsed
     */
    parseFile () {
      let count = 0
      if (this.selectedSeparator !== '' && this.uploadedFile != null) {
        try {
          this.processing = true
          this.errorMessages = []
          const values = this.uploadedFile.split(this.selectedSeparator).map(x => x.trim())
          this.parsedFile = values.filter((x, index) => x !== '' && values.indexOf(x) === index)
          count = this.parsedFile.length
        } catch (e) {
          this.errorMessages = ['Invalid input. (Details – ' + e.toString() + ')']
        }
        this.processing = false
      } else {
        this.parsedFile = []
      }
      return count
    }
  },
  watch: {
    /** On uploader close apply filter parsing */
    showUploader (newVal) {
      if (!newVal) {
        const valCount = this.parseFile()
        if (valCount > 0) {
          this.$emit('input', this.parsedFile)
        }
      }
    }
  }
}
</script>

<style scoped>
.uploader-opener {
  text-align: center;
  padding: 10px 14px;
}
</style>
