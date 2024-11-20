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
        @click="goToUserDetail(user.id)"
        class="user-item"
      >
        {{ user.name }} ({{ user.email }})
      </li>
    </ul>
    <p v-else>검색 결과가 없습니다.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const searchQuery = ref('')
const users = ref([
  { id: 1, name: 'Alice Johnson', email: 'alice.johnson@example.com' },
  { id: 2, name: 'Bob Smith', email: 'bob.smith@example.com' },
  { id: 3, name: 'Charlie Brown', email: 'charlie.brown@example.com' },
  { id: 4, name: 'David Wilson', email: 'david.wilson@example.com' },
  { id: 5, name: 'Eve Davis', email: 'eve.davis@example.com' },
  { id: 6, name: 'Frank Miller', email: 'frank.miller@example.com' },
])
const filteredUsers = ref([])
const currentUserId = 3 // 현재 사용자의 ID (예: Charlie)

// 사용자 데이터 초기화
const initializeUsers = () => {
  // 현재 사용자 제외 및 초기 필터링 상태
  filteredUsers.value = []
}

// 검색 필터링
const filterUsers = () => {
  if (searchQuery.value.trim() === '') {
    filteredUsers.value = [] // 검색어가 없을 때는 사용자 표시 안 함
  } else {
    filteredUsers.value = users.value.filter(user =>
      user.id !== currentUserId &&
      user.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
}

// 사용자 상세 페이지로 이동
const goToUserDetail = (userId) => {
  router.push({ name: 'userDetail', params: { id: userId } })
}

// 컴포넌트 로드 시 초기화
onMounted(initializeUsers)
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
