<template>
  <feature-intro v-model="visibility" floating step="explorer" :internal-steps="1" next-step="result" :icon="tips[currentTip].icon"
                 @nextInternalStep="nextInternalStep" :end="currentTip>0" >
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
import {mapMutations, mapState} from "vuex";

export default {
  name: "ExplorerIntro",
  components: {FeatureIntro},
  data() {
    return {
      visibility:false,
      tips: [
        {
          icon: 'mdi-star-circle',
          heading: 'Dataset explorer',
          title: 'How to pick the best parameters?',
          body: 'The dataset explorer allows you to view the number of <b>daily collected sequences</b> and the ' +
                '<b>trend of lineages</b> over time.',
          bodyAppend: 'You can move through time and select the analysis period directly from here using the ' +
                      'button at the bottom. '
        },
        {
          icon: 'mdi-lightbulb-variant-outline',
          heading: '',
          title: 'A side note',
          body: 'Don\'t worry too much about how you choose the analysis parameters; you\'ll be able to ' +
                'refine them later.\n',
          bodyAppend: 'Continue the tour by performing an analysis.'
        },
      ],
      currentTip: 0,
    }
  },
  watch: {
    currentTip() {
      this.$vuetify.goTo('#explorer')
    },
    visibility(newValue){
      if(newValue){
        this.$vuetify.goTo('#explorer')
      }
    }
  },
  methods: {
    ...mapMutations(['setLocation','setLocations', 'setDate', 'setTourStep']),

    nextInternalStep() {
      this.currentTip++
    }
  },
  mounted() {
    if(this.visibility){
      this.$vuetify.goTo('#explorer')
    }
  }
}
</script>

<style scoped>

</style>