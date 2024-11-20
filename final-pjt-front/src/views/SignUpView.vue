<template>
  <div class="signup-container">
    <p class="login-link">
      이미 계정이 있으신가요? <RouterLink to="{ name: 'logIn' }" class="link">로그인</RouterLink>
    </p>
    <h1 class="signup-title">회원가입</h1>
    <form @submit.prevent="signUp" class="signup-form">
      <label for="username" class="form-label">아이디</label>
      <input type="text" id="username" v-model.trim="username" class="form-input" placeholder="아이디를 입력하세요"><br>

      <label for="password1" class="form-label">비밀번호</label>
      <input type="password" id="password1" v-model.trim="password1" class="form-input" placeholder="비밀번호를 입력하세요"><br>

      <label for="password2" class="form-label">비밀번호 확인</label>
      <input type="password" id="password2" v-model.trim="password2" class="form-input" placeholder="비밀번호를 다시 입력하세요"><br>
      
      <input type="submit" value="회원가입하기" class="form-button">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { RouterLink } from 'vue-router';

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)

const store = useMovieStore()

const signUp = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value
  }
  store.signUp(payload)
}
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.signup-title {
  text-align: center;
  font-size: 24px;
  color: #FF9F66;
  margin-bottom: 20px;
}

.login-link {
  text-align: center;
  font-size: 14px;
  margin-bottom: 10px;
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

.signup-form {
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
</style>
