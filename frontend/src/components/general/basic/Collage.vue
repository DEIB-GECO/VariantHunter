<!--
  Component:    Collage
  Description:  Side by side images with zoom feature

  Props:
  ├── src1:           Image 1
  ├── alt1:           Alt attribute for the image 1
  ├── src2:           Image 2
  ├── alt2:           Alt attribute for the image 2
  ├── noZoom:         If true, the image cannot be opened in a popup
  └── imgMaxHeight:   Max height attribute for the image

-->

<template>
 <v-row>
    <v-col class='col-md-6 col-sm-12 pr-sm-auto mr-sm-auto mr-md-0 pr-md-0 ma-auto'>
      <Picture :src='src1' :alt='alt1' :no-zoom='noZoom' :img-max-height='imgMaxHeight' />
    </v-col>
   <v-col class='col-md-6 col-sm-12 pl-sm-auto ml-sm-auto ml-md-0 pl-md-0 ma-auto'>
      <Picture :src='src2' :alt='alt2' :no-zoom='noZoom' :img-max-height='imgMaxHeight' />
    </v-col>
  </v-row>
</template>

<script>
import Picture from '@/components/general/basic/Picture'
export default {
  name: 'Collage',
  components: { Picture },
  props: {
    /** Image 1 */
    src1: {},

    /** Alt attribute for the image 1 */
    alt1: {},

    /** Image 2 */
    src2: {},

    /** Alt attribute for the image 2 */
    alt2: {},

    /** If true, the image cannot be opened in a popup */
    noZoom: Boolean,

    /** Max height attribute for the image */
    imgMaxHeight: {}
  }
}
</script>

<style scoped>

</style>
