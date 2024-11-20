<template>
  <div>
    <h1>{{ user?.name }}님의 피드</h1>
    <div v-if="user">
      <button @click="toggleFollow" class="follow-btn">
        {{ isFollowing ? '언팔로우' : '팔로우' }}
      </button>
      <p>총 피드 수: {{ userFeeds.length }}</p>
    </div>
    <div v-else>
      <p>유저 정보를 찾을 수 없습니다.</p>
    </div>

    <div v-if="userFeeds.length > 0" class="feed-grid">
      <div 
        v-for="(feed, index) in reversedFeeds" 
        :key="index" 
        class="feed-item" 
        :style="{ backgroundImage: `url(${getImageUrl(feed.poster_path)})` }"
        @click="openModal(feed)"
      >
      </div>
    </div>
    <p v-else>피드가 없습니다.</p>

    <!-- 모달 -->
    <div v-if="selectedFeed" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h3>기록 보기</h3>
        <p><strong>관람 날짜:</strong> {{ selectedFeed.watch_date }}</p>
        <p><strong>시간:</strong> {{ selectedFeed.watch_time }}</p>
        <p><strong>장소:</strong> {{ selectedFeed.watch_place }}</p>
        <p><strong>함께한 사람:</strong> {{ selectedFeed.watch_with_who }}</p>
        <p><strong>관람 이유:</strong> {{ selectedFeed.watch_reason.join(', ') }}</p>
        <p><strong>평점:</strong> {{ selectedFeed.rating }}</p>
        <p><strong>코멘트:</strong> {{ selectedFeed.comment }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// 사용자 정보
const users = ref([
  { id: 1, name: 'Alice Johnson' },
  { id: 2, name: 'Bob Smith' },
  { id: 3, name: 'Charlie Brown' },
  { id: 4, name: 'David Wilson' },
  { id: 5, name: 'Eve Davis' },
  { id: 6, name: 'Frank Miller' },
])

// 피드 데이터
const feeds = ref([
  {
    user: 1,
    movie_id: 1129598,
    watch_date: "2024-11-01",
    watch_time: "morning",
    watch_place: "movie_theater",
    watch_with_who: "alone",
    watch_reason: ["재미있을 것 같아서", "추천을 받아서"],
    rating: 1,
    comment: "굳",
    is_share_to_feed: true,
    poster_path: '/3flIDcZF3tnR7m5OU2h7lLPQwmr.jpg',
  },
  {
    user: 2,
    movie_id: 27205,
    watch_date: "2024-11-01",
    watch_time: "morning",
    watch_place: "home",
    watch_with_who: "alone",
    watch_reason: ["추천을 받아서"],
    rating: 4,
    comment: "꿀잼",
    is_share_to_feed: true,
    poster_path: '/wIrhEUBWjRmZuL1Ix41cF2LhJrW.jpg',
  },
])

// 현재 유저
const userId = Number(route.params.id)
const user = users.value.find((u) => u.id === userId)

// 해당 유저의 피드 필터링
const userFeeds = computed(() => feeds.value.filter(feed => feed.user === userId))
const reversedFeeds = computed(() => [...userFeeds.value].reverse())

// 모달 상태
const selectedFeed = ref(null)
const openModal = (feed) => {
  selectedFeed.value = feed
}
const closeModal = () => {
  selectedFeed.value = null
}

// 팔로우 상태
const isFollowing = ref(false)
const toggleFollow = () => {
  isFollowing.value = !isFollowing.value
}

// 이미지 경로
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : 'https://via.placeholder.com/500x750?text=No+Image'
}
</script>

<style scoped>
.feed-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 20px;
}

.feed-item {
  width: 100%;
  padding-top: 100%;
  background-size: cover;
  background-position: center;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.3s;
}

.feed-item:hover {
  transform: scale(1.05);
}

.follow-btn {
  margin: 10px 0;
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.follow-btn:hover {
  background-color: #0056b3;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background: white;
  padding: 20px;
  border-radius: 10px;
  max-width: 500px;
  width: 100%;
  position: relative;
}

.close {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  font-size: 24px;
}
</style>
