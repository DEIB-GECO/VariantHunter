import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex);

const state = {
    primary_color: '#014878',
    secondary_color: '#35B1ECFF',
    toolbar_color: '#014878',
    menu_color: 'rgb(53,177,236)',
    background_card_color: '#014878',
    all_locations: [],
    all_lineages: [],
};

const getters = {

};

const mutations = {
    setAllLocations: (state, value) => {
        state.all_locations = value;
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
