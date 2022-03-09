<template>
  <v-layout justify-center row wrap>
    <v-flex class="xs12 sm12 md11 d-flex field-label">
      <span>Dataset Explorer</span>
    </v-flex>

    <v-flex class="xs12 sm12 md11 d-flex explorer-element">
      <BarChart :plot-data="plotData"/>
    </v-flex>
  </v-layout>
</template>

<script>
import BarChart from "@/components/plots/BarChart";

export default {
  name: "DatasetExplorer",
  components: {BarChart},
  props: {

    /** Granularity to be explored */
    granularity: {required: true},

    /** Location to be explored */
    location: {required: true},

    /** Date to be explored */
    date: {required: true}

  },
  computed: {

    plotData() {
      return []
    }

  },
  methods: {}
}
</script>

<style scoped>

/* Form labels styling */
.field-label {
  justify-content: center;
  padding-top: 15px !important;
  padding-bottom: 5px !important;
  color: white;
}

/* Explorer container */
.explorer-element {
  padding-top: 0 !important;
  padding-bottom: 0 !important;
}

</style>