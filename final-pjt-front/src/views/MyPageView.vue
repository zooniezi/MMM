<template>
  <div>
    <h1>{{ userName }}의 마이페이지</h1>

    <h2>프로필 부분</h2>
    <p>총 피드수: {{ totalFeeds }}</p>
    <p>
      팔로워 수: 
      <span class="link" @click="openFollowModal('followers')">
        {{ followerCount }}
      </span>
    </p>
    <p>
      팔로잉 수: 
      <span class="link" @click="openFollowModal('followings')">
        {{ followingCount }}
      </span>
    </p>

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

    <!-- 피드 상세 모달 -->
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
        <div class="comments-section">
            <h4>댓글</h4>
            <ul>
              <li v-for="(comment, index) in comments" :key="index">
                <strong>{{ comment.user }}</strong>: {{ comment.content }}
              </li>
            </ul>
            <textarea v-model="newComment" placeholder="댓글을 입력하세요..."></textarea>
            <button @click="postComment">댓글 등록</button>
        </div>
      </div>
    </div>

    <!-- 팔로워/팔로잉 목록 모달 -->
    <div v-if="isFollowModalOpen" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeFollowModal">&times;</span>
        <h3>{{ followModalType === 'followers' ? '팔로워 목록' : '팔로잉 목록' }}</h3>
        <ul>
          <li v-for="user in followModalData" :key="user.id" @click="goToUserDetail(user.username)" class="user-item">
            {{ user.username }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>


<script setup>
import { computed, onMounted, ref } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'
import axios from 'axios'

const store = useMovieStore()
const SERVER_API_URL = store.SERVER_API_URL
const router = useRouter()
// 상태 변수
const totalFeeds = computed(() => feeds.value.length)
const followerCount = ref(0)
const followingCount = ref(0)
const isLoading = ref(false)
const error = ref(null)
const userName = store.userName
const userId = ref(null)
const feeds = ref([])

// 팔로워/팔로잉 모달 상태
const isFollowModalOpen = ref(false)
const followModalType = ref('') // 'followers' 또는 'followings'
const followModalData = ref([])

// 역순 데이터 계산
const reversedFeeds = computed(() => [...feeds.value].reverse())

// 이미지 가져오기
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : 'https://via.placeholder.com/500x750?text=No+Image'
}

const selectedFeed = ref(null)

const openModal = async(feed) => {
  selectedFeed.value = feed
  // 댓글 가져오기
  await fetchComments(feed.id);
}

const closeModal = () => {
  selectedFeed.value = null
}

// 241122 재준이 추가함

const comments = ref([]);
const newComment = ref("");
// 댓글 가져오기
const fetchComments = async (feedId) => {
  try {
    const response = await axios.get(
      `${store.SERVER_API_URL}/movies/feeds/${feedId}/comments/`,
      {
        headers: {
          Authorization: `Token ${store.serverToken}`,
          "Content-Type": "application/json",
        },
      }
    );
    comments.value = response.data;
  } catch (err) {
    console.error("댓글 가져오기 실패:", err);
    comments.value = [];
  }
};

// 댓글 등록하기
const postComment = async () => {
  if (!newComment.value.trim()) return;

  try {
    const response = await axios.post(
      `${store.SERVER_API_URL}/movies/feeds/${selectedFeed.value.id}/comments/`,
      { content: newComment.value },
      {
        headers: {
          Authorization: `Token ${store.serverToken}`,
          "Content-Type": "application/json",
        },
      }
    );
    comments.value.unshift(response.data); // 새 댓글 추가
    newComment.value = ""; // 입력 필드 초기화
  } catch (err) {
    console.error("댓글 등록 실패:", err);
  }
};
// 여기까지 추가함


const goLogOut = function () {
  store.logOut()
}

// 사용자 ID 가져오기
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
    followerCount.value = response.data.follower_count;
    followingCount.value = response.data.following_count;
  } catch (err) {
    console.error('팔로우/팔로잉 데이터를 가져오는 중 오류 발생:', err);
    error.value = '팔로우/팔로잉 데이터를 가져오는 중 오류가 발생했습니다.';
  }
};

// 팔로우/팔로워 유저 상세 페이지로 이동
const goToUserDetail = (username) => {
  router.push({ name: 'userDetail', params: { username: username } })
}

// 특정 모달 데이터 가져오기
const openFollowModal = async (type) => {
  followModalType.value = type;
  try {
    const response = await axios.get(`${SERVER_API_URL}/accounts/follow/list/${userName}/`, {
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
    });
    followModalData.value = response.data[type]; // followers 또는 followings
    isFollowModalOpen.value = true;
  } catch (err) {
    console.error(`${type} 데이터를 가져오는 중 오류 발생:`, err);
  }
};

// 모달 닫기
const closeFollowModal = () => {
  isFollowModalOpen.value = false;
  followModalData.value = [];
};

// 해당 사용자의 피드 가져오기
const fetchFeeds = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await axios.get(`${SERVER_API_URL}/movies/feeds/${store.userId}/`, {
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
    });
    feeds.value = response.data;
  } catch (err) {
    console.error('피드 데이터를 가져오는 중 오류 발생:', err);
    error.value = '데이터를 가져오는 중 오류가 발생했습니다.';
  } finally {
    isLoading.value = false;
  }
};

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

li.user-item {
  padding: 5px 0;
  cursor: pointer;
  color: #007BFF;
}

li.user-item:hover {
  text-decoration: underline;
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

.link {
  cursor: pointer;
  color: blue;
  text-decoration: underline;
}

.comments-section ul {
  list-style: none;
  padding: 0;
}

.comments-section textarea {
  width: 100%;
  margin-top: 10px;
  padding: 10px;
}

.comments-section button {
  margin-top: 10px;
}
</style>
