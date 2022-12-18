<!--

  Component:    LinIndUseCase4
  Description:  Use case for lineage independent search (ex. UC.1)

-->

<template>
  <use-case source-name='Nextstrain' source-date='08/12/2022'
            name='<b>Use case 4:</b> Emergence and spread of the alpha variant in the UK'>

    <paragraph :src='form' left larger-img>
      <p>
        The following panels show a summary of the main outputs of a "lineage-independent"
        analysis, performed on an interval of 4 weeks spanning
        from 26/10/2020 to 22/11/2020 in the UK.
      </p>
    </paragraph>

    <p>
      This interval of time corresponds with the <b>emergence and spread of the Alpha
      VOC in the UK</b>. As illustrated by the <b>Mutations table</b> and the <b>Diffusion
      Heatmap</b>, 6 amino acid changes in the <i>Spike glycoprotein</i> are singled out due
      to <i>remarkable increase in frequency</i> (from 1% to 11%).
      These include: P681H, A570D, D1118H, S982A, T716I, N501Y.

    </p>

    <div class="with-borders f_tertiary">
      <pic :src='table' class="mb-2"/>
      <collage :src1="heatmap1" :src2="heatmap2"/>
    </div>

    <p class='mt-5'>
      Similar patterns of <i>increase in frequency</i> of the 6 selected amino acid changes
      can be observed also from the <b>Diffusion Trend</b> chart and <b>Log<sub>2</sub> Odd Ratio</b> plots.
    </p>

    <p>
      Importantly, the 6 amino acid changes highlighted in the plot account for the complete
      set of amino-acid changes in Spike glycoprotein characteristic of the <b>Alpha VOC</b>.
    </p>

    <div class="with-borders f_tertiary">
      <pic :src='trend'/>
      <pic :src='odd'/>
    </div>

  </use-case>
</template>

<script>

import UseCase from "@/components/guides/tool/UseCase.vue";
import Paragraph from "@/components/general/basic/Paragraph.vue";
import Pic from "@/components/general/basic/Pic.vue";
import Collage from "@/components/general/basic/Collage.vue";

export default {
  name: 'LinIndUseCase4',
  components: {Collage, Pic, Paragraph, UseCase},

  data() {
    return {
      /** Images */
      form: require('@/assets/guide/lin_ind/uc/uc4/form.png'),
      table: require('@/assets/guide/lin_ind/uc/uc4/table.png'),
      heatmap1: require('@/assets/guide/lin_ind/uc/uc4/heatmap1.png'),
      heatmap2: require('@/assets/guide/lin_ind/uc/uc4/heatmap2.png'),
      trend: require('@/assets/guide/lin_ind/uc/uc4/trend.png'),
      odd: require('@/assets/guide/lin_ind/uc/uc4/odd.png'),
    }
  }
}
</script>

<style scoped>

</style>