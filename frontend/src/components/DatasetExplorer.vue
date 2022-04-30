<!--
  Component:    DatasetExplorer
  Description:  Component to explore the number of sequences available in the dataset

  Props:
  └── withLineages: Flag for lineage search

  Events:
  ├── weekSelection:  Emitted when the user select the 4 weeks to analyze
  └── error:          Emitted on server errors
-->

<template>
  <v-layout justify-center row wrap>
    <template>
      <!-- Heading -->
      <v-flex class='xs12 d-flex main-label'>
        <span>Dataset Explorer</span>
      </v-flex>

      <!-- Label -->
      <v-flex class='xs12 d-flex sub-label'>
        <span>{{ title }}</span>
      </v-flex>

      <!-- Histogram loading animation -->
      <v-flex v-if='isLoading.histogram' class='xs12 sm12 md11 d-flex'>
        <v-skeleton-loader width='100%' type='image' />
      </v-flex>

      <!-- Histogram plot -->
      <v-flex v-if='showPlot.histogram' class='xs12 sm12 md11 d-flex explorer-element'>
        <ExplorerHistogram :sequence-data='sequencesData' @timeRangeChange='(tr) => onTimeRangeChanges(tr)' />
      </v-flex>

      <!-- Breakdown loading animation -->
      <v-flex v-if='isLoading.breakdown' class='xs12 sm12 md11 d-flex'>
        <v-skeleton-loader width='100%' type='image' />
      </v-flex>

      <v-flex v-if='isDisabled.breakdown' class='xs12 sm12 md11 d-flex disabled-label mb-2'>
        <sub>
          <v-icon color='white' small left>mdi-information-outline</v-icon>
          Reduce the time range to at most 4 weeks to see lineages breakdown </sub>
      </v-flex>

      <!-- Breakdown plot -->
      <v-flex v-if='showPlot.breakdown' class='xs12 sm12 md11 d-flex explorer-element lineage-breakdown'>
        <LineagesBreakdown :lineages-data='lineagesData' />
      </v-flex>
    </template>

    <!-- Button to fill in the date -->
    <v-flex v-if='showPlot.breakdown' justify-center class='xs12 d-flex'>
      <v-btn outlined depressed rounded small color='white'
             @click.native='emitAnalysisPeriod()'>
        <v-icon left>mdi-calendar</v-icon>
        <v-tooltip bottom max-width='400' color="white" open-delay='0'>
          <template v-slot:activator="{ on, attrs }">
            <span v-bind="attrs" v-on="on">
              Consider these 4 weeks
            </span>
          </template>
          <span style='color: rgb(68, 68, 68)'>Fill the form using the currently selected 4 weeks as analysis period. </span>
        </v-tooltip>
      </v-btn>
    </v-flex>

  </v-layout>
</template>

<script>
import ExplorerHistogram from '@/components/plots/ExplorerHistogram'
import axios from 'axios'
import LineagesBreakdown from '@/components/plots/LineagesBreakdown'
import { dateDiff } from '@/utils/dateService'
import { mapState } from 'vuex'

