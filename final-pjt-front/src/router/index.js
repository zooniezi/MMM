import { createRouter, createWebHistory } from 'vue-router'
import { useMovieStore } from '@/stores/movie'

import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import CreateFeedView from '@/views/CreateFeedView.vue'
import EditUserView from '@/views/EditUserView.vue'
import RecommendView from '@/views/RecommendView.vue'
import SearchUserView from '@/views/SearchUserView.vue'
import MyPageView from '@/views/MyPageView.vue'
import UserDetailView from '@/views/UserDetailView.vue'

import CreateFeedMovie from '@/components/CreateFeedMovie.vue'
import CreateFeedInfo from '@/components/CreateFeedInfo.vue'


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
      name: 'logIn',
      component: LoginView,
    },
    {
      path: '/signup',
      name: 'signUp',
      component: SignUpView,
    },
    {
      path: '/create-feed',
      // name: 'createFeed',
      component: CreateFeedView,
      children: [
        {
          path: '',
          name: 'createFeed',
          component: CreateFeedMovie,
        },
        {
          path: 'info/:id',
          name: 'createFeedInfo',
          component: CreateFeedInfo,
        },
      ],
    },
    {
      path: '/edit-user',
      name: 'editUser',
      component: EditUserView,
    },
    {
      path: '/recommend',
      name: 'recommend',
      component: RecommendView,
    },
    {
      path: '/search-user',
      name: 'searchUser',
      component: SearchUserView,
    },
    {
      path: '/my-page',
      name: 'myPage',
      component: MyPageView,
    },
    {
      path: '/user/:id',
      name: 'userDetail',
      component: UserDetailView,
    },
  ]
})

// 비로그인/로그인 기준 페이지 접근 제한 기능(완료)
router.beforeEach((to, from, next) => {
  const store = useMovieStore()
  const isAuthenticated = store.isLogin

  const publicPages = ['logIn', 'signUp']
  const authRequired = !publicPages.includes(to.name)

  if (authRequired && !isAuthenticated) {
    return next({ name: 'logIn' })
  }

  if ((to.name === 'logIn' || to.name === 'signUp') && isAuthenticated) {
    return next({ name: 'home' })
  }
  next()
})

export default router

