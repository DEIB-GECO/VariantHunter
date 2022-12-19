<!--

  Component:    ResultInfo
  Description:  Info summary section of the result panel

-->

<template>
  <v-row class="mt-6" no-gutters id="summary">

    <!-- Sequences from -->
    <v-col>
      <summary-intro/>
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon>
            <v-icon left large color="primary">mdi-map-marker-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Sequences from</v-list-item-title>
            <v-list-item-subtitle>{{ locationData }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>

    <!-- Analysis period -->
    <v-col>
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon>
            <v-icon left large color="primary">mdi-calendar-week-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Analysis period</v-list-item-title>
            <v-list-item-subtitle>{{ period }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>

    <!-- Performed on -->
    <v-col>
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon>
            <v-icon left large color="primary">mdi-clock-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Analysis performed on</v-list-item-title>
            <v-list-item-subtitle>{{ getCurrentAnalysis.query.performedOn }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>

    <!-- Dataset info  -->
    <v-col>
      <result-dataset-info/>
    </v-col>

    <!-- Lineages info  -->
    <v-col cols="12" md="8" lg="6" v-if="getCurrentAnalysis.query.lineage">
      <lineages-info/>
    </v-col>

    <!-- Tags -->
    <v-col cols="12" md="8" lg="6">
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon>
            <v-icon left large color="primary">mdi-tag-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Tag group
              <icon-with-tooltip icon="mdi-help-circle-outline" bottom size="medium" :delay="0"
                                 tip="Tags allow related analyses to be grouped together and can be useful for preserving filtering/ordering options"/>
            </v-list-item-title>
            <tag-editor/>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>

    <!-- Notes -->
    <v-col cols="12">
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon>
            <v-icon left large color="primary">mdi-note-edit-outline</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Notes</v-list-item-title>
            <v-list-item-subtitle v-if="notes || editNoteMode">
              <v-textarea outlined v-model="notes" auto-grow clearable clear-icon="mdi-backspace-outline" hide-details
                          @click:clear="editNoteMode=false"/>
            </v-list-item-subtitle>
            <v-list-item-subtitle v-else>
              <btn-with-tooltip bottom tip="Add notes related to the current analysis" text="Add notes" append-icon
                                icon="mdi-pencil" size="x-small" outlined :click-handler="()=>editNoteMode=true"/>
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>

  </v-row>
</template>

<script>
import {mapGetters, mapMutations} from "vuex";
import {computeDateLabel} from "@/store/utils/utils";
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip.vue";
import TagEditor from "@/components/controls/TagEditor.vue";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip.vue";
import SummaryIntro from "../../intros/SummaryIntro.vue";
import ResultDatasetInfo from "@/components/analysis/info/ResultDatasetInfo.vue";
import LineagesInfo from "@/components/analysis/info/LineagesInfo.vue";

export default {
  name: "ResultInfo",
  components: {LineagesInfo, ResultDatasetInfo, SummaryIntro, IconWithTooltip, TagEditor, BtnWithTooltip},

  data() {
    return {
      /** Boolean flag set to true if note editing is enabled */
      editNoteMode: false,
    }
  },

  computed: {
    ...mapGetters(['getCurrentAnalysis']),

    /** Notes for the current analysis */
    notes: {
      set(newVal) {
        this.setNotes(newVal)
      },
      get() {
        return this.getCurrentAnalysis.notes
      }
    },

    /** Location data */
    locationData() {
      const {granularity, location} = this.getCurrentAnalysis.query
      const {region, country, continent} = location

      switch (granularity) {
        case 'region':
          return region.text + ', ' + country.text + ', ' + continent.text
        case 'country':
          return country.text + ', ' + continent.text
        default:
          return continent.text
      }
    },

    /** Analysis period */
    period() {
      return computeDateLabel(this.getCurrentAnalysis.query.endDate, 27, 0)
    },

  },
  methods: {
    ...mapMutations(['setNotes']),
  }
}
</script>

<style scoped>
</style>