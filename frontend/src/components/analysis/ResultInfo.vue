<template>
  <v-row class="mt-6" no-gutters>
    <v-col>
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
          <v-list-item-content>
            <v-list-item-title>{{ getCurrentAnalysis.query.datasetType.toUpperCase() }} dataset</v-list-item-title>
            <v-list-item-subtitle>updated on {{ getCurrentAnalysis.query.datasetAsOf }}</v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>
    <v-col cols="12" md="4" lg="12">
      <v-list color="transparent">
        <v-list-item>
          <v-list-item-icon>
            <v-icon left large color="primary">mdi-tag-multiple</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>Tag group <icon-with-tooltip icon="mdi-help-circle-outline" bottom size="medium"
                                 tip="Tags allow related analyses to be grouped together and can be useful for preserving filtering options"/>
                </v-list-item-title>
            <v-list-item-subtitle class="break-spaces" v-if="tag!==null || addTagMode">
              <v-chip v-if="tag!==null" :color="tags[tag].tagColor.color"
                        :dark="tags[tag].tagColor.isDark" class="mr-1 mb-1" close close-icon="mdi-minus"
                        @click:close="removeTag(tag)">
                  {{ tag }}
                </v-chip>
                <span class="white rounded-xl add-tag mr-1 mb-1">
                <v-combobox height="15px" flat v-model="newTag" hide-details :items="Object.keys(tags)" light color="f_primary" persistent-placeholder placeholder="select/add tag "
                            :search-input.sync="newTagInput" @keydown.enter="addTagManager()"/>
                <icon-with-tooltip color="f_primary" size="medium" bottom tip="Click here to add a tag or replace the current one"
                                   :icon="tag!==null?'mdi-swap-horizontal':'mdi-plus'"
                                   :click-handler="()=>addTagManager()"/>
              </span>
            </v-list-item-subtitle>
            <v-list-item-subtitle v-else>
              <btn-with-tooltip bottom tip="Add a tag to the current analysis" text="Add tag" append-icon
                                icon="mdi-plus" size="x-small" outlined :click-handler="()=>addTagMode=true"/>
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-col>
    <v-col cols="12" md="8" lg="12">
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
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";

export default {
  name: "ResultInfo",
  components: {IconWithTooltip, BtnWithTooltip},
  data() {
    return {

      editNoteMode: false,

      addTagMode: false,
      newTag: '',
      newTagInput: '',
    }
  },
  computed: {
    ...mapState(['tags']),
    ...mapGetters(['getCurrentAnalysis']),

    notes: {
      set(newVal) {
        this.setNotes(newVal)
      },
      get() {
        return this.getCurrentAnalysis.notes
      }
    },

    tag() {
      return this.getCurrentAnalysis.tag
    },

    locationData() {
      const {granularity, location} = this.getCurrentAnalysis.query
      const {region, country, continent} = location

      switch (granularity) {
        case 'region':
          return region + ', ' + country + ', ' + continent
        case 'country':
          return country + ', ' + continent
        default:
          return continent
      }
    },

    period() {
      return computeDateLabel(this.getCurrentAnalysis.query.endDate, 27, 0)
    }
  },
  methods: {
    ...mapMutations(['setNotes', 'addTag', 'removeTag']),

    addTagManager() {
      const input = this.newTagInput ? this.newTagInput : this.newTag
      if (input) {
        this.addTag(input)
        this.newTag = ''
        this.newTagInput = ''
      }
    }
  }
}
</script>

<style scoped>
.add-tag {
  padding: 5px 0 5px 10px;
  width: 200px;
  size: 14px !important;
  height: 32px;
  display: inline-flex;
  align-content: center;
  align-items: center;
}

.add-tag .v-text-field {
  padding-top: 0 !important;
}
</style>