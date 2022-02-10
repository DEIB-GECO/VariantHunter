import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const state = {
    toolbar_color: '#014878',
    menu_color: 'rgb(53,177,236)',
    background_card_color: '#014878',
    all_geo: [],
    all_lineages: [],
};

const getters = {

};

const mutations = {
    setAllGeo: (state, value) => {
        state.all_geo = value;
    },
    setAllLineages: (state, value) => {
        state.all_lineages = value;
    },
};

const actions = {

};

export default new Vuex.Store({
    state,
    getters,
    mutations,
    actions
})
