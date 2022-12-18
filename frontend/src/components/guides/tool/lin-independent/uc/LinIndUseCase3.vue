<!--

  Component:    LinIndUseCase3
  Description:  Use case for lineage independent search (ex. UC.2)

-->

<template>
  <use-case source-name='Nextstrain' source-date='08/12/2022'
            name='<b>Use case 3</b>: Early spread of the Delta variant in the UK'>

    <paragraph :src='form' left larger-img>
      <p>
        The following panels show a summary of the main outputs of a "lineage-independent"
        analysis, performed on an interval of 4 weeks spanning
        from 10/04/2021 to 07/05/2021 in the UK.
      </p>
    </paragraph>

    <paragraph :src='table' right larger-img>
      <p>
        This interval of time corresponds with the <b>early spread of the Delta VOC in the UK</b>.
      </p>
      <p>
        The mutation table illustrates the relative prevalence/association of
        <span class='monospaced'>S_N501Y</span> and <span class='monospaced'>S_L452R</span>,
        two amino acid changes <i>characteristic of the Alpha and Delta VOC respectively</i>
        in different sub-lineages of SARS-CoV-2.<br/>
        While <span class='monospaced'>S_N501Y</span> is mostly associated with <i>Alpha-related lineages</i>,
        <span class='monospaced'>S_L452R</span> is observed almost exclusively in <i>lineages/sub-lineages of
        Delta</i>.
      </p>
    </paragraph>

    <paragraph :src='heatmap' left larger-img>
      <p>
        The <b>Diffusion Heatmap</b> illustrates the prevalence of 6 amino acid changes
        in the Spike glycoprotein <b>characteristic of the Alpha variant</b>
        <span class='monospaced'>(P681H, D1118H, S982A, A570D, T716I, N501Y) </span>
        and 7 amino acid changes <b>characteristic of the Delta variant</b>
        <span class='monospaced'>(T19R, S478K, R158G, D950N, P681R, L452R, G142D)</span>.
      </p>
      <p>
        A clear <i>increase</i> in Delta variant-associated changes and a concomitant
        <i>decrease</i> in changes characteristic of the Alpha variant can be observed.
      </p>
    </paragraph>

    <paragraph :src='trend' right larger-img>
      <p>
        Interestingly, G142D which is associated with the majority of the sub-lineages
        of the Delta, but is not ubiquitous in the descendants of this VOC, shows a
        clearly distinct pattern, indicative of the spread and diffusion of different
        sub-lineages of this variant.
      </p>
      <p>
        Equivalent patterns are also recovered by the <b>Diffusion Trend</b> chart.
      </p>
    </paragraph>

  </use-case>

</template>

<script>
import UseCase from "@/components/guides/tool/UseCase.vue";
import Paragraph from "@/components/general/basic/Paragraph.vue";

export default {
  name: 'LinIndUseCase3',
  components: {Paragraph, UseCase},

  data() {
    return {
       /** Images */
      form: require('@/assets/guide/lin_ind/uc/uc3/form.png'),
      table: require('@/assets/guide/lin_ind/uc/uc3/table.png'),
      heatmap: require('@/assets/guide/lin_ind/uc/uc3/heatmap.png'),
      trend: require('@/assets/guide/lin_ind/uc/uc3/trend.png'),

    }
  }
}
</script>

<style scoped>

</style>