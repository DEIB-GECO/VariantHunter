<!--
  Component:    Tab
  Description:  Standard tab layout

  Props:
  ├── allLocations: list of all the possible locations. Required.
  └── allLineages: list of all the possible lineages. Required.
-->

<template>
  <div>

    <!-- Analysis definition form -->
    <v-container class="root-container">
      <v-container class="child-container">
        <div class="card-container">

          <v-card :color="secondary_color">
            <v-layout class="card-content" justify-center row wrap>

              <!-- Form header -->
              <v-flex class="xs12 d-flex form-header">
                <h2>DEFINE ANALYSIS</h2>
              </v-flex>

              <!-- Form fields -->
              <slot name="form"></slot>

              <!-- Send button -->
              <v-flex class="xs12 sm6 md12 d-flex form-controls">
                <v-btn :disabled="formError"
                       class="white--text"
                       color="#011936"
                       @click="$emit('send')"
                >
                  <v-icon left>mdi-magnify</v-icon>  START ANALYSIS
                </v-btn>
              </v-flex>
            </v-layout>
          </v-card>
        </div>

      </v-container>
    </v-container>

    <!-- Analysis results -->
    <v-container class="root-container">
      <v-container v-if="resultLength > 0" class="child-container">
        <div ref="result" class="card-container">
          <slot name="results"></slot>
        </div>
      </v-container>
    </v-container>


    <!-- Progress circle -->
    <v-overlay :value="isLoading">
      <v-progress-circular
          indeterminate
          size="64"
      ></v-progress-circular>
    </v-overlay>

    <!-- Error message -->
    <v-overlay :value="errorOccurred">
      <v-container>
        <v-alert dismissible elevation="24" type="error" @input="$emit('closeErrorAlert')">
          <b>The server is temporarily unreachable</b><br/>
          An error occurred while contacting the server. Please try again later.
        </v-alert>
      </v-container>
    </v-overlay>

  </div>
</template>

<script>

import {mapState} from "vuex";

export default {
  name: "Tab",
  props: {
    /** Progress circe flag: true if the progress circle is displayed */
    isLoading: {required: true},

    /** Server error flag */
    errorOccurred: {required: true},

    /** Form error flag: true if the form cannot be sent */
    formError: {required: true},

    /** Result length */
    resultLength: {required: true},
  },
  computed: {
    ...mapState(['secondary_color']),
  },
  watch:{

    /** Whenever a new result is produced, scroll to make it visible */
    resultLength(newLength,oldLength){
      if(newLength>oldLength && this.$refs.result!==undefined)
        this.$refs.result.scrollIntoView();
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
}

/* Form controls styling */
.form-controls {
  margin-top: 26px !important;
  justify-content: center !important;
}

</style>