import Vue from 'vue'
import Vuex from 'vuex'
import {state} from '@/store/state'
import {getters} from "@/store/getters";
import {mutations} from "@/store/mutations";
import {actions} from "@/store/actions";
import VuexPersistence from 'vuex-persist';
import localForage from 'localforage';

const vuexLocal = new VuexPersistence({
    reducer (val) {
      if(val.reset) {
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

