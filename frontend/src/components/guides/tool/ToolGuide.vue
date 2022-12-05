<!--
  Component:    ToolGuide
  Description:  Usage guide for the tool
-->

<template>
  <v-container class='ml-0 ml-sm-auto mr-0 mr-sm-auto mt-10'>
    <h3>
      <v-icon left color='text_var1' large>mdi-human-greeting</v-icon>
      What is VariantHunter
    </h3>
    <div class='pl-6 pl-sm-10 pr-6 pr-sm-10'>
      <p>
        <i>VariantHunter</i> analyzes the frequencies of amino acid mutations of <i>SARS-CoV-2</i> in order to <b>observe
        interesting variant trends</b> or <b>identify novel emerging variants</b>.
      </p>
      <p>
        The
        <a href="http://cerilab.deib.polimi.it/variant_hunter" target="_blank">
          <v-btn color='secondary' x-small depressed outlined rounded>
            <v-icon x-small>mdi-link</v-icon>
            &nbsp;online version of the tool
          </v-btn>
        </a>
        contains updated data from
        <i>GenBank</i>,
        curated and made openly available by <i>Nextstrain</i> at
        <a href='https://nextstrain.org/ncov/open/global' target='_blank' class='link-alt'>this link</a> ,
        and regularly imported within <i>VariantHunter</i>.

        If users wish to use <i>private</i> data or <i>GISAID</i> data, they may employ our
        <i>Docker implementation</i>, as explained below in the
        <a href='#docker' class='link-alt'>dedicated section</a>.
      </p>
      <p>
        <i>VariantHunter</i> supports two modes of analysis: <b>Lineage Independent</b> and <b>Lineage
        Dependent</b>.
        Each mode allows to open several analysis sessions (managed in panels that can be <i>expanded, collapsed, or
        deleted</i> at the user's choice).
      </p>

      <Paragraph :src='introImg' img-max-height='230' left no-zoom>
        <p>
          The underlying mechanism of both methodologies is the same: each amino acid mutation is analyzed for a
          <b>time period of 4 weeks</b>.<br />
          For each week, the <i>frequency of the mutation</i> (computed as
          <span class='formula'>"number of sequencing harboring the mutation"/"total number of sequences collected in that week"</span>)
          is considered (see the four blue dots in the Figure);
          then, a linear model is fitted on the four data points (red line in the Figure).
        </p>
      </Paragraph>
      <p>
        The <b>slope</b> of the regression line represents <i>how fast the mutation is growing</i> (i.e., its
        percentage is increasing). <i>Positive slopes</i> indicate an increasing trend, while <i>negative</i>
        values of the slope indicate a decreasing trend.
      </p>
      <p>
        <b>Chi squared tests</b> are computed to test the <i>significance of the change of frequency</i> of the
        mutation.
      </p>
      <p>
        The main results of both analyses are summarized in a <b>table of mutations</b>, reporting their
        <i>prevalence</i> over the 4 weeks, their <i>slope</i>, and Chi squared tests <i>p-values</i>.
        In addition, different visualizations support the intuition of the observed trends of diffusion:
        a <b>heatmap</b> and various <b>line-plots</b> that represent <i>prevalence</i> or their <i>odd ratios</i>.
      </p>
    </div>

    <v-container class='pl-0 pl-sm-10 pr-0 pr-sm-10 pb-5'>

      <v-expansion-panels multiple class='mt-3' flat>

        <!-- LINEAGE INDEPENDENT -->
        <LinIndGuide />

        <!-- LINEAGE SPECIFIC -->
        <LinDepGuide />

      </v-expansion-panels>
    </v-container>

  </v-container>
</template>

<script>

import Paragraph from '@/components/general/basic/Paragraph'
import LinIndGuide from '@/components/guides/tool/LinIndGuide'
import LinDepGuide from '@/components/guides/tool/LinDepGuide'
import { mapState } from 'vuex'

export default {
  name: 'ToolGuide',
  components: { LinDepGuide, LinIndGuide, Paragraph },
  data () {
    return {
      /** Images */
      introImg: require('../../../assets/guide/intro.png')
    }
  }
}
</script>

<style scoped>
.formula {
  padding: 0;
  font-family: monospace !important;
}

.command {
  text-transform: uppercase !important;
  font-weight: 300 !important;
}

.highlight {
  background: rgba(255, 255, 0, .45);
}

.linkk-alt{
  color: darkgrey !important;
}

</style>
