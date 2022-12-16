<!--

  Component:    DefinitionIntro
  Description:  Definition step of the app-tour

-->

<template>
  <feature-intro v-model="visibility" floating step="definition" :internal-steps="2" prev-step="tour" next-step="explorer" :icon="tips[currentTip].icon"
                 @nextInternalStep="nextInternalStep" @nextStep="$emit('showExplorer')">
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
  name: "DefinitionIntro",
  components: {FeatureIntro},

  data() {
    return {
      /** Boolean flag set to true if the step is visible */
      visibility:false,

      /** Tips steps */
      tips: [
        {
          icon: 'mdi-magnify',
          heading: 'Analysis type',
          title: 'Here you can define a new analysis',
          body: 'Start by selecting the type of analysis you want to perform: you ' +
              'can choose the <b>lineage-independent analysis</b> or decide to focus on a <b>specific lineage</b>.'
        },
        {
          icon: 'mdi-map-marker',
          heading: 'Analysis parameters',
          title: 'Location',
          body: 'Next, you need to set the location of interest: either a <b>region</b>, ' +
              'a <b>country</b>, or an entire <b>continent</b>.',
          bodyAppend: 'Type its name directly (e.g., "Europe") or proceed in an ' +
              'exploratory manner, adding a slash (e.g., "Europe/" to see European countries).'
        },
        {
          icon: 'mdi-clock-outline',
          heading: 'Analysis parameters',
          title: 'Analysis period',
          body: 'Now you just need to choose the analysis period: specifically, you will need to select ' +
              'the end date of a <b>4-week analysis period</b>.',
          bodyAppend: 'The amino acid mutations that will be examined will be those present in the ' +
              'last week considered, and their trend over the period will be analyzed.'
        }
      ],

      /** Current tip step */
      currentTip: 0,
    }
  },

  computed: {
    ...mapState(['lastUpdate','selectedLocation','selectedDate']),
  },

  watch: {
    currentTip() {
      this.$vuetify.goTo('#top')
    },
    visibility(newValue){
      if(newValue){
        this.$vuetify.goTo('#top')
      }
    }
  },

  methods: {
    ...mapMutations(['setLocation','setLocations', 'setDate']),

    /** Go to the next internal step */
    nextInternalStep(diff) {
      this.$emit('selectMode')
      if(!this.selectedLocation && this.currentTip>0) {
        this.setLocations([])
        this.setLocation('Europe')
      }
      if(!this.selectedDate && this.currentTip>1)
        this.setDate([this.lastUpdate])

      this.currentTip+=diff
    }
  },

  mounted() {
    if(this.visibility){
      this.$vuetify.goTo('#top')
    }

  }
}
</script>

<style scoped>

</style>