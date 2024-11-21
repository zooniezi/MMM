<template>
  <div>
    <h1>{{ userName }}의 마이페이지</h1>

    <h2>프로필 부분</h2>
    <p>총 피드수: {{ totalFeeds }}</p>
    <p>팔로워 수: {{ followerCount }}</p>
    <p>팔로잉 수: {{ followingCount }}</p>

    <h2>나의 피드</h2>
    <div class="feed-grid">
      <div 
        v-for="(feed, index) in reversedFeeds" 
        :key="index" 
        class="feed-item" 
        @click="openModal(feed)"
        :style="{ backgroundImage: `url(${getImageUrl(feed.poster_path)})` }"
      >
      </div>
    </div>

    <h2>옵션(햄버거 바)</h2>
    <RouterLink :to="{ name: 'editUser' }">회원정보 수정</RouterLink><br>
    <button @click="goLogOut">로그아웃</button>

    <!-- 모달 -->
    <div v-if="selectedFeed" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h3>나의 기록</h3>
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
import { computed, onMounted, ref } from 'vue'
import { useMovieStore } from '@/stores/movie'
import axios from 'axios'

const store = useMovieStore()
const SERVER_API_URL = store.SERVER_API_URL

// 상태 변수
const totalFeeds = computed(() => feeds.value.length)
const followerCount = ref(0)
const followingCount = ref(0)
const isLoading = ref(false)
const error = ref(null)
const userName = store.userName
const userId = ref(null)
const feeds = ref([])

// 역순 데이터 계산
const reversedFeeds = computed(() => [...feeds.value].reverse())

// 이미지 가져오기(완료)
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : 'https://via.placeholder.com/500x750?text=No+Image'
}

const selectedFeed = ref(null)

const openModal = (feed) => {
  selectedFeed.value = feed
}

const closeModal = () => {
  selectedFeed.value = null
}

const goLogOut = function () {
  store.logOut()
}

// 사용자 ID 가져오기(완료)
const getUserId = async function () {
  try {
    const res = await axios({
      method: 'get',
      url: `${SERVER_API_URL}/accounts/userinfo/${store.userName}/`,
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
    });
    userId.value = res.data.id;
  } catch (err) {
    console.error(err);
  }
};

// 팔로우/팔로잉 정보 가져오기
const fetchFollowData = async () => {
  try {
    const response = await axios.get(`${SERVER_API_URL}/accounts/follow/list/${userName}/`, {
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
    });
    // API 응답 데이터에서 팔로워 및 팔로잉 수를 추출
    followerCount.value = response.data.follower_count;
    followingCount.value = response.data.following_count;
  } catch (err) {
    console.error('팔로우/팔로잉 데이터를 가져오는 중 오류 발생:', err);
    error.value = '팔로우/팔로잉 데이터를 가져오는 중 오류가 발생했습니다.';
  }
};

// 해당 사용자의 피드 가져오기(완료)
const fetchFeeds = async () => {
  isLoading.value = true
  error.value = null

  try {
    const response = await axios.get(`${SERVER_API_URL}/movies/feeds/${store.userId}/`, {
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
    })
    feeds.value = response.data // API 응답 데이터를 feeds에 저장
  } catch (err) {
    console.error('피드 데이터를 가져오는 중 오류 발생:', err)
    error.value = '데이터를 가져오는 중 오류가 발생했습니다.'
  } finally {
    isLoading.value = false // 로딩 상태 종료
  }
}

// 컴포넌트 마운트 시 API 호출
onMounted(async () => {
  await getUserId(); // 사용자 ID 가져오기
  await fetchFeeds(); // 피드 가져오기
  await fetchFollowData(); // 팔로워/팔로잉 정보 가져오기
});
</script>


<style scoped>
.feed-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* 3열 그리드 */
  gap: 10px; /* 아이템 간격 */
  margin-top: 20px;
}

.feed-item {
  width: 100%;
  padding-top: 100%; /* 1:1 비율 유지 */
  background-size: 110%; /* 약간 확대하여 마진 효과 */
  background-position: center; /* 중앙 기준 */
  background-repeat: no-repeat; /* 반복 방지 */
  border-radius: 10px; /* 외곽 둥글게 */
  overflow: hidden; /* 외곽 밖 이미지는 잘라냄 */
  cursor: pointer; /* 클릭 가능 표시 */
  transition: transform 0.3s, background-size 0.3s; /* 호버 효과 포함 */
}

.feed-item:hover {
  transform: scale(1.05); /* 컨테이너 확대 */
  /* background-size: 115%; */
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
  font-weight: bold;
}
</style>
