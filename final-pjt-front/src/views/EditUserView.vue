<template>
  <div>
    <h1>회원 정보 수정</h1>
    <button @click="deleteUser">회원 탈퇴</button>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import axios from 'axios'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const router = useRouter()
const store = useMovieStore()

const deleteUser = () => {
  const SERVER_API_URL = store.SERVER_API_URL

  if (confirm("정말로 회원 탈퇴를 진행하시겠습니까?")) {
    axios({
      method: 'delete',
      url: `${SERVER_API_URL}/accounts/delete/`,
      headers: {
        Authorization: `Token ${store.serverToken}` // 인증 토큰 전달
      }
    })
      .then(() => {
        alert("회원 탈퇴가 완료되었습니다.")
        store.serverToken = null // 토큰 제거
        router.push({ name: 'logIn' }) // 로그인 페이지로 리다이렉트
      })
      .catch((err) => {
        console.error(err.response)
        alert("회원 탈퇴 중 문제가 발생했습니다.")
      })
  }
}

</script>

<style scoped>

</style>