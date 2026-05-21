import api from './client'

export const fetchUserById = async (userId: number) => {
  const response = await api.get(`/api/v1/users/user/${userId}`)
  return response.data.data
}

export const fetchUserWithProjects = async () => {
  const response = await api.get(`/api/v1/users/me/projects`)
  return response.data.data
}