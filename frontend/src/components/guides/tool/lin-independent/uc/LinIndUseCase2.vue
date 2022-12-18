<!--

  Component:    LinIndUseCase2
  Description:  Use case for lineage independent search (ex. UC.3)

-->

<template>
  <use-case source-name='Nextstrain' source-date='08/12/2022'
            name='<b>Use case 2</b>: Spread of the Omicron variant and displacement of Delta in Europe and North America'>

    <p>
      A "lineage-independent" analysis was applied to study the prevalence of amino acid
      changes in the Spike glycoprotein in an interval of time spanning
      from 05/12/2021 to 01/01/2022 in <b>Europe</b> and in <b>North America</b>. <br/>
      This interval coincides with the rapid emergence and spread of the Omicron VOC of SARS-CoV-2 worldwide.
    </p>

    <p>
      A clear <i>decrease</i> in the prevalence of 6 amino acid changes <b>characteristic of the Delta VOC</b>
      <span class='monospaced'>(G142D, D950N, L452R, R158G, P681R, T19R)</span>
      and a concomitant and striking <i>increase</i> of amino acid changes characteristic of the
      <b>Omicron VOC</b><sup>*</sup> of SARS-CoV-2 is observed both in <i>Europe</i> and <i>North America</i>.
    </p>

    <p>
      Identical patterns are recovered both from the <b>Diffusion Heatmap</b> and <b>Diffusion Trend</b> chart.
    </p>
    <p><sub><v-icon x-small>mdi-asterisk</v-icon><i>: a selection of 11 defining amino acid changes is shown for space constraints</i></sub></p>

    <div class="f_tertiary with-borders">
      <collage :src1='full1' :src2='full2'/>
    </div>

  </use-case>
</template>

<script>
import Collage from "@/components/general/basic/Collage.vue";
import UseCase from "@/components/guides/tool/UseCase.vue";

export default {
  name: 'LinIndUseCase2',
  components: {Collage, UseCase},

  data() {
    return {
      /** Images */
      full1: require('@/assets/guide/lin_ind/uc/uc2/full1.png'),
      full2: require('@/assets/guide/lin_ind/uc/uc2/full2.png')
    }
  }
}
</script>

<style scoped>

</style>