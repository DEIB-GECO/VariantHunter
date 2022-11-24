<!--
  Component:    Picture
  Description:  Image with zoom feature

  Props:
  ├── src:          Image for the paragraph
  ├── alt:          Alt attribute for the image
  ├── noZoom:       If true, the image cannot be opened in a popup
  └── imgMaxHeight: Max height attribute for the image

-->

<template>
    <v-img :src='src' :alt='alt' contain :max-height='imgMaxHeight' :class='"rounded "+(noZoom? "":"zoom-in-action")' eager
           @click='manageImgZoom' >
    <!-- Dialog element for image -->
    <v-dialog v-model='showImg' transition='dialog-bottom-transition'>
      <v-img :src='src' :alt='alt' contain eager class='rounded-xl zoom-out-action' @click='showImg=false' />
    </v-dialog>
    </v-img>
</template>

<script>
export default {
  name: 'Picture',
  props: {
    /** Image for the paragraph */
    src: {},

    /** Alt attribute for the image */
    alt: {},

    /** Max height attribute for the image */
    imgMaxHeight: {},

    /** If true, the image cannot be opened in a popup */
    noZoom: Boolean
  },
  data () {
    return {
      /** Visibility flag for the img dialog */
      showImg: false
    }
  },
  methods: {
    manageImgZoom () {
      if (!this.noZoom) {
        this.showImg = true
      }
    }
  }
}
</script>

<style scoped>

/** Cursor behavior */
.zoom-out-action{
  cursor: zoom-out !important;
}
.zoom-in-action{
  cursor: zoom-in;
}

</style>
