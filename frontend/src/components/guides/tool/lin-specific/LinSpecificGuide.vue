<!--

  Component:    LinSpecificGuide
  Description:  Usage guide for the lineage dependent search feature

-->

<template>
  <function-guide title='Discover <b>lineage-specific</b> search'>

    <!-- Function guide -->
    <template v-slot:default>
      <paragraph :src='formImg' left larger-img>
        <p>
          In this analysis the user is required to specify one or more lineages of interest,
          in addition to the other search parameters.<br/>
          Lineages can be specified simply by entering their name in the lineage-selection form.
          To include a specific lineage with its decendants in the Pango hierarchy, users can employ the star-notation (e.g., BA.2.*).
        </p>
        <p>
          <i>In this example we choose the lineage BA.2.</i>
        </p>
      </paragraph>

      <paragraph :src='tableImg' right larger-img>
        <p>
          The same visual elements are shown as in the previous analysis mode.<br/>
          Here, however, counts shown for each amino-acid change  are reported only for the selected lineage(s).
        </p>
        <p>
          As shown in the figure, in this mode <b>amino acid changes</b> that are <b>characteristic of the selected
          lineage</b> (common to at least 50% of the sequences of the database assigned to
          that lineage) are <span class='char-mut'>highlighted in yellow</span>.
        </p>
      </paragraph>

      Here, the <b>P-values</b> in the table are computed using a Chi-square test of independence of
      variables in a contingency table. They represent:
      <ul>
        <li>
          <i>"P-value with mut"</i>: if the population «with mutation» is growing differently compared
          to the entire population of genome sequences;
        </li>
        <li>
          <i>"P-value without mut"</i>: if the population «without mutation» is growing differently compared
          to the entire population of genome sequences;
        </li>
        <li>
          <i>"P-value comparative"</i>: if the population «with mutation» is growing differently compared
          to the population «without mutation».
        </li>
      </ul>

      <paragraph :src='heatmapImg' left larger-img>
        <p>
          By selecting in the table only the amino-acid changes that are
          <span class='char-mut'>highlighted in yellow</span>
          <i>(i.e., characterizing for BA.2)</i> we observe the following <b>Heatmap</b>,
          where most mutations are fixed for four weeks, while 8 of them (at the top
          of the heatmap) have increased their prevalence from  about 75% to almost 100%.
        </p>
      </paragraph>

      <paragraph :src='diffusionImg' right>
        <p>The trend is clearly shown in the <b>Diffusion Trend</b> chart.</p>
      </paragraph>

      <paragraph :src='oddImg' right>
        <p>
          By looking at the <b>Log<sub>2</sub> Odd Ratio</b> plots we can appreciate an interesting trend of these 8 mutations
          (hovering on the dots, the details on the diffusion's growth are shown).
        </p>
      </paragraph>
      
      <paragraph :src='odd2Img' right>
         <p>By using the <span class='command'>Next/Prev Week</span> buttons below the plot, a user
          can <b>navigate in time</b> replicating the same analysis using a four-week period shifted of
          one week ahead or behind.
        </p>
        <p>
          <i>
            In the figure, we show the selected mutations when the <span class='command'>Next Week</span>
            is analyzed, including also the week of March 27th, 2022.
          </i>
        </p>
      </paragraph>

       <paragraph :src='cmdImg' left>
        <p>
        In both analysis modes, users can replicate the current analysis shifting the selected period of 1 / 2 weeks backward 
        or 1 / 2 weeks forward. This function is provided in the top right corner of the screen, by clicking on the clock symbol.   
        </p>
        <p>
        In the same menu, users can select the airplane symbol to switch from the current location to a more general granularity 
        (from Region to Country, from Country to Continent).
        </p>
        <p>
        Finally, the third symbol can be used to switch from the current analysis mode (Lineage Specific) to the more general Lineage Independent one.
        </p>
      </paragraph>


      <p>
        This specific mode of analysis can support the discovery of new sub-lineages. We provide  relevant
        use cases captured at different times of the use of VariantHunter: three new sub-lineages were
        identified during April 2022, whereas two new sub-lineages were identified in December 2022.
      </p>
    </template>

    <!-- Use cases -->
    <template v-slot:use-cases>
      <lin-spec-use-case1/>
      <lin-spec-use-case2/>
      <lin-spec-use-case3/>
      <lin-spec-use-case4/>
      <lin-spec-use-case5/>

    </template>

  </function-guide>
</template>

<script>
import FunctionGuide from '@/components/guides/tool/FunctionGuide.vue'
import Paragraph from '@/components/general/basic/Paragraph.vue'
import LinSpecUseCase3 from "@/components/guides/tool/lin-specific/uc/LinSpecUseCase3.vue";
import LinSpecUseCase4 from "@/components/guides/tool/lin-specific/uc/LinSpecUseCase4.vue";
import LinSpecUseCase5 from "@/components/guides/tool/lin-specific/uc/LinSpecUseCase5.vue";
import LinSpecUseCase2 from "@/components/guides/tool/lin-specific/uc/LinSpecUseCase2.vue";
import LinSpecUseCase1 from "@/components/guides/tool/lin-specific/uc/LinSpecUseCase1.vue";

export default {
  name: 'LinSpecificGuide',
  components: {
    LinSpecUseCase1,
    LinSpecUseCase2, LinSpecUseCase5, LinSpecUseCase4, LinSpecUseCase3, Paragraph, FunctionGuide},

  data() {
    return {
      /** Images */
      formImg: require('@/assets/guide/lin_dep/form.png'),
      tableImg: require('@/assets/guide/lin_dep/table.png'),
      heatmapImg: require('@/assets/guide/lin_dep/heatmap.png'),
      diffusionImg: require('@/assets/guide/lin_dep/diffusion.png'),
      oddImg: require('@/assets/guide/lin_dep/odd.png'),
      cmdImg: require('@/assets/guide/lin_dep/cmd.png'),
      odd2Img: require('@/assets/guide/lin_dep/odd2.png'),
    }
  }
}
</script>

<style scoped>


</style>
