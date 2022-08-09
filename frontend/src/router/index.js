import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/:category',
    name: "category",
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    // route level code-splitting
    // this generates a separate chunk (login.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "login" */ '../views/LoginView.vue')
  },
  {
    path: '/register',
    name: 'register',
    // route level code-splitting
    // this generates a separate chunk (login.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "login" */ '../views/RegistrationView.vue')
  },
  {
    path: '/ideaForm',
    name: 'ideaForm',
    // route level code-splitting
    // this generates a separate chunk (login.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "login" */ '../views/IdeaFormView.vue')
  },
  {
    path: '/ideaForm/:ideaId',
    name: 'ideaFormUpdating',
    component: () => import('../views/IdeaFormView.vue')
  },
  {
    path: '/idea/:ideaId',
    name: 'idea',
    component: () => import('../views/IdeaView.vue')
  },
  {
    path: '/profile/:username',
    name: 'profile',
    component: () => import('../views/ProfileView.vue')
  },
  {
    path: '/updateProfile',
    name: 'updateProfile',
    component: () => import('../views/UpdateProfileView.vue')
  },
  {
    path: '/changePassword',
    name: 'changePassword',
    component: () => import('../views/ChangePasswordView.vue')
  },
  {
    path: '/chat',
    name: 'chat',
    component: () => import('../views/ChatView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
