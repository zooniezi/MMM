<template>
  <div class="profile-page">
    <!-- 유저 정보 섹션 -->
    <div class="user-info">
      <div class="avatar">
        <img :src="userProfile.image" alt="Profile Picture" />
      </div>
      <div class="stats">
        <p><strong>{{ totalFeeds }}</strong> posts</p>
        <p><strong>{{ followerCount }}</strong> followers</p>
        <p><strong>{{ followingCount }}</strong> following</p>
      </div>
    </div>

    <!-- 팔로워/팔로잉 버튼 -->
    <div class="actions">
      <button @click="openModal('followers')">View Followers</button>
      <button @click="openModal('followings')">View Followings</button>
    </div>

    <!-- 모달 -->
    <div v-if="isModalOpen" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>{{ modalTitle }}</h2>
        <ul>
          <li v-for="user in userList" :key="user.id">{{ user.name }}</li>
        </ul>
        <button @click="closeModal">Close</button>
      </div>
    </div>

    <!-- 목록 섹션 -->
    <div v-if="showList" class="list">
      <h3>{{ showList === 'followers' ? 'Followers' : 'Following' }}</h3>
      <ul>
        <li v-for="user in userList" :key="user.id">{{ user.name }}</li>
      </ul>
    </div>

    <!-- 피드 섹션 -->
    <div class="feeds">
      <div v-for="feed in feeds" :key="feed.id" class="feed-card">
        <img :src="feed.image" alt="Feed Image" />
        <p>{{ feed.caption }}</p>
      </div>
    </div>
  </div>

  <div>
    <p>여기는 햄버거 바 이다옹.</p>
    <RouterLink :to="{ name: 'editUser' }">editUser</RouterLink> |
    <button>로그아웃</button>
  </div>

</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useMovieStore } from '@/stores/movie'
import { RouterLink } from 'vue-router'

const store = useMovieStore()
const SERVER_API_URL = store.SERVER_API_URL

// 유저 정보 및 상태 변수
const userProfile = ref({ image: '', name: '' })
const totalFeeds = ref(0)
const followerCount = ref(0)
const followingCount = ref(0)
const feeds = ref([])
const userList = ref([])
const showList = ref(null)

// 데이터 가져오기
axios.get(`${SERVER_API_URL}/api/user-stats/`)
  .then((res) => {
    totalFeeds.value = res.data.total_feeds
    followerCount.value = res.data.follower_count
    followingCount.value = res.data.following_count
    userProfile.value = {
      image: res.data.profile_image,
      name: res.data.username,
    }
  })
  .catch((err) => {
    console.error(err)
  })

axios.get(`${SERVER_API_URL}/api/user-feeds/`)
  .then((res) => {
    feeds.value = res.data.feeds
  })
  .catch((err) => {
    console.error(err)
  })

// 팔로워/팔로잉 목록 가져오기
const fetchList = (type) => {
  const endpoint = type === 'followers' ? 'followers' : 'followings'
  axios.get(`${SERVER_API_URL}/api/${endpoint}/`)
    .then((res) => {
      userList.value = res.data
      showList.value = type
    })
    .catch((err) => {
      console.error(err)
    })
}

// 모달 열기
const openModal = (type) => {
  const endpoint = type === 'followers' ? 'followers' : 'followings'
  modalTitle.value = type === 'followers' ? 'Followers' : 'Followings'
  axios.get(`${SERVER_API_URL}/api/${endpoint}/`)
    .then((res) => {
      userList.value = res.data
      isModalOpen.value = true
    })
    .catch((err) => {
      console.error(err)
    })
}

// 모달 닫기
const closeModal = () => {
  isModalOpen.value = false
  userList.value = []
}

</script>

<style scoped>
.profile-page {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 0 auto;
  padding: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.avatar img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 16px;
}

.stats p {
  margin: 4px 0;
}

.actions {
  margin-bottom: 16px;
}

.actions button {
  margin-right: 8px;
  padding: 8px 16px;
  border: none;
  background-color: #007bff;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

.actions button:hover {
  background-color: #0056b3;
}

.list {
  margin-bottom: 16px;
}

.feeds {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.feed-card img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.feed-card p {
  text-align: center;
  margin-top: 4px;
}
</style>
