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
  <v-col>

    <!-- Label -->
    <v-row class='text-body-1 font-weight-medium text-center'>
      <v-col>{{ title }}</v-col>
    </v-row>

    <!-- Histogram loading animation -->
    <v-row v-if='isLoading.histogram'>
      <v-col>
        <v-skeleton-loader width='100%' type='image'/>
      </v-col>
    </v-row>

    <!-- Histogram plot -->
    <v-row v-if='showPlot.histogram'>
      <explorer-histogram :sequence-data='sequencesData' @timeRangeChange='(tr) => onTimeRangeChanges(tr)'/>
    </v-row>

    <!-- Breakdown loading animation -->
    <v-row v-if='isLoading.breakdown'>
      <v-col>
        <v-skeleton-loader width='100%' type='image'/>
      </v-col>
    </v-row>

    <v-row v-if='isDisabled.breakdown' class='disabled-label'>
      <v-col><sub>
        <v-icon color='white' small left>mdi-information-outline</v-icon>
        Reduce the time range to at most 4 weeks to see lineages breakdown </sub></v-col>
    </v-row>

    <!-- Breakdown plot -->
    <v-row v-if='showPlot.breakdown' class='lineage-breakdown'>
      <lineages-breakdown :lineages-data='lineagesData'/>
    </v-row>

    <!-- Button to fill in the date -->
    <v-row v-if='showPlot.breakdown' class='text-center'>
      <v-col>
        <btn-with-tooltip bottom color="primary" text="Consider these 4 weeks" icon="mdi-calendar"
                          :click-handler="()=>emitAnalysisPeriod()"
                          tip="Fill the form using the currently selected 4 weeks as analysis period."/>
      </v-col>
    </v-row>

  </v-col>
</template>

<script>
import ExplorerHistogram from '@/components/explorer/ExplorerHistogram'
import axios from 'axios'
import LineagesBreakdown from '@/components/explorer/LineagesBreakdown'
import {dateDiff} from '@/utils/dateService'
import {mapState} from 'vuex'
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";

export default {
  name: 'DatasetExplorer',
  components: {BtnWithTooltip, LineagesBreakdown, ExplorerHistogram},
  props: {
    /** Flag for lineage search. */
    withLineages: Boolean
  },
  data() {
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
    ...mapState(['selectedLocation', 'selectedLineage']),

    /** Visibility flag for the plots */
    hasResult() {
      return this.selectedLocation !== null
    },

    /** Visibility flag for the plots */
    showPlot() {
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
    title() {
      if (!this.showPlot.histogram) {
        return this.isLoading.histogram
            ? 'Loading data...'
            : 'Start exploring the dataset by selecting some parameters... '
      } else {
        return (
            'Sequence availability per day for: ' + this.selectedLocation +
            (this.selectedLineage && this.withLineages ? ', lineage ' + this.selectedLineage : '')
        )
      }
    }
  },
  methods: {
    /** Fetches from the server the info on the available sequences for the selected parameters */
    fetchSequenceInfo() {
      if (this.selectedLocation) {
        this.isLoading.histogram = true
        const sequenceAPI = `/explorer/getSequenceInfo`
        const queryParams = {
          location: this.selectedLocation,                          // possibly it has no value
          lineage: this.withLineages ? this.selectedLineage : null   // possibly it has no value
        }

        axios
            .get(sequenceAPI, {params: queryParams})
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
    fetchLineageBreakdownInfo() {
      if (this.selectedLocation && this.selectedRange) {
        this.isLoading.breakdown = true
        const sequenceAPI = `/explorer/getLineagesBreakdown`
        const queryParams = {
          location: this.selectedLocation,    // possibly it has no value
          begin: this.selectedRange[0],
          end: this.selectedRange[1],
        }
        axios
            .get(sequenceAPI, {params: queryParams})
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
    onTimeRangeChanges(newRange) {
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
    emitAnalysisPeriod() {
      this.$emit('weekSelection', [null, this.selectedRange[1]])
    }
  },
  beforeMount() {
    // Fetch the sequence info on show/hide section
    this.fetchSequenceInfo()
  },
  watch: {

    /** Fetch sequence info on location value changes */
    selectedLocation() {
      this.fetchSequenceInfo()
    },

    /** Fetch sequence info on lineage value changes */
    selectedLineage() {
      this.fetchSequenceInfo()
    },

    /** Reset lineages data on sequence info reset */
    sequencesData(newVal) {
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
