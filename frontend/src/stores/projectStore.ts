import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchProjects, createProject } from '@/api/projects'

export const useProjectStore = defineStore('project', () => {
  const projects = ref([] as any[])
  const isLoading = ref(false)

  const loadProjects = async () => {
    isLoading.value = true
    try {
      projects.value = await fetchProjects()
    } catch (error) {
      console.error('Failed to load projects', error)
      projects.value = []
    } finally {
      isLoading.value = false
    }
  }

  const addProject = async (repoName: string) => {
    try {
      const newProject = await createProject(repoName)
      projects.value = [newProject, ...projects.value]
      return newProject
    } catch (error) {
      console.error('Create project failed', error)
      return null
    }
  }

  return { projects, isLoading, loadProjects, addProject }
})
