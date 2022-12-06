<!--

  Component:    IconWithTooltip
  Description:  Icon with tooltip element embedded

  Props:
  ├── zIndex:         zIndex of the tip
  ├── contentClass:   Class of the button
  ├── color:          Color of the icon
  ├── hoverColor:     Color of the icon on hover
  ├── assignId:       HTML id to be assigned
  ├── icon:           Icon
  ├── dark:           Dark appearance flag
  ├── tip:            Tip text
  ├── size:           Size of the button
  ├── left:           Position the tip to the left
  ├── right:          Position the tip to the right
  ├── top:            Position the tip at the top,
  ├── bottom:         Position the tip at the bottom,
  └── clickHandler:   Click handler function

  Slots:
  └── tip:            Tip slot

-->

<template>
  <v-tooltip :disabled="tip===''" :bottom="bottom" :left="left" :right="right" :top="top" allow-overflow z-index="999"
             :close-delay="0" max-width="400px">

    <!-- Activator icon -->
    <template v-slot:activator="{ on, attrs }">
      <v-btn icon :small="size==='small'" :class="contentClass" :color="(isHover && hoverColor)?hoverColor:color"
             v-bind="attrs" v-on="on" @click.stop="onClick()" @mouseenter="isHover=true" @mouseleave="isHover=false">
        <v-icon :color="(isHover && hoverColor)?hoverColor:color" :size="size" :dark="dark">
          {{ icon }}
        </v-icon>
      </v-btn>
    </template>

    <!-- Tip -->
    <slot name="tip">
      <span>{{ tip }}</span>
    </slot>

  </v-tooltip>
</template>

<script>
export default {
  name: "IconWithTooltip",

  props: {
    /** Color of the icon */
    color: {default: ''},

    /** Color of the icon on hover */
    hoverColor: {},

    /** zIndex of the tip */
    zIndex: {default: 10},

    /** Icon */
    icon: {},

    /** Dark appearance flag */
    dark: Boolean,

    /** Tip text */
    tip: {},

    /** Size of the button */
    size: {},

    /** Position the tip to the left */
    left: Boolean,

    /** Position the tip to the right */
    right: Boolean,

    /** Position the tip at the top */
    top: Boolean,

    /** Position the tip at the bottom */
    bottom: Boolean,

    /** Click handler function */
    clickHandler: {},

    /** HTML id to be assigned */
    assignId: {},

    /** Class of the button */
    contentClass: {default: ''},
  },

  data() {
    return {
      /** Boolean flag set to true when mouse is hovering the button */
      isHover: false
    }
  },
  methods: {
    /** On click handler */
    onClick() {
      if (this.clickHandler)
        this.clickHandler()
    }
  }
}
</script>

<style scoped>

</style>