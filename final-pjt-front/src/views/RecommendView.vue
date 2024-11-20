<template>
  <div>
    <h1>영화 추천</h1>
    <div>
      <label for="place">시간: </label>
      <select v-model="selectedTime" id="time">
        <option value="" disabled>선택하세요</option>
        <option v-for="place in places" :key="place" :value="place">
          {{ place }}
        </option>
      </select>
    </div>

    <div>
      <label for="with">누구랑: </label>
      <select v-model="selectedWith" id="with">
        <option value="" disabled>선택하세요</option>
        <option v-for="withs in withOptions" :key="withs" :value="withs">
          {{ withs }}
        </option>
      </select>
    </div>

    <div>
      <label for="genre">장르: </label>
      <select v-model="selectedGenre" id="genre">
        <option value="" disabled>선택하세요</option>
        <option v-for="genre in genres" :key="genre" :value="genre">
          {{ genre }}
        </option>
      </select>
    </div>

    <button @click="getRecommendation">추천 받기</button>

    <div v-if="recommendation">
      <h2>추천 결과</h2>
      <p>추천 영화: {{ recommendation.title }}</p>
      <p>줄거리: {{ recommendation.description }}</p>
      <img :src="recommendation.image" alt="영화 포스터" class="movie-poster" />
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from "@/stores/movie";
import { ref } from "vue"

const store = useMovieStore()

// 데이터 정의
const places = ["집", "영화관", "야외"];
const withOptions = ["혼자", "가족", "친구", "연인"]; // 배열로 정의
const genres = ["액션", "코미디", "드라마", "스릴러", "애니메이션"];

// 추천 영화 데이터
const movies = [
  {
    title: "어벤져스",
    place: "영화관",
    with: "친구",
    genre: "액션",
    description: "슈퍼히어로들이 힘을 합쳐 세상을 구한다!",
    image: "https://via.placeholder.com/150?text=Avengers", // 영화 포스터 URL
  },
  {
    title: "업",
    place: "집",
    with: "가족",
    genre: "애니메이션",
    description: "모험을 떠나는 노인과 소년의 감동적인 이야기.",
    image: "https://via.placeholder.com/150?text=Up",
  },
  {
    title: "라라랜드",
    place: "야외",
    with: "연인",
    genre: "드라마",
    description: "꿈을 좇는 두 남녀의 사랑과 도전.",
    image: "https://via.placeholder.com/150?text=La+La+Land",
  },
  {
    title: "조커",
    place: "혼자",
    with: "혼자",
    genre: "스릴러",
    description: "한 남자의 비극적이고 충격적인 이야기.",
    image: "https://via.placeholder.com/150?text=Joker",
  },
  {
    title: "인사이드 아웃",
    place: "집",
    with: "가족",
    genre: "애니메이션",
    description: "감정이 의인화된 독창적인 애니메이션.",
    image: "https://via.placeholder.com/150?text=Inside+Out",
  },
];

// 선택 상태 관리
const selectedTime = ref("");
const selectedWith = ref("");
const selectedGenre = ref("");
const recommendation = ref(null);

// 추천 결과 함수
function getRecommendation() {
  recommendation.value = movies.find(
    (movie) =>
      movie.place === selectedTime.value &&
      movie.with === selectedWith.value &&
      movie.genre === selectedGenre.value
  );

  if (!recommendation.value) {
    recommendation.value = {
      title: "추천 결과 없음",
      description: "조건에 맞는 영화가 없습니다.",
      image: "https://via.placeholder.com/150?text=No+Image", // 기본 이미지
    };
  }

  const recommendMovie = function () {
    const payload = {
      watch_time: selectedTime.value,
      watch_with_who: selectedWith.value,
      genre_id: selectedGenre.value,
    }

    console.log(payload)

    axios({
      method: 'post',
      url: `${store.SERVER_API_URL}/movies/recommend`,
      headers: {
        Authorization: `Token ${store.serverToken}`,
        'Content-Type': 'application/json',
      },
      data: payload,
    })
      .then((res) => {
        console.log('영화 추천 성공:', res.data)
      })
      .catch((err) => {
        console.error('영화 추천 실패:', err)
      })
  }
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
