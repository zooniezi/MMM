<template>
  <div class="movie-info">
    <h2>{{ movie.title }}</h2>
    <img :src="getImageUrl(movie.poster_path)" :alt="movie.title" />
    <p><strong>개봉일:</strong> {{ movie.release_date }}</p>
    <p><strong>평점:</strong> {{ movie.vote_average }}</p>
    <p><strong>줄거리:</strong> {{ movie.overview }}</p>
    <button @click="goBack">뒤로 가기</button>
  </div>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 전달된 영화 데이터 가져오기
const movie = route.state.movie || {}

// 이미지 경로 처리
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w300${path}`
    : 'https://via.placeholder.com/300x450?text=No+Image'
}

// 뒤로 가기
const goBack = () => {
  router.push({ name: 'createFeedMovie' }) // 영화 검색 화면으로 이동
}
</script>

<style scoped>
/* 스타일은 필요에 따라 추가 */
</style>
