<template>
  <div class="profile-page" v-if="profileUser">
    <div class="profile-header">
      <h1>{{ profileUser.name }}</h1>
      <p class="login">@{{ profileUser.github_login }}</p>
      <p class="bio">{{ profileUser.bio || 'No bio yet' }}</p>
      <p class="location">📍 {{ profileUser.location || 'Not specified' }}</p>
      <p class="email">✉️ {{ profileUser.email !== 'user have not email' ? profileUser.email : 'No public email' }}</p>
    </div>
  </div>
  <div v-else-if="loading">Loading profile...</div>
  <div v-else>User not found</div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const route = useRoute()
const userStore = useUserStore()

const profileUser = ref<any | null>(null)
const loading = ref(false)

const loadProfile = async (userId: number) => {
  loading.value = true
  const user = await userStore.fetchUserProfile(userId)
  profileUser.value = user
  loading.value = false
}

onMounted(async () => {
  const userId = route.params.id ? Number(route.params.id) : userStore.currentUser?.id
  if (userId) {
    await loadProfile(userId)
  } else if (userStore.currentUser) {
    await loadProfile(userStore.currentUser.id)
  }
})

watch(() => route.params.id, async (newId) => {
  if (newId) await loadProfile(Number(newId))
})
</script>

<style scoped>
.profile-page { max-width: 700px; margin: 2rem auto; background: white; border-radius: 16px; padding: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
.profile-header h1 { margin-bottom: 0.25rem; }
.login { color: #3b82f6; font-size: 0.9rem; margin-bottom: 1rem; }
.bio, .location, .email { margin: 0.5rem 0; }
</style>
