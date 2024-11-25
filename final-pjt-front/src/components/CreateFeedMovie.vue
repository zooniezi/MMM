<template>
  <div class="movie-search">
    <h2 class="my-font-size">{{ title }}</h2>
    <div class="input-group mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="영화 제목을 입력하세요"
        v-model="searchQuery"
        @keyup.enter="fetchMovies"
      />
      <button class="btn btn-primary" @click="fetchMovies">확인</button>
    </div>

    <div v-if="isLoading" class="text-center mt-3">
      <div class="spinner-border text-warning" role="status">
        <span class="visually-hidden">로딩 중...</span>
      </div>
    </div>
    <div v-else-if="movies.length" class="movie-list mt-4">
      <div class="row">
        <div
          class="col-sm-6 col-md-4 col-lg-3 mb-3"
          v-for="movie in movies"
          :key="movie.id"
          @click="goToMovieInfo(movie)"
        >
          <div class="card h-100">
            <img
              :src="getImageUrl(movie.poster_path)"
              :alt="movie.title"
              class="card-img-top movie-poster"
            />
            <div class="card-body text-center">
              <h5 class="card-title">{{ movie.title }}</h5>
              <p class="card-text">
                개봉: {{ movie.release_date?.slice(0, 4) || 'N/A' }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      v-else-if="!isLoading && movies.length === 0 && searchQuery.trim()"
      class="text-center mt-3"
    >
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const TMDB_TOKEN = import.meta.env.VITE_TMDB_TOKEN
const BASE_URL = 'https://api.themoviedb.org/3'

// 상태 관리
const searchQuery = ref('')
const movies = ref([])
const isLoading = ref(false)

// 제목 변경 상태 및 반복 로직
const title = ref('영화를 선택하세요')
const titles = ['영화를 선택하세요', '영화를 선택하세요.', '영화를 선택하세요..', '영화를 선택하세요...']
let titleIndex = 0
let intervalId

const updateTitle = () => {
  title.value = titles[titleIndex]
  titleIndex = (titleIndex + 1) % titles.length
}

onMounted(() => {
  intervalId = setInterval(updateTitle, 1000) // 0.5초 간격으로 변경
})

onUnmounted(() => {
  clearInterval(intervalId)
})

// 이미지 URL 생성
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
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
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.movie-poster {
  height: 300px;
  object-fit: contain;
  background-color: rgb(0, 0, 0);
}

.card {
  background-color: #f9f9f9;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.my-font-size {
  font-size: 1rem;
}
</style>
