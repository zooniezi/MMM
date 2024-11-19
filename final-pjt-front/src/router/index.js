import { createRouter, createWebHistory } from 'vue-router'
import { useMovieStore } from '@/stores/movie'

import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import SignUpView from '@/views/SignUpView.vue'
import CreateFeedView from '@/views/CreateFeedView.vue'
import EditUserView from '@/views/EditUserView.vue'
import RecommendView from '@/views/RecommendView.vue'
import SearchFriendView from '@/views/SearchFriendView.vue'
import MyPageView from '@/views/MyPageView.vue'

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
      // name: 'createFeed', // 이름 추가
      component: CreateFeedView,
      children: [
        {
          path: '', // 기본 자식 라우트
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
      path: '/search-friend',
      name: 'searchFriend',
      component: SearchFriendView,
    },
    {
      path: '/my-page',
      name: 'myPage',
      component: MyPageView,
    },
  ]
})

router.beforeEach((to, from, next) => {
  console.log('네비게이션 가드 실행됨:', to.name)
  const store = useMovieStore()
  const isAuthenticated = store.isLogin

  const publicPages = ['logIn', 'signUp']
  const authRequired = !publicPages.includes(to.name)

  if (authRequired && !isAuthenticated) {
    console.log('로그인 필요:', to.name)
    return next({ name: 'logIn' })
  }

  if ((to.name === 'logIn' || to.name === 'signUp') && isAuthenticated) {
    console.log('이미 로그인 상태:', to.name)
    return next({ name: 'home' })
  }

  next()
})

export default router

