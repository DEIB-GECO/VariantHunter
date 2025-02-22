<!--

  Component:    ListItem
  Description:  Item for lists

  Props:
  ├── link:           Boolean flag set to true if the list item is a link
  ├── expandOnHover:  Boolean flag set to true if the element expands on hover
  ├── dense:          Boolean flag set to true if dense style is used
  ├── withActions:    Boolean flag set to true if item has actions
  ├── title:          List element title
  ├── subtitle:       List element subtitle
  └── icon:           List element icon

  Slots:
  └── action:         Actions slot

-->

<template>
  <v-list-item :class="dense?'':'taller-list-item'" :link="link" @mouseenter="showTip=true" @mouseleave="showTip=false">
    <v-list-item-icon class="align-middle">
      <v-icon>{{ icon }}</v-icon>
    </v-list-item-icon>
    <v-list-item-content>
      <v-list-item-title class="text-body-2 font-weight-bold">{{ title }}</v-list-item-title>
      <v-expand-transition>
        <v-list-item-subtitle v-if="showTip || !expandOnHover" class="text-body-3">{{ subtitle }}</v-list-item-subtitle>
      </v-expand-transition>
    </v-list-item-content>
    <v-list-item-action v-if="withActions">
      <slot name="actions"></slot>
    </v-list-item-action>
  </v-list-item>
</template>


<script>
export default {
  name: "ListItem",

  props: {
    /** Boolean flag set to true if the list item is a link*/
    link: Boolean,

    /** Boolean flag set to true if the element expands on hover */
    expandOnHover: Boolean,

    /** Boolean flag set to true if dense style is used */
    dense: Boolean,

    /** Boolean flag set to true if item has actions */
    withActions: Boolean,

    /** List element title */
    title: {},

    /** List element subtitle */
    subtitle: {},

    /** List element icon */
    icon: {}
  },

  data() {
    return {
      /** Boolean flag set to true if subtitle is shown  */
      showTip: false
    }
  }
}
</script>

<style scoped>
.align-middle {
  margin-bottom: auto !important;
  margin-top: auto !important;
}
</style>
<style>
.taller-list-item {
  height: 56px;
}
</style>