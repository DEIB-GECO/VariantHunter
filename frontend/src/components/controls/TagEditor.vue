<!--

  Component:    TagEditor
  Description:  Tag editing component to change, un-assign or rename tags

-->

<template>
  <div>

    <!-- Add tag mode -->
    <v-list-item-subtitle v-if="tag!==null || addTagMode" class="break-spaces">

      <!-- Current tag if set with rename and un-assign buttons-->
      <v-chip v-if="tag!==null" :color="tags[tag].tagColor.color" :dark="tags[tag].tagColor.isDark"
              :light="!tags[tag].tagColor.isDark" class="mr-1 mb-1 pr-0">
        <span v-if="!renameMode" class="tag-name mr-6">{{ tag }}</span>
        <span v-else class="mr-1 rename-tag"><v-text-field v-model="newName"/></span>
        <v-divider vertical/>
        <icon-with-tooltip v-if="!renameMode" icon="mdi-form-textbox" bottom tip="Rename this tag"
                           :click-handler="openRenameMode" size="medium"/>
        <icon-with-tooltip v-else icon="mdi-check" bottom tip="Rename this tag" :click-handler="()=>renameTag(tag)"
                           size="medium"/>
        <icon-with-tooltip v-if="!renameMode" icon="mdi-close-circle-outline" hover-color="error" bottom
                           tip="Un-assign tag" :click-handler="()=>removeTag(tag)" size="medium"/>
      </v-chip>

      <!-- Change tag mode: combobox with confirmation button -->
      <span v-if="!renameMode" class="white rounded-xl add-tag mr-1 mb-1">
          <v-combobox height="15px" flat v-model="newTag" hide-details :items="Object.keys(tags)" light
                      color="f_primary" persistent-placeholder
                      :placeholder="tag!==null?'change tag':'select / add tag '"
                      :search-input.sync="newTagInput" @keydown.enter="addTagManager()" class="combobox-tag">
            <template v-slot:prepend-item>
              <div class="px-3 pb-3 text-body-4 compact-text-4">Select a tag or type <br/>the name of the new one</div>
            </template>
            <template v-slot:no-data>
              <div class="px-3 no-data text-break text-body-4 compact-text-4">
                Press <kbd>enter</kbd> to create '{{ newTagInput ? newTagInput.toUpperCase() : newTagInput }}' tag.
              </div>
            </template>
          </v-combobox>
          <icon-with-tooltip color="f_primary" size="medium" bottom
                             tip="Click here to add a tag or replace the current one"
                             :icon="tag!==null?'mdi-pencil-outline':'mdi-plus'"
                             :click-handler="()=>addTagManager()"/>
      </span>

    </v-list-item-subtitle>

    <!-- No tag initial view: button to open add tag mode -->
    <v-list-item-subtitle v-else>
      <btn-with-tooltip bottom tip="Add a tag to the current analysis" text="Add tag" append-icon
                        icon="mdi-plus" size="x-small" outlined :click-handler="()=>addTagMode=true"/>
    </v-list-item-subtitle>

  </div>
</template>

<script>
import {mapActions, mapGetters, mapMutations, mapState} from "vuex";
import BtnWithTooltip from "@/components/general/basic/BtnWithTooltip";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";

export default {
  name: "TagEditor",
  components: {IconWithTooltip, BtnWithTooltip},

  data() {
    return {
      /** Boolean flag set to true if add tag mode is enabled (if no tag is set show add form) */
      addTagMode: false,
      /** Tag name to be assigned (and confirmed with enter). Used in add tag mode */
      newTag: '',
      /** Tag name to be assigned (but just typed). Used in add tag mode */
      newTagInput: '',

      /** Boolean flag set to true if renaming mode is enabled (trying to rename a tag) */
      renameMode: false,
      /** New name for the tag. Used in rename mode */
      newName: '',
    }
  },

  computed: {
    ...mapState(['tags']),
    ...mapGetters(['getCurrentAnalysis']),

    /** Currently assigned tag. Possibly null */
    tag() {
      return this.getCurrentAnalysis.tag
    },
  },

  methods: {
    ...mapActions(['updateTagName']),
    ...mapMutations(['addTag', 'removeTag']),

    /** Opener for the rename mode */
    openRenameMode() {
      this.renameMode = true
      this.newName = this.tag // set current name in the edit field
    },

    /**
     * Actually perform the renaming of an existing tag and close rename mode
     */
    renameTag() {
      if (this.newName && this.newName.toUpperCase() !== this.tag)
        this.updateTagName({oldName: this.tag, newName: this.newName}).then(() => this.renameMode = false)
      else
        this.renameMode = false
    },

    /**
     * Add/replace tag to the current analysis
     */
    addTagManager() {
      const input = this.newTagInput ? this.newTagInput : this.newTag
      if (input) {
        this.addTag(input.toUpperCase()) // if the tag does not exist it will be created
        // reset form
        this.newTag = ''
        this.newTagInput = ''
      }
    },
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

.rename-tag input {
  padding-bottom: 0 !important;
}

.tag-name {
  min-width: 93px;
}
</style>