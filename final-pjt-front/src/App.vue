<template>
  <div class="container custom-container">
    <!-- 네비게이션 바 -->
    <AppNavbar v-if="!$route.meta.hideNavbar" />

    <!-- 메인 콘텐츠 -->
    <main class="content">
      <RouterView />
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
/* 화면 전체를 flexbox로 구성 */
.custom-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 화면 전체 높이를 차지하도록 설정 */
  margin: 0 auto;
  max-width: 800px;
  padding: 0 15px;
}

/* 메인 콘텐츠가 flex-grow로 푸터를 하단에 고정 */
.content {
  flex: 1;
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
