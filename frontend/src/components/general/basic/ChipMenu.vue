<!--

  Component:    ChipMenu
  Description:  Composable chip menu

  Props:
  ├── activatorText:        Text of the activator
  ├── activatorIcon:        Icon of the activator
  ├── activatorOutlined:    Boolean flag set to true to use the outlined appearance
  ├── small:                Boolean flag set to true to use the small size activator
  ├── color:                Color of the activator
  ├── attach:               Attach to HTML element
  ├── hideOnLeave:          Boolean flag set to true to hide menu on content leave
  └── closeOnContentClick:  Boolean flag set to true to close menu on content click

  Slots:
  └── default:            Default slot

-->

<template>
  <v-menu v-model="showMenu" rounded :attach="attach" offset-y content-class="rounded-xl"
          :close-on-content-click="closeOnContentClick">

    <!-- Activator chip -->
    <template v-slot:activator="{ on, attrs }">
      <v-chip :small="small" dark :color="color" :outlined="activatorOutlined" :class="'text-uppercase'"
              v-bind="attrs" v-on="on">
        <v-icon left :small="small">{{ activatorIcon }}</v-icon>
        {{ activatorText }}
      </v-chip>
    </template>

    <!-- Menu content -->
    <v-card class="f_text_dark--text" max-width="300px" color="f_tertiary" @mouseleave="onMouseLeave">
      <v-container>
        <slot></slot>
      </v-container>
    </v-card>

  </v-menu>
</template>

<script>
export default {
  name: "ChipMenu",

  props: {
    /** Text of the activator */
    activatorText: {},

    /** Icon of the activator */
    activatorIcon: {},

    /** Boolean flag set to true to use the outlined appearance */
    activatorOutlined: {default: true},

    /** Boolean flag set to true to use the small size activator */
    small: Boolean,

    /** Color of the activator */
    color: {default: 'tertiary'},

    /** Attach to HTML element */
    attach: {},

    /** Boolean flag set to true to hide menu on content leave */
    hideOnLeave: Boolean,

    /** Boolean flag set to true to close menu on content click */
    closeOnContentClick: {default: true},
  },

  data() {
    return {
      /** Boolean visibility flag for the menu */
      showMenu: false,
    }
  },

  methods: {
    /** On mouse leave event manager */
    onMouseLeave() {
      if (this.hideOnLeave) {
        this.showMenu = false
      }
    }
  }
}
</script>

<style scoped>

</style>