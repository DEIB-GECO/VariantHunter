<!--

  Component:    LinIndUseCase1
  Description:  Use case for lineage independent search

-->

<template>
  <use-case source-name='Nextstrain' source-date='08/12/2022'
            name='<b>Use case 1</b>: Spread of the Omicron 4 and 5 variants and displacement of Omicron 1 and 2'>

    <paragraph :src='form' left larger-img>
      <p>
        A "lineage-independent" analysis was performed to study the prevalence of amino acid changes in
        the Spike glycoprotein in <i>North America</i>.<br/>
        An interval ranging from 15/05/2022 to 11/06/2022, which corresponds with the displacement
        of Omicron <b>BA.1.*</b> and <b>BA.2.*</b> lineages by the newly
        emerged <b>BA.5.*</b> and <b>BA.4.*</b> lineages, was selected.
      </p>
    </paragraph>

    <paragraph :src='table' right larger-img>
      <p>
        Compared with BA.1* and BA.*2, BA.5* and BA.4* lack Q493R, but carry 2 additional amino
        acid changes in Spike: L452R and F486V.<br/>
        This pattern is clearly recapitulated by the "expanded" mutation table reported in the figure,
        where the different distribution of F486V and Q493R across sub-variants
        of Omicrons can be clearly appreciated.
      </p>
    </paragraph>

    <paragraph :src='heatmap' left larger-img>
      <p class='mt-5'>
        The <b>Diffusion Heatmap</b> shows an almost 5-fold increase in the prevalence of L452R and
        F486V, between 15/05/2022 and 11/06/2022, and a concomitant reduction in the prevalence of Q493R.
      </p>
    </paragraph>
    <paragraph :src='trend' left larger-img>
      <p>
        The same pattern is also recovered from the matched <b>Diffusion Trend</b> plot.
      </p>
    </paragraph>

  </use-case>
</template>

<script>
import UseCase from "@/components/guides/tool/UseCase.vue";
import Paragraph from "@/components/general/basic/Paragraph.vue";

export default {
  name: 'LinIndUseCase1',
  components: { Paragraph, UseCase},

  data() {
    return {
      /** Images */
      form: require('@/assets/guide/lin_ind/uc/uc1/form.png'),
      table: require('@/assets/guide/lin_ind/uc/uc1/table.png'),
      heatmap: require('@/assets/guide/lin_ind/uc/uc1/heatmap.png'),
      trend: require('@/assets/guide/lin_ind/uc/uc1/trend.png'),
    }
  }
}
</script>

<style scoped>

</style>