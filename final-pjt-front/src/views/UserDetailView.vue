<template>
  <div class="px-0">
    <h1 class="page-title">{{ userName }}의 페이지</h1>
    <div class="profile-section">
      <p>총 피드: {{ userFeeds.length }}</p>
      <div>
        <p>
          팔로워:
          <span class="link" @click="openFollowModal('followers')">{{ followerCount }}</span>
        </p>
        <p>
          팔로잉:
          <span class="link" @click="openFollowModal('followings')">{{ followingCount }}</span>
        </p>
      </div>
  
      <button 
        @click="toggleFollow" 
        :class="['btn', isFollowing ? 'btn-outline-danger' : 'btn-outline-primary']"
      >
        {{ isFollowing ? '언팔로우' : '팔로우' }}
      </button>
    </div>

    <br>

    <div class="row row-cols-3 g-1">
      <div v-for="(feed, index) in reversedFeeds" :key="index" class="col">
        <div class="card-container position-relative" @click="openModal(feed)">
          <img
            :src="getImageUrl(feed.poster_path)"
            alt="포스터"
            class="poster-image"
          />
          <div class="comment-count position-absolute">
            <span v-if="feed.comments_count === null">Loading...</span>
            <span v-else>{{ feed.comments_count }} Comments</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 모달 -->
    <div v-if="selectedFeed" class="modal show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-memo">
          <div class="modal-body d-flex">
            <!-- 왼쪽: 포스터 -->
            <div class="poster-section">
              <img
                :src="getImageUrl(selectedFeed.poster_path)"
                alt="포스터"
                class="poster-image-large"
              />
            </div>
            <!-- 오른쪽: 상세 정보 -->
            <div class="details-section">
              <div class="modal-header p-0">
                <h2 class="modal-title">{{ userName }}의 기록</h2>
                <button type="button" class="btn-close" @click="closeModal"></button>
              </div>
              <div class="modal-body d-inline">
                <div class="pt-2">
                  <p><strong>영화 제목:</strong> {{ selectedFeed.movie?.title }}</p>
                  <p><strong>관람 날짜:</strong> {{ selectedFeed.watch_date }}</p>
                  <p><strong>시간:</strong> {{ selectedFeed.watch_time }}</p>
                  <p><strong>장소:</strong> {{ selectedFeed.watch_place }}</p>
                  <p><strong>함께한 사람:</strong> {{ selectedFeed.watch_with_who }}</p>
                  <p><strong>관람 이유:</strong> {{ selectedFeed.watch_reason.join(', ') }}</p>
                  <p><strong>평점:</strong> {{ selectedFeed.rating }}</p>
                  <p><strong>코멘트:</strong> {{ selectedFeed.comment }}</p>
                </div>

                <!-- 감정 표현 기능 -->
                <div class="emoji-section">
                  <button
                    v-for="emoji in emojiOptions"
                    :key="emoji.value"
                    :class="{ active: selectedEmoji === emoji.value }"
                    @click="toggleEmoji(emoji.value)"
                  >
                    {{ emoji.label }} ({{ emojiCounts[emoji.value] || 0 }})
                  </button>

                </div>
                <div class="comments-section">
                    <h4>댓글 ({{ commentCount }})</h4>

                    <ul class="list-group">
                      <li
                        v-for="(comment, index) in comments"
                        :key="comment.id"
                        class="list-group-item"
                      >
                        <div>
                          <strong>{{ comment.user }}</strong>: {{ comment.content }}
                        </div>
                        <div class="comment-meta d-flex justify-content-between mt-1">
                          <span class="text-muted small">{{ formatTime(comment.created_at) }}</span>
                          <button
                            class="btn btn-danger btn-sm"
                            @click="deleteComment(comment.id)"
                          >
                            삭제
                          </button>
                        </div>
                      </li>
                    </ul>

                    <textarea v-model="newComment" class="form-control my-3" placeholder="댓글을 입력하세요..."></textarea>
                    <button @click="postComment" class="btn btn-primary w-100">댓글 등록</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

   <!-- 팔로워/팔로잉 목록 모달 -->
   <div v-if="isFollowModalOpen" class="follow-modal">
      <div class="follow-modal-content">
        <div class="modal-header d-flex justify-content-between align-items-center">
          <h5 class="modal-title">{{ followModalType === 'followers' ? '팔로워' : '팔로잉' }}</h5>
          <button type="button" class="btn-close" @click="closeFollowModal"></button>
        </div>
        <hr>
        <div class="modal-body">
          <ul class="list-group">
            <li
              v-for="user in followModalData"
              :key="user.id"
              class="list-group-item d-flex justify-content-between align-items-center"
              @click="goToUserDetail(user.username)"
            >
              <div class="me-2">
                <span>{{ user.username }}</span>
              </div>
              <button class="btn btn-outline-primary btn-sm">프로필 보기</button>
            </li>
          </ul>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import axios from 'axios'

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
const commentCount = ref(0); // 댓글 개수 상태 추가
const selectedEmoji = ref(null);
const emojiCounts = ref({});
const comments = ref([]);
const newComment = ref("");
const followerCount = ref(0)
const followingCount = ref(0)

