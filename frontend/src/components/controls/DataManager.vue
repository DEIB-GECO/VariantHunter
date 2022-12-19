<!--

  Component:    DataManager
  Description:  Component to manage data storage.
                It includes commands to restart app tour, clear history or init the app

  Props:
  └── mode: Appearance of the component. Either 'full' or 'icon'.
            In 'icon' mode only clear history icon is shown.

-->

<template>
  <span>

    <!-- Full mode component: list of options -->
    <v-list v-if="mode==='full'" subheader>
      <v-list-item class="mt-5">
        <v-list-item-content>

          <!-- Restart app-tour option -->
          <div class="width-100 text-center">
            <v-btn outlined :color="restarted?'success':'error'" class="mb-2" @click="resetTour">
              <v-icon left :color="restarted?'success':'error'">{{restarted?'mdi-check-outline':'mdi-lightbulb-variant-outline'}}</v-icon>
              Restart app tour
            </v-btn>
          </div>

          <!-- Clear history option -->
          <div class="width-100 text-center">
            <v-btn outlined color="error" class="mb-2" @click="askConfirm('clear')">
              <v-icon left>mdi-trash-can-outline</v-icon>
              Clear analysis history
            </v-btn>
          </div>

          <!-- Init app option -->
          <div class="width-100 text-center">
            <v-btn outlined color="error" class="mb-2" @click="askConfirm('init')">
              <v-icon left>mdi-close-box</v-icon>
              Clear storage and initialize
            </v-btn>
          </div>

        </v-list-item-content>
      </v-list-item>
    </v-list>

    <!-- Icon mode component: icon to clear history only -->
    <icon-with-tooltip v-else hover-color="error" icon="mdi-trash-can-outline" bottom tip="Clear all analyses"
                       size="medium" :click-handler="()=>askConfirm('clear')"/>

    <!-- Confirmation popup: are you sure? -->
    <v-dialog v-model="confirmPopUp">
      <v-overlay v-if="popUp" v-model="confirmPopUp">
        <v-alert prominent type="error" icon="mdi-exclamation-thick" max-width="70vw" width="800px"
                 class="py-10 px-7 rounded-xl rounded-l-0 bg_var2 text_var1--text" border="left" colored-border>
          <div class="pl-4">
            <div class="text-h5 font-weight-bold">{{ popUp.title }}</div>
            <div class="text-body-1 mt-1 mb-6" v-html="popUp.subtitle"/>
          </div>
          <div class="text-right pl-4 mt-6">
            <v-btn rounded elevation="0" @click="confirmPopUp=false" class="mr-2 mb-2">No, go back</v-btn>
            <v-btn rounded elevation="0" color="error" class="mr-2 mb-2" @click="popUp.fn">Yes, proceed</v-btn>
          </div>
        </v-alert>
      </v-overlay>
    </v-dialog>

  </span>
</template>

<script>
import {mapActions, mapMutations} from "vuex";
import IconWithTooltip from "@/components/general/basic/IconWithTooltip";

export default {
  name: "DataManager",
  components: {IconWithTooltip},

  props: {
    /**
     * Appearance of the component. Either 'full' or 'icon'.
     * In 'icon' mode only clear history icon is shown.
     */
    mode: {default: 'full'},
  },

  data() {
    return {
      /** Boolean visibility flag for the confirmation popup */
      confirmPopUp: false,

      /** Popups config */
      popUps: {
        'init': {
          title: "Are you sure you want to initialize the app?",
          subtitle: "You will lose all your previous analyses data and preferences. <br/>The operation cannot be undone.<br/>The page will be reloaded.",
          fn: this.initApp,
        },
        'clear': {
          title: "Are you sure you want to clear previous analyses?",
          subtitle: "You will lose all your previous analyses data. </br> The operation cannot be undone.",
          fn: this.clearStorage,
        }
      },

      /** Flag set to true to show confirmation message for the app tour restart */
      restarted: false,

      /** Current popup config */
      popUp: undefined,
    }
  },

  methods: {
    ...mapActions(['clearHistory']),
    ...mapMutations(['resetState', 'setTourStep', 'setCurrentAnalysis']),

    /**
     * Show the confirmation popup associated with the specified id
     * @param id Id of the popup config to be shown
     */
    askConfirm(id) {
      this.confirmPopUp = true
      this.popUp = this.popUps[id]
    },

    /** Init app by resetting the state and reloading the page */
    initApp() {
      this.confirmPopUp = false
      this.resetState()
      location.reload()
    },

    /** Clear history */
    clearStorage() {
      this.confirmPopUp = false
      this.clearHistory()
    },

    /** Reset app tour */
    resetTour() {
      this.setTourStep('tour')
      this.setCurrentAnalysis(null)
      this.restarted=true
      setTimeout(()=>this.restarted=false, 3000)
    }

  }
}
</script>

<style scoped>

</style>