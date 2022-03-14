import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const state = {
  primary_color: '#014878',
  secondary_color: '#35B1ECFF',
  debug_mode: false // If set to true, it automatically performs search with standard parameters
}

const getters = {}

const mutations = {}

const actions = {}

export default new Vuex.Store({
  state,
  getters,
  mutations,
  actions
})
