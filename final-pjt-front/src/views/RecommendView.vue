<template>
  <div class="game-style-container">
    <h1 class="page-title">영화 추천</h1>
    
    <!-- 시간 선택 -->
    <div class="option-section">
      <h2>⏰ 시간을 선택하세요!</h2>
      <div class="option-buttons">
        <button 
          v-for="time in times" 
          :key="time" 
          :class="{ selected: selectedTime === time }"
          @click="selectedTime = time"
        >
          {{ time }}
        </button>
      </div>
    </div>

    <!-- 누구와 함께 선택 -->
    <div class="option-section">
      <h2>👥 누구랑 보시나요?</h2>
      <div class="option-buttons">
        <button 
          v-for="withOption in withOptions" 
          :key="withOption" 
          :class="{ selected: selectedWith === withOption }"
          @click="selectedWith = withOption"
        >
          {{ withOption }}
        </button>
      </div>
    </div>

    <!-- 장르 선택 -->
    <div class="option-section">
      <h2>🎭 장르를 선택하세요!</h2>
      <div class="option-buttons">
        <button 
          v-for="genre in genres" 
          :key="genre.id" 
          :class="{ selected: selectedGenre === genre.name }"
          @click="selectedGenre = genre.name"
        >
          {{ genre.name }}
        </button>
      </div>
    </div>

    <!-- 최소 평점 선택 -->
    <div class="option-section">
      <h2>⭐ 어떤 영화를 원하시나요?</h2>
      <div class="rating-slider">
        <input 
          type="range" 
          min="1" 
          max="5" 
          step="1" 
          v-model="selectedRating"
        />
        <p v-if="selectedRating === '1'">사람들의 평가? 신경 쓰지 않고 가볍게 볼래요!</p>
        <p v-if="selectedRating === '2'">적당히 괜찮은 영화면 충분해요!</p>
        <p v-if="selectedRating === '3'">사람들이 재미있다고 추천한 영화를 보고 싶어요!</p>
        <p v-if="selectedRating === '4'">평점이 높은, 믿고 볼 수 있는 영화를 원해요!</p>
        <p v-if="selectedRating === '5'">최고의 평가를 받은 명작만 보고 싶어요!</p>
      </div>
    </div>

    <!-- 추천 버튼 -->
    <div class="action-section">
      <button class="recommend-button" @click="getRecommendation">🎲추천 받기</button>
    </div>

    <!-- 추천 결과 -->
    <div v-if="recommendation" class="result-section">
      <h2>🎥 추천 결과</h2>
      <div class="movie-card" v-for="movie in recommendation" :key="movie.id">
        <div class="movie-foster">
          <img :src="getImageUrl(movie.poster_path)" alt="영화 포스터" class="movie-poster" />
        </div>
        <div class="movie-info">
          <h3>{{ movie.title }}</h3>
          <p>평점: {{ movie.vote_average }}</p>
          <p v-if="movie.overview !== 'nan'">개요: {{ movie.overview }}</p>
          <p v-if="movie.overview === 'nan'">개요: 없음</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import axios from "axios"
import { useMovieStore } from "@/stores/movie"

// Store 초기화
const store = useMovieStore()
const userId = store.userId

// 선택 옵션 데이터
const times = ["오전", "오후", "저녁", "밤"]
const withOptions = ["혼자", "가족", "친구", "연인", "기타"]
const genres = [
  { name: "코미디", id: 35 },
  { name: "범죄", id: 80 },
  { name: "다큐멘터리", id: 99 },
  { name: "드라마", id: 18 },
  { name: "가족", id: 10751 },
  { name: "판타지", id: 14 },
  { name: "역사", id: 36 },
  { name: "호러", id: 27 },
  { name: "음악", id: 10402 },
  { name: "미스터리", id: 9648 },
  { name: "로맨스", id: 10749 },
  { name: "SF", id: 878 },
  { name: "TV 영화", id: 10770 },
  { name: "스릴러", id: 53 },
  { name: "전쟁", id: 10752 },
  { name: "서부극", id: 37 },
]

// 선택 상태 관리
const selectedTime = ref("");
const selectedWith = ref("");
const selectedGenre = ref("");
const selectedRating = ref(0);
const recommendation = ref(null);

// 이미지 경로
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : 'https://via.placeholder.com/500x750?text=No+Image'
}

// 추천 결과 함수
function getRecommendation() {
  const genreId = genres.find((genre) => genre.name === selectedGenre.value)?.id;

  axios({
    method: "get",
    url: `${store.SERVER_API_URL}/movies/recommend/`,
    headers: {
      Authorization: `Token ${store.serverToken}`,
      "Content-Type": "application/json",
    },
    params: {
      user_id: userId,
      watch_time: selectedTime.value,
      watch_with_who: selectedWith.value,
      genre_id: genreId,
      selected_rating: selectedRating.value,
    },
  })
    .then((res) => {
      recommendation.value = res.data;
    })
    .catch((err) => {
      console.error("영화 추천 실패:", err);
    });
}
</script>

<style scoped>
.game-style-container {
  text-align: center;
  color: #333;
}

.option-section {
  margin: 20px 0;
}

.option-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}

button {
  background-color: #f0f0f0;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #fdb84f;
  transform: scale(1.05);
}

button.selected {
  background-color: #fdb84f;
  font-weight: bold;
}

.recommend-button {
  background-color: #ffa200;
  color: white;
  font-size: 1rem;
  border: none;
  border-radius: 10px;
  padding: 15px 30px;
}

.result-section {
  margin-top: 30px;
}

.movie-card {
  color: black;
  display: flex;
  align-items: center;
  justify-content: start;
  gap: 20px;
  margin: 20px auto;
  padding: 20px;
  border-radius: 15px;
  max-width: 700px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: #f0f0f0;
}

.movie-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.movie-poster {
  width: 120px;
  height: 180px;
  object-fit: cover;
  border-radius: 10px;
  background-color: #000;
  transition: transform 0.3s ease;
}

.movie-poster:hover {
  transform: scale(1.1);
}

.movie-info {
  text-align: left;
}

h3 {
  margin: 0;
  font-size: 1.5rem;
}

p {
  margin: 5px 0 0;
}

h2 {
  font-size: 1.2rem;
}

/* 스타일 추가 */
.rating-slider {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 10px 0;
}

.rating-slider input[type="range"] {
  width: 60%;
  margin: 10px 0;
}

.rating-slider p {
  margin: 0;
  font-size: 1rem;
}
</style>
