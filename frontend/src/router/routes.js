import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../components/views/HomeView.vue'
import About from '../components/views/About.vue'
import store from '../store/store.js'
import LinkTo from "@/components/views/LinkTo.vue";

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
            path: '/linkTo',
            name: 'LinkTo',
            component: LinkTo
        },
        {
            path: '/:catchAll(.*)',
            name: 'ToHome',
            component: HomeView
        }
    ]
})

/**
 * When the app opens show global loading util restore has been completed
 */
router.beforeEach(async (to, from, next) => {
    store.commit('setLoading',true)
    store.restored.then(()=>{store.commit('setLoading',false)})
    next();
});

export default router;
