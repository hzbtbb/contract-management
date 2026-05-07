import request from '@/utils/request'

export const uploadContract = (data) => {
  return request({
    url: '/contracts/upload',
    method: 'post',
    data,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

export const getContracts = (params) => {
  return request({
    url: '/contracts/',
    method: 'get',
    params
  })
}

export const getContract = (id) => {
  return request({
    url: `/contracts/${id}`,
    method: 'get'
  })
}

export const updateContract = (id, data) => {
  return request({
    url: `/contracts/${id}`,
    method: 'put',
    data
  })
}

export const deleteContract = (id) => {
  return request({
    url: `/contracts/${id}`,
    method: 'delete'
  })
}

export const getDashboardStats = (params) => {
  return request({
    url: '/contracts/dashboard/stats',
    method: 'get',
    params
  })
}

export const downloadContractRecord = (id) => {
  return request({
    url: `/contracts/${id}/download`,
    method: 'post'
  })
}

export const downloadContractFile = (id) => {
  return request({
    url: `/contracts/${id}/download`,
    method: 'get',
    responseType: 'blob'
  })
}
