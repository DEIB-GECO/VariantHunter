<!--

  Component:    OddRatioIntro
  Description:  Odd ratio step of the app-tour

-->

<template>
  <feature-intro v-model="visibility" floating step="odd-ratio" :internal-steps="1" next-step="summary"
                 prev-step="trend" :icon="tips[currentTip].icon"
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
  name: "OddRatioIntro",
  components: {FeatureIntro},
  data() {
    return {
      /** Boolean flag set to true if the step is visible */
      visibility: false,

      /** Tips steps */
      tips: [
        {
          id: 'intro',
          icon: 'mdi-align-vertical-bottom',
          heading: 'Odd ratio',
          title: 'Diffusion Odd Ratio',
          body: 'This visualization makes it possible to quickly compare the growth of the spread ' +
              'of the various mutations between weeks.',
        },
        {
          id: 'pov',
          icon: 'mdi-eye-outline',
          heading: 'Odd ratio',
          title: 'Multiple points of view are available',
          body: 'You can compare the frequencies of each week against those of the previous week ' +
              '<span class="text-body-4">(WEEK-BY-WEEK)</span> or against those of the first week ' +
              'of the period <span class="text-body-4">(WEEK-TO-FIRST-WEEK)</span>.',
        }
      ],

       /** Current tip step */
      currentTip: 0,
    }
  },

  watch: {
    currentTip() {
      this.$vuetify.goTo('#odd-ratio')
    },
    visibility(newValue) {
      if (newValue) {
        this.$vuetify.goTo('#odd-ratio')
      }
    }
  },

  methods: {
    /** Go to the next internal step */
    nextInternalStep(diff) {
      this.currentTip+=diff

      if (this.tips[this.currentTip].id==='pov'){
        const el= document.getElementById('odd-ratio-tab1')
        if(el)
          el.click() // collapse odd-ratio section
      }
    },
  },

  mounted() {
    if (this.visibility) {
      this.$vuetify.goTo('#odd-ratio')
    }

  }
}
</script>

<style scoped>

</style>