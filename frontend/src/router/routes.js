import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import About from '../views/About.vue'
Vue.use(VueRouter)

export default new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/variant_hunter/',
      name: 'Home',
      component: Home
    },
    {
      path: '/variant_hunter/about',
      name: 'About',
      component: About
    },
    {
      path: '/:catchAll(.*)',
      name: 'ToHome',
      component: Home
    }
  ]
})
