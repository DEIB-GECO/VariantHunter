<template>
  <v-list rounded nav dense>
    <list-item icon="mdi-tune-variant" title="Preferences" link subtitle="App settings" expand-on-hover
               @click.native="showSettings=true"/>

    <v-dialog v-model="showSettings" fullscreen hide-overlay transition="dialog-bottom-transition" scrollable>
      <v-card>
        <v-toolbar flat dark color="f_primary" class="px-5">
          <v-toolbar-title class="font-weight-bold">Preferences</v-toolbar-title>
          <v-spacer/>
          <v-btn icon dark @click="showSettings = false">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-toolbar>

        <v-divider/>

        <v-card-text class="py-3">
          <v-list thwo-line subheader>
            <v-subheader class="text-body-1">Appearance</v-subheader>
            <v-list-item>
              <v-list-item-icon>
                <v-icon left>mdi-weather-night</v-icon>
              </v-list-item-icon>
              <v-list-item-content class="py-0 my-0">
                <v-list-item-title class="break-spaces">Dark theme</v-list-item-title>
                <v-list-item-subtitle class="break-spaces">Use the dark theme for the application</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch v-model="darkTheme" inset></v-switch>
              </v-list-item-action>
            </v-list-item>

             <v-list-item class="mt-2">
              <v-list-item-icon>
                <v-icon left>mdi-lightbulb-auto-outline</v-icon>
              </v-list-item-icon>
              <v-list-item-content class="py-0 my-0">
                <v-list-item-title class="break-spaces">Automatically switch to dark theme</v-list-item-title>
                <v-list-item-subtitle class="break-spaces">Match the theme of the application with the one of the system</v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-action>
                <v-switch v-model="autoDarkTheme" inset></v-switch>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card-text>

        <div style="flex: 1 1 auto;"></div>
      </v-card>
    </v-dialog>

  </v-list>
</template>

<script>
import ListItem from "@/components/general/basic/ListItem";

export default {
  name: "AppPreferences",
  components: {ListItem},
  data() {
    return {
      showSettings: false,

      autoDarkTheme:true,

    }
  },
  computed: {
    darkTheme: {
      get() {
        return this.$vuetify.theme.dark
      },
      set() {
        this.$vuetify.theme.dark = !this.$vuetify.theme.dark
      }
    }

  },
  methods: {
    toggleTheme(evt) {
      if(this.autoDarkTheme) {
        this.$vuetify.theme.dark = evt.matches
      }
    },
  },

  /**
   * Listen for external dark mode changes
   */
  mounted() {
    const matcher = window.matchMedia('(prefers-color-scheme: dark)')
    matcher.addEventListener('change', this.toggleTheme)
    this.toggleTheme(matcher)
  }
}
</script>

<style scoped>

</style>