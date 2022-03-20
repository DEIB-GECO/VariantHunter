<!--
  Component:    SectionElement
  Description:  Container for a section of the result (tables, plots,..).
                It is equipped with a show/hide section body control.

  Props:
  ├── icon:   Icon name for the title. MDI icon are used.
  └── title:  Title for the section.

  Slots:
  └── default:  The content of the section body
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
            <hr />
          </h2>
          <span class='expand-collapse-icon'>
            <v-icon v-if='showSectionBody' small color='primary' @click='invertVisibility'>mdi-arrow-collapse</v-icon>
            <v-icon v-else small color='primary' @click='invertVisibility'>mdi-arrow-expand</v-icon>
          </span>
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

    /** Collapse the section by default */
    collapsed: Boolean
  },
  data () {
    return {
      /** Flag for the visibility of the section body */
      showSectionBody: !this.collapsed
    }
  },
  methods: {
    /** Change the visibility flag value for the section body*/
    invertVisibility () {
      this.showSectionBody = !this.showSectionBody
    }
  }
}
</script>

<style scoped>

/* Expand-collapse icon */
.expand-collapse-icon {
  right: 24px;
  height: 24px;
  text-align: center;
  position: absolute;
  background: white;
  border-radius: 10px 10px 0 0;
  width: 25px;
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
  margin-top: 30px;
}

</style>
