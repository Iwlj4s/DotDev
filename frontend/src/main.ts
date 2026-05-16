import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'
import './style.css'
import { useUserStore } from './stores/userStore'

const app = createApp(App)
const pinia = createPinia()
app.use(pinia)
app.use(router)

// Attempt to load current user (will use cookie set by backend)
const userStore = useUserStore()
userStore.loadCurrentUser().catch(() => {})

app.mount('#app')
