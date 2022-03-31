<!--
  Component:    TableControls
  Description:  Component to add controls to the header of a v-table

  Props:
  ├── downloadLoading:  Download flag: true if a file download is in progress:
  └── showPValues:      Flag to show the p_values in the table

  Events:
  ├── showPValues:  Emitted whenever a show/hide p-values button is pressed
  ├── downloadData: Emitted whenever download data button is pressed
  └── downloadAll:  Emitted whenever download all button is pressed
-->

<template>
  <v-container class='table-controls'>
    <v-layout justify-center row wrap>

      <!---- Show/hide p-values info button ---->
      <v-flex justify-center class='xs12 sm6 md3 d-flex'>
        <v-btn v-if='!showPValues' outlined depressed rounded small color='primary' @click='$emit("showPValues",true)'>
          <v-icon left>mdi-plus-circle-outline</v-icon>
          Show p-values
        </v-btn>
        <v-btn v-else depressed rounded small color='primary' @click='$emit("showPValues",false)'>
          <v-icon left>mdi-minus-circle-outline</v-icon>
          Hide p-values
        </v-btn>
      </v-flex>

      <!---- Show/hide columns descriptions button ---->
      <DialogOpener :button-prefix='false' title='Columns description'>
        <ul>
          <li>
            <b>Mut: </b>
            the name of the mutation. <br/> In case of lineage specific analysis, the mutations
            characterizing the lineage are <span class='char-mut'>highlighted</span>.
          </li>
          <li>
            <b>Slope: </b>
            is calculated through a linear interpolation of the
            diffusion (percentage). (y=<b>m</b>x + q)
          </li>
          <li>
            <b>P value with mut: </b>
            shows if the population «with mutation» is growing
            differently compared to everything.
          </li>
          <li>
            <b>P value without mut: </b>
            shows if the population «without mutation» is growing
            differently compared to everything.
          </li>
          <li>
            <b>P value comparative: </b>
            shows if the population «with mutation» is growing
            differently compared to the population «without mutation».
          </li>
        </ul>
      </DialogOpener>

      <!---- Download data button ---->
      <v-flex justify-center class='xs12 sm6 md3 d-flex'>
        <v-btn :loading='downloadLoading' outlined depressed rounded small color='primary'
               @click='$emit("downloadData")'>
          <v-icon left>mdi-download-circle-outline</v-icon>
          Download data
        </v-btn>
      </v-flex>

      <!---- Print result button ---->
      <v-flex justify-center class='xs12 sm6 md3 d-flex'>
        <v-btn :loading='downloadLoading' outlined depressed rounded small color='primary'
               @click='$emit("downloadAll")'>
          <v-icon left>mdi-printer</v-icon>
          Download all
        </v-btn>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import DialogOpener from '@/components/general/DialogOpener'

export default {
  name: 'TableControls',
  components: { DialogOpener },
  props: {
    /* Download flag: true if a file download is in progress */
    downloadLoading: { required: true },

    /** Flag to show the p_values in the table */
    showPValues: { required: true }
  }
}
</script>

<style scoped>

/* Table options */
.table-controls {
  padding-top: 25px;
  padding-bottom: 18px;
}

.table-controls .d-flex {
  padding-bottom: 7px !important;
  padding-top: 0 !important;
}

</style>
