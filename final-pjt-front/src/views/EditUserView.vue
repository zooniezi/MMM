<template>
  <div>
    <h1 class="page-title">회원정보 수정</h1>
    <button class="delete-button" @click="deleteUser">회원 탈퇴</button>
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
.page-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.delete-button {
  background-color: #ff4d4f; /* 경고를 주는 빨간색 */
  color: #ffffff; /* 글씨를 흰색으로 */
  border: none; /* 기본 테두리 제거 */
  padding: 10px 20px; /* 여백 추가 */
  font-size: 16px; /* 버튼 글씨 크기 */
  font-weight: bold; /* 글씨 굵게 */
  border-radius: 5px; /* 모서리를 둥글게 */
  cursor: pointer; /* 클릭 가능하게 */
  transition: background-color 0.3s ease; /* 색상 변화 애니메이션 */
}

.delete-button:hover {
  background-color: #d9363e; /* 더 진한 빨간색으로 변경 */
}

.delete-button:active {
  background-color: #b71c1c; /* 클릭 시 더 어두운 색 */
}
</style>
