<template>
  <div>
    <h1>로그인</h1>
    <form @submit.prevent="logIn">
      <label for="username">username: </label>
      <input type="text" id="username" v-model.trim="username"><br>

      <label for="password">password: </label>
      <input type="password" id="password" v-model.trim="password"><br>

      <input type="submit" value="logIn">
      <p>
        <span class="signup-link" @click="goToSignUp">새 계정을 만드시겠어요?</span>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router';

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
.signup-link {
  color: blue;
  cursor: pointer;
}
.signup-link:hover {
  color: darkblue;
}
</style>