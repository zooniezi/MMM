<template>
  <div>
    <RouterLink :to="{ name: 'home' }">Home</RouterLink> |
    <RouterLink :to="{ name: 'login' }">Home</RouterLink> |
    <RouterLink :to="{ name: 'signup' }">Home</RouterLink> |
  </div>
  <RouterView />
</template>

<script setup>

</script>

<style scoped>

</style>