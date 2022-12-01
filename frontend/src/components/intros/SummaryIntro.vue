<template>
  <feature-intro v-model="visibility" floating step="summary" :internal-steps="1" next-step="navbar"
                 :icon="tips[currentTip].icon" @nextStep="hideOddRatio"
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
  name: "SummaryIntro",
  components: {FeatureIntro},
  data() {
    return {
      visibility: false,
      tips: [
        {
          id: 'intro',
          icon: 'mdi-folder-text',
          heading: 'Others',
          title: 'A summary',
          body: 'At the bottom you will find a summary of the search parameters, and you can also add your own notes',
        },
        {
          id: 'tags',
          icon: 'mdi-pound',
          heading: 'Tags',
          title: 'Add, change or rename tags',
          body: 'From here you can also manage the tag associated with the analysis',
        }
      ],
      currentTip: 0,
    }
  },
  watch: {
    currentTip() {
      this.$vuetify.goTo('#summary')
    },
    visibility(newValue) {
      if (newValue) {
        this.$vuetify.goTo('#summary')
      }
    }
  },
  methods: {

    nextInternalStep() {
      this.currentTip++
    },
  },
  mounted() {
    if (this.visibility) {
      this.$vuetify.goTo('#summary')
    }

  }
}
</script>

<style scoped>

</style>