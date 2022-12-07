import Vue from 'vue'
import Vuex from 'vuex'
import {state} from '@/store/state'
import {getters} from "@/store/getters";
import {mutations} from "@/store/mutations";
import {actions} from "@/store/actions";
import VuexPersistence from 'vuex-persist';
import localForage from 'localforage';
import {version} from '../../package.json';

/**
 * Set the store object to be persistent
 * @type {VuexPersistence<unknown>}
 */
const vuexLocal = new VuexPersistence({
    /**
     * Function to be called whenever a store data is updated
     * @param val       Current store obj
     * @returns {{}|*}  Next store obj
     */
    reducer(val) {
        // Reset storage if reset flag or new version of the app
        if (val.reset || val.version !== version) {
            return {}
        }
        return val
    },
    storage: localForage,
    asyncStorage: true,
});

Vue.use(Vuex);

export default new Vuex.Store({
    state,
    mutations,
    getters,
    actions,
    plugins: [vuexLocal.plugin],
})

