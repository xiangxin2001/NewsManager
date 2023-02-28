import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '@/views/index/Index.vue'
import Register from '@/views/register/Register.vue'
import NotFound from '@/views/notfound/NotFound.vue'
import Login from '@/views/login/Login.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component:Index
  },
  {
    path:'/reg',
    name:'register',
    component:Register
  },
  {
    path:'/login',
    name:'login',
    component:Login
  },
  {
    path: '/*', 
    component: NotFound
  }
]

const router = new VueRouter({
  mode:"history",
  base:process.env.BASE_URL,
  routes
})

export default router
