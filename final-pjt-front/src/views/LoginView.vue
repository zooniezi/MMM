<template>
  <div class="login-container">
    <h1 class="login-title">로그인</h1>
    <form @submit.prevent="logIn" class="login-form">
      <label for="username" class="form-label">아이디: </label>
      <input type="text" id="username" v-model.trim="username" class="form-input"><br>

      <label for="password" class="form-label">비밀번호: </label>
      <input type="password" id="password" v-model.trim="password" class="form-input"><br>

      <input type="submit" value="로그인하기" class="submit-button">
      <p>
        <span class="signup-link" @click="goToSignUp">계정이 없으신가요?</span>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref(null)
const password = ref(null)

const store = useMovieStore()

const logIn = function () {
  const payload = {
    username: username.value,
    password: password.value
  }

  store.logIn(payload)
}

// SignUp 페이지로 이동
const goToSignUp = () => {
  router.push({ name: 'signUp' })
}
</script>

<style scoped>

</style>
