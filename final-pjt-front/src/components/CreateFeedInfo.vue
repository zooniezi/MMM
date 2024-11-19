<template>
  <!-- 단계별 폼 -->
  <form @submit.prevent="addFeed">
    <div v-if="currentStep === 1">
      <label for="watch_date">시청 날짜:</label>
      <input type="date" id="watch_date" v-model="watchDate" />
      <button type="button" @click="nextStep">다음</button>
    </div>
    <!-- 시청 시간 -->
    <div v-if="currentStep === 2">
      <label>시청 시간:</label>
      <div>
        <label>
          <input type="radio" value="morning" v-model="watchTime" />
          오전
        </label>
        <label>
          <input type="radio" value="afternoon" v-model="watchTime" />
          오후
        </label>
        <label>
          <input type="radio" value="evening" v-model="watchTime" />
          저녁
        </label>
        <label>
          <input type="radio" value="night" v-model="watchTime" />
          밤
        </label>
      </div>
      <button type="button" @click="previousStep">이전</button>
      <button type="button" @click="nextStep">다음</button>
    </div>

    <!-- 시청 장소 -->
    <div v-if="currentStep === 3">
      <label>시청 장소:</label>
      <div>
        <label>
          <input type="radio" value="movie_theater" v-model="watchPlace" />
          영화관
        </label>
        <label>
          <input type="radio" value="home" v-model="watchPlace" />
          집
        </label>
        <label>
          <input type="radio" value="friend_home" v-model="watchPlace" />
          친구 집
        </label>
        <label>
          <input type="radio" value="other" v-model="watchPlace" />
          기타
        </label>
      </div>
      <button type="button" @click="previousStep">이전</button>
      <button type="button" @click="nextStep">다음</button>
    </div>

    <!-- 함께 본 사람 -->
    <div v-if="currentStep === 4">
      <label>함께 본 사람:</label>
      <div>
        <label>
          <input type="radio" value="alone" v-model="watchWithWho" />
          혼자
        </label>
        <label>
          <input type="radio" value="family" v-model="watchWithWho" />
          가족
        </label>
        <label>
          <input type="radio" value="friend" v-model="watchWithWho" />
          친구
        </label>
        <label>
          <input type="radio" value="lover" v-model="watchWithWho" />
          연인
        </label>
        <label>
          <input type="radio" value="other" v-model="watchWithWho" />
          기타
        </label>
      </div>
      <button type="button" @click="previousStep">이전</button>
      <button type="button" @click="nextStep">다음</button>
    </div>
    
    <div v-if="currentStep === 5">
      <label>시청 이유:</label>
      <div>
        <label><input type="checkbox" value="재미있을 것 같아서" v-model="watchReason" /> 재미있을 것 같아서</label>
        <label><input type="checkbox" value="추천을 받아서" v-model="watchReason" /> 추천을 받아서</label>
        <label><input type="checkbox" value="좋아하는 배우가 나와서" v-model="watchReason" /> 좋아하는 배우가 나와서</label>
        <label><input type="checkbox" value="좋아하는 영화감독이라" v-model="watchReason" /> 좋아하는 영화감독이라</label>
        <label><input type="checkbox" value="기타" v-model="watchReason" /> 기타</label>
      </div>
      <button type="button" @click="previousStep">이전</button>
      <button type="button" @click="nextStep">다음</button>
    </div>

    <!-- 평점 -->
    <div v-if="currentStep === 6">
      <label>평점:</label>
      <div>
        <label>
          <input type="radio" value="1" v-model.number="rating" />
          1점
        </label>
        <label>
          <input type="radio" value="2" v-model.number="rating" />
          2점
        </label>
        <label>
          <input type="radio" value="3" v-model.number="rating" />
          3점
        </label>
        <label>
          <input type="radio" value="4" v-model.number="rating" />
          4점
        </label>
        <label>
          <input type="radio" value="5" v-model.number="rating" />
          5점
        </label>
      </div>
      <button type="button" @click="previousStep">이전</button>
      <button type="button" @click="nextStep">다음</button>
    </div>
  
    <div v-if="currentStep === 7">
      <label for="comment">한줄 평:</label>
      <textarea id="comment" placeholder="영화에 대한 한줄 평을 입력하세요" v-model="comment"></textarea>
      <button type="button" @click="previousStep">이전</button>
      <button type="button" @click="nextStep">다음</button>
    </div>
  
    <div v-if="currentStep === 8">
      <label for="is_share_to_feed">
        <input
          type="checkbox"
          id="is_share_to_feed"
          v-model="isShareToFeed"
        />
        피드를 공유하시겠습니까?
      </label>
      <button type="button" @click="previousStep">이전</button>
      <button type="submit">저장</button>
    </div>
  </form>

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

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie'

const store = useMovieStore()
const route = useRoute()
const router = useRouter()
const movieId = route.params.id

const TMDB_TOKEN = import.meta.env.VITE_TMDB_TOKEN
const BASE_URL = 'https://api.themoviedb.org/3'

const movie = ref(null)
const isLoading = ref(true)
const userId = ref(null)
const movieGenres = ref([])

// 단계별 폼 관리
const currentStep = ref(1) // 현재 단계

// 입력 상태
const watchDate = ref(null)
const watchTime = ref('')
const watchPlace = ref('')
const watchWithWho = ref('')
const watchReason = ref([])
const rating = ref(0)
const comment = ref('')
const isShareToFeed = ref(false)

// 이미지 URL 생성
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : 'https://via.placeholder.com/500x750?text=No+Image'
}

// 사용자 ID 가져오기
const getUserId = function () {
  axios({
    method: 'get',
    url: `${store.SERVER_API_URL}/accounts/userinfo/${store.userName}/`,
    headers: {
      Authorization: `Token ${store.serverToken}`,
    },
  })
    .then((res) => {
      userId.value = res.data.id
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
    movieGenres.value = movie.value.genres.map((genre) => genre.id)
  } catch (error) {
    console.error('영화 정보 불러오기 실패:', error)
    movie.value = null
  } finally {
    isLoading.value = false
  }
}

// 단계 이동
const nextStep = () => {
  if (currentStep.value < 8) currentStep.value++
}
const previousStep = () => {
  if (currentStep.value > 1) currentStep.value--
}

// 뒤로 가기
const goBack = () => {
  router.back()
}

// 피드 추가
const addFeed = function () {
  const payload = {
    user_id: userId.value,
    movie_id: movieId,
    genre_ids: movieGenres.value,
    watch_date: watchDate.value,
    watch_time: watchTime.value,
    watch_place: watchPlace.value,
    watch_with_who: watchWithWho.value,
    watch_reason: watchReason.value,
    rating: rating.value,
    comment: comment.value,
    is_share_to_feed: isShareToFeed.value,
  }

  axios({
    method: 'post',
    url: `${store.SERVER_API_URL}/feeds/`,
    headers: {
      Authorization: `Token ${store.serverToken}`,
    },
    data: payload,
  })
    .then((res) => {
      console.log('피드 추가 성공:', res.data)
      router.push('/feeds')
    })
    .catch((err) => {
      console.error('피드 추가 실패:', err)
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
.loading,
.error {
  text-align: center;
  margin-top: 20px;
  font-size: 18px;
  color: #999;
}

form {
  margin-top: 20px;
}

input,
select,
textarea {
  width: 100%;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  margin: 10px 5px;
  padding: 10px 20px;
  background-color: #42b883;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #358a6b;
}
</style>
