<template>
  <div>
    <h1>Home</h1>

    <!-- 로딩 중 -->
    <div v-if="isLoading">로딩 중...</div>

    <!-- 에러 메시지 -->
    <div v-else-if="error">{{ error }}</div>

    <!-- 친구 피드 리스트 -->
    <div v-else class="feed-grid">
      <div
        v-for="(feed, index) in reversedFeeds"
        :key="index"
        class="feed-item"
        @click="openModal(feed)"
        :style="{ backgroundImage: `url(${getImageUrl(feed.movie?.poster_path)})` }"
      >
      </div>
    </div>

    <!-- 모달 -->
    <div v-if="selectedFeed" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h3>친구의 기록</h3>
        <p><strong>영화 제목:</strong> {{ selectedFeed.movie?.title }}</p>
        <p><strong>평점:</strong> {{ selectedFeed.rating }}</p>
        <p><strong>코멘트:</strong> {{ selectedFeed.comment }}</p>
        <p><strong>관람 날짜:</strong> {{ selectedFeed.watch_date }}</p>

        <!-- 댓글 섹션 -->
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
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import { useMovieStore } from "@/stores/movie";

// 상태 관리
const store = useMovieStore();
const feedData = ref([]);
const comments = ref([]);
const newComment = ref("");
const isLoading = ref(false);
const error = ref(null);
const selectedFeed = ref(null);

// 역순 데이터 계산
const reversedFeeds = computed(() => [...feedData.value].reverse());

// 이미지 URL 처리
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : "https://via.placeholder.com/500x750?text=No+Image";
};

// 모달 관리
const openModal = async (feed) => {
  selectedFeed.value = feed;

  // 댓글 가져오기
  await fetchComments(feed.id);
};

const closeModal = () => {
  selectedFeed.value = null;
  comments.value = [];
};

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

// 데이터 가져오기
const fetchFollowedUsersFeed = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await axios.get(`${store.SERVER_API_URL}/movies/feeds/followed/`, {
      headers: {
        Authorization: `Token ${store.serverToken}`,
      },
    });
    feedData.value = response.data;
  } catch (err) {
    console.error("피드 데이터를 가져오는 중 오류 발생:", err);
    error.value = "피드 데이터를 가져오는 데 실패했습니다.";
  } finally {
    isLoading.value = false;
  }
};

// 컴포넌트 마운트 시 데이터 가져오기
onMounted(() => {
  fetchFollowedUsersFeed();
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
  background-size: 110%;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s, background-size 0.3s;
}

.feed-item:hover {
  transform: scale(1.05);
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
