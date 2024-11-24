<template>
  <div class="px-0">
    <h1 class="page-title">홈</h1>
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
        <div class="modal-content bg-memo">
          <div class="modal-body d-flex">
            <!-- 왼쪽: 포스터 -->
            <div class="poster-section">
              <img
                :src="getImageUrl(selectedFeed.movie?.poster_path)"
                alt="포스터"
                class="poster-image-large"
              />
            </div>
            <!-- 오른쪽: 상세 정보 -->
            <div class="details-section">
              <div class="modal-header p-0">
                <h2 class="modal-title">{{ selectedFeed.user }}의 기록</h2>
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
    </div>


    
  </div>
</template>


<script setup>
import { ref, computed, onMounted } from "vue"
import { useMovieStore } from "@/stores/movie"
import axios from "axios"

// 상태 관리
const store = useMovieStore();
const feedData = ref([]);
const comments = ref([]);
const newComment = ref("");
const isLoading = ref(false);
const selectedFeed = ref(null);
const commentCount = ref(0); // 댓글 개수 상태 추가
const selectedEmoji = ref(null);
const emojiCounts = ref({});

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

// 감정 표현 옵션
const emojiOptions = [
  { label: "😊", value: 1 },
  { label: "😢", value: 2 },
  { label: "😡", value: 3 },
  { label: "❤️", value: 4 },
  { label: "👍", value: 5 },
];

// 모달 관리
const openModal = async (feed) => {
  selectedFeed.value = feed;
  console.log(selectedFeed.value)
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
};

const closeModal = () => {
  selectedFeed.value = null;
  comments.value = [];
  commentCount.value = 0;
  selectedEmoji.value = null;
  emojiCounts.value = {};
};

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
</style>
