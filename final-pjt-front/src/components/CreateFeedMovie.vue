<template>
  <div class="movie-search">
    <h2>영화 검색</h2>
    <input
      type="text"
      placeholder="영화 제목을 입력하세요"
      v-model="searchQuery"
    />
    <button @click="fetchMovies">확인</button>

    <div v-if="isLoading">로딩 중...</div>
    <div v-else-if="movies.length" class="movie-list">
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
    <div v-else-if="!isLoading && movies.length === 0 && searchQuery.trim()">
      검색 결과가 없습니다.
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

// 상태 관리
const searchQuery = ref('') // 입력값
const movies = ref([]) // 검색 결과
const isLoading = ref(false) // 로딩 상태

// 이미지 URL 생성
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w200${path}`
    : 'https://via.placeholder.com/200x300?text=No+Image'
}

// 검색 API 호출
const fetchMovies = async () => {
  if (!searchQuery.value.trim()) {
    alert('검색어를 입력해주세요.')
    return
  }

  isLoading.value = true
  try {
    const response = await axios.get(`${BASE_URL}/search/movie`, {
      headers: {
        Authorization: `Bearer ${TMDB_TOKEN}`,
      },
      params: {
        query: searchQuery.value.trim(),
        language: 'ko-KR',
      },
    })
    movies.value = response.data.results
  } catch (error) {
    console.error('영화 검색 실패:', error)
    movies.value = []
  } finally {
    isLoading.value = false
  }
}

// 상세 페이지 이동
const goToMovieInfo = (movie) => {
  if (!movie || !movie.id) {
    console.error('유효하지 않은 영화 데이터:', movie)
    return
  }

  router.push({
    name: 'createFeedInfo',
    params: { id: movie.id },
  })
}
</script>



<style scoped>
.movie-search {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

input {
  width: 80%;
  padding: 10px;
  margin-top: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  margin-left: 10px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #358a6b;
}

.movie-list {
  margin-top: 20px;
}

.movie-poster {
  width: 100px;
  height: 150px;
  object-fit: cover;
}

li {
  list-style: none;
  cursor: pointer;
  margin: 10px 0;
  transition: background-color 0.2s ease;
}

li:hover {
  background-color: #f0f0f0;
}
</style>


