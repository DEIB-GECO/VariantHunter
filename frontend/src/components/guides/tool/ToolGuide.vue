<!--

  Component:    ToolGuide
  Description:  Usage guide for the tool

-->

<template>
  <v-container class='ml-0 ml-sm-auto mr-0 mr-sm-auto mt-10'>
    <h3>
      <v-icon left color='text_var1' large>mdi-human-greeting</v-icon>
      What is Variant<span class="primary--text">Hunter</span>
    </h3>
    <div class='pl-6 pl-sm-10 pr-6 pr-sm-10'>
      <p>
        <i>VariantHunter</i> analyzes the prevalence of non-synonymous genomic variants in the genome of SARS-CoV-2 to <b>observe
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
        <a href="https://www.insdc.org/" target="_blank"><i>INSDC databases</i></a>,
        curated and made openly available by <i>Nextstrain</i> at
        <a href='https://nextstrain.org/ncov/open/global' target='_blank' class='link-alt'>this link</a> ,
        and regularly imported within <i>VariantHunter</i>.

        If users wish to use their own data or restricted access data <i>(GISAID)</i>, they may employ our
        Docker implementation, as explained below in the <a href='#docker' class='link-alt'>dedicated section</a>.
      </p>
      <p>
        <i>VariantHunter</i> supports two modes of analysis: <b>Lineage Independent</b> and <b>Lineage
        Specific</b>.
        Each mode allows the user to open several analysis sessions <del>(managed in panels that can be expanded, collapsed, or
        deleted at the user's choice). </del><!-- TODO -->
      </p>

      <paragraph :src='introImg' img-max-height='230' left no-zoom>
        <p>
          The underlying mechanism of both methodologies is the same: each amino acid change is analyzed over a
          <b>time period of 4 weeks</b>.<br/>
          For each week, the <i>frequency of the change</i> (computed as
          <span class='formula'>"number of sequences harboring the change"/"total number of sequences collected in that week"</span>)
          is considered (see the four blue dots in the Figure);
          then, a linear model is fitted on the four data points (red line in the Figure).
        </p>
      </paragraph>
      <p>
        The <b>slope</b> of the regression line represents <i>how fast the mutation is growing</i> (i.e., its
        prevalence is increasing). Positive slopes indicate an increasing trend, while negative
        values of the slope indicate a decreasing trend.
      </p>
      <p>
        <b>Chi-square tests</b> are computed to test the <i>significance of the increase/decrease in prevalence</i>.
      </p>
      <p>
        The main results of both analyses are summarized in a <b>table</b>, reporting the
        prevalence over the 4 weeks of amino-acid changes, their slope, and Chi-square tests p-values.
        In addition, different visualizations are provided to support the intuition of the observed trends of diffusion:
        a <b>heatmap</b> and various <b>line-plots</b> that represent prevalence or their odd ratios.
      </p>
    </div>

    <v-container class='pl-0 pl-sm-10 pr-0 pr-sm-10 pb-5'>

      <v-expansion-panels multiple class='mt-3' flat>

        <!-- LINEAGE INDEPENDENT -->
        <lin-independent-guide/>

        <!-- LINEAGE SPECIFIC -->
        <lin-specific-guide/>

      </v-expansion-panels>
    </v-container>

  </v-container>
</template>

<script>

import Paragraph from '@/components/general/basic/Paragraph'
import LinIndependentGuide from '@/components/guides/tool/lin-independent/LinIndependentGuide'
import LinSpecificGuide from '@/components/guides/tool/lin-specific/LinSpecificGuide.vue'

export default {
  name: 'ToolGuide',
  components: {LinSpecificGuide, LinIndependentGuide, Paragraph},

  data() {
    return {
      /** Images */
      introImg: require('@/assets/guide/intro.png')
    }
  }
}
</script>

<style scoped>
#app .formula {
  padding: 0;
  font-family: monospace !important;
}
</style>
<style>
.with-borders {
  border: solid 1px #e3e3e3;
  border-radius: 4px;
  padding: 28px 3px;
}
</style>
