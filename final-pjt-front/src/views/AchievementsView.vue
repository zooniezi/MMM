<template>
  <div>
    <h1 class="page-title">도전과제</h1>
    

    <!-- 도전과제 진행률 -->
    <div class="progress-section">
      <p>도전과제 진행률</p>
      <div class="progress-bar-container">
        <div class="progress-bar" :style="{ width: progressRate + '%' }"></div>
      </div>
      <p>{{ achievedCount }} / {{ achievements.length }} ({{ progressRate }}%)</p>
    </div>

    <!-- 도전과제 리스트 -->
    <div class="my-section">
      <ul class="achievement-list">
        <li
          v-for="(achievement, index) in achievements"
          :key="index"
          :class="{ achieved: achievement.achieved, unachieved: !achievement.achieved }"
        >
          <!-- 뱃지 이미지 -->
          <img
            :src="achievement.image"
            alt="뱃지"
            class="achievement-badge"
            :class="{ grayscale: !achievement.achieved }"
          />
          <!-- 도전과제 제목 및 설명 -->
          <div class="achievement-details">
            <p class="achievement-title" :class="{ grayscale: !achievement.achieved }">{{ achievement.title }}</p>
            <p class="achievement-description" :class="{ grayscale: !achievement.achieved }">{{ achievement.description }}</p>
          </div>
          <!-- 달성 여부 -->
          <span v-if="achievement.achieved" class="achievement-good">
            달성 완료
          </span>
          <span v-if="!achievement.achieved" class="achievement-bad">
            미달성
          </span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import axios from 'axios';
import { computed, onMounted, ref } from 'vue';


const store = useMovieStore()

// 진행률 계산
const achievedCount = computed(() => achievements.value.filter(a => a.achieved).length);
const progressRate = computed(() => Math.round((achievedCount.value / achievements.value.length) * 100));

// 도전과제 데이터
const achievements = ref([
  {
    image: "./src/assets/achievements/01_first.png",
    title: "산뜻한 출발",
    description: "첫 피드를 작성합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/02_aim.png",
    title: "저격수다!",
    description: "작성한 피드에 10개 이상의 이모지를 받습니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/03_4-seasons.png",
    title: "모든 날 모든 순간",
    description: "봄,여름,가을,겨울에 영화를 시청했습니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/04_alone.png",
    title: "아무 일도 없었다...",
    description: "혼자 10편의 영화를 감상했습니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/05_lover.png",
    title: "자기야 이건 누구랑 본거야?",
    description: "연인과 함께 10편의 영화를 감상했습니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/06_blacksmith.png",
    title: "할 말을 잃었습니다",
    description: "영화를 100편 등록했습니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/07_shovel.png",
    title: "난 누군가 또 여긴 어딘가",
    description: "아무도 등록하지 않았던 영화를 피드에 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/08.png",
    title: "범인은 이 안에 있어",
    description: "피드에 '미스터리' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/09.png",
    title: "주먹이 운다",
    description: "피드에 '액션' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/10.png",
    title: "세상의 전부를 그곳에 두고 왔다",
    description: "피드에 '어드벤처' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/11.png",
    title: "미안하다 이거 보여주려고 어그로 끌었다",
    description: "피드에 '애니메이션' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/12.png",
    title: "삐에론 우릴 보고 웃지",
    description: "피드에 '코미디' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/13.png",
    title: "너 내가 누군지 아니",
    description: "피드에 '범죄' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/14.png",
    title: "예능이 아니라 다큐인데요",
    description: "피드에 '다큐멘터리' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/15.png",
    title: "연극이 끝난 후",
    description: "피드에 '드라마' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/16.png",
    title: "즐거운 나의 집",
    description: "피드에 '가족' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/17.png",
    title: "마술 하나 보여줄까?",
    description: "피드에 '판타지' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/18.png",
    title: "내가 왕이 될 상인가",
    description: "피드에 '역사' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/19.png",
    title: "어떻게 지평좌표계로 고정하셨죠?",
    description: "피드에 '공포' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/20.png",
    title: "방금 락스타 되는 상상함",
    description: "피드에 '음악' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/21.png",
    title: "당신의 눈동자에 건배",
    description: "피드에 '로맨스' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/22.png",
    title: "엄마는 외계인",
    description: "피드에 'SF' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/23.png",
    title: "텔레비전에 내가 나왔으면 정말 좋겠네",
    description: "피드에 'TV 영화' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/24.png",
    title: "슉 슈슉... 슈슉 슉... 슉 슉 슈슉",
    description: "피드에 '스릴러' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/25.png",
    title: "36계 줄행랑",
    description: "피드에 '전쟁' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/26.png",
    title: "황야의 무법자",
    description: "피드에 '서부' 장르의 영화를 10개 등록합니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/27.png",
    title: "평점이 이븐하게 익지 않았어요",
    description: "부여할 수 있는 모든 평점을 등록했습니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/28.png",
    title: "국가권력급 영화광",
    description: "영화를 1000편 등록했습니다.",
    achieved: false,
  },
  {
    image: "./src/assets/achievements/29.png",
    title: "말 그대로 궁극의 유저!",
    description: "모든 도전과제를 달성했습니다.",
    achieved: false,
  },
]);

