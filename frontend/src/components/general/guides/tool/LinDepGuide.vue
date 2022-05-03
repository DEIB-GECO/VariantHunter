<!--
  Component:    LinDepGuide
  Description:  Usage guide for the lineage dependent search feature
-->

<template>
  <FunctionGuide title='Discover <b>lineage-specific</b> search'>

    <!-- Function guide -->
    <template v-slot:default>
      <Paragraph :src='FormImg' left larger-img>
        <p>
          In this analysis the user is required, in addition to the other search parameters,
          to specify a <b>lineage</b> of interest.
        </p>
        <p>
          <i>In this example we choose the lineage BA.2.</i>
        </p>
      </Paragraph>

      <Paragraph :src='TableImg' right larger-img>
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

      <Paragraph :src='HeatmapImg' left larger-img>
        <p>
          By selecting in the table only the mutations that are
          <span class='highlight'>highlighted in yellow</span>
          <i>(i.e., characterizing for BA.2)</i> we observe the following <b>Heatmap</b>,
          where most mutations are fixed for four weeks, while 8 of them (at the top
          of the map) have increased from about 75% to almost 100%.
        </p>
      </Paragraph>

      <Paragraph :src='DiffusionImg' right larger-img>
        <p>The trend is clear in the <b>Diffusion Trend Chart</b>.</p>
      </Paragraph>

      <Paragraph :src='OddImg' left larger-img>
        <p>
          By looking at the <b>Odd Ratio Plots</b> we can appreciate an interesting trend of these 8 mutations
          (hovering on the dots, the details on the diffusion's growth are shown).
        </p>
      </Paragraph>

      <Paragraph :src='Odd2Img' right larger-img>
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

    <!-- Use cases -->
    <template v-slot:use-cases>

      <!-- UC1 -->
      <UseCase name='<b>Use case 1</b>: Omicron BA.2.12.2 lineage'>
        <p>
          Here we report a collection of screenshots from <b>Pango designation</b>
          <span class='monospaced'>issue 499</span>
          <a href='https://github.com/cov-lineages/pango-designation/issues/499' target='_blank'>
            (https://github.com/cov-lineages/pango-designation/issues/499)
          </a>
          , which led to the definition of the <b>BA.2.12.2 sublineage</b> of <i>SARS-CoV-2</i>.<br />
          The novel lineage is defined by a <span class='monospaced'>L452Q</span> amino acid change
          in the <i>spike glycoprotein</i> according to the submitter.
        </p>
        <div class='with-borders'>
          <Picture :src='uc1.img1' img-max-height='300' />
          <Collage :src1='uc1.img2' :src2='uc1.img3' img-max-height='300' />
          <Picture :src='uc1.img4' img-max-height='300' />
        </div>
        <Paragraph :src='uc1.img5' left larger-img>
          <p class='mt-sm-5'>
            Then, we report the main results of a Variant-Hunter "lineage-specific" analysis executed
            on the <b>BA.2.12 lineage</b> in the geographic location <i>(USA)</i> and interval of time
            <i>(March 2022)</i> where the novel lineage first emerged.
          </p>
        </Paragraph>
        <Picture :src='uc1.img6' />
        <p class='mt-5'>
          A clear <i>increase</i> in the prevalence of <span class='monospaced'>L452Q</span>
          within <b>lineage BA.2.12.2</b> is observed both from the <b>Diffusion Odds Ratio</b> plot
          and the <b>Diffusion Heatmap</b>. <br />
          As outlined from the <b>Diffusion Odds Ratio</b> plot the amino acid change that defines
          the new lineage seems to be associated with a clear <i>growth advantage</i>.
        </p>
        <Picture :src='uc1.img7' />
        <Picture :src='uc1.img8' />
        <p class='mt-5'>
          <i>Please note that in this plot values
            <span class='monospaced'>around 1</span> indicate a steady state:
            (no increase or decrease in frequency),
            values <span class='monospaced'>below 1</span> indicate a decrease,
            and values <span class='monospaced'>> 1</span> are indicative of
            rapid increase/relative growth advantage.</i>
        </p>
      </UseCase>

      <!-- UC2 -->
      <UseCase name='<b>Use case 2</b>: Omicron BA.1.15.2 lineage'>
        <p>
          Here we report a collection of screenshots from <b>Pango designation</b>
          <span class='monospaced'>issue 508</span>
          <a href='https://github.com/cov-lineages/pango-designation/issues/508' target='_blank'>
            (https://github.com/cov-lineages/pango-designation/issues/508)
          </a>
          , which led to the definition of the <b>BA.1.15.2 sublineage</b> of <i>SARS-CoV-2</i>.<br />
          The novel lineage is defined by a <span class='monospaced'>Q628K</span> amino acid change
          in the <i>spike glycoprotein</i> according to the submitter.
        </p>
        <div class='with-borders'>
          <Picture :src='uc2.img1' img-max-height='300' />
          <Collage :src1='uc2.img2' :src2='uc2.img3' img-max-height='300' />
          <Picture :src='uc2.img4' img-max-height='300' />
        </div>
        <Paragraph :src='uc2.img5' left larger-img>
          <p class='mt-sm-5'>
            Then, we report the main results of a Variant-Hunter "lineage-specific" analysis executed
            on the <b>BA.1.15 lineage</b> in the geographic location <i>(USA)</i> and interval of time
            <i>(March 2022)</i> where the novel lineage first emerged.
          </p>
        </Paragraph>
        <Picture :src='uc2.img6' />
        <p class='mt-5'>
          A clear <i>increase</i> in the prevalence of <span class='monospaced'>Q628K</span>
          within <b>lineage BA.1.15.2</b> is observed both from the <b>Diffusion Odds Ratio</b> plot
          and the <b>Diffusion Heatmap</b>.
        </p>
        <Paragraph :src='uc2.img7' right larger-img>
          <p>
            Interestingly, we also observe a similar increase in the prevalence of
            <span class='monospaced'>S:V320I</span>, an amino acid change that to the best of
            our knowledge is <u>not</u> currently associated with/does <u>not</u> define any sub-lineage of
            <b>BA.1.15</b>.
          </p>
        </Paragraph>
        <Paragraph :src='uc2.img8' left larger-img>
          <p>
            Both <span class='monospaced'>S:V320I</span> and <span class='monospaced'>S:Q628K</span>
            show a similar relative growth advantage according to the <b>Diffusion Odds Ratio</b> plot
            compared to the amino acid changes that define the parental lineage. <br />
            After a rapid surge in frequency <span class='monospaced'>from 1 to 12%</span>,
            the two novel mutations seem to <i>“stabilize”</i> around <span class='monospaced'>15%</span>,
            in the last week of the interval considered in the analysis, and show an odd ratio of
            <span class='monospaced'>~1</span>.
          </p>
        </Paragraph>
        <p>
          <i>Please note that in this plot values
            <span class='monospaced'>around 1</span> indicate a steady state:
            (no increase or decrease in frequency),
            values <span class='monospaced'>below 1</span> indicate a decrease,
            and values <span class='monospaced'>> 1</span> are indicative of
            rapid increase/relative growth advantage.</i>
        </p>
      </UseCase>

      <!-- UC3 -->
      <UseCase name='<b>Use case 3</b>: Delta AY.122.6 lineage'>
        <p>
          Here we report a collection of screenshots from <b>Pango designation</b>
          <span class='monospaced'>issue 394</span>
          <a href='https://github.com/cov-lineages/pango-designation/issues/394' target='_blank'>
            (https://github.com/cov-lineages/pango-designation/issues/394)
          </a>
          , which led to the definition of the <b>AY.122.6 sublineage</b> of the <i>Delta SARS-CoV-2 variant</i>.<br />
          The novel lineage is defined by a <span class='monospaced'>E484A</span> amino acid change
          in the <i>spike glycoprotein</i> according to the submitter; and shows a relative growth advantage
          in <i>France</i> compared to the parental <b>lineage AY.122</b>.
        </p>
        <div class='with-borders'>
          <Picture :src='uc3.img1' img-max-height='300' />
          <Collage :src1='uc3.img2' :src2='uc3.img3' img-max-height='300' />
          <Picture :src='uc3.img4' img-max-height='300' />
        </div>
        <Paragraph :src='uc3.img5' left larger-img>
          <p class='mt-sm-5'>
            Then, we report a summary of the main results of a Variant-Hunter "lineage-specific" analysis executed
            on the <b>AY.122 lineage</b> in the geographic location <i>(France)</i> and interval of time
            <i>(November-December 2021)</i> where the novel lineage first emerged.
          </p>
        </Paragraph>
        <p>
          <i>
            In this case all the analyses were executed by means of the Docker implementation of Variant Hunter,
            using a dump of the <b>GISAID database obtained on 06/02/2022</b>
          </i>
        </p>
        <Picture :src='uc3.img6' />
        <p class='mt-5'>
          A clear increase in the prevalence of <span class='monospaced'>S:E484A</span>
          and of another amino acid change in spike, <span class='monospaced'>S:181V</span>
          can be clearly observed within <b>lineage AY.122</b> from the main output of Variant Hunter.
        </p>
        <Paragraph :src='uc3.img7' right larger-img>
          <p>
            According to the <b>Diffusion Heatmap</b> both changes show a <i>consistent increase</i>
            in prevalence <span class='monospaced'>(from 10 to 26%)</span> in the interval of
            time included in the analysis.
          </p>
        </Paragraph>
        <Paragraph :src='uc3.img8' left larger-img>
          <p>
            The <b>Diffusion Odds Ratio</b> plot is consistent with a relative advantage
            in growth for both amino acid changes, as demonstrated by the <i>constant increase</i>
            in the "diffusion" odd ratio and by the fact that values of odd ratio > 1 are
            recovered at every time point of the 4 weeks interval considered in the analysis
          </p>
        </Paragraph>
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
  name: 'LinDepGuide',
  components: { Collage, Picture, Paragraph, UseCase, FunctionGuide },
  data () {
    return {
      /** Images */
      FormImg: require('../../../../assets/guide/lin_dep/form.png'),
      TableImg: require('../../../../assets/guide/lin_dep/table.png'),
      HeatmapImg: require('../../../../assets/guide/lin_dep/heatmap.png'),
      DiffusionImg: require('../../../../assets/guide/lin_dep/diffusion.png'),
      OddImg: require('../../../../assets/guide/lin_dep/odd.png'),
      Odd2Img: require('../../../../assets/guide/lin_dep/odd2.png'),

      uc1: {
        img1: require('../../../../assets/guide/lin_dep/uc/uc1/img1.png'),
        img2: require('../../../../assets/guide/lin_dep/uc/uc1/img2.png'),
        img3: require('../../../../assets/guide/lin_dep/uc/uc1/img3.png'),
        img4: require('../../../../assets/guide/lin_dep/uc/uc1/img4.png'),
        img5: require('../../../../assets/guide/lin_dep/uc/uc1/img5.png'),
        img6: require('../../../../assets/guide/lin_dep/uc/uc1/img6.png'),
        img7: require('../../../../assets/guide/lin_dep/uc/uc1/img7.png'),
        img8: require('../../../../assets/guide/lin_dep/uc/uc1/img8.png')
      },

      uc2: {
        img1: require('../../../../assets/guide/lin_dep/uc/uc2/img1.png'),
        img2: require('../../../../assets/guide/lin_dep/uc/uc2/img2.png'),
        img3: require('../../../../assets/guide/lin_dep/uc/uc2/img3.png'),
        img4: require('../../../../assets/guide/lin_dep/uc/uc2/img4.png'),
        img5: require('../../../../assets/guide/lin_dep/uc/uc2/img5.png'),
        img6: require('../../../../assets/guide/lin_dep/uc/uc2/img6.png'),
        img7: require('../../../../assets/guide/lin_dep/uc/uc2/img7.png'),
        img8: require('../../../../assets/guide/lin_dep/uc/uc2/img8.png')
      },

      uc3: {
        img1: require('../../../../assets/guide/lin_dep/uc/uc3/img1.png'),
        img2: require('../../../../assets/guide/lin_dep/uc/uc3/img2.png'),
        img3: require('../../../../assets/guide/lin_dep/uc/uc3/img3.png'),
        img4: require('../../../../assets/guide/lin_dep/uc/uc3/img4.png'),
        img5: require('../../../../assets/guide/lin_dep/uc/uc3/img5.png'),
        img6: require('../../../../assets/guide/lin_dep/uc/uc3/img6.png'),
        img7: require('../../../../assets/guide/lin_dep/uc/uc3/img7.png'),
        img8: require('../../../../assets/guide/lin_dep/uc/uc3/img8.png')
      }
    }
  }
}
</script>

<style scoped>
.with-borders {
  border: solid 1px #e3e3e3;
  border-radius: 30px;
  padding: 28px 3px;
}

</style>
