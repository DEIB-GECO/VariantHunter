<!--
  Component:    Paragraph
  Description:  Paragraph with an image

  Props:
  ├── src:          Image for the paragraph
  ├── right:        If true, the text is on the right side
  ├── left:         If true, the text is on the left side
  ├── alt:          Alt attribute for the image
  └── imgMaxHeight: Max height attribute for the image

  Slots:
  └── default:      Text of the paragraph
-->

<template>
  <v-row>
    <v-col :class='src? "col-md-6 col-sm-5" : ""' :order='right? 2 : 0'>
      <slot>
        <p>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut
          labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco
          laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in
          voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
          cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </p>
      </slot>
    </v-col>
    <v-col v-if='src' class='col-md-6 col-sm-7'>
      <v-img :src='src' :alt='alt' contain :max-height='imgMaxHeight' />
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'Paragraph',
  props: {
    /** Image for the paragraph */
    src: {},

    /** Alt attribute for the image */
    alt: {},

    /** Max height attribute for the image */
    imgMaxHeight: {},

    /** If true, the text is on the left side */
    left: Boolean,

    /** If true, the text is on the right side */
    right: Boolean
  }
}
</script>

<style scoped>
</style>
