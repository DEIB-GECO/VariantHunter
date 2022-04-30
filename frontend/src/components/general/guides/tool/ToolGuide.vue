<!--
  Component:    ToolGuide
  Description:  Usage guide for the tool
-->

<template>
  <v-container class='ml-0 ml-sm-auto mr-0 mr-sm-auto mt-10'>
    <h3>
      <v-icon left color='#000000DE' large>mdi-human-greeting</v-icon>
      What is VariantHunter
    </h3>
    <div class='pl-6 pl-sm-10 pr-6 pr-sm-10'>
      <p>
        <i>VariantHunter</i> analyzes the frequencies of amino acid mutations of <i>SARS-CoV-2</i> in order to <b>observe
        interesting variant trends</b> or <b>identify novel emerging variants</b>.

        <i>VariantHunter</i> supports two modes of analysis: <b>Lineage Independent</b> and <b>Lineage
        Dependent</b>.
      <p />
      <p>
        Each mode allows to open several analysis sessions (managed in panels that can be <i>expanded, collapsed, or
        deleted</i> at the user's choice).
      </p>

      <Paragraph :src='introImg' img-max-height='230' left>
        <p>
          The underlying mechanism of both methodologies is the same: each amino acid mutation is analyzed for a
          <b>time period of 4 weeks</b>.<br />
          For each week, the <i>frequency of the mutation</i> (computed as
          <span class='formula'>"number of sequencing harboring the mutation"/"total number of sequences collected in that week"</span>)
          is considered (see the four blue dots in the Figure);
          then, a linear model is fitted on the four data points (red line in the Figure).
        </p>
      </Paragraph>
      <p>
        The <b>slope</b> of the regression line represents <i>how fast the mutation is growing</i> (i.e., its
        percentage is increasing). <i>Positive slopes</i> indicate an increasing trend, while <i>negative</i>
        values of the slope indicate a decreasing trend.
      </p>
      <p>
        <b>Chi squared tests</b> are computed to test the <i>significance of the change of frequency</i> of the
        mutation.
      </p>
      <p>
        The main results of both analyses are summarized in a <b>table of mutations</b>, reporting their
        <i>prevalence</i> over the 4 weeks, their <i>slope</i>, and Chi squared tests <i>p-values</i>.
        In addition, different visualizations support the intuition of the observed trends of diffusion:
        a <b>heatmap</b> and various <b>line-plots</b> that represent <i>prevalence</i> or their <i>odd ratios</i>.
      </p>
    </div>

    <v-container class='pl-0 pl-sm-10 pr-0 pr-sm-10 pb-5'>

      <v-expansion-panels class='mt-3' flat>

        <!-- LINEAGE INDEPENDENT -->
        <FunctionGuide title='Discover lineage-independent search' no-use-cases>

          <!-- Function guide -->
          <template v-slot:default>
            <Paragraph :src='linIndFormImg' left larger-img>
              <p>
                In this analysis, the user is required to select a <b>location</b> of interest
                <i>(New York State in the example)</i> and a <b>period of interest</b> &nbsp; <i>(four weeks ending
                on March 20th, 2022 in the example)</i>.
              </p>
            </Paragraph>
            <Paragraph :src='linIndExplorerImg' right larger-img>
              <p>
                The choice of the time-span to be analyzed can be supported by the use of
                the <b>Dataset Explorer</b>, a bar-plot of sequences collected on each date in the
                selected location.
              </p>
              <p>
                When used on 4-weeks mode, the explorer also shows a
                diagram of <b>daily lineages breakdown</b> &nbsp; <i>(on March 18th, in the example, 39%
                sequences were BA.2, 28% BA.1.1, 22% BA.2.12.1, and 11% from other minor lineages)</i>.</p>
            </Paragraph>

            <Paragraph :src='linIndTableImg' left larger-img>
              The tool analyzes the data of the selected four-week span, returning a <b>table</b> such as the one in the
              Figure:
              <ul>
                <li>each line corresponds to a mutation of interest;</li>
                <li>the <b>slope</b> represents how fast the frequency of the mutation increased in the selected period;
                </li>
                <li>the four following columns report the <b>frequency of the mutation</b> in each of the four weeks;
                </li>
                <li>the &nbsp;
                  <v-icon small color='#000000de'>mdi-plus-circle-outline</v-icon>&nbsp;<span class='command'>SHOW P-VALUES</span>
                  button adds, to the end of the table, three columns of <b>Chi squared tests</b> defined in
                  &nbsp;
                  <v-icon small color='#000000de'>mdi-help-circle-outline</v-icon>&nbsp;<span class='command'>TABLE INTERPRETATION</span>;
                </li>
                <li>data and all the visuals of the analysis can be <b>downloaded</b>.</li>
              </ul>
            </Paragraph>

            <Paragraph :src='linIndTableFiltersImg' right larger-img>
              <p>Above the table, we can use <b>filtering options</b> to choose the protein harbouring mutations
                and the specific mutations to be shown in the table and following analysis.</p>
              These can be selected:
              <ul>
                <li>from a <b>text list</b> uploaded from the user;</li>
                <li>from the list of <b>characterizing mutations</b> of lineages;</li>
                <li>from a scrollable <b>list</b> with checkboxes.</li>
              </ul>
            </Paragraph>

            <p>
              All the mutations selected in the table (through checkboxes at the left-hand side of the rows)
              are shown in the following visual representations.
            </p>

            <Paragraph :src='linIndHeatmapImg' left larger-img>
              <p>
                A <b>Heatmap</b> allows to observe the increasing and decreasing trends in a fast way.
              </p>
              <p>
                <i>
                  In the example, it is apparent that a group of 10 mutations on top is decreasing (representing
                  BA.1)
                  and a group of 8 mutations at the bottom is increasing together (representing BA.2).
                  Other mutations have less clear trends.
                </i>
              </p>
            </Paragraph>

            <Paragraph :src='linIndDiffusionImg' right larger-img>
              <p>
                The <b>Diffusion Trend Chart</b> also allows to appreciate the point of intersection between the two
                groups of lineages with opposite trend <i>(just before the second week of March 2022)</i>.
              </p>
              <p>
                Here, mutations in the legend on the right can be selected and deselected with a click.
              </p>
              <p>
                A user may note that, at the bottom of the graph, a couple of mutations are growing from very low
                prevalence (around 0%) to almost 15%.
              </p>
            </Paragraph>

            <Paragraph :src='linIndOddImg' left larger-img>
              <p>
                Such growth can be appreciated more clearly by observing the <b>Diffusion Odd Ratio Plots</b>, where
                the odd ratio is computed by comparing frequencies of each week against the previous one
                (first plot) or against the first week of the period (second plot).
              </p>
              <p>
                <i>In the example, the two green lines represent the mutations S_L452Q and S_S704L.</i>
              </p>
            </Paragraph>

            <Paragraph :src='linIndExpansionImg' right larger-img>
              <p>
                When we select these two specific mutations in the table (by using the Mutation filter), the application allows to
                visualize a heatmap (and other plots) only with those. By expanding each mutation line in the table,
                it is possible to examine the <b>breakdown of total sequences</b> with that mutation across different
                lineages, for each single analyzed week.
              </p>
              <p>
                <i>The two observed mutations are predominantly exhibited by sequences assigned to the BA.2.12.1
                  lineage.</i>
              </p>
            </Paragraph>
          </template>

        </FunctionGuide>

        <!-- LINEAGE SPECIFIC -->
        <FunctionGuide title='Discover lineage-specific search' no-use-cases>

          <!-- Function guide -->
          <template v-slot:default>
            <Paragraph :src='linDepFormImg' left larger-img>
              <p>
                In this analysis the user is required, in addition to the other search parameters,
                to specify a <b>lineage</b> of interest.
              </p>
              <p>
                <i>In this example we choose the lineage BA.2.</i>
              </p>
            </Paragraph>

            <Paragraph :src='linDepTableImg' right larger-img>
              <p>
                The same visual elements are shown as in the previous analysis mode.<br />
                Here, however, counts shown for each mutation only represent the sequences of
                the selected lineage that are found in each week.
              </p>
              <p>
                As shown in the figure, in this mode <b>mutations</b> that are <b>typical of the selected
                lineage</b> (appearing in at least 50% of the sequences of the database assigned to
                that lineage) are <span class='highlight'>highlighted in yellow</span>.
              </p>
            </Paragraph>

            Here, the <b>P-values</b> in the table are computed using a Chi-square test of independence of
            variables in a contingency table. They represent:
            <ul>
              <li>
                <i>"P-value with mut"</i>: if the population «with mutation» is growing differently compared
                to everything;
              </li>
              <li>
                <i>"P-value without mut"</i>: if the population «without mutation» is growing differently compared
                to everything;
              </li>
              <li>
                <i>"P-value comparative"</i>: if the population «with mutation» is growing differently compared
                to the population «without mutation».
              </li>
            </ul>

            <Paragraph :src='linDepHeatmapImg' left larger-img>
              <p>
                By selecting in the table only the mutations that are
                <span class='highlight'>highlighted in yellow</span>
                <i>(i.e., characterizing for BA.2)</i> we observe the following <b>Heatmap</b>,
                where most mutations are fixed for four weeks, while 8 of them (at the top
                of the map) have increased from about 75% to almost 100%.
              </p>
            </Paragraph>

            <Paragraph :src='linDepDiffusionImg' right larger-img>
              <p>The trend is clear in the <b>Diffusion Trend Chart</b>.</p>
            </Paragraph>

            <Paragraph :src='linDepOddImg' left larger-img>
              <p>
                By looking at the <b>Odd Ratio Plots</b> we can appreciate an interesting trend of these 8 mutations
                (hovering on the dots, the details on the diffusion's growth are shown).
              </p>
            </Paragraph>

            <Paragraph :src='linDepOdd2Img' right larger-img>
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
            </Paragraph>
          </template>

        </FunctionGuide>
      </v-expansion-panels>
    </v-container>

  </v-container>
</template>

<script>

import Paragraph from '@/components/general/Paragraph'
import FunctionGuide from '@/components/general/guides/tool/FunctionGuide'

export default {
  name: 'ToolGuide',
  components: { FunctionGuide, Paragraph },
  data () {
    return {
      /** Images */
      introImg: require('../../../../assets/guide/intro.png'),

      linIndFormImg: require('../../../../assets/guide/li_form.png'),
      linIndExplorerImg: require('../../../../assets/guide/li_explorer.png'),
      linIndTableImg: require('../../../../assets/guide/li_table.png'),
      linIndTableFiltersImg: require('../../../../assets/guide/li_table_filters.png'),
      linIndHeatmapImg: require('../../../../assets/guide/li_heatmap.png'),
      linIndDiffusionImg: require('../../../../assets/guide/li_diffusion.png'),
      linIndOddImg: require('../../../../assets/guide/li_odd.png'),
      linIndExpansionImg: require('../../../../assets/guide/li_expansion.png'),

      linDepFormImg: require('../../../../assets/guide/ld_form.png'),
      linDepTableImg: require('../../../../assets/guide/ld_table.png'),
      linDepHeatmapImg: require('../../../../assets/guide/ld_heatmap.png'),
      linDepDiffusionImg: require('../../../../assets/guide/ld_diffusion.png'),
      linDepOddImg: require('../../../../assets/guide/ld_odd.png'),
      linDepOdd2Img: require('../../../../assets/guide/ld_odd2.png')

    }
  }
}
</script>

<style scoped>
.formula {
  padding: 0;
  font-family: monospace !important;
}

.command {
  text-transform: uppercase !important;
  font-weight: 300 !important;
}

.highlight {
  background: rgba(255, 255, 0, .45);
}
</style>
