import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

export const useMovieStore = defineStore('movie', () => {
  const SERVER_API_URL = 'http://127.0.0.1:8000'
  const serverToken = ref(null)
  const userName = ref(null)
  const userId = ref(null) // userId 상태

  const isLogin = computed(() => {
    return serverToken.value !== null
  })

  const router = useRouter()

  // 회원가입 요청 액션
  const signUp = function (payload) {
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${SERVER_API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then(() => {
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        if (err.response && err.response.status === 400) {
          if (err.response.data.username) {
            alert("이미 존재하는 아이디입니다.")
          }
          if (err.response.data.password1) {
            const passwordErrors = err.response.data.password1
            if (passwordErrors.includes('This password is too common.')) {
              alert("너무 흔한 비밀번호입니다.")
            }
            if (passwordErrors.includes('This password is too short. It must contain at least 8 characters.')) {
              alert("비밀번호는 최소 8자 이상이어야 합니다.")
            }
          }
          if (err.response.data.non_field_errors) {
            alert("두 비밀번호가 일치하지 않습니다. 다시 입력해주세요.")
          }
        }
      })
  }

  // 로그인 요청 액션
  const logIn = function (payload) {
    const { username, password } = payload

    axios({
      method: 'post',
      url: `${SERVER_API_URL}/accounts/login/`,
      data: {
        username, password
      }
    })
      .then((res) => {
        serverToken.value = res.data.key
        userName.value = username
        router.push({ name: 'home' })
        // 로그인 후 사용자 ID 가져오기
        fetchUserId()
      })
      .catch((err) => {
        if (err.response && err.response.status === 400) {
          alert("아이디 또는 비밀번호가 올바르지 않습니다. 다시 확인해주세요.")
        }
      })
  }

  // 로그아웃 요청 액션
  const logOut = function () {
    axios({
      method: 'post',
      url: `${SERVER_API_URL}/accounts/logout/`,
    })
      .then(() => {
        serverToken.value = null
        userName.value = null
        userId.value = null
        router.push({ name: 'logIn' })
      })
      .catch((err) => {
        console.error(err)
      })
  }

  let isFetching = false // 중복 호출 방지 플래그

  const fetchUserId = async function () {
    if (!userName.value || !serverToken.value) {
      console.error('UserName or ServerToken is not set. Cannot fetch userId.')
      return
    }

    if (userId.value !== null || isFetching) {
      console.log('UserId is already fetched or fetching is in progress.')
      return
    }

    isFetching = true
    try {
      const res = await axios({
        method: 'get',
        url: `${SERVER_API_URL}/accounts/userinfo/${userName.value}/`,
        headers: {
          Authorization: `Token ${serverToken.value}`,
        },
      })
      if (res.data && res.data.id) {
        userId.value = res.data.id
        console.log('Fetched UserId:', userId.value)
      } else {
        console.error('Invalid response structure:', res.data)
      }
    } catch (err) {
      console.error('Failed to fetch UserId:', err)
    } finally {
      isFetching = false
    }
  }

  return { 
    SERVER_API_URL, 
    serverToken, 
    isLogin, 
    userName, 
    userId, 
    signUp, 
    logIn, 
    logOut, 
    fetchUserId,
  }
}, { persist: true })
