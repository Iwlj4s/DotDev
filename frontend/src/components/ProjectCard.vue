<template>
  <div class="project-card">
    <div class="card-header">
      <h3>
        <a :href="githubUrl" target="_blank" rel="noopener noreferrer">
          {{ project.owner_name }}/{{ project.repo_name }}
        </a>
      </h3>
      <div class="meta">
        <span class="owner">by {{ project.user_name || project.owner_name }}</span>
      </div>
    </div>
    <div class="card-body">
      <p class="description">{{ project.description || 'No description provided.' }}</p>
      <div class="readme-preview">
        <p class="readme">{{ truncatedReadme }}</p>
      </div>
    </div>
    <div class="card-footer">
      <small>Updated: {{ formattedDate }}</small>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
const props = defineProps<{ project: any }>()

const githubUrl = computed(() => {
  const data = props.project.github_data
  return data?.html_url || `https://github.com/${props.project.owner_name}/${props.project.repo_name}`
})

const formattedDate = computed(() => {
  if (!props.project.repo_updated_at) return 'unknown'
  return new Date(props.project.repo_updated_at).toLocaleDateString()
})

const truncatedReadme = computed(() => {
  const readme = props.project.full_readme || ''
  return readme.length > 200 ? readme.slice(0, 200) + '…' : readme
})
</script>

<style scoped>
.project-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  overflow: hidden;
  transition: transform 0.1s ease;
}
.project-card:hover {
  transform: translateY(-2px);
}
.card-header {
  padding: 1rem 1rem 0.5rem;
  border-bottom: 1px solid #edf2f7;
}
.card-header h3 {
  margin: 0 0 0.25rem;
  font-size: 1.1rem;
}
.card-header a {
  text-decoration: none;
  color: #2563eb;
}
.meta {
  font-size: 0.8rem;
  color: #64748b;
}
.card-body {
  padding: 1rem;
}
.description {
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
  color: #334155;
}
.readme-preview {
  background: #f8fafc;
  padding: 0.75rem;
  border-radius: 8px;
  font-size: 0.8rem;
  color: #1e293b;
}
.readme { margin: 0; white-space: pre-wrap; }
.card-footer {
  padding: 0.75rem 1rem;
  background: #f9fafb;
  font-size: 0.7rem;
  color: #6c757d;
  border-top: 1px solid #edf2f7;
}
</style>
