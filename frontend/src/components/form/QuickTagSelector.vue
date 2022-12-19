<!--

  Component:    QuickTagSelector
  Description:  Component to quickly select a tag/create a tag to be associated with a new analysis

-->

<template>
  <v-col v-if="showTagSelector" class="text-body-3">
    <v-row class="px-5 pt-2">
      <v-col cols="auto">
        <!-- Headings -->
        <div class="text-overline text-optional font-weight-regular">Optional</div>
        <span class="primary--text"><span class="compact-text-5 font-weight-black">Tag</span>: assign to</span>

        <!-- Selector -->
        <v-card class="rounded-xl add-tag ml-3 pr-3" elevation="0" :color="tagColor.color" height="24px" max-width="190"
                :light="!tagColor.isDark" :dark="tagColor.isDark">
          <v-combobox height="10px" flat v-model="newTag" hide-details :items="allTags"
                      color="f_primary" persistent-placeholder placeholder="select / add tag"
                      :search-input.sync="newTagInput">
            <template v-slot:no-data>
              <div class="px-3 no-data text-break">
                Press <kbd>enter</kbd> to create '{{ newTagInput ? newTagInput.toUpperCase() : newTagInput }}' tag.
              </div>
            </template>
          </v-combobox>
        </v-card>

        <!-- Options to avoid tag and hint -->
        <icon-with-tooltip icon="mdi-tag-off-outline" bottom size="medium" color="primary" hover-color="error"
                           tip="Click to assign no tag" :click-handler="()=>newTag=null" :delay="0"/>
        <icon-with-tooltip icon="mdi-help-circle-outline" bottom size="medium" color="primary" hover-color="warning" :delay="0"
                           tip="Tags allow related analyses to be grouped together and can be useful for preserving filtering/ordering options"/>
      </v-col>
    </v-row>
  </v-col>
</template>

<script>
import {mapState} from "vuex";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";

export default {
  name: "QuickTagSelector",
  components: {IconWithTooltip},

  data() {
    return {
      /** Tag name to be assigned (and confirmed with enter). Used in add tag mode */
      newTag: '',

      /** Tag name to be assigned (but just typed). Used in add tag mode */
      newTagInput: '',
    }
  },

  computed: {
    ...mapState(['tags']),

    /** All values for tags */
    allTags() {
      return Object.keys(this.tags)
    },

    /** Currently selected tag color*/
    tagColor() {
      const input = this.newTagInput ? this.newTagInput : this.newTag
      if (input && typeof input == 'string' && this.allTags.includes(input.toUpperCase())) {
        return this.tags[input].tagColor
      }
      return {color: undefined, isDark: this.$vuetify.theme.dark}
    },

    /** Boolean visibility flag set to true iff there is at least one tag */
    showTagSelector() {
      return Object.keys(this.tags).length > 0
    }
  },

  watch: {
    /** On tag name changes update model */
    newTag(newVal) {
      this.$emit('input', newVal ? newVal.toUpperCase() : newVal)
    }
  },

  /** On mount set the tag to the last created tag */
  mounted() {
    if (this.showTagSelector) {
      this.newTag = Object.entries(this.tags).sort((a, b) => b[1].createdAt - a[1].createdAt)[0][0]
    }
  }
}
</script>

<style scoped>
.no-data {
  max-width: 170px;
}

.text-optional {
  line-height: 10px !important;
  font-size: 10px !important;
  opacity: 0.7;
}
</style>