<template>
  <div v-if="isLoading" class="loading">영화 정보를 불러오는 중...</div>
  <div v-else-if="movie">
    <h2>{{ movie.title }}</h2>
    <img
      :src="getImageUrl(movie.poster_path)"
      :alt="movie.title"
      class="movie-poster"
    />
    <p><strong>개봉일:</strong> {{ movie.release_date }}</p>
    <p><strong>평점:</strong> {{ movie.vote_average }}</p>
    <p><strong>줄거리:</strong> {{ movie.overview || '내용 없음' }}</p>
    <button @click="goBack">뒤로 가기</button>
  </div>
  <div v-else class="error">영화 정보를 불러올 수 없습니다.</div>

  <div>
    <label for="dropdown">Select an option:</label>
    <select id="dropdown" v-model="selectedOption">
      <option value="option1">Option 1</option>
      <option value="option2">Option 2</option>
      <option value="option3">Option 3</option>
    </select>
    <p>You selected: {{ selectedOption }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie'

const store = useMovieStore()

const route = useRoute()
const router = useRouter()
const movieId = route.params.id // 동적 라우트 ID

const TMDB_TOKEN = import.meta.env.VITE_TMDB_TOKEN
const BASE_URL = 'https://api.themoviedb.org/3'

const movie = ref(null) // 영화 정보
const isLoading = ref(true) // 로딩 상태
const userId = ref(null)
let movieGenres = {}

// 이미지 URL 생성
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : 'https://via.placeholder.com/500x750?text=No+Image'
}



const getUserId = function () {
  axios({
    method: 'get',
    url: `${store.SERVER_API_URL}/accounts/userinfo/${store.userName}/`,
    headers: {
      Authorization: `Token ${store.serverToken}`, // 인증 토큰 추가
    },
  })
    .then((res) => {
      // console.log(res.data)
      userId.value = res.data.id
      // console.log(userId.value)
    })
    .catch((err) => {
      console.error('유저 정보를 가져오는 데 실패했습니다:', err)
    })
}

// 영화 정보 API 호출
const fetchMovieDetails = async (id) => {
  try {
    const response = await axios.get(`${BASE_URL}/movie/${id}`, {
      headers: {
        Authorization: `Bearer ${TMDB_TOKEN}`,
      },
      params: {
        language: 'ko-KR',
      },
    })
    movie.value = response.data
    console.log(movie.value)
    movieGenres.value = movie.value.genres.map((genre) => genre.id)
    console.log('영화 장르:', movieGenres.value)
  } catch (error) {
    console.error('영화 정보 불러오기 실패:', error)
    movie.value = null
  } finally {
    isLoading.value = false
  }
}

// 뒤로 가기
const goBack = () => {
  router.back()
}

const watchData = ref(null)

const addFeed = function () {
  const payload = {
    user_id: userId.value,
    movie_id: movieId.value,
    genre_ids: movieGenres.value,
    watch_date: watchData.value,
    // watch_time: ,
    // watch_place: ,
    // watch_with_who: ,
    // watch_reason: ,
    // rating: ,
    // comment: ,
    // is_share_to_feed: ,
  }
  axios({
      method: 'post',
      url: `${SERVER_API_URL}/accounts/signup/`,
      data: {
        username, password1, password2
      }
    })
      .then((res) => {
        // console.log(res)
        // console.log('회원가입 성공')
        const password = password1
        logIn({ username, password })
      })
      .catch((err) => {
        console.log(err)
      })
}

// 컴포넌트 마운트 시 데이터 로드
onMounted(() => {
  getUserId()
  if (movieId) {
    fetchMovieDetails(movieId)
  } else {
    isLoading.value = false
  }
})
</script>


<style scoped>

</style>
