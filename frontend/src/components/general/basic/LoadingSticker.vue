<template>
  <v-snackbar max-width="500px" v-model="showSnackbar" :timeout="isLoading?'-1':(error?'10000':'10000')"
              :color="isLoading?'secondary':(error?'error':'')">
    <v-list class="text-left transparent tip rounded-xl white--text " two-line>
      <v-list-item class="justify-center">
        <v-list-item-icon>
          <v-progress-circular v-if="isLoading" class="mr-4" indeterminate/>
          <v-icon v-if="error">mdi-exclamation-thick</v-icon>
        </v-list-item-icon>
        <v-list-item-content>
          <v-list-item-title class="font-weight-bold">
            {{ isLoading ? 'Please wait...' : (error?'An error occurred while contacting the server. Try again.':'') }}
          </v-list-item-title>
          <v-list-item-subtitle>{{ isLoading ? loadingMessage : (error?('Details: ' + error):'') }}</v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
    </v-list>
    <v-btn v-if="error" rounded small text v-bind="attrs" @click="showSnackbar = false">
        Hide
    </v-btn>
  </v-snackbar>

</template>

<script>
export default {
  name: 'LoadingSticker',
  props: {
    isLoading: {},

    error: {},

    /** loadingMessages: 4 loading messages to show*/
    loadingMessages: {default: []},
  },
  data() {
    return {
      showSnackbar: false,
      /** timers: array of active timers */
      timers: [],
      loadingMessage: undefined,
    }
  },
  watch: {
    error(newVal) {
      this.showSnackbar = newVal!==undefined
    },
    isLoading(newVal) {
      if(newVal){
        this.showSnackbar = true
        this.setTimers()
      }else{
        this.showSnackbar= this.error!==undefined
      }
    }
  },
  methods:{
    setTimers(){
      if (this.loadingMessages.length > 0) {
      this.loadingMessage = this.loadingMessages[0].text
      for (let loadingMessage of this.loadingMessages.slice(1))
        this.timers.push(window.setTimeout(() => {
          this.loadingMessage = loadingMessage.text
        }, loadingMessage.time))
      }
    },
    removeTimers(){
      this.timers.forEach(timer => clearTimeout(timer))
    }
  },
  /**
   * Remove timers
   */
  unmounted() {
    this.removeTimers()
  }
}
</script>

<style>
/** Prevent vuetify line breaks */
.tip .v-list-item__title {
  font-size: 0.875rem;
  line-height: 1rem;
  white-space: initial !important;
  font-weight: 600;
}

/** Higher opacity values for the subtitle*/
.tip .v-list-item__subtitle {
  opacity: initial;
}
</style>