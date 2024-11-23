<script setup>
import { RouterLink } from 'vue-router'
import logo from '@/assets/logo2.png'
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm">
    <div class="container">
      <!-- 로고 -->
      <RouterLink :to="{ name: 'home' }" class="navbar-brand">
        <img :src="logo" alt="Logo" width="100" />
      </RouterLink>

      <!-- 토글 버튼 (모바일) -->
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <!-- 메뉴 항목 -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <RouterLink :to="{ name: 'home' }" class="nav-link">홈</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'createFeed' }" class="nav-link">피드 생성</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'editUser' }" class="nav-link">회원정보 수정</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'recommend' }" class="nav-link">영화 추천</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'searchUser' }" class="nav-link">유저 찾기</RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink :to="{ name: 'myPage' }" class="nav-link">마이페이지</RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<style scoped>
/* 부트스트랩의 내장 스타일로 충분히 꾸며지지만 추가 커스터마이징 가능 */
.navbar-brand img {
  max-width: 100px;
}

.nav-link {
  color: #555 !important; /* 링크 기본 색상 */
  font-weight: 500; /* 약간 굵게 */
}

.nav-link:hover {
  color: #ff5f00 !important; /* 링크 hover 시 오렌지 색상 */
}
</style>
