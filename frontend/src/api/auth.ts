import api from './client'

export const fetchCurrentUser = async () => {
  const response = await api.get('/api/v1/users/me/')
  return response.data.data
}

export const loginWithCode = async (code: string) => {
  const response = await api.post('/api/v1/github_auth/login', { github_code: code })
  return response.data
}

export const logoutApi = async () => {
  const response = await api.post('/api/v1/users/logout')
  return response.data
}
