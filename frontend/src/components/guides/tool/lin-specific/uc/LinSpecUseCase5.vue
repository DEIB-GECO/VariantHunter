<!--

  Component:    LinSpecUseCase5
  Description:  Use case for lineage specific search (ex. UC.3)

-->

<template>
  <use-case source-name='Gisaid' source-date='06/02/2022'
            name='<b>Use case 5</b>: Delta AY.122.6 lineage'>
    <p>
      Here we report a collection of screenshots from <b>Pango designation</b>
      <span class='monospaced'>issue 394</span>
      <a href='https://github.com/cov-lineages/pango-designation/issues/394' target='_blank'>
        (https://github.com/cov-lineages/pango-designation/issues/394)
      </a>
      , which led to the definition of the <b>AY.122.6 sub-lineage</b> of the <i>Delta variant</i>.<br/>
      The novel lineage is defined by the <span class='monospaced'>E484A</span> amino acid change
      in the <i>Spike glycoprotein</i> according to the submitter; and shows a relative growth advantage
      in <i>France</i> compared to the parental <b>lineage AY.122</b>.
    </p>

    <div class='with-borders white'>
      <pic :src='img1' img-max-height='300'/>
      <collage :src1='img2' :src2='img3' img-max-height='300'/>
      <pic :src='img4' img-max-height='300'/>
    </div>

    <paragraph :src='form' left larger-img>
      <p class='mt-sm-5'>
        A summary of the main results of a Variant Hunter "lineage-specific" analysis, executed
        on the <b>AY.122 lineage</b> in the geographic location <i>(France)</i> and interval of time
        <i>(November-December 2021)</i> where the novel lineage first emerged, is reported.
      </p>
    </paragraph>

    <p>
      <i>
        In this case all the analyses were executed by means of the Docker implementation of Variant Hunter,
        using a dump of the <b>GISAID database obtained on 06/02/2022</b>.
      </i>
    </p>

    <pic :src='table'/>
    <p class='mt-5'>
      From the main output of Variant Hunter a clear increase in the prevalence
      of <span class='monospaced'>E484A</span> and of another amino acid change in the Spike glycoprotein,
      <span class='monospaced'>G181V</span> can be observed within <b>lineage AY.122</b>.
    </p>

    <p>
      According to the <b>Diffusion Heatmap</b><sup>
      <v-icon small color="text_var1">mdi-numeric-1</v-icon>
    </sup> both changes show a <i>consistent increase</i>
      in prevalence <span class='monospaced'>(from 10% to 26%)</span> in the interval of
      time included in the analysis.
    </p>

    <p>
      The <b>Odds Ratio</b><sup>
      <v-icon small color="text_var1">mdi-numeric-2</v-icon>
    </sup> plot is consistent with a relative advantage
      in growth for both amino acid changes (<span class='monospaced'>E484A</span> and
      <span class='monospaced'>G181V</span>), as illustrated by the
      <i>constant increase</i> of the "diffusion" odd ratio in the corresponding plot;
      and by the fact that values of odd ratio > 1 are recovered at every time point of
      the 4 weeks interval considered in the analysis.<br/>
    </p>

    <div class="f_tertiary with-borders">
      <pic :src='heatmap'/>
      <div class="text-body-5 compact-text-4 mx-2 f_primary--text font-italic">
        <v-icon small color="f_primary">mdi-numeric-1</v-icon>
        : Screenshots from Variant Hunter 1.0. The app layout may differ from the version in use.
      </div>
      <pic :src='odd'/>
      <div class="text-body-5 compact-text-4 mx-2 f_primary--text font-italic">
        <v-icon small color="f_primary">mdi-numeric-2</v-icon>
        : Screenshots from Variant Hunter 1.0. The log<sub>2</sub> scale was not yet being applied. The app layout may
        differ from
        the version in use.
      </div>
    </div>

    <p class="mt-5">
      <i>
        Indeed, in this plot values
        <span class='monospaced'>around 1</span> indicate a steady state:
        no increase or decrease in frequency,
        values <span class='monospaced'>below 1</span> indicate a decrease,
        and values <span class='monospaced'>> 1</span> are indicative of
        rapid increase/relative growth advantage.
      </i>
    </p>
  </use-case>
</template>

<script>
import UseCase from "@/components/guides/tool/UseCase.vue";
import Paragraph from "@/components/general/basic/Paragraph.vue";
import Pic from "@/components/general/basic/Pic.vue";
import Collage from "@/components/general/basic/Collage.vue";

export default {
  name: 'LinSpecUseCase5',
  components: {Collage, Pic, Paragraph, UseCase},

  data() {
    return {
      img1: require('@/assets/guide/lin_dep/uc/uc5/img1.png'),
      img2: require('@/assets/guide/lin_dep/uc/uc5/img2.png'),
      img3: require('@/assets/guide/lin_dep/uc/uc5/img3.png'),
      img4: require('@/assets/guide/lin_dep/uc/uc5/img4.png'),
      form: require('@/assets/guide/lin_dep/uc/uc5/form.png'),
      table: require('@/assets/guide/lin_dep/uc/uc5/table.png'),
      heatmap: require('@/assets/guide/lin_dep/uc/uc5/heatmap.png'),
      odd: require('@/assets/guide/lin_dep/uc/uc5/odd.png')
    }
  }
}
</script>

<style scoped>

</style>