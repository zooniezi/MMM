<template>
  <div class="app-container">
    <!-- 네비게이션 바 -->
    <AppNavbar v-if="!$route.meta.hideNavbar" />

    <!-- 메인 콘텐츠 -->
    <main class="container content">
      <RouterView :key="$route.params.username" />
    </main>

    <!-- 푸터 -->
    <footer class="footer">
      <p>© 2024 MMM (MyMovieMemo). 영화에 경험을 담다.</p>
    </footer>
  </div>
</template>

<script setup>
import AppNavbar from './components/AppNavbar.vue';
</script>

<style scoped>
/* 앱의 전체 컨테이너 설정 */
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 화면 전체 높이를 채우도록 설정 */
}

/* 메인 콘텐츠 */
.container.content {
  flex-grow: 1; /* 남은 공간을 차지하도록 설정 */
  max-width: 800px;
}

/* 푸터 스타일 */
.footer {
  background-color: #F9F9F9;
  text-align: center;
  padding: 10px 15px;
  border-top: 1px solid #e9ecef;
  font-size: 14px;
  color: #555;
}
</style>
