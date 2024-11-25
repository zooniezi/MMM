<template>
  <h1 class="page-title">유저 찾기</h1>
  <div>
    
    <input 
      v-model="searchQuery" 
      type="text" 
      placeholder="Search users..." 
      @input="filterUsers"
      class="mb-3"
    />
    <ul v-if="filteredUsers.length > 0" class="m-0">
      <span 
        v-for="user in filteredUsers" 
        :key="user.id" 
        @click="goToUserDetail(user.username)"
        class="user-item m-0"
      >
        {{ user.username }}
      </span>
    </ul>
    <p v-else class="empty-result">검색 결과가 없습니다.</p>
    <p v-if="loading" class="loading">로딩 중...</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie';
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const store = useMovieStore()
const router = useRouter()
const searchQuery = ref('') // 검색어
const users = ref([]) // 전체 사용자 목록
const filteredUsers = ref([]) // 필터링된 사용자 목록
const loading = ref(false) // 로딩 상태
const error = ref(null) // 에러 메시지

// 사용자 데이터 가져오기
const fetchUsers = async () => {
  loading.value = true
  error.value = null
  try {
    const response = await axios.get(`${store.SERVER_API_URL}/accounts/allusers/without_admin/`)
    users.value = response.data
    filterUsers() // 초기 필터링
  } catch (err) {
    error.value = '사용자 목록을 가져오는 데 실패했습니다.'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// 검색 필터링
const filterUsers = () => {
  if (searchQuery.value.trim() === '') {
    filteredUsers.value = [] // 검색어가 없을 때는 사용자 표시 안 함
  } else {
    filteredUsers.value = users.value.filter(user =>
      user.id !== store.userId &&
      user.username.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
}

// 사용자 상세 페이지로 이동
const goToUserDetail = (username) => {
  router.push({ name: 'userDetail', params: { username: username } })
}

// 컴포넌트 로드 시 사용자 데이터 가져오기
onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
/* 전체 배경 및 폰트 */
div {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

input {
  margin-bottom: 10px;
  padding: 8px;
  width: 100%;
  border: 2px solid #ffa200;
  border-radius: 20px;
  outline: none;
  font-size: 16px;
}

input:focus {
  border-color: #ff9900;
  box-shadow: 0 0 8px rgba(255, 200, 97, 0.4);
}

ul {
  list-style: none;
  padding: 0;
}

span.user-item {
  padding: 10px;
  cursor: pointer;
  color: #ffffff;
  background-color: #ffa200;
  border-radius: 15px;
  text-align: center;
  margin-bottom: 5px;
  transition: background-color 0.3s ease;
}

span.user-item:hover {
  background-color: #ffb73a;
}

p.empty-result, p.loading, p.error {
  color: #ffa200;
  font-style: italic;
  text-align: center;
  margin-top: 10px;
}

p.empty-result {
  font-size: 16px;
}

p.loading {
  animation: blink 1s infinite;
}

@keyframes blink {
  50% {
    opacity: 0.6;
  }
}
</style>
