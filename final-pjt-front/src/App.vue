<template>
  <div class="container">
    <!-- 네비게이션 바 -->
    <AppNavbar />

    <!-- 메인 콘텐츠 -->
    <main>
      <RouterView />
    </main>

    <!-- 푸터 -->
    <footer>
      <p>© 2024 MMM (MyMovieMemo). 영화에 경험을 담다.</p>
    </footer>
  </div>
</template>

<script setup>
import AppNavbar from './components/AppNavbar.vue';

</script>

<style scoped>

</style>
