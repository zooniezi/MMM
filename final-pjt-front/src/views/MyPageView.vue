<template>
  <div>
    <h1>마이페이지</h1>
    <p>총 피드수: {{ totalFeeds }}</p>
    <p>팔로워 수: {{ followerCount }}</p>
    <p>팔로잉 수: {{ followingCount }}</p>
  </div>

  <div>
    <p>햄버거 바 구현해야 함</p>
    <RouterLink :to="{ name: 'editUser' }">editUser</RouterLink>
    <button @click="goLogOut">로그아웃</button>
  </div>

</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie'
import { RouterLink } from 'vue-router'

const store = useMovieStore()
const SERVER_API_URL = store.SERVER_API_URL

// 유저 정보 및 상태 변수
const totalFeeds = ref(0)
const followerCount = ref(0)
const followingCount = ref(0)

const feeds = ref([])
const userList = ref([])
const showList = ref(null)

const goLogOut = function () {
  store.logOut()
}

</script>

<style scoped>

</style>
