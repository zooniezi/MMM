<template>
  <div class="logo-container">
    <img :src="logo" alt="Logo" width="150" />
  </div>
  <div class="login-container">
    <h1 class="login-title">로그인</h1>
    <form @submit.prevent="logIn" class="login-form">
      <label for="username" class="form-label">아이디</label>
      <input type="text" id="username" v-model.trim="username" class="form-input" placeholder="아이디를 입력하세요"><br>

      <label for="password" class="form-label">비밀번호</label>
      <input type="password" id="password" v-model.trim="password" class="form-input" placeholder="비밀번호를 입력하세요"><br>

      <input type="submit" value="로그인하기" class="form-button">
      <p class="sign-up-link">
        계정이 없으신가요? <span @click="goToSignUp" class="link">회원가입</span>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'
import logo from '@/assets/logo2.png'

// Router 및 상태 관리 초기화
const router = useRouter()
const store = useMovieStore()

// 로그인 폼 입력값
const username = ref('')
const password = ref('')

// 로그인 함수
const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }
  store.logIn(payload)
}

// 회원가입 페이지로 이동
const goToSignUp = function() {
  router.push({ name: 'signUp' })
}
</script>

<style scoped>
/* 로고를 중앙에 배치 */
.logo-container {
  display: flex;
  justify-content: center; /* 수평 중앙 */
  align-items: center; /* 수직 중앙 */
  height: 150px; /* 로고 컨테이너 높이 (적절히 조절 가능) */
  margin-bottom: 20px;
}

.login-container {
  max-width: 400px;
  margin: 0 auto; /* 수평 중앙 */
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  font-size: 24px;
  color: #FF5F00;
  margin-bottom: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.form-label {
  margin-bottom: 5px;
  font-size: 14px;
  color: #555;
}

.form-input {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  width: 100%;
  box-sizing: border-box;
}

.form-input:focus {
  border-color: #FF9F66;
  outline: none;
  box-shadow: 0 0 5px rgba(255, 162, 40, 0.5);
}

.form-button {
  padding: 10px;
  background-color: #FF9F66;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.form-button:hover {
  background-color: #FF5F00;
}

.sign-up-link {
  text-align: center;
  margin-top: 10px;
  font-size: 14px;
  color: #555;
}

.link {
  color: #FF9F66;
  cursor: pointer;
  text-decoration: underline;
}

.link:hover {
  color: #FF5F00;
}
</style>
