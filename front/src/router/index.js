import Vue from 'vue'
import VueRouter from 'vue-router'
import app from '../App.vue'
import Register from '@/views/register/Register.vue'
import NotFound from '@/views/notfound/NotFound.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component:app
  },
  {
    path:'/reg',
    name:'register',
    component:Register
  },
  {
    path: '/*', 
    component: NotFound
  },
]

const router = new VueRouter({
  mode:"history",
  base:process.env.BASE_URL,
  routes
})

export default router
