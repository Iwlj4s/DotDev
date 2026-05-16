import api from './client'

export const fetchProjects = async () => {
  const response = await api.get('/api/v1/projects/')
  return response.data.data
}

export const createProject = async (repoName: string) => {
  const response = await api.post('/api/v1/projects/create', { repo_name: repoName })
  return response.data.data
}
