<template>
  <div class="container mt-4">
    <h1>홈</h1>
    <div class="row row-cols-3 g-1">
      <div v-for="(feed, index) in reversedFeeds" :key="index" class="col">
        <div v-if="feed.is_share_to_feed">
          <div class="card-container position-relative" @click="openModal(feed)">
            <img
              :src="getImageUrl(feed.movie?.poster_path)"
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
    </div>

    <!-- 모달 -->
    <div v-if="selectedFeed" class="modal show d-block" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedFeed.user }} 님의 기록</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <p><strong>영화 제목:</strong> {{ selectedFeed.movie?.title }}</p>
            <p><strong>평점:</strong> {{ selectedFeed.rating }}</p>
            <p><strong>코멘트:</strong> {{ selectedFeed.comment }}</p>
            <p><strong>관람 날짜:</strong> {{ selectedFeed.watch_date }}</p>
            <div class="comments-section">
              <h4>댓글 ({{ commentCount }})</h4>
              <ul class="list-group">
                <li
                  v-for="(comment, index) in comments"
                  :key="index"
                  class="list-group-item"
                >
                  <strong>{{ comment.user }}</strong>: {{ comment.content }}
                </li>
              </ul>
              <textarea
                v-model="newComment"
                class="form-control my-3"
                placeholder="댓글을 입력하세요..."
              ></textarea>
              <button @click="postComment" class="btn btn-primary w-100">
                댓글 등록
              </button>
            </div>
          </div>
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
const selectedFeed = ref(null);
const commentCount = ref(0); // 댓글 개수 상태 추가

// 역순 데이터 계산
const reversedFeeds = computed(() => [...feedData.value].reverse());

// 이미지 URL 처리
const getImageUrl = (path) => {
  return path
    ? `https://image.tmdb.org/t/p/w500${path}`
    : "https://via.placeholder.com/500x750?text=No+Image";
};

// 댓글 개수 업데이트
const updateFeedCommentCount = (feedId, count) => {
  const feed = feedData.value.find((f) => f.id === feedId);
  if (feed) feed.comments_count = count;
};

// 댓글 동기화 함수
const syncCommentsCount = async () => {
  try {
    const results = await Promise.all(
      feedData.value.map((feed) =>
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

// 모달 관리
const openModal = async (feed) => {
  selectedFeed.value = feed;
  await fetchComments(feed.id);
};

const closeModal = () => {
  selectedFeed.value = null;
  comments.value = [];
  commentCount.value = 0;
};

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

// 댓글 등록하기
const postComment = async () => {
  if (!newComment.value.trim()) return;

  try {
    const response = await axios.post(
      `${store.SERVER_API_URL}/movies/feeds/${selectedFeed.value.id}/comments/`,
      { content: newComment.value },
      { headers: { Authorization: `Token ${store.serverToken}` } }
    );
    comments.value.unshift(response.data);
    newComment.value = "";
    commentCount.value++;
    updateFeedCommentCount(selectedFeed.value.id, commentCount.value);
  } catch (err) {
    console.error("댓글 등록 실패:", err);
  }
};

// 데이터 가져오기
const fetchFollowedUsersFeed = async () => {
  isLoading.value = true;

  try {
    const response = await axios.get(`${store.SERVER_API_URL}/movies/feeds/followed/`, {
      headers: { Authorization: `Token ${store.serverToken}` },
    });
    feedData.value = response.data.map((feed) => ({
      ...feed,
      comments_count: null, // 초기 상태
    }));

    // 댓글 개수 동기화
    await syncCommentsCount();
  } catch (err) {
    console.error("피드 데이터 가져오기 실패:", err);
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
/* 카드 설정 */
.card-container {
  width: 100%;
  aspect-ratio: 1 / 1;
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
</style>