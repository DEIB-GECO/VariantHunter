<!--

  Component:    AppPreferences
  Description:  App preferences panel

-->

<template>
  <v-list rounded nav dense>
    <!-- Preferences opener -->
    <list-item icon="mdi-tune-variant" title="Preferences" link subtitle="App settings" expand-on-hover
               @click.native="showSettings=true"/>

    <!-- Preference panel -->
    <v-dialog v-model="showSettings" eager fullscreen hide-overlay transition="dialog-bottom-transition" scrollable>
      <v-card>

        <!-- Headings -->
        <v-toolbar flat dark color="f_primary" class="px-5">
          <v-toolbar-title class="font-weight-bold">Preferences</v-toolbar-title>
          <v-spacer/>
          <v-btn icon dark @click="showSettings = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <!-- List of preferences -->
        <v-card-text class="py-3">

          <!-- Appearance preferences-->
          <v-list thwo-line subheader>
            <v-subheader class="text-body-1">Appearance</v-subheader>
            <v-list-item>
              <v-list-item-icon>
                <v-icon left :color="darkTheme?'#bc7fbf':'#AB4AFF'">mdi-weather-night</v-icon>
              </v-list-item-icon>
              <v-list-item-content class="py-0 my-0">
                <v-list-item-title class="break-spaces">Dark theme</v-list-item-title>
                <v-list-item-subtitle class="break-spaces">Use the dark theme for the application
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch v-model="darkTheme" @change="autoDarkTheme=false" inset></v-switch>
              </v-list-item-action>
            </v-list-item>

            <v-list-item class="mt-2">
              <v-list-item-icon>
                <v-icon left color="#ff6e3e">mdi-lightbulb-auto-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content class="py-0 my-0">
                <v-list-item-title class="break-spaces">Automatically switch to dark theme</v-list-item-title>
                <v-list-item-subtitle class="break-spaces">Match the theme of the application with the one of the
                  system
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch v-model="autoDarkTheme" inset></v-switch>
              </v-list-item-action>
            </v-list-item>
          </v-list>

          <v-divider/>

          <!-- Information section -->
          <v-list thwo-line subheader>
            <v-subheader class="text-body-1">Information</v-subheader>
            <v-list-item>
              <v-list-item-icon>
                <v-icon left color="success">mdi-check-decagram</v-icon>
              </v-list-item-icon>
              <v-list-item-content class="py-0 my-0">
                <v-list-item-title class="break-spaces">Version {{ version }}</v-list-item-title>
                <v-list-item-subtitle class="break-spaces underlined-links">
                  <a href="https://github.com/DEIB-GECO/VariantHunter/releases" target="_blank">More about Variant
                    Hunter releases</a>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>

            <v-list-item>
              <v-list-item-icon>
                <v-icon left>mdi-bug</v-icon>
              </v-list-item-icon>
              <v-list-item-content class="py-0 my-0">
                <v-list-item-title class="break-spaces">Report a bug / Request a feature</v-list-item-title>
                <v-list-item-subtitle class="break-spaces underlined-links">
                  <a href="https://github.com/DEIB-GECO/VariantHunter/issues/new" target="_blank">Open issue on
                    GitHub</a>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-divider/>

          <!-- Keyboard shortcut info -->
          <v-list thwo-line subheader class="mt-5">
            <v-list-item>
              <v-list-item-icon>
                <v-icon left color="#ffbc00">mdi-keyboard-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content class="py-0 my-0">
                <v-list-item-title class="break-spaces">Keyboard shortcuts</v-list-item-title>
                <v-list-item-subtitle class="break-spaces underlined-links">
                  <v-row no-gutters>
                    <v-col cols="12" sm="6" md="4" lg="3" v-for="[id,{title, kbd}] in Object.entries(shortcuts)"
                           :key="id">
                      {{ title }}
                      <span class="ml-2"><span v-html="kbd[0]"/><v-icon small>mdi-plus</v-icon><span
                          v-html="kbd[1]"/></span>
                    </v-col>
                  </v-row>
                </v-list-item-subtitle>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <!-- Reset options-->
          <data-manager/>

        </v-card-text>

        <div style="flex: 1 1 auto;"/>
      </v-card>
    </v-dialog>

  </v-list>
</template>

<script>
import ListItem from "@/components/general/basic/ListItem"
import {shortcuts} from "@/utils/keyboardService";
import DataManager from "@/components/controls/DataManager";
import {mapMutations, mapState} from "vuex";

export default {
  name: "AppPreferences",
  components: {DataManager, ListItem},

  data() {
    return {
      /** Boolean visibility flag for the panel */
      showSettings: false,
    }
  },
  computed: {
    ...mapState(['version', 'darkMode','autoDarkMode']),

    /** Map shortcuts data */
    shortcuts() {
      return shortcuts
    },

    /** Dark theme option */
    darkTheme: {
      get() {
        return this.darkMode
      },
      set(newVal) {
        this.setState({name: 'darkMode', newVal})
      }
    },


    /** Auto dark theme option */
    autoDarkTheme: {
      get() {
        return this.autoDarkMode
      },
      set(newVal) {
        this.setState({name: 'autoDarkMode', newVal})
      }
    },
  },

  methods: {
    ...mapMutations(['setState']),
  },
}
</script>

<style scoped>

</style>