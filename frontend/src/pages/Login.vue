<template>
  <div class="login-page">
    <div class="login-card">
      <h2>Sign in with GitHub</h2>
      <a :href="githubAuthUrl" class="github-btn">
        <span>🔐 Login via GitHub</span>
      </a>
      <p class="info">You will be redirected to GitHub for authentication.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const githubAuthUrl = 'http://127.0.0.1:8000/api/v1/github_auth/github'
</script>

<style scoped>
.login-page { display: flex; justify-content: center; align-items: center; min-height: 60vh; }
.login-card { background: white; padding: 2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 300px; }
.github-btn { display: inline-block; background: #24292f; color: white; padding: 0.6rem 1.2rem; border-radius: 6px; text-decoration: none; margin: 1rem 0; }
.info { font-size: 0.8rem; color: #666; }
</style>
