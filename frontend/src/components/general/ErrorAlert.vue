<!--
  Component:    ErrorAlert
  Description:  Error alert to be shown in case an error occurs

  Props:
  ├── errorMessage: The error event
  └── v-model:      Error flag. True iff an error has occurred.
-->

<template>
  <v-overlay :value='value'>
    <v-container>
      <v-alert
        dismissible
        elevation='24'
        type='error'
        @input='reloadPage()'
      >
        <b>The server is temporarily unreachable</b><br />
        An error occurred while contacting the server. Please try again later.<br /><br />
        Error details: <br />
        {{ errorMessage }}
      </v-alert>
    </v-container>
  </v-overlay>
</template>

<script>
export default {
  name: 'ErrorAlert',
  props: {
    /** Error flag. True iff an error has occurred. */
    value: { type: Boolean },

    /** The error event*/
    errorMessage: {}
  },
  methods: {
    /** Reload the page */
    reloadPage () {
      window.location.reload()
    }
  }
}
</script>

<style scoped></style>
