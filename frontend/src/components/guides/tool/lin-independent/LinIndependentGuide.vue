<!--

  Component:    LinIndependentGuide
  Description:  Usage guide for the lineage independent search feature

-->

<template>
  <function-guide title='Discover <b>lineage-independent</b> search'>

    <!-- Function guide -->
    <template v-slot:default>

      <!-- FORM -->
      <paragraph :src='formImg' left larger-img>
        <p>
          In this analysis type, the user is required to select a <b>location</b> <i>(New York State in the example)</i>
          and a <b>time interval of interest</b> <i>(four weeks ending
          on March 20th, 2022 in the example)</i>.
        </p>
      </paragraph>

      <!-- EXPLORER -->
      <paragraph :src='explorerImg' left larger-img>
        <p>
          The choice of the "time-window" to be analyzed can be supported/refined by the use of
          the <b>Dataset Explorer</b>, which provides a bar-plot of sequences collected on each date in the
          selected location.
        </p>
        <p>
          When used in 4-weeks mode, the explorer also shows a <b>daily breakdown</b> by lineage of the available
          data <i>(on March 18th, in the example, 39% sequences were BA.2, 28% BA.1.1, 22% BA.2.12.1, and 11%
          from other minor lineages)</i>.</p>
      </paragraph>

      <!-- TABLE OVERVIEW -->
      <paragraph :src='TableImg' right larger-img>
        The tool analyzes the data of the selected four-week span, returning a <b>table</b> such as the one in the
        Figure:
        <ul>
          <li>each line corresponds to an amino-acid change;</li>
          <li>the <b>slope</b> represents the rate of growth/decrease in prevalence;
          </li>
          <li>the four columns that follow report the <b>prevalence</b> of the amino-acid change at each of the four
            weeks;
          </li>
          <li>by clicking the
            <v-icon small color='text_var1'>mdi-plus-circle-outline</v-icon>&nbsp;<span
                class='command'>SHOW P-VALUES</span> button, it is also possible to show the p-values related
            to the <b>Chi-square tests</b> defined in
            <v-icon small color='text_var1'>mdi-help-circle-outline</v-icon>&nbsp;<span class='command'>TABLE INTERPRETATION</span>;
          </li>
          <li>data and all the visuals of the analysis can be downloaded.</li>
        </ul>
      </paragraph>

      <!-- TABLE FILTERING OPTS -->
      <paragraph :src='tableFiltersImg' right larger-img>
        <p>
          The <b>filters</b> above the table can be used to restrict the scope of the analysis and select
          a specific gene or collection of amino-acid changes to be shown in the table and following analysis.
        </p>
        These can be selected:
        <ul>
          <li>from a <b>text list</b> pasted by the user;</li>
          <li>from the list of <b>amino-acid changes characterizing a lineage</b> (prevalence in lineage &gE;50%);
          </li>
          <li>from the drop-down menu with the checkboxes.</li>
        </ul>
      </paragraph>

      <p>
        Mutations can be selected by ticking the related checkboxes. Selected mutations can be analyzed using the
        <a href="https://cov-spectrum.org/" target="_blank"><i>covSPECTRUM application</i></a>, documented in their
        Bioinformatics
        publication <a href="https://doi.org/10.1093/bioinformatics/btab856" target="_blank">(Chen et al., 2022)</a>.
        A corresponding query is performed on covSPECTRUM using the same country/continent-level location, time period,
        and list of mutations
        (either in conjunction = logical AND - or in disjunction = logical OR).
      </p>

      <!-- EXPANSION PANEL -->
      <paragraph :src='expansionImg' right larger-img>
        <p>
          Each line in the mutation table can be expanded to examine the <b>breakdown of the sequences</b> associated
          with a specific amino-acid change across the different lineages, for each analyzed week.
        </p>
        <p>
          <i>In the figure, the amino-acid change is predominantly exhibited by sequences assigned to the BA.2.12.1
            lineage.</i>
        </p>
        <p>Using the
          <v-icon small color='text_var1'>mdi-text</v-icon>&nbsp;<span class='command'>CHANGE NOTATION</span>
          button, it is possible to enable grouping of lineages by level in the Pango hierarchy.
          The first option allows to summarize the counts using a level-1 star notation
          (e.g., B.1.* includes both B.1 and all its descendants).
          Similarly, the second option summarizes the counts using a level-2 star notation
          (e.g., B.1.1.* includes both B.1.1 and all its descendants).
          In both cases, lineages exceeding 10% (in at least one of the four observed weeks) are not aggregated.
        </p>
      </paragraph>

      <!-- MUTATION HISTORY -->
      <paragraph :src='historyImg' left>
        Each mutation present in the table can be further explored, by clicking
        on the <v-icon small color='text_var1'>mdi-information-variant</v-icon> symbol on the left of the checkbox.
        This opens a dialog that informs on two aspects:
        <ol>
          <li>which lineages are characterized by the selected mutation (the mutation appears in at least 50% of
            sequences of those lineages contained in the database);
          </li>
          <li>how the sequences harboring the selected mutation distribute over the available lineages.</li>
        </ol>
        <br/>
        <p>
          <i>In the figure, S_S704L is considered characterizing for 12 lineages (including B.1.434); 92.3% of sequences
            with this mutation are of the BA.2.12.1 lineage.</i>
        </p>
      </paragraph>

      <p>
        All the amino acid changes selected in the table (through the checkboxes at the left-hand side of the rows)
        are shown in the following visual representations.
      </p>

      <!-- DIFFUSION HEATMAP -->
      <p>The <b>Diffusion Heatmap</b> allows to observe the increasing and decreasing trends in a fast way.
        The tabs at the top of the section can be used to change the scaling of color gradients in the heatmap.
      </p>
      Specifically:
      <ul>
        <li><b>Diffusion</b>: colors are scaled between 1 and 100 based on the prevalence of amino acid changes (dark
          blue = low
          prevalence, red = high prevalence). This visualization facilitates the identification of highly prevalent
          amino
          acid changes.
        </li>
        <li><b>Growth</b>: colors are scaled based on the ratio between the minimum and maximum prevalence of every
          amino acid change. This visualization facilitates the identification of amino acid changes that had an
          increase or decrease in prevalence (dark blue to red = increase; red to dark blue = decrease).
        </li>
      </ul>
      <br/>
      <p>
        <i>
          In the example below, it is evident that a group of 10 changes at the top is decreasing (representing BA.1)
          while,
          conversely, the 8 at the bottom are increasing together (representing BA.2).
          Other amino acid changes have less clear trends.
        </i>
      </p>
      <collage :src1="heatmapImg1" :src2="heatmapImg2" class="my-2"/>


      <!-- DIFFUSION TREND -->
      <paragraph :src='diffusionImg' right larger-img>
        <p>
          The <b>Diffusion Trend</b> chart also allows to appreciate the point of intersection between the two
          groups of lineages with opposite trends <i>(just before the second week of March 2022)</i>.
        </p>
        <p>
          Here, amino acid changes in the legend on the right can be selected and deselected with a click.
        </p>
        <p>
          <i>A user may note that, at the bottom of the graph, a couple of amino acid changes (S_L452Q and S_S704L) are
            growing from a very low prevalence (around 0%) to almost 15%.</i>
        </p>
      </paragraph>

      <!-- ODD RATIO -->
      <paragraph :src='oddImg' left larger-img>
        <p>
          Such growth can be appreciated more clearly by observing the <b>Log<sub>2</sub> Odd Ratio</b> plots, where
          the log<sub>2</sub> odd ratio is computed by comparing frequencies of each week against the previous one
          (first plot) or against the first week of the period (second plot). <br/> The log<sub>2</sub> scale is used to
          facilitate the comparison of the magnitude of the change between increasing and decreasing amino-acid changes.

        </p>
        <p>
          <i>In the example, the two lines at the top represent the S_L452Q and S_S704L amino acid changes.</i>
        </p>
      </paragraph>

      <paragraph :src='cmdImg' left>
        <p>
          Users can replicate the current analysis shifting the selected period of 1 / 2 weeks backward
          or 1 / 2 weeks forward. This function is provided in the top right corner of the screen, by clicking on the
          <v-icon small color='text_var1'>mdi-clock-edit-outline</v-icon> symbol.
        </p>
        <p>
          In the same menu, users can select the <v-icon small color='text_var1'>mdi-airplane-edit</v-icon> symbol
          to switch from the current location to a more general granularity (from Region to Country, from Country to Continent).
        </p>
      </paragraph>


    </template>

    <!-- Use cases -->
    <template v-slot:use-cases>
      <lin-ind-use-case1/>
      <lin-ind-use-case2/>
      <lin-ind-use-case3/>
      <lin-ind-use-case4/>
    </template>

  </function-guide>
