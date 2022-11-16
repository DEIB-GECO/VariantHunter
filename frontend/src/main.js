import Vue from 'vue'
import axios from 'axios';
import router from './router/routes.js'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import store from './store/store'
import VueClipboard from 'vue-clipboard2'
import './styles/style.css'
import { publicPath } from '../vue.config'
import { cacheAdapterEnhancer, throttleAdapterEnhancer } from 'axios-extensions';

Vue.config.productionTip = false


// enhance the original axios adapter with throttle and cache enhancer
Vue.prototype.$axios = axios.create({
	baseURL: publicPath + 'api/',
	headers: { 'Cache-Control': 'no-cache' },
    adapter: throttleAdapterEnhancer(cacheAdapterEnhancer(axios.defaults.adapter))
});

new Vue({
  vuetify,
  store,
  router,
  render: (h) => h(App)
}).$mount('#app')

Vue.use(VueClipboard)
