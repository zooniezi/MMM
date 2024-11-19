import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'
import { useRouter } from 'vue-router'

// axios.defaults.xsrfCookieName = 'csrftoken'
// axios.defaults.xsrfHeaderName = 'X-CSRFToken'

export const useMovieStore = defineStore('movie', () => {
  const SERVER_API_URL = 'http://127.0.0.1:8000'
  const serverToken = ref(null)

  const isLogin = computed(() => {
    if (serverToken.value === null) {
      return false
    } else {
      return true
    }
  })
  const router = useRouter()

  // 회원가입 요청 액션
  const signUp = function (payload) {
    // const username = payload.username
    // const password1 = payload.password1
    // const password2 = payload.password2
    const { username, password1, password2 } = payload

    axios({
      method: 'post',
      url: `${SERVER_API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        // console.log(res)
        // console.log('회원가입 성공')
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        if (err.response && err.response.status === 400) {
          console.log(err.response)
          console.log(err.response.data)
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
        router.push({ name: 'home' })
      })
      .catch((err) => {
        if (err.response && err.response.status === 400) {
          alert("아이디 또는 비밀번호가 올바르지 않습니다. 다시 확인해주세요.")
        }
      })
  }
  
  // [추가기능] 로그아웃
  const logOut = function () {
    axios({
      method: 'post',
      url: `${SERVER_API_URL}/accounts/logout/`,
    })
      .then((res) => {
        console.log(res.data)
        serverToken.value = null
        router.push({ name: 'logIn' })
      })
      .catch((err) => {
        console.log(err)
      })
  }

  return { SERVER_API_URL, serverToken, isLogin, signUp, logIn, logOut }
})
