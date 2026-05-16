<template>
  <div>
    <NavBar />
    <main class="container">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import NavBar from './components/NavBar.vue'
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}
</style>
