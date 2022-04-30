<!--
  Component:    ErrorAlert
  Description:  Error and warning alerts manager.
                It manages external events as well as screen size warning

  Props:
  ├── errorMessage: The external error event
  └── value:      Error flag. True iff an external error has occurred.
-->

<template>
  <v-overlay :value='value || showWarning' z-index='4'>

    <!-- Error message -->
    <v-container v-if='value'>
      <v-alert dismissible elevation='24' type='error' transition='v-expand-x-transition'
               @input='reloadPage()'>
        <b>The server is temporarily unreachable</b><br />
        An error occurred while contacting the server. Please try again later.<br /><br />
        Error details: <br />
        {{ errorMessage }}
      </v-alert>
    </v-container>

    <!-- Warning message -->
    <v-container v-if='showWarning'>
      <v-alert dismissible elevation='24' :icon='warningIcon' type='warning'
               transition='v-expand-x-transition' @input='showWarning=false'>
        <b>{{warningTitle}}</b><br />
        {{ warningMessage }}
      </v-alert>
    </v-container>
  </v-overlay>
</template>

<script>
export default {
  name: 'ErrorAlert',
  props: {
    /** Error flag. True iff an external error has occurred. */
    value: { type: Boolean },

    /** The external error event*/
    errorMessage: {}
  },
  data () {
    return {
      /** Warning visibility flag. True iff a warning message is shown */
      showWarning: false,

      /** Warning title */
      warningTitle: '',

      /** Warning message */
      warningMessage: '',

      /** Warning icon */
      warningIcon: ''
    }
  },
  created () {
    window.addEventListener('resize', this.checkWindowSize)
  },
  destroyed () {
    window.removeEventListener('resize', this.checkWindowSize)
  },
  methods: {
    /** Reload the page */
    reloadPage () {
      window.location.reload()
    },

    /** Window size checker */
    checkWindowSize () {
      const windowWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth
      const screenSize = window.screen.width

      if (windowWidth <= 520) {
        const isSmallDevice = screenSize <= 520
        this.showWarning = true
        this.warningIcon =
          isSmallDevice
            ? 'mdi-phone-rotate-landscape'
            : 'mdi-arrow-expand-horizontal'
        this.warningTitle =
          isSmallDevice
            ? 'This device is too small'
            : 'Resize your browser window'
        this.warningMessage =
          isSmallDevice
            ? 'This device is too small to allow graphs and visualizations to be displayed clearly. Please rotate it or try a larger device.'
            : 'The window width is too small for graphs and visualizations to be displayed clearly. Please resize your browser window.'
      } else {
        this.showWarning = false
      }
    }
  },
  mounted () {
    this.checkWindowSize()
  }
}
</script>

<style scoped></style>
