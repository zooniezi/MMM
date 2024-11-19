<template>
  <div>
    <h1>Create Feed</h1>
    <router-view /> <!-- 자식 라우트를 렌더링 -->
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router' // vue-router에서 useRouter 가져오기

const router = useRouter() // router 객체 정의

// 예시: 특정 동작을 위해 router 사용 가능
console.log(router.currentRoute.value)
</script>

<style scoped>
/* 필요하면 스타일 추가 */
</style>