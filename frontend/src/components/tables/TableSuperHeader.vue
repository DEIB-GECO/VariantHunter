<!--
  Component:    TableSuperHeader
  Description:  Component to add super header to a v-table

  Props:
  ├── showPValues:  Flag to show the p_values in the table
  └── withLineages: Lineages flag. True if the data refers to a lineage specific analysis. Required
-->

<template>
  <thead class='main-headers'>
  <tr>
    <th :colspan='withLineages ? 2 : 3' class='empty-main-header' />
    <th colspan='1' class='empty-main-header' />
    <th colspan='1' class='empty-main-header' />
    <th colspan='4'>
      Mutation diffusion in % &nbsp;&nbsp; (num of affected sequences)
    </th>
    <th v-if='showPValues' colspan='3'>P-values</th>
  </tr>
  </thead>
</template>

<script>
export default {
  name: 'TableSuperHeader',
  props: {
    /** Lineages flag. True if the data refers to a lineage specific analysis. Required */
    withLineages: { required: true },

    /** Flag to show the p_values in the table */
    showPValues: { required: true }
  }
}
</script>

<style scoped>

/* Custom main headers styling*/
.main-headers {
  background: var(--tertiary-color-light);
}

.main-headers th {
  letter-spacing: 0.05em;
  word-spacing: 0.1em;
  text-align: center !important;
  border-top: var(--primary-color) solid 1px !important;
  padding-top: 7px !important;
  padding-bottom: 7px !important;
  height: fit-content !important;
}

.main-headers th:not(:last-child) {
  border-right: thin solid rgba(0, 0, 0, 0.12) !important;
}

.empty-main-header {
  border-bottom: none !important;
}

</style>