</template>

<script>
import FunctionGuide from '@/components/guides/tool/FunctionGuide.vue'
import Paragraph from '@/components/general/basic/Paragraph.vue'
import Collage from '@/components/general/basic/Collage.vue'
import LinIndUseCase1 from "@/components/guides/tool/lin-independent/uc/LinIndUseCase1.vue";
import LinIndUseCase2 from "@/components/guides/tool/lin-independent/uc/LinIndUseCase2.vue";
import LinIndUseCase3 from "@/components/guides/tool/lin-independent/uc/LinIndUseCase3.vue";
import LinIndUseCase4 from "@/components/guides/tool/lin-independent/uc/LinIndUseCase4.vue";

export default {
  name: 'LinIndependentGuide',
  components: {LinIndUseCase4, LinIndUseCase3, LinIndUseCase2, LinIndUseCase1, Collage, Paragraph, FunctionGuide},

  data() {
    return {
      /** Images */
      formImg: require('@/assets/guide/lin_ind/form.png'),
      explorerImg: require('@/assets/guide/lin_ind/explorer.png'),
      cmdImg: require('@/assets/guide/lin_ind/cmd.png'),
      TableImg: require('@/assets/guide/lin_ind/table.png'),
      historyImg: require('@/assets/guide/lin_ind/history.png'),
      tableFiltersImg: require('@/assets/guide/lin_ind/table_filters.png'),
      heatmapImg1: require('@/assets/guide/lin_ind/heatmap1.png'),
      heatmapImg2: require('@/assets/guide/lin_ind/heatmap2.png'),
      diffusionImg: require('@/assets/guide/lin_ind/diffusion.png'),
      oddImg: require('@/assets/guide/lin_ind/odd.png'),
      expansionImg: require('@/assets/guide/lin_ind/expansion.png'),
    }
  }
}
</script>

<style scoped>

</style>
