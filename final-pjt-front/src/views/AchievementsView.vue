<template>
  <div>
    <h1 class="page-title">도전과제</h1>

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
            <p class="achievement-title">{{ achievement.title }}</p>
            <p class="achievement-description">{{ achievement.description }}</p>
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
import { ref } from 'vue';

// 도전과제 데이터
const achievements = ref([
  {
    image: "https://picsum.photos/100?random=1",
    title: "첫 도전",
    description: "첫 번째 도전과제를 성공적으로 달성했습니다.",
    achieved: true,
  },
  {
    image: "https://picsum.photos/100?random=2",
    title: "연속 도전",
    description: "연속으로 3일 동안 도전과제를 달성했습니다.",
    achieved: false,
  },
  {
    image: "https://picsum.photos/100?random=3",
    title: "고급 도전",
    description: "난이도 높은 도전과제를 달성했습니다.",
    achieved: true,
  },
  {
    image: "https://picsum.photos/100?random=4",
    title: "챔피언",
    description: "10개의 도전과제를 성공적으로 완료했습니다.",
    achieved: false,
  },
  {
    image: "https://picsum.photos/100?random=5",
    title: "레전드",
    description: "모든 도전과제를 완벽히 완료했습니다.",
    achieved: true,
  },
]);
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
  border-radius: 50%;
  object-fit: cover;
  margin-right: 15px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* 미달성 뱃지 흑백 처리 */
.achievement-badge.grayscale {
  filter: grayscale(100%);
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
</style>
