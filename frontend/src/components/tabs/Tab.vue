<!--
  Component:    Tab
  Description:  Standard tab layout

  Props:
  ├── isLoading:    Progress circe flag: true if the progress circle is displayed
  ├── visible:      Visibility flag for the tab: true iff this is the current tab
  ├── withLineage:  Flag to show/hide lineage selector.
  └── resultLength: Result length

  Events:
  └── send:    Emitted on form send

  Slots:
  └── results:   The result section
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

              <!-- Form fields -->
              <!---- Location ---->
              <v-flex v-if="selectedGranularity !== 'world'"
                      :class='withLineages? "xs12 sm12 md11 d-flex":"xs12 sm12 md7 d-flex"'>
                <LocationSelector @error='e=> $emit("error",e)' />
              </v-flex>

              <!---- Date ---->
              <v-flex :class='withLineages?"xs12 sm6 md5 d-flex":"xs12 sm6 md4 d-flex"'>
                <DatePicker />
              </v-flex>

              <!---- Lineage ---->
              <v-flex v-if='visible && withLineages'
                      :class="selectedGranularity === 'world'? 'xs12 sm4 md5 d-flex' : 'xs12 sm6 md6 d-flex'">
                <LineageSelector @error='e=> $emit("error",e)' />
              </v-flex>

              <!-- Send button -->
              <v-flex class='xs12 sm6 md3 d-flex form-controls'>
                <v-btn :disabled='formError' class='white--text' :color='primary_color'
                       @click="$emit('send'); showExplorer = false" depressed small>
                  <v-icon left>mdi-magnify</v-icon>
                  ANALYSE
                </v-btn>
                &nbsp;&nbsp;&nbsp;&nbsp;
                <v-btn class='white--text delete-action' :color='primary_color'
                       @click='clearForm(); showExplorer = false' depressed small>
                  <v-icon left>mdi-close</v-icon>
                  CLEAR
                </v-btn>
              </v-flex>

              <!-- Explorer slot-->
              <v-expand-transition v-if='visible'>
                <v-flex v-if='showExplorer' class='xs12 d-flex'>
                  <DatasetExplorer :with-lineages='withLineages' @weekSelection='onWeekSelection'
                                   @error='e=> $emit("error",e)' />
                </v-flex>
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
import LocationSelector from '@/components/form/LocationSelector'
import DatePicker from '@/components/form/DatePicker'
import LineageSelector from '@/components/form/LineageSelector'
import { mapStateTwoWay } from '@/utils/bindService'
import DatasetExplorer from '@/components/DatasetExplorer'

export default {
  name: 'Tab',
  components: { DatasetExplorer, LineageSelector, DatePicker, LocationSelector },
  props: {
    /** Visibility flag for the tab: true iff this is the current tab */
    visible: Boolean,

    /** Progress circe flag: true if the progress circle is displayed */
    isLoading: { required: true },

    /** Result length */
    resultLength: { required: true },

    /** Flag to show/hide lineage selector. */
    withLineages: Boolean
  },
  data () {
    return {
      /** Visibility flag for the DatasetExplorer */
      showExplorer: false
    }
  },
  computed: {
    ...mapState(['primary_color', 'secondary_color']),
    ...mapStateTwoWay({
      selectedGranularity: 'SET_GRANULARITY',
      selectedLocation: 'SET_LOCATION',
      selectedDate: 'SET_END_DATE',
      selectedLineage: 'SET_LINEAGE'
    }),

    /** Form error flag: true if the form cannot be sent */
    formError () {
      if (this.withLineages) {
        return !(
          (this.selectedGranularity === 'world' && this.selectedDate !== null && this.selectedLineage !== null) ||
          (this.selectedGranularity !== null && this.selectedLocation !== null && this.selectedDate !== null && this.selectedLineage !== null)
        )
      } else {
        return !(
          (this.selectedGranularity === 'world' && this.selectedDate != null) ||
          (this.selectedGranularity !== null && this.selectedLocation !== null && this.selectedDate !== null)
        )
      }
    }
  },
  methods: {
    /** Clears the form */
    clearForm () {
      this.selectedDate = null
      this.selectedLocation = null
      this.selectedGranularity = null
      this.selectedLineage = null
    },

    /**
     * Handler for weekSelection event from Dataset Explorer
     * @param range The selected range
     */
    onWeekSelection (range) {
      this.showExplorer = false
      document.getElementById('top').scrollIntoView()
      this.selectedDate = range
      if (!this.formError) {
        this.$emit('send')
      }
    }
  },
  watch: {
    visible (newVal) {
      if (!newVal) {
        this.showExplorer = false
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
.single-tab {
  min-height: 740px;
}

@media only screen and  (max-width: 599px) {
  .single-tab {
    min-height: 835px !important; /* Prevent datepicker to overflow */
  }
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

.delete-action:hover{
  background-color: red !important;
  border-color: red !important;
}
</style>
