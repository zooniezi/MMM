<script setup>
import { RouterLink } from 'vue-router'

</script>

<template>
  <nav>
    <RouterLink :to="{ name: 'home' }">Home</RouterLink> |
    <RouterLink :to="{ name: 'logIn' }">logIn</RouterLink> |
    <RouterLink :to="{ name: 'createFeed' }">createFeed</RouterLink> |
    <RouterLink :to="{ name: 'editUser' }">editUser</RouterLink> |
    <RouterLink :to="{ name: 'recommend' }">recommend</RouterLink> |
    <RouterLink :to="{ name: 'searchFriend' }">searchFriend</RouterLink> |
    <RouterLink :to="{ name: 'myPage' }">myPage</RouterLink> |
  </nav>
</template>
