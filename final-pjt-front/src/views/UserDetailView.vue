<template>
  <div>
    <h1>{{ userName }}님의 피드</h1>
    <div v-if="user">
      <button @click="toggleFollow" class="follow-btn">
        {{ isFollowing ? '언팔로우' : '팔로우' }}
      </button>
      <p>총 피드 수: {{ userFeeds.length }}</p>
    </div>
    <div v-else>
      <p>유저 정보를 찾을 수 없습니다.</p>
    </div>
    <div v-if="Object.keys(followData).length > 0">
      <h2>팔로우/팔로워 정보</h2>
      <div>
        <p><strong>팔로워 수:</strong> {{ followData.follower_count }}</p>
        <p><strong>팔로잉 수:</strong> {{ followData.following_count }}</p>
      </div>
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie'

// 스토어 및 라우터 초기화
const store = useMovieStore()
const route = useRoute()
const router = useRouter()

// 상태 변수
const user = ref(null) // 현재 유저 데이터
const userId = ref(0)
const userName = route.params.username
const userFeeds = ref([]) // 현재 유저의 피드
const isFollowing = ref(false) // 팔로우 상태
const selectedFeed = ref(null) // 모달에 표시할 피드
const users = ref([]) // 전체 사용자 목록
const loading = ref(false) // 로딩 상태
const error = ref(null) // 에러 메시지





// 현재 로그인한 사용자의 ID (스토어에서 가져오기)
const currentUserId = store.userId // 스토어에 currentUserId가 있다고 가정

// 피드 역순 정렬
const reversedFeeds = computed(() => [...userFeeds.value].reverse())

// 이미지 경로
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : 'https://via.placeholder.com/500x750?text=No+Image'
}

// 사용자 데이터 가져오기
const fetchUsers = async () => {
  try {
    const response = await axios.get(`${store.SERVER_API_URL}/accounts/allusers/without_admin/`, {
      headers: { Authorization: `Token ${store.serverToken}` },
    });
    users.value = response.data;
  } catch (err) {
    console.error('사용자 목록을 가져오는 데 실패했습니다:', err);
    error.value = '사용자 목록을 가져오는 데 실패했습니다.';
  }
};

// username으로 id 가져오기
const getIdByUsername = (username) => {
  const user = users.value.find(user => user.username === username);
  return user ? user.id : null; // id가 없으면 null 반환
};

// 특정 사용자의 피드 가져오기
const fetchUserFeeds = async (userId) => {
  try {
    loading.value = true;
    const response = await axios.get(`${store.SERVER_API_URL}/movies/feeds/${userId}/`, {
      headers: { Authorization: `Token ${store.serverToken}` },
    });
    userFeeds.value = response.data;
  } catch (err) {
    console.error('피드 데이터를 가져오는 중 오류 발생:', err);
    error.value = '피드 데이터를 가져오는 중 오류가 발생했습니다.';
  } finally {
    loading.value = false;
  }
};

// 사용자 데이터와 피드 가져오기
const fetchUserData = async () => {
  try {
    // 사용자 목록 가져오기
    await fetchUsers();

    // username으로 userId 가져오기
    const targetUserId = getIdByUsername(userName);
    if (!targetUserId) {
      console.error('유효한 사용자 ID를 찾을 수 없습니다.');
      user.value = null;
      return;
    }

    userId.value = targetUserId;

    // 해당 userId로 사용자 데이터 설정
    user.value = users.value.find(u => u.id === targetUserId) || null;

    // 해당 유저의 피드 가져오기
    await fetchUserFeeds(targetUserId);

    // 팔로우 상태 확인
    await checkFollowStatus();
  } catch (err) {
    console.error('사용자 데이터와 피드를 가져오는 중 오류가 발생했습니다:', err);
    error.value = '데이터를 가져오는 중 문제가 발생했습니다.';
  }
};

// 모달 제어
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








// 팔로우 상태 확인
const checkFollowStatus = async () => {
  try {
    const response = await axios.get(`${store.SERVER_API_URL}/accounts/follow/${userName}/`, {
      headers: { Authorization: `Token ${store.serverToken}` },
    });
    isFollowing.value = response.data.isFollowed;
  } catch (err) {
    console.error('팔로우 상태 확인 중 오류 발생:', err);
    error.value = '팔로우 상태를 확인할 수 없습니다.';
  }
};

// 팔로우/언팔로우 토글
const toggleFollow = async () => {
  try {
    const response = await axios.post(`${store.SERVER_API_URL}/accounts/follow/${userName}/`, null, {
      headers: { Authorization: `Token ${store.serverToken}` },
    });

    // 팔로우 상태 업데이트
    isFollowing.value = !isFollowing.value;

    // 팔로워 수 업데이트
    if (isFollowing.value) {
      followData.value.follower_count += 1; // 팔로우하면 팔로워 수 증가
      followData.value.followers.push({ id: currentUserId, username: store.currentUsername }); // 팔로워 리스트에 추가
    } else {
      followData.value.follower_count -= 1; // 언팔로우하면 팔로워 수 감소
      followData.value.followers = followData.value.followers.filter(f => f.id !== currentUserId); // 팔로워 리스트에서 제거
    }
  } catch (err) {
    console.error('팔로우 요청 중 오류 발생:', err);
    error.value = '팔로우 요청 중 문제가 발생했습니다.';
  }
};


// 팔로우/팔로워 정보 가져오기
const followData = ref({}); // 팔로우/팔로워 정보 저장
const fetchFollowData = async () => {
  try {
    const response = await axios.get(`${store.SERVER_API_URL}/accounts/follow/list/${userName}/`, {
      headers: { Authorization: `Token ${store.serverToken}` },
    });
    followData.value = response.data; // API 응답 데이터 저장
  } catch (err) {
    console.error('팔로우/팔로워 정보를 가져오는 중 오류 발생:', err);
    error.value = '팔로우/팔로워 정보를 가져오는 데 실패했습니다.';
  }
};


// 컴포넌트 로드 시 데이터 가져오기
onMounted(async () => {
  await fetchUserData(); // 사용자 데이터 및 피드 가져오기
  await fetchFollowData(); // 팔로우/팔로워 정보 가져오기
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
