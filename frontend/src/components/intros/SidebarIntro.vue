<!--

  Component:    SidebarIntro
  Description:  Sidebar step of the app-tour

-->

<template>
  <feature-intro v-model="visibility" floating step="navbar" :internal-steps="1" :next-step="null"
                 prev-step="summary" :icon="tips[currentTip].icon" end
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
  name: "SidebarIntro",
  components: {FeatureIntro},
  data() {
    return {
      /** Boolean flag set to true if the step is visible */
      visibility:false,

      /** Tips steps */
      tips: [
        {
          id: 'intro',
          icon: 'mdi-menu-open',
          heading: 'Sidebar',
          title: 'Browse through your past analyses',
          body: 'All the analyses you perform remain stored, even when you close the browser.',
          bodyAppend: 'You can find them all in the sidebar.',
        },
        {
          id: 'done',
          icon: 'mdi-bullseye-arrow',
          heading: 'That\'s it!',
          title: 'Happy variant hunting!',
          body: ' ',
          bodyAppend: 'You can restart the tour from the preferences',
        }
      ],

      /** Current tip step */
      currentTip: 0,
    }
  },

  watch: {
    currentTip() {
      this.$vuetify.goTo('#result-top')
    },
    visibility(newValue) {
      if (newValue) {
        this.$vuetify.goTo('#result-top')
      }
    }
  },

  methods: {
    /** Go to the next internal step */
    nextInternalStep(diff) {
      this.currentTip+=diff
    },
  },

  mounted() {
    if (this.visibility) {
      this.$vuetify.goTo('#result-top')
    }

  }
}
</script>

<style scoped>

</style>