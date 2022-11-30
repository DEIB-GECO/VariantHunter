<template>
  <feature-intro v-model="visibility" floating step="heatmap" :internal-steps="1" next-step="trend"
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
  name: "HeatmapIntro",
  components: {FeatureIntro},
  data() {
    return {
      visibility: false,
      tips: [
        {
          id: 'intro',
          icon: 'mdi-chart-gantt',
          heading: 'Heatmap',
          title: 'Diffusion Heatmap',
          body: 'A Heatmap allows to observe the increasing and decreasing trends in a fast way.',
        },
        {
          id: 'select',
          icon: 'mdi-checkbox-marked',
          heading: 'Heatmap',
          title: 'Select to show in the plot',
          body: 'By default, the 10 mutations with the most pronounced trend are shown.' +
              'To visualize the ones you are interested in, check the corresponding boxes in the table.',
        }
      ],
      currentTip: 0,
    }
  },
  watch: {
    currentTip() {
      this.$vuetify.goTo('#diffusion-heatmap')
    },
    visibility(newValue) {
      if (newValue) {
        this.$vuetify.goTo('#diffusion-heatmap')
      }
    }
  },
  methods: {

    nextInternalStep() {
      this.currentTip++
    }
  },
  mounted() {
    if (this.visibility) {
      this.$vuetify.goTo('#diffusion-heatmap')
    }

  }
}
</script>

<style scoped>

</style>