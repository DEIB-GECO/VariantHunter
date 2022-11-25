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
                    <span v-if="useLocalOpt">{{ options.local.value}}</span>
                    <v-chip v-else x-small :color="tags[tag]?.tagColor.color" :light="!tags[tag]?.tagColor.isDark"
                    :dark="tags[tag]?.tagColor.isDark" class="text-uppercase text-body-5">
              {{ tag }}
            </v-chip>
                  </span>
                </template>
                <div class="mb-3" v-html="useLocalOpt ? options.local.subtitle : options.tag.subtitle"/>
                Press <v-icon color="warning" small>mdi-swap-vertical</v-icon> to edit.
              </v-tooltip>
              <v-menu v-model="showOptions" content-class="rounded-xl navbar-menu" offset-y open-on-click
                      :open-on-hover="false" :close-on-content-click="false" max-width="80vw">
                <template v-slot:activator="{ attrs, on }">
                  <span v-bind="attrs" v-on="on">
                    <icon-with-tooltip bottom color="dark-grey" hover-color="warning" size="medium"
                                       icon="mdi-swap-vertical"
                                       :tip="showOptions?'':'Change the scope of the filtering options'"
                                       :click-handler="()=>showOptions=!showOptions"/>
                  </span>
                </template>
                <div class="bg_var1">
                  <!-- Scope filtering menu options -->
                  <v-list color="bg_var1" rounded dense>
                    <v-list-item v-for="[key,opt] in Object.entries(options)" :key="key" link dense
                                 @click="changeScope(key)"
                                 :class="(useLocalOpt && key==='local')?'v-list-item--active':''">
                      <v-icon class="pr-3" color="primary">{{ opt.icon }}</v-icon>
                      <v-list-item-content>
                        <!-- Title and description -->
                        <v-list-item-title class="primary--text">{{ opt.title }}</v-list-item-title>
                        <v-list-item-subtitle v-html="opt.subtitle" class="break-spaces"/>

                        <!-- Tag selector for tag option only-->
                        <div v-if="key==='tag' && !tag" :class="'text-body-4 mt-2 '+(missingTagWarning? 'error--text':'warning--text')">
                          <v-icon small :color="missingTagWarning?'error':'warning'" left>mdi-alert-circle</v-icon>No tag associated with this analysis.
                          <span class="error--text">{{missingTagWarning?'Add one. ':''}}</span>
                        </div>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                  <tag-editor class="ml-14 pb-10 pr-3"/>
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
                         :characterizing-muts='characterizingMuts'/>
    </v-col>
  </v-row>
</template>

<script>
import {mapGetters, mapMutations, mapState} from "vuex";
import MutationSelector from "@/components/form/MutationSelector";
import FieldSelector from "@/components/form/FieldSelector";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import TagEditor from "@/components/controls/TagEditor";

export default {
  name: "ResultFilters",
  components: {TagEditor, IconWithTooltip, FieldSelector, MutationSelector},
  data() {
    return {
      showOptions: false,
      missingTagWarning:false,

      options: {
        'local': {
          icon: 'mdi-feature-search-outline',
          value: 'this analysis only',
          title: 'Local scope',
          subtitle: 'Filters are applied to <span class="font-weight-bold">this analysis only</span>.',
        },
        'tag': {
          icon: 'mdi-tag-multiple-outline',
          title: 'Tag-based scope',
          subtitle: 'Filters are applied to <span class="font-weight-bold">all the analyses belonging to the tag group</span> associated with this analysis.',
        },
      }
    }
  },
  computed: {
    ...mapState(['tags']),
    ...mapGetters(['getCurrentAnalysis', 'getCurrentOpt', 'useLocalOpt']),

    tag() {
      return this.getCurrentAnalysis.tag
    },

    withLineages() {
      return this.getCurrentAnalysis.query.lineage !== null
    },

    characterizingMuts() {
      return this.withLineages ? this.getCurrentAnalysis.characterizingMuts : null
    },

    /** Possible proteins values computed based on data results */
    possibleProteins() {
      const set = new Set(this.getCurrentAnalysis.rows.map(({protein}) => protein))
      return [...set].sort()
    },

    /** Possible mutations values computed based on data results */
    possibleMutations() {
      const set = new Set(this.getCurrentAnalysis.rows.map(({item_key}) => item_key))
      return [...set].sort()
    },

    /** Selected mutation to further filter the data. Takes the form <PROTEIN>_<MUT> */
    selectedMutation: {
      set(newVal) {
        this.setOpt({local: this.useLocalOpt, opt: 'muts', value: newVal})
      },
      get() {
        return this.getCurrentOpt.muts
      }
    },

    /** Selected protein to further filter the data */
    selectedProtein: {
      set(newVal) {
        this.setOpt({local: this.useLocalOpt, opt: 'protein', value: newVal})
      },
      get() {
        return this.getCurrentOpt.protein
      }
    },


  },
  methods: {
    ...mapMutations(['setOpt']),

    /**
     * Changes the scope of the filters
     * @param value Either 'tag','local'
     */
    changeScope(value) {
      switch (value) {
        case 'tag':
          if (!this.tag) {
            // No tag defined for the current analysis
            this.missingTagWarning = true
          } else {
            // Just switch to tag based filters
            this.setOpt({local: true, opt: 'useLocalOpt', value: false})
            this.showOptions=false
          }
          break
        case 'local':
          // Just switch to local filters
          this.setOpt({local: true, opt: 'useLocalOpt', value: true})
          this.showOptions=false
          break
      }
    }
  },
}
</script>

<style scoped>

</style>