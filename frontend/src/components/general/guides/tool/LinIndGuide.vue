<!--
  Component:    LinIndGuide
  Description:  Usage guide for the lineage independent search feature
-->

<template>
  <FunctionGuide title='Discover <b>lineage-independent</b> search'>

    <!-- Function guide -->
    <template v-slot:default>
      <Paragraph :src='FormImg' left larger-img>
        <p>
          In this analysis, the user is required to select a <b>location</b> of interest
          <i>(New York State in the example)</i> and a <b>period of interest</b> &nbsp; <i>(four weeks ending
          on March 20th, 2022 in the example)</i>.
        </p>
      </Paragraph>
      <Paragraph :src='ExplorerImg' right larger-img>
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

      <Paragraph :src='TableImg' left larger-img>
        The tool analyzes the data of the selected four-week span, returning a <b>table</b> such as the one in the
        Figure:
        <ul>
          <li>each line corresponds to a mutation of interest;</li>
          <li>the <b>slope</b> represents how fast the frequency of the mutation increased in the selected period;
          </li>
          <li>the four following columns report the <b>frequency of the mutation</b> in each of the four weeks;
          </li>
          <li>the &nbsp;
            <v-icon small color='#000000de'>mdi-plus-circle-outline</v-icon>&nbsp;<span
              class='command'>SHOW P-VALUES</span>
            button adds, to the end of the table, three columns of <b>Chi squared tests</b> defined in
            &nbsp;
            <v-icon small color='#000000de'>mdi-help-circle-outline</v-icon>&nbsp;<span class='command'>TABLE INTERPRETATION</span>;
          </li>
          <li>data and all the visuals of the analysis can be <b>downloaded</b>.</li>
        </ul>
      </Paragraph>

      <Paragraph :src='TableFiltersImg' right larger-img>
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

      <Paragraph :src='HeatmapImg' left larger-img>
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

      <Paragraph :src='DiffusionImg' right larger-img>
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

      <Paragraph :src='OddImg' left larger-img>
        <p>
          Such growth can be appreciated more clearly by observing the <b>Diffusion Odd Ratio Plots</b>, where
          the odd ratio is computed by comparing frequencies of each week against the previous one
          (first plot) or against the first week of the period (second plot).
        </p>
        <p>
          <i>In the example, the two green lines represent the mutations S_L452Q and S_S704L.</i>
        </p>
      </Paragraph>

      <Paragraph :src='ExpansionImg' right larger-img>
        <p>
          When we select these two specific mutations in the table (by using the Mutation filter), the application
          allows to
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

    <!-- Use cases -->
    <template v-slot:use-cases>

      <!-- UC1 -->
      <UseCase name='<b>Use case 1:</b> Emergence and spread of the alpha variant in the UK'>
        <Paragraph :src='uc1.img1' left larger-img>
          <p>
            The following panels show a summary of the main outputs of a "lineage-independent"
            Variant Hunter analysis, performed on an interval of 4 weeks spanning
            from 26/10/2020 to 16/11/2020 in the UK.
          </p>
        </Paragraph>
        <p>
          This interval of time corresponds with the <b>emergence and spread of the Alpha
          variant in the UK</b>. As illustrated by the <b>Mutation table</b> and the <b>Diffusion
          Heatmap</b>, 6 amino acid changes in the <i>Spike glycoprotein</i> are singled out due
          to <i>remarkable increase in frequency</i> (from 1% to 11%).
        </p>
        <Picture :src='uc1.img2' :alt='uc1.alt2' />
        <Picture :src='uc1.img3' :alt='uc1.alt3' />
        <p class='mt-5'>
          Similar patterns of <i>increase in frequency</i> of the 6 selected amino acid changes
          can be observed also from the <b>Diffusion Trend Chart</b> and <b>Diffusion Odds Ratio</b> plots.
        </p>
        <p>
          Importantly, the 6 amino acid changes highlighted in the plot account for the complete
          set of amino-acid changes in Spike of the <b>Alpha SARS-CoV-2 variant</b>.
        </p>
        <Picture :src='uc1.img4' :alt='uc1.alt4' />
        <Picture :src='uc1.img5' :alt='uc1.alt5' />
      </UseCase>

      <!-- UC2 -->
      <UseCase name='<b>Use case 2</b>: Early spread of the Delta SARS-CoV-2 variant in the UK'>
        <Paragraph :src='uc2.img1' left larger-img>
          <p>
            The following panels show a summary of the main outputs of a "lineage-independent"
            Variant Hunter analysis, performed on an interval of 4 weeks spanning
            from 10/04/2021 to 07/05/2021 in the UK.
          </p>
        </Paragraph>
        <Paragraph :src='uc2.img2' right larger-img>
          <p>
            This interval of time corresponds with the <b>early spread of the Delta variant in the UK</b>.
          </p>
          <p>
            The mutation table illustrates the relative prevalence/association of
            <span class='monospaced'>S:N501Y</span> and <span class='monospaced'>S:L452R</span>,
            two amino acid changes <i>characteristic of Alpha and Delta respectively</i>
            in different sub-lineages of <i>SARS-CoV-2</i>.<br />
            While <span class='monospaced'>S:N501Y</span> is mostly associated with <i>Alpha-related lineages</i>,
            <span class='monospaced'>S:L452R</span> is observed almost exclusively in <i>lineages/sub-lineages of
            Delta</i>.
          </p>
        </Paragraph>
        <Paragraph :src='uc2.img3' left larger-img>
          <p>
            The <b>Diffusion Heatmap</b> illustrates the prevalence of 6 amino acid changes
            in the Spike glycoprotein <b>characteristic of the Alpha variant</b>
            <span class='monospaced'>(N501Y, T716I, A570D, S982A, D1118H, P681H) </span>
            and a matched number of amino acid changes <b>characteristic of the Delta variant</b>
            <span class='monospaced'>(L452R, P681R, D950N, R158G, S478K, T19R)</span>.
          </p>
          <p>
            A clear <i>increase</i> in Delta variant associated changes and a concomitant
            <i>decrease</i> in changes characteristic of the Alpha variant can be observed.
          </p>
        </Paragraph>
        <Paragraph :src='uc2.img4' right larger-img>
          <p>
            Equivalent patterns are also recovered by the <b>Diffusion Trend Chart</b>.
          </p>
        </Paragraph>
      </UseCase>

      <!-- UC3 -->
      <UseCase
        name='<b>Use case 3</b>: Spread of the Omicron variant and displacement of Delta in Europe and North America'>
        <p>
          A "lineage-independent" analysis was applied to study the prevalence of amino acid
          changes in the Spike glycoprotein in an interval of time spanning
          from 05/12/2021 to 01/01/2022 in <b>Europe</b> and in <b>North America</b>. <br />
          This interval coincides the rapid emergence and spread of the Omicron variant of SARS-CoV-2 worldwide.
        </p>
        <p>
          A clear <i>decrease</i> in the prevalence of 6 amino acid changes <b>characteristic of the Delta variant</b>
          <span class='monospaced'>(L452R, P681R, D950N, R158G, S478K, T19R)</span>
          and a concomitant and striking <i>increase</i> of 23 amino acid changes associated with the
          <b>Omicron variant</b> of <i>SARS-CoV-2</i> is observed both in <i>Europe</i> and <i>North America</i>.
        </p>
        <p>
          Equivalent patterns are recovered both from the <b>Diffusion Heatmap</b> and <b>Diffusion Trend Chart</b>.
          <br />
          <i>The greater uniformity of plots describing mutation trends in Europe vs
            North America may indicate greater accuracy in sequencing processes.</i>
        </p>
        <Collage :src1='uc3.img1' :alt1='uc3.alt1' :src2='uc3.img2' :alt2='uc3.alt2'></Collage>
      </UseCase>
    </template>

  </FunctionGuide>
