import { defineStore } from 'pinia'
import { ref } from 'vue'
import { login, getCurrentUser } from '@/api/auth'
import { ElMessage } from 'element-plus'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)

  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  const setUserInfo = (info) => {
    userInfo.value = info
  }

  const userLogin = async (loginForm) => {
    try {
      const res = await login(loginForm)
      setToken(res.access_token)
      await getUserInfo()
      ElMessage.success('登录成功')
      return true
    } catch (error) {
      return false
    }
  }

  const getUserInfo = async () => {
    try {
      const res = await getCurrentUser()
      setUserInfo(res)
      return res
    } catch (error) {
      return null
    }
  }

  const logout = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }

  return {
    token,
    userInfo,
    setToken,
    setUserInfo,
    userLogin,
    getUserInfo,
    logout
  }
})
