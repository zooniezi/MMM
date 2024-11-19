<template>
  <div>
    <h1>Create Feed</h1>
    <RouterView />
  </div>
</template>

<script setup>
import { RouterView, useRouter } from 'vue-router'

const router = useRouter() // router 객체 정의

// 예시: 특정 동작을 위해 router 사용 가능
console.log(router.currentRoute.value)
</script>

<style scoped>
/* 필요하면 스타일 추가 */
</style>