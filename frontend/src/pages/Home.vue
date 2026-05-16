<template>
  <div class="home">
    <h1>📁 Projects Feed</h1>
    <div v-if="projectStore.isLoading">Loading projects...</div>
    <div v-else-if="projectStore.projects.length === 0">No projects found.</div>
    <div class="projects-grid">
      <ProjectCard v-for="project in projectStore.projects" :key="project.id" :project="project" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useProjectStore } from '@/stores/projectStore'
import ProjectCard from '@/components/ProjectCard.vue'

const projectStore = useProjectStore()

onMounted(() => {
  projectStore.loadProjects()
})
</script>

<style scoped>
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}
</style>
