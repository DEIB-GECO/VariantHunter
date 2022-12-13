<!--

  Component:    BtnWithTooltip
  Description:  Button with tooltip element embedded

  Props:
  ├── contentClass:   Class of the button
  ├── color:          Color of the button text
  ├── hoverColor:     Color of the button text on hover
  ├── text:           Button text
  ├── icon:           Button icon
  ├── appendIcon:     Append icon flag
  ├── dark:           Dark appearance flag
  ├── outlined:       Outlined appearance
  ├── outlined:       Disabled flag
  ├── tip:            Tip text
  ├── size:           Size of the button
  ├── left:           Position the tip to the left
  ├── right:          Position the tip to the right
  ├── top:            Position the tip at the top,
  ├── bottom:         Position the tip at the bottom,
  └── clickHandler:   Click handler function

  Slots:
  ├── btn:            Activator slot
  └── tip:            Tip slot

-->

<template>
  <v-tooltip :disabled="tip===''" :bottom="bottom" content-class="rounded-xl tooltip" :left="left" :right="right"
             :top="top" allow-overflow z-index="999" max-width="400px">

    <!-- Activator button -->
    <template v-slot:activator="{ on, attrs }">
      <v-btn depressed :outlined="outlined" rounded :small="size==='small'" :x-small="size==='x-small'" :dark="dark"
             :class="contentClass" :disabled="disabled"
             :color="(isHover && hoverColor)?hoverColor:color" v-bind="attrs" v-on="on" @click.stop="onClick()"
             @mouseenter="isHover=true" @mouseleave="isHover=false">
        <slot name="btn">
          <v-icon v-if="!appendIcon && icon" :small="size==='small'" :x-small="size==='x-small'" left :dark="dark">
            {{ icon }}
          </v-icon>
          {{ text }}
          <v-icon v-if="appendIcon && icon" :small="size==='small'" :x-small="size==='x-small'" right :dark="dark">
            {{ icon }}
          </v-icon>
        </slot>
      </v-btn>
    </template>

    <!-- Tooltip content -->
    <span class="compact-tooltip">
      <slot name="tip">
        <span v-html="tip"/>
      </slot>
    </span>

  </v-tooltip>
</template>

<script>
export default {
  name: "BtnWithTooltip",

  props: {
    /** Class of the button */
    contentClass: {},

    /** Color of the button text */
    color: {},

    /** Color of the button text on hover */
    hoverColor: {},

    /** Button text */
    text: {},

    /** Button icon */
    icon: {},

    /** Append icon flag*/
    appendIcon: Boolean,

    /** Dark appearance flag */
    dark: Boolean,

    /** Outlined appearance*/
    outlined: Boolean,

    /** Disabled flag*/
    disabled: Boolean,

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

    /** Click handler function*/
    clickHandler: {},
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

<style>


</style>