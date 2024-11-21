<template>
  <div>
    <h1>유저 찾기</h1>
    <input 
      v-model="searchQuery" 
      type="text" 
      placeholder="Search users..." 
      @input="filterUsers"
    />
    <ul v-if="filteredUsers.length > 0">
      <li 
        v-for="user in filteredUsers" 
        :key="user.id" 
        @click="goToUserDetail(user.username)"
        class="user-item"
      >
        {{ user.username }}
      </li>
    </ul>
    <p v-else>검색 결과가 없습니다.</p>
    <p v-if="loading">로딩 중...</p>
    <p v-if="error">{{ error }}</p>
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
    console.log(users.value)
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
input {
  margin-bottom: 10px;
  padding: 5px;
  width: 100%;
}

ul {
  list-style: none;
  padding: 0;
}

li.user-item {
  padding: 5px 0;
  cursor: pointer;
  color: #007BFF;
}

li.user-item:hover {
  text-decoration: underline;
}

p {
  color: #777;
  font-style: italic;
}
</style>