// 팔로워/팔로잉 모달 상태
const isFollowModalOpen = ref(false)
const followModalType = ref('') // 'followers' 또는 'followings'
const followModalData = ref([])

// 현재 로그인한 사용자의 ID (스토어에서 가져오기)
const currentUserId = store.userId

// 피드 역순 정렬
const reversedFeeds = computed(() => [...userFeeds.value].reverse())

// 이미지 경로
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : 'https://via.placeholder.com/500x750?text=No+Image'
}

// 이모지 추가/삭제 기능
const toggleEmoji = async (emoji) => {
  if (!selectedFeed.value) return;

  // 같은 이모지를 다시 선택하면 삭제 요청
  if (selectedEmoji.value === emoji) {
    try {
      await axios.delete(
        `${store.SERVER_API_URL}/movies/feeds/${selectedFeed.value.id}/emoji/`,
        {
          headers: {
            Authorization: `Token ${store.serverToken}`,
          },
        }
      );
      selectedEmoji.value = null; // 선택된 이모지 초기화
      emojiCounts.value[emoji] = (emojiCounts.value[emoji] || 1) - 1; // 개수 감소
    } catch (err) {
      console.error("이모지 삭제 실패:", err);
    }
  } else {
    // 새로운 이모지 추가 요청
    try {
      const response = await axios.post(
        `${store.SERVER_API_URL}/movies/feeds/${selectedFeed.value.id}/emoji/`,
        { emoji },
        {
          headers: {
            Authorization: `Token ${store.serverToken}`,
            "Content-Type": "application/json",
          },
        }
      );
      selectedEmoji.value = response.data.emoji; // 선택된 이모지 업데이트
      emojiCounts.value[emoji] = (emojiCounts.value[emoji] || 0) + 1; // 개수 증가
    } catch (err) {
      console.error("이모지 추가 실패:", err);
    }
  }
};

// 감정 표현 옵션
const emojiOptions = [
  { label: "😊", value: 1 },
  { label: "😢", value: 2 },
  { label: "😡", value: 3 },
  { label: "❤️", value: 4 },
  { label: "👍", value: 5 },
];

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
    userFeeds.value = response.data.map((feed) => ({
      ...feed,
      comments_count: null, // 초기 상태
    }));
    // 댓글 개수 동기화
    await syncCommentsCount()
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

  // 서버에서 선택된 이모지 및 개수 가져오기
  try {
    const response = await axios.get(
      `${store.SERVER_API_URL}/movies/feeds/${feed.id}/emoji/list/`,
      {
        headers: {
          Authorization: `Token ${store.serverToken}`,
        },
      }
    );

    // 이모지 개수 계산
    const counts = {};
    response.data.forEach((emoji) => {
      counts[emoji.emoji] = (counts[emoji.emoji] || 0) + 1;
    });
    emojiCounts.value = counts;

    // 사용자 선택된 이모지 설정
    const userEmoji = response.data.find((e) => e.user === store.userName);
    selectedEmoji.value = userEmoji ? userEmoji.emoji : null;
  } catch (err) {
    console.error("이모지 데이터를 가져오는 중 오류 발생:", err);
    emojiCounts.value = {};
  }
}
const closeModal = () => {
  selectedFeed.value = null
  comments.value = [];
  commentCount.value = 0;
  selectedEmoji.value = null;
  emojiCounts.value = {};
}

// 댓글 부분
// 댓글 개수 업데이트
const updateFeedCommentCount = (feedId, count) => {
  const feed = userFeeds.value.find((f) => f.id === feedId);
  if (feed) feed.comments_count = count;
}

// 댓글 가져오기
const fetchComments = async (feedId) => {
  try {
    const response = await axios.get(
      `${store.SERVER_API_URL}/movies/feeds/${feedId}/comments/`,
      { headers: { Authorization: `Token ${store.serverToken}` } }
    );
    comments.value = response.data;
    commentCount.value = response.data.length;
    updateFeedCommentCount(feedId, commentCount.value);
  } catch (err) {
    console.error("댓글 가져오기 실패:", err);
  }
};

// 댓글 동기화 함수
const syncCommentsCount = async () => {
  try {
    const results = await Promise.all(
      userFeeds.value.map((feed) =>
        axios
          .get(`${store.SERVER_API_URL}/movies/feeds/${feed.id}/comments/`, {
            headers: { Authorization: `Token ${store.serverToken}` },
          })
          .then((response) => ({
            feedId: feed.id,
            commentsCount: response.data.length,
          }))
      )
    );
    results.forEach(({ feedId, commentsCount }) =>
      updateFeedCommentCount(feedId, commentsCount)
    );
  } catch (err) {
    console.error("댓글 동기화 실패:", err);
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
      followerCount.value += 1; // 팔로우하면 팔로워 수 증가
    } else {
      followerCount.value -= 1; // 언팔로우하면 팔로워 수 감소
    }
  } catch (err) {
    console.error('팔로우 요청 중 오류 발생:', err);
    error.value = '팔로우 요청 중 문제가 발생했습니다.';
  }
};


