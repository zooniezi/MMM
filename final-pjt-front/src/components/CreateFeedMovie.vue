<template>
  <div class="movie-search">
    <h2>영화 검색</h2>
    <input
      type="text"
      placeholder="영화 제목을 입력하세요"
      v-model="searchQuery"
      @input="fetchMovies"
    />
    <div v-if="movies.length" class="movie-list">
      <ul>
        <li v-for="movie in movies" :key="movie.id" @click="goToMovieInfo(movie)">
          <img
            :src="getImageUrl(movie.poster_path)"
            :alt="movie.title"
            class="movie-poster"
          />
          <p>{{ movie.title }} ({{ movie.release_date?.slice(0, 4) || 'N/A' }})</p>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const TMDB_TOKEN = import.meta.env.VITE_TMDB_TOKEN
const BASE_URL = 'https://api.themoviedb.org/3'

const searchQuery = ref('')
const movies = ref([])

const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w200${path}`
    : 'https://via.placeholder.com/200x300?text=No+Image'
}

const fetchMovies = async () => {
  if (searchQuery.value.trim() === '') {
    movies.value = []
    return
  }

  try {
    const response = await axios.get(`${BASE_URL}/search/movie`, {
      headers: {
        Authorization: `Bearer ${TMDB_TOKEN}`,
      },
      params: {
        query: searchQuery.value,
        language: 'ko-KR',
      },
    })
    movies.value = response.data.results
  } catch (error) {
    console.error('영화 검색 실패:', error)
    movies.value = []
  }
}

const goToMovieInfo = (movie) => {
  router.push({
    name: 'createFeedInfo',
    params: { id: movie.id }, // ID 전달
    state: { movie }, // 영화 객체를 state로 전달
  })
}
</script>

<style scoped>
/* 스타일은 필요에 따라 추가 */
</style>
