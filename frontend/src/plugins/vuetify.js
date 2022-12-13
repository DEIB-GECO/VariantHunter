import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'

Vue.use(Vuetify)

const vuetify = new Vuetify({
  theme: {
    themes: {
      light: {
        // fixed color
        f_primary: '#014878',
        f_secondary: '#35B1EC',
        f_tertiary: '#D2ECF8',
        f_accent: '#1976D2',
        f_text_light: '#FFFFFF',
        f_text_dark: '#1E1E1E',

        // text colors
        text_var1: '#1E1E1E',
        text_var2: '#FFFFFF',
        text_var3: '#808080',

        // background colors
        bg_var1:'#D2ECF8',
        bg_var2:'#FFFFFF',
        bg_var3:'#FFFFFF',

        // dynamic color
        primary: '#014878',
        secondary: '#35B1EC',
        tertiary: '#D2ECF8',
        accent: '#1976D2',
      },
      dark: {
        // fixed color
        f_primary: '#014878',
        f_secondary: '#35B1EC',
        f_tertiary: '#D2ECF8',
        f_accent: '#1976D2',
        f_text_light: '#FFFFFF',
        f_text_dark: '#1E1E1E',

        // text colors
        text_var1: '#FFFFFF',
        text_var2: '#1E1E1E',
        text_var3: '#FFFFFF',

        // background colors
        bg_var1:'#33383A',
        bg_var2:'#33383A',
        bg_var3:'#D2ECF8',

        // dynamic color
        primary: '#D2ECF8',
        secondary: '#35B1EC',
        tertiary: '#014878',
        accent: '#1976D2',
      }
    },
    options: { customProperties: true },
  },
})

export default vuetify
