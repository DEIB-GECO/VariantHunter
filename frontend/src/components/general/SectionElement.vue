<!--
  Component:    SectionElement
  Description:  Container for a section of the result (tables, plots,..).
                It is equipped with a show/hide section body control.

  Props:
  ├── icon:   Icon name for the title. MDI icon are used.
  ├── title:  Title for the section.
  └── tabs:   Array of labels for the tabs of the section

  Slots:
  └── default:  The content of the section body

  Emit:
  └── tabCange:  Emitted on tab change together with the selected tab index

-->

<template>
  <v-flex class='xs12 d-flex' justify-center>
    <v-layout justify-center row wrap>

      <!-- Section Heading -->
      <v-flex class='xs12 d-flex' justify-center>
        <div>
          <h2 class='result-heading'>
            <v-icon left color='white'>{{ icon }}</v-icon>
            {{ title }}
          </h2>

          <!-- Section Options -->
          <div class='section-options'>

            <!-- Tabs-->
            <span v-for='(tab, index) in tabs' v-bind:key='index'
                  :class='tabLabelClass + (currentTab!==index?" current-tab":"")' @click='currentTab=index' >
              {{ tab }}
            </span>

            <!-- Expand/collapse option-->
            <span class='expand-collapse-icon'>
              <v-icon v-if='showSectionBody' small color='primary' @click='invertVisibility'>mdi-arrow-collapse</v-icon>
              <v-icon v-else small color='primary' @click='invertVisibility'>mdi-arrow-expand</v-icon>
            </span>

          </div>
        </div>
      </v-flex>

      <!-- Section Body Collapsed -->
      <v-flex v-if='!showSectionBody' class='xs12 d-flex section-container' justify-center>
        <div class='collapsed-element' />
      </v-flex>

      <!-- Section Body Expanded -->
      <v-expand-transition>
        <v-flex v-if='showSectionBody' class='xs12 d-flex section-container' justify-center>
          <slot></slot>
        </v-flex>
      </v-expand-transition>

    </v-layout>
  </v-flex>
</template>

<script>
export default {
  name: 'SectionElement',
  props: {
    /** Title for the section */
    title: { required: true },

    /** Icon name for the title. MDI icon are used. */
    icon: { required: true },

    /** Array of labels for the tabs of the section */
    tabs: { default () { return [] } },

    /** Collapse the section by default */
    collapsed: Boolean
  },
  data () {
    return {
      /** Flag for the visibility of the section body */
      showSectionBody: !this.collapsed,

      /** Currently selected tab */
      currentTab: 0
    }
  },
  computed: {
    tabLabelClass () {
      return 'tab-icon ' + (this.showSectionBody ? '' : 'hidden ')
    }
  },
  methods: {
    /** Change the visibility flag value for the section body*/
    invertVisibility () {
      this.showSectionBody = !this.showSectionBody
    }
  },
  watch: {
    /** Emit tabChange when tab is changed */
    currentTab () {
      this.$emit('tabChange', this.currentTab)
    }
  }
}
</script>

<style scoped>

/** Section options labels */
.section-options {
  right: 24px;
  left: 24px;
  position: absolute;
}

.section-options span {
  height: 25px;
  font-size: 14px;
  border-radius: 10px 10px 0 0;
  text-align: center;
  background: white;
  text-transform: uppercase;
  letter-spacing: 0.005em;
  color: #1a76d2;
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

.hidden-tab{
  display: none;
}
.current-tab{
  background: #e3e3e3 !important;
}

/* Collapse body element */
.collapsed-element {
  width: 100%;
  border-radius: 4px 0 4px 4px;
  height: 5px;
  background: white;
}

/* Heading of table and graphs */
.result-heading {
  color: white;
  font-weight: 800;
  word-spacing: 5px;
  margin-top: 25px;
  border-bottom: solid 4px white;
  margin-bottom: 4px;
}

</style>
