<!--

  Component:    LinSpecUseCase1
  Description:  Use case for lineage specific search

-->

<template>
  <use-case source-name='Nextstrain' source-date='08/12/2022'
            name='<b>Use case 1</b>: Hydra BN.1.9 lineage'>
    <p>
      <b>BN.1.9</b> is a recently (November 2022) emerged sub-lineage of the Omicron BN.1,
      circulating in different countries and defined by a V58F amino-acid substitution in
      the E protein. The lineage was defined by the <b>Pango designation</b>
      <span class='monospaced'>issue 1327</span>
      <a href='https://github.com/cov-lineages/pango-designation/issues/1327' target='_blank'>
        (https://github.com/cov-lineages/pango-designation/issues/1327)
      </a>.<br/>
      A screenshot is reported below.
    </p>

    <div class='with-borders white'>
      <pic :src='img1'/>
    </div>

    <paragraph :src='form' left larger-img>
      <p class='mt-sm-5'>
        A "lineage specific" analysis by Variant Hunter was applied to investigate this case of study.
        Genomic sequences assigned to <b>BN.1</b>, and isolated in <i>North America</i>
        in between <i>17-10-2022 and 14-11-2022</i>, were selected.
      </p>
    </paragraph>

    <p class='mt-5'>
      The analysis was restricted to the E gene. Notwithstanding the limited number of available
      sequences, an increase in the prevalence of E V58F, the amino acid change that defines the
      novel lineage, can be observed from the <b>Mutation Table</b>.
    </p>
    <pic :src='table'/>

    <p class='mt-5'>
      The same conclusion is supported both by the "Growth speed" <b>Diffusion Heatmap</b>
      and by the <b>Diffusion Trend</b> plot, which provide a visual representation of the results.
    </p>

    <div class="f_tertiary with-borders">
      <pic :src='heatmap'/>
      <pic :src='odd'/>
    </div>

    <p class='mt-5'>
      All in all this use case demonstrates that variant Hunter can identify trends in the
      change of prevalence in amino-acid changes <b>also if/when a limited number of sequences is concerned</b>.
    </p>

  </use-case>
</template>

<script>
import UseCase from "@/components/guides/tool/UseCase.vue";
import Paragraph from "@/components/general/basic/Paragraph.vue";
import Pic from "@/components/general/basic/Pic.vue";
import Collage from "@/components/general/basic/Collage.vue";

export default {
  name: 'LinSpecUseCase1',
  components: {Pic, Paragraph, UseCase},

  data() {
    return {
      /** Images */
      img1: require('@/assets/guide/lin_dep/uc/uc1/img1.png'),
      form: require('@/assets/guide/lin_dep/uc/uc1/form.png'),
      table: require('@/assets/guide/lin_dep/uc/uc1/table.png'),
      diffusion: require('@/assets/guide/lin_dep/uc/uc1/diffusion.png'),
      heatmap: require('@/assets/guide/lin_dep/uc/uc1/heatmap.png'),
      
    }
  }
}
</script>

<style scoped>

</style>