</template>

<script>
import FunctionGuide from '@/components/general/guides/tool/FunctionGuide'
import UseCase from '@/components/general/guides/tool/UseCase'
import Paragraph from '@/components/general/Paragraph'
import Picture from '@/components/general/Picture'
import Collage from '@/components/general/Collage'

export default {
  name: 'LinIndGuide',
  components: { Collage, Picture, Paragraph, UseCase, FunctionGuide },
  data () {
    return {
      /** Images */
      FormImg: require('../../../../assets/guide/lin_ind/form.png'),
      ExplorerImg: require('../../../../assets/guide/lin_ind/explorer.png'),
      TableImg: require('../../../../assets/guide/lin_ind/table.png'),
      TableFiltersImg: require('../../../../assets/guide/lin_ind/table_filters.png'),
      HeatmapImg: require('../../../../assets/guide/lin_ind/heatmap.png'),
      DiffusionImg: require('../../../../assets/guide/lin_ind/diffusion.png'),
      OddImg: require('../../../../assets/guide/lin_ind/odd.png'),
      ExpansionImg: require('../../../../assets/guide/lin_ind/expansion.png'),

      uc1: {
        img1: require('../../../../assets/guide/lin_ind/uc/uc1/img1.png'),
        alt1: '',

        img2: require('../../../../assets/guide/lin_ind/uc/uc1/img2.png'),
        alt2: '',

        img3: require('../../../../assets/guide/lin_ind/uc/uc1/img3.png'),
        alt3: '',

        img4: require('../../../../assets/guide/lin_ind/uc/uc1/img4.png'),
        alt4: '',

        img5: require('../../../../assets/guide/lin_ind/uc/uc1/img5.png'),
        alt5: ''
      },

      uc2: {
        img1: require('../../../../assets/guide/lin_ind/uc/uc2/img1.png'),
        alt1: '',

        img2: require('../../../../assets/guide/lin_ind/uc/uc2/img2.png'),
        alt2: '',

        img3: require('../../../../assets/guide/lin_ind/uc/uc2/img3.png'),
        alt3: '',

        img4: require('../../../../assets/guide/lin_ind/uc/uc2/img4.png'),
        alt4: ''
      },

      uc3: {
        img1: require('../../../../assets/guide/lin_ind/uc/uc3/img1.png'),
        alt1: '',

        img2: require('../../../../assets/guide/lin_ind/uc/uc3/img2.png'),
        alt2: ''
      }

    }
  }
}
</script>

<style scoped>

</style>
