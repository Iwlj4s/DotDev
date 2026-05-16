import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import Profile from '@/pages/Profile.vue'
import Login from '@/pages/Login.vue'
import AuthCallback from '@/pages/AuthCallback.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/profile/:id?', name: 'profile', component: Profile, props: true },
  { path: '/login', name: 'login', component: Login },
  { path: '/auth/callback', name: 'auth-callback', component: AuthCallback },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
