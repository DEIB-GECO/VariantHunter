<!--
  Component:    TableControls
  Description:  Component to add controls to the header of a v-table
                Controls includes options to download data, show p-values and show table interpretation

  Events:
  └── showPValues:  Emitted on show p-values preference change together with the new value

-->

<template>
  <v-container class='table-controls'>
    <v-layout justify-center row wrap>

      <!---- Button to show/hide table interpretation ---->
      <dialog-opener :button-prefix='false' color="primary"
                     title="<span class='d-sm-none'>Info</span><span class='hidden-xs-only'><span class='hidden-sm-and-down'>Table</span> interpretation</span>">
        <!-- Table interpretation info -->
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
            <div class='li-content'>Name of the considered mutation. <br/> In case of <i>lineage specific analysis</i>,
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
              differently compared to the entire population of genome sequences. Its value is computed using a <i>Chi-square
                test</i> of independence of variables in a contingency table.
              The reported values have been <a
                  href="https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html"
                  target="_blank">corrected</a> for multiple tests.
            </div>
          </li>
          <li class='li-table'>
            <div class='li-name'>P-value without mut</div>
            <div class='li-content underlined-links'>Shows if the population «without mutation» is growing
              differently compared to the entire population of genome sequences. Its value is computed using a <i>Chi-square
                test</i> of independence of variables in a contingency table.
              The reported values have been <a
                  href="https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html"
                  target="_blank">corrected</a> for multiple tests.
            </div>
          </li>
          <li class='li-table'>
            <div class='li-name'>P-value comparative</div>
            <div class='li-content underlined-links'>Shows if the population «with mutation» is growing
              differently compared to the population «without mutation». Its value is computed using a <i>Chi-square
                test</i> of independence of variables in a contingency table.
              The reported values have been <a
                  href="https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.multipletests.html"
                  target="_blank">corrected</a> for multiple tests.
            </div>
          </li>
        </ul>
      </dialog-opener>

      <!---- Button to show/hide p-values ---->
      <v-flex justify-center class='d-flex pa-1'>
        <v-btn v-if='!showPValues' outlined depressed rounded small color='primary' @click='showPValues=true'>
          <v-icon left>mdi-plus-circle-outline</v-icon>
          <span class='hidden-xs-only'>Show&nbsp;</span>p-values
        </v-btn>
        <v-btn v-else depressed rounded small color='primary' class="text_var2--text" @click='showPValues=false'>
          <v-icon left>mdi-minus-circle-outline</v-icon>
          <span class='hidden-xs-only'>Hide&nbsp;</span>p-values
        </v-btn>
      </v-flex>

      <!---- Button to download data ---->
      <v-flex justify-center class='d-flex pa-1'>
        <download-data control-type="button"/>
      </v-flex>

    </v-layout>
  </v-container>
</template>

<script>
import DialogOpener from '@/components/general/basic/DialogOpener'
import DownloadData from "@/components/controls/DownloadData";

export default {
  name: 'TableControls',
  components: {DownloadData, DialogOpener},

  data() {
    return {
      /** Boolean visibility flag set to true if p_values are to be shown */
      showPValues: false,
    }
  },

  watch: {
    /** On button press emit preference on p-values' visibility */
    showPValues(newVal) {
      this.$emit("showPValues", newVal)
    }
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
