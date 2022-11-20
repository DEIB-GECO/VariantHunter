import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../components/views/HomeView.vue'
import About from '../components/views/About.vue'
import store from '../store/store.js'

Vue.use(VueRouter)

const router = new VueRouter({
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

router.beforeEach(async (to, from, next) => {
    store.commit('setLoading',true)
    store.restored.then(()=>{store.commit('setLoading',false)})
    next();
});

export default router;
