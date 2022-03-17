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
            <v-container v-if='false' fluid>
              <v-row>
                <v-col cols='12'>
                  Please, paste here the list of mutation to be filtered. <br />
                  The list will be automatically parsed to fill in the filter.
                </v-col>
                <v-col cols='12'>
                  <v-text-field v-model='selectedSeparator' label='Separator' :rules='rules' hide-details='auto'
                                outlined dense />
                </v-col>
                <v-col cols='12'>
                  <v-textarea label='File content' auto-grow outlined rows='4' row-height='20' clearable dense @input='checkUploaded' />
                </v-col>
              </v-row>
            </v-container>
            <v-container fluid>
              <v-row>
                <v-col cols='12'>
                  This feature is not yet available
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

      selectedSeparator: ',',

      rules: [
        value => !!value || 'Required.',
        value => (value && value.length === 1) || 'The separator must be only one character long'
      ]
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
    checkUploaded () {

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
