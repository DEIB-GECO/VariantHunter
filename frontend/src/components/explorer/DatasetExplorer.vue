<!--
  Component:    DatasetExplorer
  Description:  Component to explore the number of sequences available in the dataset

  Props:
  └── withLineages: Boolean flag set to true if lineage-specific mode

  Events:
  └── weekSelection:  Emitted when the user select the 4 weeks to analyze
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
        <v-skeleton-loader width='100%' height="390" class="explorer-loader" type='image'/>
      </v-col>
    </v-row>

    <!-- Histogram plot -->
    <v-row v-if='showPlot.histogram'>
      <explorer-histogram :sequence-data='sequencesData' @timeRangeChange='(tr) => onTimeRangeChanges(tr)'/>
    </v-row>

    <!-- Breakdown loading animation -->
    <v-row v-show='isLoading.breakdown'>
      <v-col>
        <v-skeleton-loader width='100%' height="390" class="explorer-loader" type='image'/>
      </v-col>
    </v-row>

    <v-row v-if='isDisabled.breakdown' class='disabled-label warning--text'>
      <v-col><sub>
        <v-icon color='warning' small left>mdi-information-outline</v-icon>
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
                          :click-handler="()=>emitAnalysisPeriod()" content-class="text_var2--text"
                          tip="Fill the form using the currently selected 4 weeks as analysis period."/>
      </v-col>
    </v-row>

    <loading-sticker :error="error"/>

  </v-col>
</template>

<script>
import ExplorerHistogram from '@/components/explorer/ExplorerHistogram'
import LineagesBreakdown from '@/components/explorer/LineagesBreakdown'
import {dateDiff} from '@/utils/dateService'
import {mapGetters, mapState} from 'vuex'
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";
import LoadingSticker from "@/components/general/basic/LoadingSticker";
import {toText} from "@/utils/formatterService";

export default {
  name: 'DatasetExplorer',
  components: {LoadingSticker, BtnWithTooltip, LineagesBreakdown, ExplorerHistogram},

  props: {
    /** Boolean flag set to true if lineage-specific mode */
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
      selectedRange: null,

      /** Error data for the table and expansion. Undefined if no error. */
      error: undefined,
    }
  },
  computed: {
    ...mapState(['selectedLocation', 'selectedLineage']),
    ...mapGetters(['getSelectedLineageValues']),

    /** Mapping for toText */
    lineageText() {
      return toText(this.selectedLineage)
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
            'Sequence availability per day for: ' + this.selectedLocation.text +
            (this.lineageText && this.withLineages ? ', lineage ' + this.lineageText : '')
        )
      }
    }
  },
  methods: {
    /** Fetches from the server the info on the available sequences for the selected parameters */
    fetchSequenceInfo() {
      if (this.selectedLocation) {
        this.error = undefined
        this.isLoading.histogram = true
        const sequenceAPI = `/explorer/getSequenceInfo`
        const queryParams = new URLSearchParams();
        queryParams.append('location', this.selectedLocation.id)
        // Add lineages data
        if (this.withLineages && this.selectedLineage.count > 0) {
          this.getSelectedLineageValues.forEach(name => queryParams.append("lineages", name))
        }

        this.$axios
            .get(sequenceAPI, {params: queryParams})
            .then(res => {
              this.sequencesData = res.data
            })
            .catch((e) => {
              this.error = e
              this.sequencesData = []
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
        this.error = undefined
        this.isLoading.breakdown = true
        const sequenceAPI = `/explorer/getLineagesBreakdown`
        const queryParams = {
          location: this.selectedLocation.id,    // possibly it has no value
          begin: this.selectedRange[0],
          end: this.selectedRange[1],
        }

        this.$axios
            .get(sequenceAPI, {params: queryParams, cache: false})
            .then(res => this.lineagesData = res.data)
            .catch((e) => {
              this.error = e
              this.lineagesData = {}
            })
            .finally(() => this.isLoading.breakdown = false)
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

  /** Fetch the sequence info on show/hide section */
  beforeMount() {
    this.fetchSequenceInfo()
  },

  watch: {
    /** Fetch sequence info on tab changes */
    withLineages() {
      this.fetchSequenceInfo()
    },

    /** Fetch sequence info on location value changes */
    selectedLocation() {
      this.fetchSequenceInfo()
    },

    /** Fetch sequence info on lineage value changes */
    getSelectedLineageValues() {
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

<style>
.explorer-loader * {
  height: 100%;
}
</style>
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
