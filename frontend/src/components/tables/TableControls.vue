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

      <!---- Show/hide table interpretation button ---->
      <DialogOpener :button-prefix='false' title='Table interpretation'>
        <p>The mutation table depicts the trend of all and only the <b>mutations detected in
          the last week of the considered analysis period</b>. Only mutations affecting at least 0.5% of
          the sequences collected in the week are shown.</p>
        <ul class='ul-table'>
          <li class='li-table'>
            <div class='li-name'>Protein</div>
            <div class='li-content'>Name of the considered protein.</div>
          </li>
          <li class='li-table'>
            <div class='li-name'>Mut</div>
            <div class='li-content'>Name of the considered mutation. <br /> In case of <i>lineage specific analysis</i>,
              the mutations characterizing the lineage are <span class='char-mut'>highlighted</span></div>
          </li>
          <li class='li-table'>
            <div class='li-name'>Slope</div>
            <div class='li-content'>Slope computed through linear interpolation of the
              diffusion (percentage): y=<b>m</b>x + q
            </div>
          </li>
          <li class='li-table'>
            <div class='li-name'>Mutation diffusion</div>
            <div class='li-content'>Diffusion of the mutation as a percentage of the number of sequences collected in
              the week.
              The spread is shown for the four weeks of interest.
            </div>
          </li>
          <li class='li-table'>
            <div class='li-name'>P-value with mut</div>
            <div class='li-content underlined-links'>Shows if the population «with mutation» is growing
              differently compared to everything. Its value is computed using a <i>Chi-square
                test</i> of independence of variables in a contingency table.
              The reported values have been <a href="https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html" target="_blank">corrected</a> for multiple tests.
            </div>
          </li>
          <li class='li-table'>
            <div class='li-name'>P-value without mut</div>
            <div class='li-content underlined-links'>Shows if the population «without mutation» is growing
              differently compared to everything. Its value is computed using a <i>Chi-square
                test</i> of independence of variables in a contingency table.
              The reported values have been <a href="https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html" target="_blank">corrected</a> for multiple tests.
            </div>
          </li>
          <li class='li-table'>
            <div class='li-name'>P-value comparative</div>
            <div class='li-content underlined-links'>Shows if the population «with mutation» is growing
              differently compared to the population «without mutation». Its value is computed using a <i>Chi-square
                test</i> of independence of variables in a contingency table.
              The reported values have been <a href="https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html" target="_blank">corrected</a> for multiple tests.
            </div>
          </li>
        </ul>
      </DialogOpener>

      <!---- Download data button ---->
      <v-flex justify-center class='xs12 sm6 md3 d-flex'>
        <v-tooltip bottom max-width='400' color='white' open-delay='0'>
          <template v-slot:activator='{ on, attrs }'>
            <v-btn v-bind='attrs' v-on='on' :loading='downloadLoading' color='primary'
                   outlined depressed rounded small @click='$emit("downloadData")'>
              <v-icon left>mdi-download-circle-outline</v-icon>
              Download data
            </v-btn>
          </template>
          <span style='color: rgb(68, 68, 68)'>Download this table as a .csv file</span>
        </v-tooltip>
      </v-flex>

      <!---- Print result button ---->
      <v-flex justify-center class='xs12 sm6 md3 d-flex'>
        <v-tooltip bottom max-width='400' color='white' open-delay='0'>
          <template v-slot:activator='{ on, attrs }'>
            <v-btn v-bind='attrs' v-on='on' :loading='downloadLoading' color='primary'
                   outlined depressed rounded small @click='$emit("downloadAll")'>
              <v-icon left>mdi-printer</v-icon>
              Download all
            </v-btn>
          </template>
          <span style='color: rgb(68, 68, 68)'>Download the entire tab as a .png file</span>
        </v-tooltip>
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
