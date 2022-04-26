import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  primary_color: '#014878',
  secondary_color: '#35B1ECFF',
  tertiary_color_light: '#D2ECF8FF',
  tertiary_color_dark: '#1976D2FF'
}

export default new Vuex.Store({
  state
})
