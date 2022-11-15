import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../components/views/HomeView.vue'
import About from '../components/views/About.vue'
Vue.use(VueRouter)

export default new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/variant_hunter',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/variant_hunter/about',
      name: 'About',
      component: About
    },
    {
      path: '/:catchAll(.*)',
      name: 'ToHome',
      component: HomeView
    }
  ]
})
