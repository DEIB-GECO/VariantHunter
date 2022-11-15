import Vue from 'vue'
import './plugins/axios'
import router from './router/routes.js'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import store from './store/store'
import VueClipboard from 'vue-clipboard2'
import './styles/style.css'

Vue.config.productionTip = false

new Vue({
  vuetify,
  store,
  router,
  render: (h) => h(App)
}).$mount('#app')

Vue.use(VueClipboard)
