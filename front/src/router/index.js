import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '@/views/index/Index.vue'
import Register from '@/views/register/Register.vue'
import NotFound from '@/views/notfound/NotFound.vue'
import Login from '@/views/login/Login.vue'
import Detail from '@/views/detail/Detail.vue'
import Category from '@/views/categroy/Category.vue'
import Search from '@/views/search/Search.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component:Index,
    alias: '/home',
  },
  {
    path:'/reg',
    name:'register',
    component:Register,
    alias: '/reg/',
  },
  {
    path:'/login',
    name:'login',
    component:Login,
    alias: '/login/',
  },
  {
    path:'/search',
    name:'news_search',
    component:Search,
    alias: '/search/',
  },
  {
    path:'/detail/:news_id',
    name:'news_detail',
    component:Detail,
  },
  {
    path:'/category/:category_id',
    name:'news_category',
    component:Category,
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
