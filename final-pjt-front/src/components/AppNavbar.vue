<script setup>
import { RouterLink } from 'vue-router'
import logo from '@/assets/logo.jpg'
</script>

<template>
  <nav>
    <img :src="logo" alt="Logo" width="100" />
    <RouterLink :to="{ name: 'home' }">홈</RouterLink> |
    <RouterLink :to="{ name: 'createFeed' }">피드 생성</RouterLink> |
    <RouterLink :to="{ name: 'editUser' }">회원정보 수정</RouterLink> |
    <RouterLink :to="{ name: 'recommend' }">영화 추천</RouterLink> |
    <RouterLink :to="{ name: 'searchUser' }">유저 찾기</RouterLink> |
    <RouterLink :to="{ name: 'myPage' }">마이페이지</RouterLink>
  </nav>
</template>
