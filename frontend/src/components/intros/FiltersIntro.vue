<template>
  <feature-intro v-model="visibility" floating step="filters" :internal-steps="4" next-step="table"
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
import {mapMutations, mapState} from "vuex";

export default {
  name: "FiltersIntro",
  components: {FeatureIntro},
  data() {
    return {
      visibility: false,
      tips: [
        {
          id: 'toolbar',
          icon: 'mdi-pencil',
          heading: 'Controls',
          title: 'Controls at your fingertips',
          body: 'In the toolbar at the top, you can find all the controls to adjust the search parameters.',
          bodyAppend: 'You can also add a relevant search to favorites or download the data as cvs or png file.'
        },
        {
          id: 'filter-glb',
          icon: 'mdi-filter-cog',
          heading: 'Filters',
          title: 'Filter by mutation or protein',
          body: 'You can filter the results by choosing only the protein you are interested in or by ' +
              'selecting a set of mutations.',
        },
        {
          id: 'filter-adv',
          icon: 'mdi-image-auto-adjust',
          heading: 'Filters',
          title: 'Advanced options',
          body: 'You can also select only the mutations characterizing a set of lineages, or use the advanced ' +
              'editor to fill in the filter faster.',
          bodyAppend: 'For lineage-specific analysis you can also directly select all the non-characterizing mutations.'
        },
        {
          id: 'tags',
          icon: 'mdi-tag-text',
          heading: 'Filters',
          title: '#Tags!',
          body: 'You can associate a tag with the analyses you perform. This allows you to group the analyses and ' +
              'maintain the same filtering and sorting options for all analyses.',
          bodyAppend: 'We\'ll see later how to do it.'
        },
        {
          id: 'scopes',
          icon: 'mdi-search-web',
          heading: 'Filters',
          title: 'Filtering scopes',
          body: 'By default, the filtering scope is <b>local</b>. This means that you apply the filters to the ' +
              'current analysis only. You can switch to the <b>tag-based</b> one at any time.',
          bodyAppend: 'And switch back whenever you want. You won\'t have to set it every time.'
        }
      ],
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

    nextInternalStep() {
      this.currentTip++

      switch (this.tips[this.currentTip].id) {
        case 'filter-adv':
          document.getElementById('mutation-selector').click()
          break;
        case 'scopes':
          this.$emit('showScopeMenu')
          break;
      }
    }
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