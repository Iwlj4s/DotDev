<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">📘 DotDev</router-link>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Projects</router-link>
        <template v-if="userStore.currentUser">
          <router-link :to="`/profile/${userStore.currentUser.id}`" class="nav-link">
            {{ userStore.currentUser.name || userStore.currentUser.github_login }}
          </router-link>
          <button @click="userStore.logout" class="logout-btn">Logout</button>
        </template>
        <router-link v-else to="/login" class="nav-link">Login</router-link>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/userStore'
const userStore = useUserStore()
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  padding: 0.75rem 1rem;
}
.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.logo {
  font-weight: bold;
  font-size: 1.25rem;
  text-decoration: none;
  color: #2d3748;
}
.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}
.nav-link {
  text-decoration: none;
  color: #4a5568;
}
.logout-btn {
  background: none;
  border: none;
  color: #e53e3e;
  cursor: pointer;
}
</style>
