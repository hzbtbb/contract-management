import request from '@/utils/request'

export const login = (data) => {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

export const getCurrentUser = () => {
  return request({
    url: '/auth/me',
    method: 'get'
  })
}

export const register = (data) => {
  return request({
    url: '/auth/register',
    method: 'post',
    data
  })
}

export const getUsers = () => {
  return request({
    url: '/auth/users',
    method: 'get'
  })
}

export const updateUser = (id, data) => {
  return request({
    url: `/auth/users/${id}`,
    method: 'put',
    data
  })
}

export const deleteUser = (id) => {
  return request({
    url: `/auth/users/${id}`,
    method: 'delete'
  })
}
