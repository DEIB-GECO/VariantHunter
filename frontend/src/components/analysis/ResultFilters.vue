<template>
  <v-row id="top" class="mt-5 px-5">
    <v-col cols="12" class="d-flex">
      <div class="text-h6 compact-h6 font-weight-black primary--text pb-2 mx-n5 spaced-5">
        <v-icon color='primary' left>mdi-filter-outline</v-icon>
        <span>Filters</span>

        <!-- SCOPE OPTION -->
        <span
            class="ml-8 text-body-5 compact-text-4 font-weight-regular d-block d-sm-inline rounded-xl bg_var2 py-1 pl-3">
              <span class=" text-body-5 compact-text-4 font-weight-bold">Scope</span>:&nbsp;
              <v-tooltip bottom allow-overflow z-index="10" max-width="400px" :close-delay="0">
                <template v-slot:activator="{on,attrs}">
                  <span class="mr-1 text_var1--text" v-on="on" v-bind="attrs">
                    {{ useGlobalFilters ? options.global.value : options.local.value }}
                  </span>
                </template>
                <div class="mb-3" v-html="useGlobalFilters ? options.global.tip : options.local.tip" />
                Press <v-icon color="warning" small>mdi-swap-vertical</v-icon> to edit.
              </v-tooltip>
              <v-menu v-model="showOptions" content-class="rounded-xl navbar-menu" offset-y open-on-click
                      :open-on-hover="false" close-on-content-click>
                <template v-slot:activator="{ attrs, on }">
                  <span v-bind="attrs" v-on="on">
                    <icon-with-tooltip bottom color="dark-grey" hover-color="warning" size="medium"
                                       icon="mdi-swap-vertical"
                                       :tip="showOptions?'':'Change the scope of the filtering options'"
                                       :click-handler="()=>showOptions=!showOptions"/>
                  </span>
                </template>
                <div @mouseleave="showOptions=false">
                  <v-list color="bg_var1" rounded dense width="auto">
                    <v-list-item v-for="[key,opt] in Object.entries(options)" :key="key" link dense
                                 @click="changeScope(key)">
                      <v-icon class="pr-3" color="primary">{{ opt.icon }}</v-icon>
                      <v-list-item-content>
                        <v-list-item-title class="primary--text">{{ opt.title }}</v-list-item-title>
                        <v-list-item-subtitle v-html="opt.subtitle" class="break-spaces"/>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </div>
              </v-menu>
        </span>
      </div>
    </v-col>

    <!-- Protein filter -->
    <v-col cols="12" sm="5" md="3">
      <field-selector v-model='selectedProtein' label='Protein' placeholder='All'
                      :possible-values='possibleProteins' autocomplete solo/>
    </v-col>

    <!-- Mutation filter -->
    <v-col cols="12" sm="7" md="7">
      <mutation-selector v-model='selectedMutation' :possible-values='possibleMutations'
                         :characterizing-muts='characterizingMuts' />
    </v-col>
  </v-row>
</template>

<script>
import {mapGetters, mapMutations, mapState} from "vuex";
import MutationSelector from "@/components/form/MutationSelector";
import FieldSelector from "@/components/form/FieldSelector";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";

export default {
  name: "ResultFilters",
  components: {IconWithTooltip, FieldSelector, MutationSelector},
  data() {
    return {
      showOptions: false,

      options: {
        'global': {
          icon: 'mdi-search-web',
          value: 'all analyses',
          tip: 'Filters are applied to <span class="font-weight-bold">all the analyses</span> ',
          title: 'Global scope',
          subtitle: 'Filters are applied to <span class="font-weight-bold">all the analyses</span> (this, the others and future ones).',
        },
        'local': {
          icon: 'mdi-feature-search-outline',
          value: 'this analysis',
          tip: 'Filters are applied to <span class="font-weight-bold">this analysis only</span>',
          title: 'Local scope',
          subtitle: 'Filters are applied to <span class="font-weight-bold">this analysis only</span> (this only).',
        },
        'global-new': {
          icon: 'mdi-new-box',
          value: 'all analyses',
          title: 'Global scope (advanced)',
          subtitle: 'Filters are applied to <span class="font-weight-bold">all the analyses</span> (this and future ones). <br/>' +
              'For past analyses, the current global scope will be copied to the local scope.',
        },
      }
    }
  },
  computed: {
    ...mapState(['globalFilteringOpt']),
    ...mapGetters(['getCurrentAnalysis', 'getCurrentLocalFilteringOpt']),

    withLineages() {
      return this.getCurrentAnalysis.query.lineage !== null
    },

    characterizingMuts() {
      return this.withLineages ? this.getCurrentAnalysis.characterizingMuts : null
    },

    useGlobalFilters() {
      return this.getCurrentLocalFilteringOpt.useGlobalFilters
    },

    filteringOpt() {
      return (this.useGlobalFilters ? this.globalFilteringOpt : this.getCurrentLocalFilteringOpt)
    },

    /** Possible proteins values computed based on data results */
    possibleProteins() {
      const set = new Set(this.getCurrentAnalysis.rows.map(({protein}) => protein))
      return [...set].sort()
    },

    /** Possible mutations values computed based on data results */
    possibleMutations() {
      const set = new Set(this.getCurrentAnalysis.rows.map(({protein, mut}) => protein + '_' + mut))
      return [...set].sort()
    },

    /** Selected mutation to further filter the data. Takes the form <PROTEIN>_<MUT> */
    selectedMutation: {
      set(newVal) {
        this.setFilterOpt({global: this.useGlobalFilters, opt: 'muts', value: newVal})
      },
      get() {
        return this.filteringOpt.muts
      }
    },

    /** Selected protein to further filter the data */
    selectedProtein: {
      set(newVal) {
        this.setFilterOpt({global: this.useGlobalFilters, opt: 'protein', value: newVal})
      },
      get() {
        return this.filteringOpt.protein
      }
    },


  },
  methods: {
    ...mapMutations(['setFilterOpt', 'globalOptToLocal']),

    /**
     * Changes the scope of the filters
     * @param value Either 'global','global-new','local'
     */
    changeScope(value) {
      switch (value) {
        case 'global':
          // Just switch to global filters
          this.setFilterOpt({global: false, opt: 'useGlobalFilters', value: true})
          break
        case 'global-new':
          // Convert past global to local filters and switch to global
          this.globalOptToLocal()
          this.setFilterOpt({global: false, opt: 'useGlobalFilters', value: true})
          break
        case 'local':
          // Just switch to local filters
          this.setFilterOpt({global: false, opt: 'useGlobalFilters', value: false})
          break
      }
    }
  },
}
</script>

<style scoped>

</style>