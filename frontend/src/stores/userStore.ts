import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchCurrentUser, logoutApi } from '@/api/auth'
import { fetchUserById } from '@/api/users'

export const useUserStore = defineStore('user', () => {
  const currentUser = ref(null as any)
  const isLoading = ref(false)

  const loadCurrentUser = async () => {
    isLoading.value = true
    try {
      const user = await fetchCurrentUser()
      currentUser.value = user
    } catch (error) {
      console.error('Failed to load current user', error)
      currentUser.value = null
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      await logoutApi()
    } catch (e) {
      // ignore network errors — still clear client state
      console.error('Logout API failed', e)
    }
    currentUser.value = null
    try {
      localStorage.removeItem('user')
      localStorage.removeItem('isAuthenticated')
    } catch (e) {}
    // reload to clear any auth-only UI
    window.location.href = '/'
  }

  const fetchUserProfile = async (userId: number) => {
    try {
      return await fetchUserById(userId)
    } catch (e) {
      console.error(e)
      return null
    }
  }

  return { currentUser, isLoading, loadCurrentUser, logout, fetchUserProfile }
})
