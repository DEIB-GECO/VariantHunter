<!--

  Component:    TableIntro
  Description:  Table step of the app-tour

-->

<template>
  <feature-intro v-model="visibility" floating step="table" :internal-steps="6" next-step="heatmap"
                 :icon="tips[currentTip].icon"
                 @nextInternalStep="nextInternalStep">
    <template>
      <div class="pl-4 mb-6">
        <div>
          <div class="text-uppercase text-body-5 font-weight-black letter-spacing-1" v-html="tips[currentTip].heading"/>
          <div class="text-h6 compact-h6 font-weight-bold" v-html="tips[currentTip].title"/>
          <div class="text-body-2 mt-2 " v-html="tips[currentTip].body"/>
          <div class="text-body-3 compact-text-3 mt-3" v-if="tips[currentTip].bodyAppend"
               v-html="tips[currentTip].bodyAppend"/>
        </div>
      </div>
    </template>
  </feature-intro>
</template>

<script>
import FeatureIntro from "@/components/general/basic/FeatureIntro";

export default {
  name: "TableIntro",
  components: {FeatureIntro},

  data() {
    return {
      /** Boolean flag set to true if the step is visible */
      visibility:false,

      /** Tips steps */
      tips: [
        {
          id: 'intro',
          icon: 'mdi-table-large',
          heading: 'Table',
          title: 'Mutation table',
          body: 'It depicts the trend of mutations detected in the last week of the 4-week analysis period.',
          bodyAppend: 'See \'table interpretation\' for more details about the columns.'
        },
        {
          id: 'order',
          icon: 'mdi-sort-alphabetical-ascending',
          heading: 'Table',
          title: 'Sort as you like',
          body: 'You can sort the data based on any column. Just click on the column header.',
          bodyAppend: 'Sorting options have the same scope as filters.'
        },
        {
          id: 'p-vals',
          icon: 'mdi-test-tube',
          heading: 'Table',
          title: 'What about the P-values?',
          body: 'You can show and hide p-values via the appropriate command.',
          bodyAppend: 'See \'table interpretation\' for more details about the p-values.'
        },
        {
          id: 'breakdown',
          icon: 'mdi-chevron-down',
          heading: 'Table',
          title: 'Lineage breakdown',
          body: 'In the case of lineage-independent analysis, you can expand each row to ' +
              'get the decomposition over the lineages for the period under consideration',
          bodyAppend: 'Different ways to aggregate lineages are also available.'
        },
        {
          id: 'char-mut',
          icon: 'mdi-star-shooting',
          heading: 'Table',
          title: 'Characterizing mutations',
          body: 'In the case of lineage-specific analysis, mutations characterizing ' +
              'the chosen lineage are <span class="char-mut">highlighted</span> in the table ',
        },
        {
          id: 'history',
          icon: 'mdi-information-variant',
          heading: 'Table',
          title: 'Mutation history',
          body: 'For each mutation, you can see more details about it, including the lineages ' +
              'it has characterized and the decomposition over the lineages since its appearance',
          bodyAppend: 'Just press the info button'
        },
        {
          id: 'select',
          icon: 'mdi-checkbox-marked',
          heading: 'Table',
          title: 'Go to covSPECTRUM',
          body: 'It is possible to quickly start an analysis on covSPECTRUM using the appropriate button at the bottom of the table.',
          bodyAppend: 'The generated analysis will include the period, location, and you can also select ' +
              'some mutations of interest by checking the boxes.'
        }
      ],

      /** Current tip step */
      currentTip: 0,
    }
  },

  watch: {
    currentTip() {
      this.$vuetify.goTo('#result-table')
    },
    visibility(newValue) {
      if (newValue) {
        this.$vuetify.goTo('#result-table')
      }
    }
  },

  methods: {
    /** Go to the next internal step */
    nextInternalStep() {
      this.currentTip++
      let btn = null

      switch (this.tips[this.currentTip].id) {
        case 'p-vals':
          this.$emit('showPValues', true)
          break;
        case 'breakdown':
          this.$emit('showPValues', false)
          btn = document.getElementById('1-expand')
          if (btn) btn.click()
          break;
        case 'char-mut':
          btn = document.getElementById('1-expand')
          if (btn) btn.click()
          break;

      }
    }
  },

  mounted() {
    if (this.visibility) {
      this.$vuetify.goTo('#result-table')
    }

  }
}
</script>

<style scoped>

</style>