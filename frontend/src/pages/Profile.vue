<template>
  <div class="profile-container" v-if="profileUser">
    <div class="profile-header">
      <h1>{{ profileUser.name }}</h1>
      <p class="login">@{{ profileUser.github_login }}</p>
      <p class="bio">{{ profileUser.bio || 'No bio yet' }}</p>
      <p class="location">📍 {{ profileUser.location || 'Not specified' }}</p>
      <p class="email">✉️ {{ profileUser.email !== 'user have not email' ? profileUser.email : 'No public email' }}</p>
    </div>
    <div class="projects-section" v-if="profileUser.projects && profileUser.projects.length">
      <h2>Projects</h2>
      <div class="projects-grid">
        <ProjectCard v-for="project in profileUser.projects" :key="project.id" :project="project" />
      </div>
    </div>
  </div>
  <div v-else-if="loading">Loading profile...</div>
  <div v-else>User not found</div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '@/stores/userStore'
import ProjectCard from '@/components/ProjectCard.vue'

const route = useRoute()
const userStore = useUserStore()

const profileUser = ref<any | null>(null)
const loading = ref(false)

const loadProfile = async (userId: number) => {
  loading.value = true
  const user = await userStore.fetchUserProfile(userId)
  profileUser.value = user
  loading.value = false
  console.log(user)
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
.profile-container {
  max-width: 1200px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.profile-header {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
  margin-bottom: 2rem;
}

.profile-header h1 {
  margin: 0 0 0.5rem;
  font-size: 2rem;
}

.login {
  color: #3b82f6;
  font-size: 0.95rem;
  margin: 0 0 1rem;
}

.bio, .location, .email {
  margin: 0.75rem 0;
  color: #475569;
  font-size: 0.95rem;
}

.projects-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.projects-section h2 {
  margin: 0 0 1.5rem;
  font-size: 1.5rem;
  color: #1e293b;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
}
</style>