export default {
  name: 'DatasetExplorer',
  components: { LineagesBreakdown, ExplorerHistogram },
  props: {
    /** Flag for lineage search. */
    withLineages: Boolean
  },
  data () {
    return {
      /** Loading flag. If true data are being fetched */
      isLoading: {
        histogram: false,
        breakdown: false
      },

      /** Disabled plot flag. If true plot is disabled */
      isDisabled: {
        breakdown: false
      },

      /** Array of sequence info  from the server */
      sequencesData: [],

      /** Array of lineages breakdown info  from the server */
      lineagesData: [],

      /** Currently selected time range */
      selectedRange: null
    }
  },
  computed: {
    ...mapState(['selectedGranularity', 'selectedLocation', 'selectedLineage']),

    /** Visibility flag for the plots */
    hasResult () {
      return (
        (this.selectedGranularity === 'world' || this.selectedLocation !== null)
      )
    },

    /** Visibility flag for the plots */
    showPlot () {
      return {
        histogram:
          !this.isLoading.histogram && this.sequencesData.length > 0,
        breakdown:
          !this.isLoading.histogram && this.sequencesData.length > 0 &&
          !this.isLoading.breakdown && Object.keys(this.lineagesData).length > 0 &&
          !this.isDisabled.breakdown
      }
    },

    /** Text for the label of the graph */
    title () {
      if (!this.showPlot.histogram) {
        return this.isLoading.histogram
          ? 'Loading data...'
          : 'Start exploring the dataset by selecting some parameters... '
      } else {
        return (
          'Sequence availability per day for: ' +
          (this.selectedLocation ? this.selectedLocation : this.selectedGranularity) +
          (this.selectedLineage && this.withLineages ? ', lineage ' + this.selectedLineage : '')
        )
      }
    }
  },
  methods: {
    /** Fetches from the server the info on the available sequences for the selected parameters */
    fetchSequenceInfo () {
      if (this.selectedGranularity === 'world' || this.selectedLocation) {
        this.isLoading.histogram = true
        const sequenceAPI = `/explorer/getSequenceInfo`
        const toSend = {
          granularity: this.selectedGranularity,
          location: this.selectedLocation,                          // possibly it has no value
          lineage: this.withLineages ? this.selectedLineage : null   // possibly it has no value
        }

        axios
          .post(sequenceAPI, toSend)
          .then(res => {
            this.sequencesData = res.data
          })
          .catch((e) => {
            this.$emit('error', e)
          })
          .finally(() => {
            this.isLoading.histogram = false
          })
      } else {
        this.sequencesData = []
      }
    },

    /** Fetches from the server the info on lineage breakdown for the selected parameters */
    fetchLineageBreakdownInfo () {
      if ((this.selectedGranularity === 'world' || this.selectedLocation) && this.selectedRange) {
        this.isLoading.breakdown = true
        const sequenceAPI = `/explorer/getLineagesBreakdown`
        const toSend = {
          granularity: this.selectedGranularity,
          location: this.selectedLocation,    // possibly it has no value
          range: this.selectedRange
        }
        axios
          .post(sequenceAPI, toSend)
          .then(res => {
            this.lineagesData = res.data
          })
          .catch((e) => {
            this.$emit('error', e)
          })
          .finally(() => {
            this.isLoading.breakdown = false
          })
      } else {
        this.lineagesData = {}
      }
    },

    /** Handler of time range changes events for the histogram plot */
    onTimeRangeChanges (newRange) {
      this.selectedRange = newRange
      if (newRange !== null) {
        if (dateDiff(newRange[0], newRange[1]) > 28) {
          this.isDisabled.breakdown = true
        } else {
          this.isDisabled.breakdown = false
          this.fetchLineageBreakdownInfo()
        }
      }
    },

    /**
     * Emit the selected 4 weeks analysis period
     */
    emitAnalysisPeriod () {
      this.$emit('weekSelection', [null, this.selectedRange[1]])
    }
  },
  beforeMount () {
    // Fetch the sequence info on show/hide section
    this.fetchSequenceInfo()
  },
  watch: {
    /** Reset sequence info on granularity value changes */
    selectedGranularity () {
      this.sequencesData = []
    },

    /** Fetch sequence info on location value changes */
    selectedLocation () {
      this.fetchSequenceInfo()
    },

    /** Fetch sequence info on lineage value changes */
    selectedLineage () {
      this.fetchSequenceInfo()
    },

    /** Reset lineages data on sequence info reset */
    sequencesData (newVal) {
      if (newVal.length === 0) {
        this.lineagesData = {}
      }
    }
  }
}
</script>

<style scoped>
/* Form labels styling */
.main-label span {
  font-size: 23px;
  font-weight: 800;
  text-transform: uppercase;
  margin-top: 15px;
  border-bottom: solid 4px white;
}

.main-label,
.sub-label,
.disabled-label {
  text-align: center;
  justify-content: center;
  padding-top: 5px !important;
  padding-bottom: 8px !important;
  color: white;
}

.disabled-label {
  margin-top: 10px;
}

/* Explorer container */
.explorer-element {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

.lineage-breakdown {
  margin-top: 10px !important;
}
</style>
