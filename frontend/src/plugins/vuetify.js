import Vue from 'vue'
import Vuetify from 'vuetify/lib/framework'

Vue.use(Vuetify)

const vuetify = new Vuetify({
  theme: {
    themes: {
      light: {
        primary: '#014878',
        secondary: '#35B1EC',
        tertiary: '#D2ECF8',
        accent: '#1976D2',
      },
    },
  },
})

export default vuetify
