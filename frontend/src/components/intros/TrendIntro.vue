<template>
  <feature-intro v-model="visibility" floating step="trend" :internal-steps="2" next-step="odd-ratio"
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
import {mapMutations} from "vuex";

export default {
  name: "TrendIntro",
  components: {FeatureIntro},
  data() {
    return {
      visibility: false,
      tips: [
        {
          id: 'intro',
          icon: 'mdi-chart-line',
          heading: 'Trend',
          title: 'Diffusion Trend',
          body: 'The trend chart depicts the evolution of the mutation frequencies over time.',
        },
        {
          id: 'select',
          icon: 'mdi-checkbox-marked',
          heading: 'Trend',
          title: 'Select to show in the plot',
          body: 'By default, the 10 mutations with the most pronounced trend are shown.' +
              'To visualize the ones you are interested in, check the corresponding boxes in the table.',
        },
        {
          id: 'adv',
          icon: 'mdi-checkbox-marked',
          heading: 'Trend',
          title: 'Show, hide or zoom in!',
          body: 'You can interact with the chart by selecting a specific area, and you ' +
              'can click on items in the legend to temporarily hide or show them.',
        }
      ],
      currentTip: 0,
    }
  },
  watch: {
    currentTip() {
      this.$vuetify.goTo('#diffusion-trend')
    },
    visibility(newValue) {
      if (newValue) {
        this.$vuetify.goTo('#diffusion-trend')
      }
    }
  },
  methods: {
    ...mapMutations(['setTourStep']),

    nextInternalStep() {
      this.currentTip++

      if(this.tips[this.currentTip].id==='select'){
        this.showOddRatio() // show in advance odd ratio to allow scrolling
      }
    },

    showOddRatio(){
      const el= document.getElementById('odd-ratio-expand')
      if(el)
        el.click() // expand odd-ratio section
      else
        this.setTourStep('summary') // skip odd-ratio tour if not able to expand it
    }
  },
  mounted() {
    if (this.visibility) {
      this.$vuetify.goTo('#diffusion-trend')
    }

  }
}
</script>

<style scoped>

</style>