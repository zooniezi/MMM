import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import { useMovieStore } from '@/stores/movie'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'root',
      redirect: '/login',
    },
    {
      path: '/home',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUpView,
    },
  ]
})

router.beforeEach((to) => {
  const store = useMovieStore()
  const isAuthenticated = store.isLogin // 로그인 여부 확인

  // 보호된 경로: 인증이 필요
  if (to.name === 'home' && !isAuthenticated) {
    return { name: 'login' }
  }

  // 로그인 상태에서는 로그인/회원가입 페이지로 접근 차단
  if ((to.name === 'login' || to.name === 'signup') && isAuthenticated) {
    return { name: 'home' }
  }
})

export default router