const achievementsData = ref([])

const processAchievement = function () {
  for (let i = 0; i < achievementsData.value.length; i++) {
    const idx = achievementsData.value[i].achievement_id - 1
    achievements.value[idx].achieved = true
  }
}


const fetchAchievement = async () => {
  try {
    const response = await axios.get(
      `${store.SERVER_API_URL}/achievements/get/${store.userId}/`,
      { headers: { Authorization: `Token ${store.serverToken}` } }
    );
    achievementsData.value = response.data;
    console.log(achievementsData.value)
    processAchievement();
  } catch (err) {
    console.error("도전과제 데이터 가져오기 실패:", err);
  }
};

onMounted(() => {
  fetchAchievement();
});

</script>

<style scoped>
.my-section {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.achievement-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.achievement-list li {
  display: flex;
  align-items: center;
  padding: 20px;
  margin-bottom: 10px;
  background-size: cover;
  background-position: center;
  border-radius: 10px;
  transition: transform 0.2s;
}

/* 뱃지 이미지 */
.achievement-badge {
  width: 80px;
  height: 80px;
  object-fit: contain;
  margin-right: 15px;
}

/* 미달성 뱃지 흑백 처리 */
.achievement-badge.grayscale {
  filter: grayscale(100%);
}

.achievement-title.grayscale {
  opacity: 70%;
}

.achievement-details {
  flex: 1;
}

.achievement-title {
  font-size: 18px;
  font-weight: bold;
  margin: 0;
}

.achievement-description {
  font-size: 14px;
  color: #333;
  margin: 5px 0 0;
}

.achievement-good {
  font-size: 16px;
  color: #fff; /* 글씨 색상 흰색 */
  background-color: #28a745; /* 초록색 배경 */
  padding: 5px 10px; /* 텍스트 주위 여백 */
  border-radius: 5px; /* 약간의 둥근 모서리 */
  display: inline-block; /* 텍스트를 감싸는 형태로 설정 */
}

.achievement-bad {
  font-size: 16px;
  color: #fff; /* 글씨 색상 흰색 */
  background-color: #dc3545; /* 빨간색 배경 */
  padding: 5px 10px; /* 텍스트 주위 여백 */
  border-radius: 5px; /* 약간의 둥근 모서리 */
  display: inline-block; /* 텍스트를 감싸는 형태로 설정 */
}

.progress-section {
  margin: 20px 0;
  text-align: center;
}

.progress-bar-container {
  width: 100%;
  background-color: #ddd;
  border-radius: 10px;
  overflow: hidden;
  height: 20px;
  margin: 10px 0;
}

.progress-bar {
  height: 100%;
  background-color: #28a745;
  transition: width 0.3s ease;
}
</style>
