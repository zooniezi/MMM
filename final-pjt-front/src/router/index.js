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
      name: 'createFeed',
      component: CreateFeedView,
      children: [
        {
          path: '',
          name: 'createFeedMovie',
          component: CreateFeedMovie, // 기본 화면: 영화 검색
        },
        {
          path: 'info/:id',
          name: 'createFeedInfo',
          component: CreateFeedInfo, // 상세 화면: 영화 정보
          props: true, // 라우트 파라미터를 props로 전달
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

router.beforeEach((to) => {
  const store = useMovieStore()
  const isAuthenticated = store.isLogin // 로그인 여부 확인

  // 보호된 경로 설정: 로그인과 회원가입 페이지를 제외한 모든 페이지
  const publicPages = ['logIn', 'signUp']
  const authRequired = !publicPages.includes(to.name)

  if (authRequired && !isAuthenticated) {
    return { name: 'logIn' }
  }

  // 로그인 상태에서는 로그인/회원가입 페이지로 접근 차단
  if ((to.name === 'logIn' || to.name === 'signUp') && isAuthenticated) {
    return { name: 'home' }
  }
})

export default router

