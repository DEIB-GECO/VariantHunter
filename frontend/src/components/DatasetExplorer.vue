<!--
  Component:    DatasetExplorer
  Description:  Component to explore the number of sequences available in the dataset

  Props:
  ├── granularity:  Granularity to be explored
  ├── location:     Location to be explored
  └── lineage:      Lineage to be explored

  Events:
  └── error:        Emitted on server errors
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

      <!-- Loading animation -->
      <v-flex v-if='isLoading' class='xs11 d-flex'>
        <v-skeleton-loader width='100%' type='image' />
      </v-flex>

      <!-- Plot -->
      <v-flex v-if='hasResult' class='xs12 sm12 md11 d-flex explorer-element'>
        <ExplorerHistogram :sequence-data='sequenceData' :lineages-data='lineagesData' />
      </v-flex>
    </template>
  </v-layout>
</template>

<script>
import ExplorerHistogram from '@/components/plots/ExplorerHistogram'
import axios from 'axios'

export default {
  name: 'DatasetExplorer',
  components: { ExplorerHistogram },
  props: {
    /** Granularity to be explored */
    granularity: { required: true },

    /** Location to be explored */
    location: { required: true },

    /** Lineage to be explored */
    lineage: { default: null }
  },
  data () {
    return {
      /** Loading flag. If true data are being fetched */
      isLoading: false,

      /** Array of sequence info  from the server */
      sequenceData: [],

      /** Array of lineages breakdown info  from the server */
      lineagesData: []
    }
  },
  computed: {
    /** Result flag. True iff there is a graph to be shown. */
    hasResult () {
      return (
        !this.isLoading &&
        (this.granularity === 'world' || this.location !== null)
      )
    },

    /** Text for the label of the graph */
    title () {
      if (!this.hasResult) {
        return this.isLoading
          ? 'Loading data...'
          : 'Start exploring the dataset by selecting some parameters... '
      } else {
        return (
          'Sequence availability per day for: ' +
          (this.location ? this.location : this.granularity) +
          (this.lineage ? ', lineage ' + this.lineage : '')
        )
      }
    }
  },
  methods: {
    /** Fetches from the server the info on the available sequences for the selected parameters */
    fetchSequenceInfo () {
      if (this.granularity === 'world' || this.location) {
        this.isLoading = true
        const sequenceAPI = `/explorer/getSequenceInfo`
        const toSend = {
          granularity: this.granularity,
          location: this.location, // possibly it has no value
          lineage: this.lineage // possibly it has no value
        }
        axios
          .post(sequenceAPI, toSend)
          .then(res => {
            this.sequenceData = res.data
          })
          .catch((e) => {
            this.$emit('error', e)
          })
          .finally(() => {
            this.isLoading = false
          })
      }
    },

    /** Fetches from the server the info on lineage breakdown for the selected parameters */
    fetchLineageBreakdownInfo () {
      if ((this.granularity === 'world' || this.location) && this.lineage === null) {
        this.isLoading = true
        const sequenceAPI = `/explorer/getLineageBreakdown`
        const toSend = {
          granularity: this.granularity,
          location: this.location // possibly it has no value
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
            this.isLoading = false
          })
      } else {
        this.lineagesData = []
      }
    }
  },
  beforeMount () {
    // Fetch the sequence info on show/hide section
    this.fetchSequenceInfo()
    this.fetchLineageBreakdownInfo()
  },
  watch: {
    /** Reset sequence info on granularity value changes */
    granularity () {
      this.sequenceData = []
      this.lineagesData = []
    },

    /** Fetch sequence info on location value changes */
    location () {
      this.fetchSequenceInfo()
      this.fetchLineageBreakdownInfo()
    },

    /** Fetch sequence info on lineage value changes */
    lineage () {
      this.fetchSequenceInfo()
      this.fetchLineageBreakdownInfo()
    }
  }
}
</script>

<style scoped>
/* Form labels styling */
.main-label span{
  font-size: 23px;
  font-weight: 800;
  text-transform: uppercase;
  margin-top: 15px;
  border-bottom: solid 4px white;
}

.main-label,
.sub-label {
  text-align: center;
  justify-content: center;
  padding-top: 5px !important;
  padding-bottom: 8px !important;
  color: white;
}

/* Explorer container */
.explorer-element {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}
</style>
