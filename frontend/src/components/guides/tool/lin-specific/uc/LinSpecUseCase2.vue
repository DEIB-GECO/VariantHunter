<!--

  Component:    LinSpecUseCase2
  Description:  Use case for lineage specific search

-->

<template>
  <use-case source-name='Nextstrain' source-date='08/12/2022'
            name='<b>Use case 2</b>: Omicron BA.5.2.39 lineage'>
    <p>
      <b>BA.5.2.39</b>, a sub-lineage of BA.5.2 that carries an additional R346T
      amino acid change in the Spike glycoprotein compared with its ancestor,
      was designated by <b>Pango</b>
      <span class='monospaced'>issue 1279</span>
      <a href='https://github.com/cov-lineages/pango-designation/issues/1279' target='_blank'>
        (https://github.com/cov-lineages/pango-designation/issues/1279)</a>.<br/>
      A screenshot of the issue and the original designation of the lineage is reported below.
    </p>
    <p>
      According to the submitter, BA.5.2.39 derives from an un-named/un-designated
      sub-lineage of BA.5.2 characterized by the presence of a T1050N amino-acid
      substitution in ORF1b. Interestingly this amino-acid change is observed in more
      than <span class="char-mut">50% of the genomic sequences</span> assigned to BA.5.2 at present (28/11/2022).
    </p>

    <div class='with-borders white'>
      <pic :src='img1'/>
    </div>

    <paragraph :src='form' left larger-img>
      <p class='mt-sm-5'>
        A Variant Hunter "lineage-specific" analysis was applied to study amino-acid changes in the
        <b>BA.5.2 lineage</b>, in <i>North America</i> in an interval of time between
        <i>26/09/2022 and 23/10/2022</i>, which should coincide with the emergence and spread of BA.5.2.39.
      </p>
    </paragraph>

    <p class='mt-5'>
      The <b>Mutation Table</b> shows a clear increase in the prevalence of Spike R346T in
      sequences assigned to BA.5.2 <i>(6.8% to 16%)</i> in the selected interval of time.
      Interestingly a more moderate relative increase of ORF1b_T1050N, from 77.6% to 82.3% is also observed.
    </p>
    <pic :src='table'/>

    <p class='mt-5'>
      This pattern is clearly illustrated by the “Growth speed” Diffusion heatmap, and by the matched
      Log2 odd-ratio diffusion plot, where a more than 2-fold increase in the prevalence of S_R346T is recovered.
    </p>

    <div class="f_tertiary with-borders">
      <pic :src='heatmap'/>
      <pic :src='odd'/>
    </div>

  </use-case>
</template>

<script>
import UseCase from "@/components/guides/tool/UseCase.vue";
import Paragraph from "@/components/general/basic/Paragraph.vue";
import Pic from "@/components/general/basic/Pic.vue";

export default {
  name: 'LinSpecUseCase2',
  components: {Pic, Paragraph, UseCase},

  data() {
    return {
      /** Images */
      img1: require('@/assets/guide/lin_dep/uc/uc2/img1.png'),
      form: require('@/assets/guide/lin_dep/uc/uc2/form.png'),
      table: require('@/assets/guide/lin_dep/uc/uc2/table.png'),
      heatmap: require('@/assets/guide/lin_dep/uc/uc2/heatmap.png'),
      odd: require('@/assets/guide/lin_dep/uc/uc2/odd.png')
    }
  }
}
</script>

<style scoped>

</style>
