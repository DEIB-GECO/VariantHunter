<template>
  <div>
    <v-list-item-subtitle class="break-spaces" v-if="tag!==null || addTagMode">
      <v-chip v-if="tag!==null" :color="tags[tag].tagColor.color" :dark="tags[tag].tagColor.isDark"
              :light="!tags[tag].tagColor.isDark" class="mr-1 mb-1" close close-icon="mdi-close-circle-outline"
              @click:close="removeTag(tag)">
        {{ tag }}
      </v-chip>
      <span class="white rounded-xl add-tag mr-1 mb-1">
          <v-combobox height="15px" flat v-model="newTag" hide-details :items="Object.keys(tags)" light
                      color="f_primary" persistent-placeholder placeholder="select / add tag "
                      :search-input.sync="newTagInput" @keydown.enter="addTagManager()">
            <template v-slot:no-data>
              <div class="px-3 no-data text-break">
                Press <kbd>enter</kbd> to create '{{ newTagInput ? newTagInput.toUpperCase() : newTagInput }}' tag.
              </div>
            </template>
          </v-combobox>
          <icon-with-tooltip color="f_primary" size="medium" bottom
                             tip="Click here to add a tag or replace the current one"
                             :icon="tag!==null?'mdi-swap-horizontal':'mdi-plus'"
                             :click-handler="()=>addTagManager()"/>
      </span>
    </v-list-item-subtitle>
    <v-list-item-subtitle v-else>
      <btn-with-tooltip bottom tip="Add a tag to the current analysis" text="Add tag" append-icon
                        icon="mdi-plus" size="x-small" outlined :click-handler="()=>addTagMode=true"/>
    </v-list-item-subtitle>
  </div>
</template>

<script>
import {mapGetters, mapMutations, mapState} from "vuex";
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";

export default {
  name: "TagEditor",
  components: {IconWithTooltip, BtnWithTooltip},
  data() {
    return {
      addTagMode: false,
      newTag: '',
      newTagInput: '',
    }
  },
  computed: {
    ...mapState(['tags']),
    ...mapGetters(['getCurrentAnalysis']),

    tag() {
      return this.getCurrentAnalysis.tag
    },

  },
  methods: {
    ...mapMutations(['addTag', 'removeTag']),

    addTagManager() {
      const input = this.newTagInput ? this.newTagInput : this.newTag
      if (input) {
        this.addTag(input.toUpperCase())
        this.newTag = ''
        this.newTagInput = ''
      }
    }
  }
}
</script>

<style scoped>
.no-data {
  max-width: 170px;
}
</style>
<style>
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

.add-tag input::placeholder {
  font-size: 13px;
  text-transform: uppercase;
}

.add-tag .v-select__slot {
  padding-bottom: 5px;
}
</style>