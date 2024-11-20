<template>
  <div>
    <h1>유저 찾기</h1>
    <input 
      v-model="searchQuery" 
      type="text" 
      placeholder="Search users..." 
      @input="filterUsers"
    />
    <ul>
      <li v-for="user in filteredUsers" :key="user.id">
        {{ user.name }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const users = ref([{

}])
const filteredUsers = ref([])
const currentUserId = 3 // 현재 사용자의 ID (예: 로그인 후 서버에서 받아옴)

// 사용자 목록 가져오기
const fetchUsers = async () => {
  try {
    const response = await axios.get('/api/users') // API 엔드포인트 수정 필요
    users.value = response.data.filter(user => user.id !== currentUserId)
    filteredUsers.value = [...users.value]
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
}

// 검색 필터링
const filterUsers = () => {
  filteredUsers.value = users.value.filter(user =>
    user.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
}

// 컴포넌트 로드 시 사용자 목록 가져오기
onMounted(fetchUsers)
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

li {
  padding: 5px 0;
}
</style>