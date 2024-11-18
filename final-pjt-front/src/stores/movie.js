import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios'

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

  return { SERVER_API_URL, serverToken, isLogin }
})
