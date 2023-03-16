// router.js
const routes = [
  {
    path: '/',
    component: () => import('@/pages/Home.vue'),
  },
  {
    path: '/user',
    component: () => import('@/pages/User.vue'),    
  },
  {
    path: '/admin',
    component: () => import('@/pages/Admin.vue'),
  },
]

import { createRouter, createWebHistory } from 'vue-router'
export default createRouter({
  history: createWebHistory(),
  routes
})