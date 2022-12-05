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
            path: '/',
            name: 'Home',
            component: HomeView
        },
        {
            path: '/about',
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
