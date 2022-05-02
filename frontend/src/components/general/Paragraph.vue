<!--
  Component:    Paragraph
  Description:  Paragraph with an image

  Props:
  ├── src:          Image for the paragraph
  ├── right:        If true, the text is on the right side
  ├── left:         If true, the text is on the left side
  ├── alt:          Alt attribute for the image
  ├── largerImg:    If true, the image is larger
  ├── noZoom:       If true, the image cannot be opened in a popup
  └── imgMaxHeight: Max height attribute for the image

  Slots:
  └── default:      Text of the paragraph
-->

<template>
  <v-row>
    <v-col :class='"ma-auto "+ (largerImg?"hidden-md-and-up":"hidden-sm-and-up")'>
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
    <v-col :class='(src? (largerImg? "col-md-4 col-sm-12 hidden-sm-and-down":"col-md-6 col-sm-5 hidden-xs-only") : "")+" ma-auto"' :order='right? 2 : 0'>
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
    <v-col v-if='src' :class='(largerImg? "col-md-8 col-sm-12": "col-md-6 col-sm-7")+" mb-5 mt-5"'>
      <Picture :src='src' :alt='alt' :max-height='imgMaxHeight' :no-zoom='noZoom' />
    </v-col>
  </v-row>
</template>

<script>
import Picture from '@/components/general/Picture'
export default {
  name: 'Paragraph',
  components: { Picture },
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
    right: Boolean,

    /** If true, the image is larger */
    largerImg: Boolean,

    /** If true, the image cannot be opened in a popup */
    noZoom: Boolean
  }
}
</script>

<style scoped>

</style>

