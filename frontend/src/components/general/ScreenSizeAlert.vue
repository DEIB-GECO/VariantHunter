<!--

  Component:    ScreenSizeAlert
  Description:  Small screen alert message

  Events:
  └── close: Emitted on 'okay' click

-->

<template>
  <alert-overlay :value="showWarning" @input="update" :icon="warningIcon" type="warning">
    <template>
      <div>
        <div class="text-h5 compact-h5 font-weight-bold">{{warningTitle}}</div>

        <div class="text-body-2 mt-2 mb-2">{{warningMessage}}</div>
      </div>
    </template>
  </alert-overlay>
</template>

<script>
import AlertOverlay from "@/components/general/basic/AlertOverlay";

export default {
  name: "ScreenSizeAlert",
  components: {AlertOverlay},

  data(){
    return {
      /** Warning visibility flag. True iff a warning message is shown */
      showWarning: false,
      /** Warning title */
      warningTitle: '',
      /** Warning message */
      warningMessage: '',
      /** Warning icon */
      warningIcon: '',
      /** Close flag */
      hasBeenClosed: false
    }
  },

  methods: {
    /** On alert overlay updates */
    update() {
      this.showWarning = false;
      this.hasBeenClosed = true;
      this.$emit('close')
    },

    /** Window size checker */
    checkWindowSize () {
      if(this.hasBeenClosed) return

      const windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth
      const screenSize = window.screen.width
      if (windowWidth <= 511) {
        const isSmallDevice = screenSize <= 511
        this.showWarning = true
        this.warningIcon =
          isSmallDevice
            ? 'mdi-phone-rotate-landscape'
            : 'mdi-arrow-expand-horizontal'
        this.warningTitle =
          isSmallDevice
            ? 'Best from larger devices'
            : 'Resize your browser window'
        this.warningMessage =
          isSmallDevice
            ? 'This device is too small to allow graphs and visualizations to be clearly readable. Please rotate it or try a larger device.'
            : 'The window width is too small for graphs and visualizations to be clearly readable. Please resize your browser window.'
      } else {
        this.showWarning = false
      }
    }
  },

  mounted () {
    this.checkWindowSize()
  },

  created () {
    window.addEventListener('resize', this.checkWindowSize)
  },

  destroyed () {
    window.removeEventListener('resize', this.checkWindowSize)
  },
}
</script>

<style scoped>

</style>