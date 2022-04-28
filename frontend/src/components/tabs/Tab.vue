<!--
  Component:    Tab
  Description:  Standard tab layout

  Props:
  ├── isLoading:    Progress circe flag: true if the progress circle is displayed
  ├── formError:    Form error flag: true if the form cannot be sent
  └── resultLength: Result length

  Events:
  └── send:    Emitted on form send

  Slots:
  ├── form:       The tab form fields
  └── explorer:   The explorer section
-->

<template>
  <div class='single-tab'>

    <!-- Analysis definition form -->
    <v-container class='root-container'>
      <v-container class='child-container'>
        <div class='card-container'>
          <v-card :color='secondary_color'>
            <v-layout class='card-content' justify-center row wrap>

              <!-- Form header -->
              <v-flex class='xs12 d-flex form-header'>
                <h2>
                  DEFINE ANALYSIS
                </h2>
              </v-flex>

              <!-- Form fields slot -->
              <slot name='form'></slot>

              <!-- Send button -->
              <v-flex class='xs12 sm6 md3 d-flex form-controls'>
                <v-btn :disabled='formError' class='white--text' color='#011936'
                       @click="$emit('send'); showExplorer = false">
                  <v-icon left>mdi-magnify</v-icon>
                  START ANALYSIS
                </v-btn>
              </v-flex>

              <!-- Explorer slot-->
              <v-expand-transition>
                <slot v-if='showExplorer' name='explorer'></slot>
              </v-expand-transition>

              <!-- Show/hide Explorer controls -->
              <v-flex v-if='!showExplorer' justify-center class='xs12 d-flex'>
                <v-btn outlined depressed rounded small color='white'
                       @click='showExplorer = !showExplorer'>
                  <v-icon left>mdi-compass</v-icon>
                  Show dataset explorer
                </v-btn>
              </v-flex>
              <v-flex v-if='showExplorer' justify-center class='xs12 d-flex pt-0'>
                <v-btn outlined depressed rounded small color='white'
                       @click='showExplorer = !showExplorer'>
                  <v-icon left>mdi-close-circle-outline</v-icon>
                  Hide
                </v-btn>
              </v-flex>
            </v-layout>
          </v-card>
        </div>
      </v-container>
    </v-container>

    <!-- Analysis results -->
    <v-container class='root-container'>
      <v-container v-if='resultLength > 0' class='child-container'>
        <div class='card-container'>
          <slot name='results'></slot>
        </div>
      </v-container>
    </v-container>

    <!-- Progress circle -->
    <v-overlay :value='isLoading'>
      <v-progress-circular indeterminate size='64'></v-progress-circular>
    </v-overlay>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'Tab',
  props: {
    /** Value variable for binding of the visibility flag for the Dataset Explorer */
    value: {},

    /** Progress circe flag: true if the progress circle is displayed */
    isLoading: { required: true },

    /** Form error flag: true if the form cannot be sent */
    formError: { required: true },

    /** Result length */
    resultLength: { required: true }
  },
  computed: {
    ...mapState(['secondary_color']),

    /** Flag to show/hide the explorer */
    showExplorer: {
      get () {
        return this.value
      },
      set (value) {
        this.$emit('input', value)
      }
    }
  }
}
</script>

<style scoped>
/* Root tab container styling */
.root-container {
  margin: 0 auto auto auto;
  min-width: 97vw;
  height: 100%;
}

/* Ensure datepicker menu visibility */
.single-tab{
  min-height: 750px;
}

/* Child tab container styling */
.child-container {
  background-color: var(--primary-color);
  border-radius: 8px;
  margin-top: 15px;
  margin-bottom: 0;
  min-width: 96vw;
}

/* Form container styling */
.card-container {
  margin: 15px auto;
  justify-content: center;
  padding: 15px 1vw 15px 1vw;
}

/* Form content styling */
.card-content {
  padding: 30px;
  margin: auto;
}

/* Headings */
.form-header {
  color: white;
  justify-content: center;
  text-align: center;
  margin-bottom: 15px;
}

.form-header h2 {
  font-weight: 800;
  border-bottom: solid 4px white;
  word-spacing: 5px;
}

/* Form controls styling */
.form-controls {
  margin-top: 29px !important;
  justify-content: center !important;
}
</style>
