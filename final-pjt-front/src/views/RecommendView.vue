<template>
  <div>
    <h1>영화 추천</h1>
    
    <!-- 시간 선택 -->
    <div>
      <label for="time">시간: </label>
      <select v-model="selectedTime" id="time">
        <option value="" disabled>선택하세요</option>
        <option v-for="time in times" :key="time" :value="time">
          {{ time }}
        </option>
      </select>
    </div>

    <!-- 누구와 함께 선택 -->
    <div>
      <label for="with">누구랑: </label>
      <select v-model="selectedWith" id="with">
        <option value="" disabled>선택하세요</option>
        <option v-for="withOption in withOptions" :key="withOption" :value="withOption">
          {{ withOption }}
        </option>
      </select>
    </div>

    <!-- 장르 선택 -->
    <div>
      <label for="genre">장르: </label>
      <select v-model="selectedGenre" id="genre">
        <option value="" disabled>선택하세요</option>
        <option v-for="genre in genres" :key="genre.id" :value="genre.name">
          {{ genre.name }}
        </option>
      </select>
    </div>

    <!-- 추천 버튼 -->
    <button @click="getRecommendation">추천 받기</button>

    <!-- 추천 결과 -->
      <h2>추천 결과</h2>
      <div v-for="movie in recommendation">
        <p>추천 영화: {{ movie.title }}</p>
        <p>개요: {{ movie.overview }}</p>
        <img :src="getImageUrl(movie.poster_path)" alt="영화 포스터" class="movie-poster" />
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

  // API 요청
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
    },
  })
    .then((res) => {
      // console.log("영화 추천 성공:", res.data);
      recommendation.value = res.data;
      console.log(recommendation.value)
    })
    .catch((err) => {
      console.error("영화 추천 실패:", err);
      recommendation.value = {
        title: "추천 결과 없음",
        description: "영화 추천 요청 중 오류가 발생했습니다.",
        image: "https://via.placeholder.com/150?text=Error",
      };
    });
}
</script>

<style scoped>
div {
  margin: 10px;
}
label {
  margin-right: 5px;
}
select {
  margin-right: 10px;
}
button {
  margin-top: 10px;
}
.movie-poster {
  margin-top: 10px;
  width: 150px;
  height: 150px;
  object-fit: cover;
}
</style>
