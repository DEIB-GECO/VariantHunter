<!--

  Component:    ExplorerIntro
  Description:  Explorer step of the app-tour

-->

<template>
  <feature-intro v-model="visibility" floating step="explorer" :internal-steps="isPublicEndpoint?2:1"
                 prev-step="definition" next-step="result" :icon="tips[currentTip].icon"
                 @nextInternalStep="nextInternalStep" :end="currentTip>0"
                 :next-label="isPublicEndpoint?'I\'ll do it myself':undefined">
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
      <div class="d-flex mt-n3 mb-n5" v-if="tips[currentTip].id === 'try'">
        <v-spacer/>
        <btn-with-tooltip text="Select example randomly" icon="mdi-chart-box"
                          :click-handler="selectFeatured" hover-color="secondary"
                          size="small" content-class="ml-1 mt-1 mt-md-0" top
                          tip="Run an analysis from the featured ones"/>
      </div>
    </template>
  </feature-intro>
</template>

<script>
import FeatureIntro from "@/components/general/basic/FeatureIntro";
import {mapMutations, mapState} from "vuex";
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip.vue";

export default {
  name: "ExplorerIntro",
  components: {BtnWithTooltip, FeatureIntro},
  data() {
    return {
      /** Boolean flag set to true if the step is visible */
      visibility: false,

      /** Tips steps */
      tips: [
        {
          id: 'params',
          icon: 'mdi-star-circle',
          heading: 'Dataset explorer',
          title: 'How to pick the best parameters?',
          body: 'The dataset explorer allows you to view the number of <b>daily collected sequences</b> and the ' +
              '<b>trend of lineages</b> over time.',
          bodyAppend: 'You can move through time and select the analysis period directly from here using the ' +
              'button at the bottom. '
        },
        {
          id: 'note',
          icon: 'mdi-lightbulb-variant-outline',
          heading: '',
          title: 'A side note',
          body: 'Don\'t worry too much about how you choose the analysis parameters; you\'ll be able to ' +
              'refine them later.\n',
        },
        {
          id: 'try',
          icon: 'mdi-lifebuoy',
          heading: '',
          title: 'Let\'s try to make an analysis!',
          body: 'Let\'s start with a featured analysis to continue the tour!'
        },
      ],

      /** Current tip step */
      currentTip: 0,
    }
  },

  computed: {
    ...mapState(['isPublicEndpoint'])
  },

  watch: {
    currentTip() {
      this.$vuetify.goTo('#explorer')
    },
    visibility(newValue) {
      if (newValue) {
        this.$vuetify.goTo('#explorer')
      }
    }
  },

  methods: {
    ...mapMutations(['setLocation', 'setLocations', 'setDate', 'setTourStep']),

    /** Go to the next internal step */
    nextInternalStep(diff) {
      this.currentTip += diff

      if (this.tips[this.currentTip].id === 'try' && this.isPublicEndpoint) {
        this.$vuetify.goTo('#featured')
      } else if (this.tips[this.currentTip].id === 'note' && !this.isPublicEndpoint) {
        this.tips[this.currentTip].bodyAppend = 'Continue the tour by performing an analysis.'
      }
    },

    /** Run a featured example and skip the tour intro of the app-tour for the result panel */
    selectFeatured() {
      this.setTourStep('filters')
      const example = document.getElementById('featured-0') // better if lineage-independent
      if (example) example.click()
    }
  },

  mounted() {
    if (this.visibility) {
      this.$vuetify.goTo('#explorer')
    }
  }
}
</script>

<style scoped>

</style>