<!--

  Component:    LinSpecUseCase4
  Description:  Use case for lineage specific search (ex. UC.2)

-->

<template>
  <use-case source-name='Nextstrain' source-date='19/04/2022'
            name='<b>Use case 4</b>: Omicron BA.1.15.2 lineage'>

    <p>
      Here we report a collection of screenshots from <b>Pango designation</b>
      <span class='monospaced'>issue 508</span>
      <a href='https://github.com/cov-lineages/pango-designation/issues/508' target='_blank'>
        (https://github.com/cov-lineages/pango-designation/issues/508)
      </a>
      , which led to the definition of the <b>BA.1.15.2 sub-lineage</b> of SARS-CoV-2.<br/>
      The novel lineage is defined by the <span class='monospaced'>Q628K</span> amino acid change
      in the <i>Spike glycoprotein</i> according to the submitter.
    </p>

    <div class='with-borders white'>
      <pic :src='img1' img-max-height='300'/>
      <collage :src1='img2' :src2='img3' img-max-height='300'/>
      <pic :src='img4' img-max-height='300'/>
    </div>

    <paragraph :src='form' left larger-img>
      <p class='mt-sm-5'>
        Then, we report the main results of a Variant-Hunter "lineage-specific" analysis executed
        on the <b>BA.1.15 lineage</b> in the geographic location <i>(USA)</i> and interval of time
        <i>(March 2022)</i> where the novel lineage first emerged.
      </p>
    </paragraph>

    <pic :src='table'/>
    <p class='mt-5'>
      A clear <i>increase</i> in the prevalence of <span class='monospaced'>Q628K</span>
      within <b>lineage BA.1.15.2</b> is observed both from the <b>Odds Ratio<sup>
      <v-icon small color="text_var1">mdi-numeric-2</v-icon>
    </sup></b> plot
      and the <b>Diffusion Heatmap</b><sup>
      <v-icon small color="text_var1">mdi-numeric-1</v-icon>
    </sup>.
    </p>

    <p>
      Interestingly, we also observe a similar increase in the prevalence of
      <span class='monospaced'>V320I</span>, an amino acid change that to the best of
      our knowledge is <u>not</u> currently associated with/does <u>not</u> define any sub-lineage of
      <b>BA.1.15</b>.
    </p>

    <p>
      Both <span class='monospaced'>S_V320I</span> and <span class='monospaced'>S_Q628K</span>
      show a similar relative growth advantage according to the <b>Odds Ratio</b><sup>
      <v-icon small color="text_var1">mdi-numeric-2</v-icon>
    </sup> plot
      compared to the amino acid changes that define the parental lineage. <br/>
      After a rapid surge in frequency <span class='monospaced'>from 1 to 12%</span>,
      the two novel mutations seem to <i>"stabilize"</i> around <span class='monospaced'>15%</span>,
      in the last week of the interval considered in the analysis, and show an odd ratio of
      <span class='monospaced'>~1</span>.
    </p>

    <div class="f_tertiary with-borders">
      <pic :src='heatmap'/>
      <div class="text-body-5 compact-text-4 mx-2 f_primary--text font-italic">
        <v-icon small color="f_primary">mdi-numeric-1</v-icon>
        : Screenshot from Variant Hunter 1.0. The app layout may differ from the version in use.</div>
      <pic :src='odd'/>
      <div class="text-body-5 compact-text-4 mx-2 f_primary--text font-italic">
        <v-icon small color="f_primary">mdi-numeric-2</v-icon>
        : Screenshot from Variant Hunter 1.0. The log<sub>2</sub> scale had not been applied yet. The app layout may differ from
        the version in use.</div>
    </div>

    <p class='mt-5'>
      <i>In this plot values
        <span class='monospaced'>around 1</span> indicate a steady state:
        no increase or decrease in frequency,
        values <span class='monospaced'>below 1</span> indicate a decrease,
        and values <span class='monospaced'>> 1</span> are indicative of
        rapid increase/relative growth advantage.</i>
    </p>
  </use-case>

</template>

<script>
import UseCase from "@/components/guides/tool/UseCase.vue";
import Paragraph from "@/components/general/basic/Paragraph.vue";
import Pic from "@/components/general/basic/Pic.vue";
import Collage from "@/components/general/basic/Collage.vue";

export default {
  name: 'LinSpecUseCase4',
  components: {Collage, Pic, Paragraph, UseCase},

  data() {
    return {
      /** Images */
      img1: require('@/assets/guide/lin_dep/uc/uc4/img1.png'),
      img2: require('@/assets/guide/lin_dep/uc/uc4/img2.png'),
      img3: require('@/assets/guide/lin_dep/uc/uc4/img3.png'),
      img4: require('@/assets/guide/lin_dep/uc/uc4/img4.png'),
      form: require('@/assets/guide/lin_dep/uc/uc4/form.png'),
      table: require('@/assets/guide/lin_dep/uc/uc4/table.png'),
      heatmap: require('@/assets/guide/lin_dep/uc/uc4/heatmap.png'),
      odd: require('@/assets/guide/lin_dep/uc/uc4/odd.png')
    }
  }
}
</script>

<style scoped>

</style>