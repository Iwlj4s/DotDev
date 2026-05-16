<template>
  <div class="auth-callback">
    <p v-if="loading">Processing login...</p>
    <p v-else-if="error">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { loginWithCode } from '@/api/auth'
import { useUserStore } from '@/stores/userStore'

const loading = ref(true)
const error = ref<string | null>(null)
const router = useRouter()
const userStore = useUserStore()

onMounted(async () => {
  const params = new URLSearchParams(window.location.search)
  const code = params.get('code')
  if (!code) {
    error.value = 'No code provided'
    loading.value = false
    return
  }

  try {
    await loginWithCode(code)
    // After backend sets cookie, fetch current user
    await userStore.loadCurrentUser()
    // Optionally persist minimal state for UI
    if (userStore.currentUser) {
      localStorage.setItem('user', JSON.stringify(userStore.currentUser))
      localStorage.setItem('isAuthenticated', 'true')
    }
    router.replace({ name: 'home' })
  } catch (e: any) {
    console.error(e)
    error.value = 'Login failed'
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.auth-callback { display:flex; align-items:center; justify-content:center; min-height:60vh; }
</style>
