<template>
  <div>
    <div v-if="isLoading && !noOverlay" class="v-overlay__scrim" style="opacity: 0.46; background-color: rgb(33, 33, 33); border-color: rgb(33, 33, 33);"></div>

    <v-snackbar v-if="!standalone" max-width="500px" v-model="showSnackbar"
                :timeout="isLoading?'-1':'9000'"
                :color="isLoading?'warning': (error?'error':'')">
      <v-list class="text-left transparent tip rounded-xl white--text " two-line>
        <v-list-item class="justify-center">
          <v-list-item-icon class="text-center ma-auto mr-8" >
            <v-progress-circular v-if="isLoading" indeterminate/>
            <v-icon v-if="error">mdi-exclamation-thick</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="font-weight-bold break-spaces">
              {{
                isLoading ? 'Please wait...' : (error ? errorTitle : '')
              }}
            </v-list-item-title>
            <v-list-item-subtitle class="break-spaces">{{
                isLoading ? loadingMessage : (error ? (errorBody) : '')
              }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>
      <div class="text-center" v-if="error">
        <v-btn rounded small text @click="showSnackbar = false">Hide</v-btn>
      </div>
    </v-snackbar>

    <v-list v-else class="text-left transparent tip rounded-xl white--text mx-5" two-line>
        <v-list-item class="justify-center">
          <v-list-item-icon class="text-center ma-auto mr-8">
            <v-progress-circular v-if="isLoading" color="warning" indeterminate/>
            <v-icon v-if="error">mdi-exclamation-thick</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title class="font-weight-bold break-spaces">
              {{
                isLoading ? 'Please wait...' : (error ? errorTitle : '')
              }}
            </v-list-item-title>
            <v-list-item-subtitle class="break-spaces">{{
                isLoading ? loadingMessage : (error ? (errorBody) : '')
              }}
            </v-list-item-subtitle>
          </v-list-item-content>
        </v-list-item>
      </v-list>

  </div>

</template>

<script>
export default {
  name: 'LoadingSticker',
  props: {
    noOverlay: Boolean,
    isLoading: {default: false},
    standalone: Boolean(false),
    error: {default: undefined},


    /** loadingMessages: 4 loading messages to show*/
    loadingMessages: {default:()=>[]},
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
      this.showSnackbar = newVal !== undefined
    },
    isLoading(newVal) {
      if (newVal) {
        this.showSnackbar = true
        this.setTimers()
      } else {
        this.showSnackbar = this.error !== undefined
      }
    }
  },
  computed:{
    errorTitle(){
      if(this.error===423)
        return 'Dataset update in progress'
      else
        return 'An error occurred while contacting the server.'
    },

     errorBody(){
      if(this.error===423)
        return 'Sorry, we are updating the dataset. This operation may take some time. Please try again later.'
      else
        return this.error
    }
  },
  methods: {
    setTimers() {
      if (this.loadingMessages.length > 0) {
        this.loadingMessage = this.loadingMessages[0].text
        for (let loadingMessage of this.loadingMessages.slice(1))
          this.timers.push(window.setTimeout(() => {
            this.loadingMessage = loadingMessage.text
          }, loadingMessage.time))
      }
    },
    removeTimers() {
      this.timers.forEach(timer => clearTimeout(timer))
    }
  },
  /**
   * Add timers
   */
  mounted() {
    this.showSnackbar=this.isLoading || this.error

    if(this.standalone || this.isLoading)
      this.setTimers()
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