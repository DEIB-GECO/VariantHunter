<!--
  Component:    SectionElement
  Description:  Container for a section of the result (tables, plots,..).
                It is equipped with a show/hide section body control.

  Props:
  ├── icon:       Icon name for the title
  ├── title:      Title for the section
  ├── subtitle:   Subtitle for the section
  ├── caption:    Additional text to be displayed under the subtitle
  ├── tabs:       Array of labels for the tabs of the section
  ├── collapsed:  Collapse the section by default
  └── assignId:   HTML id to be assigned to the section

  Slots:
  └── default:  The content of the section body

  Events:
  └── tabChange:  Emitted on tab change together with the selected tab index

-->

<template>
  <v-row v-bind:id="assignId">
    <v-col>

      <!-- Section headings -->
      <v-row>
        <v-col >
          <div :class="'text-h5 compact-h5 font-weight-black primary--text mt-8  spaced-5 mb-'+(tabs.length>0?'4':'2')">
            <v-icon left color="primary">{{ icon }}</v-icon>
            <span v-html="title"/>
            <v-fade-transition hide-on-leave>
            <div v-if="subtitle && showSectionBody" class="ml-11">
              <div class="text-body-0 compact-text-0 font-weight-medium " v-html="subtitle"/>
              <div class="text-body-4 compact-text-2 font-weight-regular">{{ caption }}</div>
            </div>
            </v-fade-transition>
          </div>

          <!-- Section options -->
          <div :class="'options-container '+((tabs.length>0 && showSectionBody)?'mt-6':'')">
            <div class='section-options'>

              <!-- Tabs-->
              <span v-for='(tab, index) in tabs' v-bind:key='index' v-bind:id="assignId+'-tab'+index"
                    :class='tabLabelClass + (currentTab!==index?" current-tab":"")' @click='currentTab=index'>
              {{ tab }}
              </span>

              <!-- Expand/collapse option-->
              <span class='expand-collapse-icon'>
              <v-icon v-if='showSectionBody' small color='f_primary' v-bind:id="assignId+'-collapse'"
                      @click='invertVisibility'>mdi-arrow-collapse</v-icon>
              <v-icon v-else small color='f_primary' @click='invertVisibility' v-bind:id="assignId+'-expand'">mdi-arrow-expand</v-icon>
            </span>

            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Section body collapsed -->
      <v-row v-if='!showSectionBody' class='section-container' justify-center>
        <div class='collapsed-element'/>
      </v-row>

      <!-- Section body expanded -->
      <v-expand-transition>
        <v-row v-if='showSectionBody' class='section-container' justify-center>
          <slot></slot>
        </v-row>
      </v-expand-transition>

    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'SectionElement',

  props: {
    /** Title for the section */
    title: {required: true},

    /** Subtitle for the section */
    subtitle: {},

    /** Additional text to be displayed under the subtitle */
    caption: {},

    /** Icon name for the title */
    icon: {required: true},

    /** Array of labels for the tabs of the section */
    tabs: {
      default() {
        return []
      }
    },

    /** Collapse the section by default */
    collapsed: Boolean,

    /** HTML id to be assigned to the section */
    assignId:{}
  },

  data() {
    return {
      /** Flag for the visibility of the section body */
      showSectionBody: !this.collapsed,

      /** Currently selected tab */
      currentTab: 0
    }
  },
  computed: {
    tabLabelClass() {
      return 'tab-icon ' + (this.showSectionBody ? '' : 'hidden-tab ')
    }
  },
  methods: {
    /** Change the visibility flag value for the section body*/
    invertVisibility() {
      this.showSectionBody = !this.showSectionBody
    }
  },
  watch: {
    /** Emit tabChange when tab is changed */
    currentTab() {
      this.$emit('tabChange', this.currentTab)
    }
  }
}
</script>

<style scoped>

/** Section options labels */
.section-options {
  right: 0;
  left: 0;
  position: absolute;
}

.options-container {
  top: -13px;
  position: relative;
}

.section-options span {
  height: 25px;
  font-size: 14px;
  border-radius: 10px 10px 0 0;
  text-align: center;
  background: white;
  text-transform: uppercase;
  letter-spacing: 0.005em;
  color: var(--v-f_primary-base);
  cursor: pointer;
}

/* Expand-collapse icon */
.expand-collapse-icon {
  float: right;
  width: 25px;
}

.tab-icon:first-child {
  margin-left: 15px;
}

.tab-icon {
  float: left;
  padding: 3px 15px 0 15px;
  margin-right: 10px;
}

.hidden-tab {
  display: none;
}

.current-tab {
  background: #e3e3e3 !important;
}

/* Collapse body element */
.collapsed-element {
  width: 100%;
  border-radius: 4px;
  height: 5px;
  background: white;
}

.section-container {
  padding: 8px;
  border-radius: 8px;
  background: white;
}

</style>
