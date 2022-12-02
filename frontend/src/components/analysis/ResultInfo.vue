<template>
  <v-row class="mt-6" no-gutters id="summary">
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
    <v-col>
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon>
            <v-icon left large color="primary">mdi-database-outline</v-icon>
          </v-list-item-icon>
          <v-tooltip top right allow-overflow z-index="999" :close-delay="0" max-width="400px">
            <template v-slot:activator="{ on, attrs }">
              <v-list-item-content v-on="on" v-bind="attrs">
                <v-list-item-title>{{ datasetInfo['file_type'].toUpperCase() }} dataset
                </v-list-item-title>
                <v-list-item-subtitle>updated on {{datasetInfo['last_update'] }}
                </v-list-item-subtitle>
              </v-list-item-content>
            </template>
            <div class="pa-3">
              <div class="text-body-3 font-weight-bold mb-3">
                <v-icon left>mdi-database-outline</v-icon>
                Dataset used
              </div>
              <div class="mb-3">
                <div>
                  <v-icon small left>mdi-connection</v-icon>
                  Metadata provider
                </div>
                <span class="text-uppercase font-weight-bold ml-6">{{ datasetInfo['file_type'] }}</span>
              </div>
              <div class="mb-3" v-if="!(noBegin && noEnd)">
                <div>
                  <v-icon small left>mdi-clock-outline</v-icon>
                  Available period
                </div>
                <div class="text-body-5 ml-6">The data set was limited to the following time period:</div>
                <span class="text-uppercase font-weight-bold ml-6">[ {{ begin }} &nbsp;;&nbsp; {{ end }} ]</span>
              </div>
              <div class="mb-3" v-if="!(noCountryFilter)">
                <div>
                  <v-icon small left>mdi-map-marker-outline</v-icon>
                  Available countries
                </div>
                <div class="text-body-5 ml-6">The dataset was limited to the following countries:</div>
                <span class="text-uppercase font-weight-bold ml-6">{{ datasetInfo['filtered_countries'] }}</span>
              </div>
            </div>
          </v-tooltip>

        </v-list-item>
      </v-list>
    </v-col>
    <v-col cols="12" md="8" lg="12">
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon>
            <v-icon left large color="primary">mdi-tag-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Tag group
              <icon-with-tooltip icon="mdi-help-circle-outline" bottom size="medium"
                                 tip="Tags allow related analyses to be grouped together and can be useful for preserving filtering/ordering options"/>
            </v-list-item-title>
            <tag-editor/>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>
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
import {mapGetters, mapMutations, mapState} from "vuex";
import {computeDateLabel} from "@/store/utils/utils";
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";
import TagEditor from "@/components/controls/TagEditor";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";
import SummaryIntro from "../intros/SummaryIntro";

export default {
  name: "ResultInfo",
  components: {SummaryIntro, IconWithTooltip, TagEditor, BtnWithTooltip},
  data() {
    return {
      editNoteMode: false,
    }
  },
  computed: {
    ...mapGetters(['getCurrentAnalysis']),

    notes: {
      set(newVal) {
        this.setNotes(newVal)
      },
      get() {
        return this.getCurrentAnalysis.notes
      }
    },

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

    period() {
      return computeDateLabel(this.getCurrentAnalysis.query.endDate, 27, 0)
    },

    datasetInfo(){
      return this.getCurrentAnalysis.query.datasetInfo
    },

    noBegin(){
      return this.datasetInfo['begin_date']==='beginning'
    },
    noEnd(){
      return this.datasetInfo['end_date']==='end'
    },
    noCountryFilter(){
      return this.datasetInfo['filtered_countries']==='all'
    },

    begin(){
      return this.noBegin?'N.A.':this.datasetInfo['begin_date']
    },
    end(){
      return this.noEnd?'N.A.':this.datasetInfo['end_date']
    }
  },
  methods: {
    ...mapMutations(['setNotes']),
  }
}
</script>

<style scoped>
</style>