// 팔로우/팔로워 정보 가져오기
const followData = ref({}); // 팔로우/팔로워 정보 저장

// 팔로우/팔로잉 정보 가져오기
const fetchFollowData = async () => {
  try {
    const response = await axios.get(`${store.SERVER_API_URL}/accounts/follow/list/${userName}/`, {
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
  console.log(`Fetching ${type} data...`); // 디버깅 로그
  try {
    const response = await axios.get(`${store.SERVER_API_URL}/accounts/follow/list/${userName}/`, {
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
    });
    followModalData.value = response.data[type];
    isFollowModalOpen.value = true;
    console.log("Fetched data:", followModalData.value); // 데이터 확인
  } catch (err) {
    console.error(`${type} 데이터를 가져오는 중 오류 발생:`, err);
  }
};

// 모달 닫기
const closeFollowModal = () => {
  isFollowModalOpen.value = false;
  followModalData.value = [];
};

const formatTime = (timestamp) => {
  const date = new Date(timestamp);
  return date.toLocaleString(); // 원하는 포맷으로 변경 가능
};

const deleteComment = async (commentId) => {
  try {
    await axios.delete(
      `${store.SERVER_API_URL}/movies/feeds/${selectedFeed.value.id}/comments/${commentId}/`,
      { headers: { Authorization: `Token ${store.serverToken}` } }
    );
    // 로컬 상태에서 댓글 제거
    comments.value = comments.value.filter((comment) => comment.id !== commentId);
    commentCount.value--;
    updateFeedCommentCount(selectedFeed.value.id, commentCount.value);
  } catch (err) {
    console.error("댓글 삭제 실패:", err);
  }
};


// 컴포넌트 로드 시 데이터 가져오기
onMounted(async () => {
  await fetchUserData(); // 사용자 데이터 및 피드 가져오기
  await fetchFollowData(); // 팔로우/팔로워 정보 가져오기
});
</script>

<style scoped>
/* 카드 설정 */
.card-container {
  width: 100%;
  aspect-ratio: 1 / 1;
  border-radius: 10px;
  background-color: black;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  transition: opacity 0.3s ease-in-out;
  cursor: pointer;
}

/* 카드 Hover 효과 */
.card-container:hover {
  opacity: 0.8;
}

/* 포스터 이미지 */
.poster-image {
  height: 100%;
  width: auto;
  object-fit: contain;
}

/* 댓글 개수 표시 */
.comment-count {
  bottom: 10px;
  left: 10px;
  color: white;
  font-size: 14px;
  font-weight: bold;
  background-color: rgba(0, 0, 0, 0.6);
  padding: 5px 10px;
  border-radius: 5px;
  display: none; /* 기본적으로 숨김 */
}

/* Hover 시 댓글 개수 보이기 */
.card-container:hover .comment-count {
  display: block;
}


/* 모달 커스터마이징 */
.modal {
  background: rgba(0, 0, 0, 0.5);
}

.modal-content {
  border-radius: 10px;
  overflow: hidden;
}

/* 모달 내부 레이아웃 */
.modal-body {
  display: flex; /* 좌우로 배치 */
  padding: 0; /* 기본 패딩 제거 */
  align-items: stretch; /* 높이 균등 정렬 */
}

.modal-dialog {
  max-width: 90%; /* 기본 50%에서 90%로 확장 */
  width: 90%; /* 전체 너비의 90% 사용 */
}

/* 포스터 섹션 */
.poster-section {
  flex: 1.5; /* 왼쪽 영역 비율을 더 크게 설정 */
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: black;
}

.poster-image-large {
  width: 100%; /* 포스터가 전체 영역을 차지하도록 설정 */
  max-width: 500px; /* 최대 너비를 제한 */
  height: auto; /* 비율 유지 */
  object-fit: contain;
  border-radius: 5px;
}

/* 상세 정보 섹션 */
.details-section {
  flex: 2; /* 오른쪽 영역 비율 */
  padding: 20px;
  overflow-y: auto;
}

/* 감정 표현 버튼 */
.emoji-section button {
  margin-right: 5px;
  padding: 5px 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  background-color: white;
  cursor: pointer;
}

.emoji-section button.active {
  background-color: #ffa200;
  color: white;
  border-color: #ffa200;
}

/* 댓글 섹션 */
.comments-section {
  margin-top: 20px;
}

.list-group-item {
  word-wrap: break-word; /* 긴 텍스트 자동 줄바꿈 */
}

.link {
  cursor: pointer;
  color: blue;
  text-decoration: underline;
}

/* 모달 배경 */
.follow-modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1050;
  padding: 20px;
  overflow-y: auto;
}

/* 모달 컨텐츠 */
.follow-modal-content {
  background: white;
  padding: 15px;
  border-radius: 10px;
  max-width: 400px;
  width: 100%;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.profile-section {
  padding: 20px;
  background: #f9f9f9;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
