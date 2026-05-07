<template>
  <div class="login-container">
    <div class="login-card">
      <div class="card-header">
        <h2>吉林省人工影响天气办公室</h2>
        <h3>合同管理系统</h3>
      </div>
      <el-form :model="loginForm" :rules="rules" ref="loginFormRef" class="login-form">
        <el-form-item prop="username">
          <el-input v-model="loginForm.username" placeholder="用户名" size="large" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="密码" size="large" prefix-icon="Lock" @keyup.enter="handleLogin" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" class="login-btn" @click="handleLogin" :loading="loading">
            登录
          </el-button>
        </el-form-item>
      </el-form>
      <div class="tips">
        <p>默认账号：admin / admin123</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'

const router = useRouter()
const userStore = useUserStore()

const loginFormRef = ref(null)
const loading = ref(false)
const loginForm = ref({
  username: '',
  password: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const handleLogin = async () => {
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      const success = await userStore.userLogin(loginForm.value)
      loading.value = false
      if (success) {
        router.push('/')
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.login-container::before {
  content: '';
  position: absolute;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: float 20s linear infinite;
}

@keyframes float {
  0% { transform: translate(0, 0); }
  100% { transform: translate(-50px, -50px); }
}

.login-card {
  width: 420px;
  padding: 48px 40px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.card-header {
  text-align: center;
  margin-bottom: 40px;
}

.card-header h2 {
  margin: 0 0 8px 0;
  color: #1d1d1f;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.5px;
}

.card-header h3 {
  margin: 0;
  color: #86868b;
  font-size: 17px;
  font-weight: 400;
}

.login-form {
  margin-top: 32px;
}

.login-form :deep(.el-form-item) {
  margin-bottom: 20px;
}

.login-form :deep(.el-input__wrapper) {
  background: #f5f5f7;
  border-radius: 12px;
  box-shadow: none;
  border: 1px solid transparent;
  transition: all 0.3s;
}

.login-form :deep(.el-input__wrapper:hover) {
  background: #e8e8ed;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  background: #fff;
  border-color: #0071e3;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

.login-btn {
  width: 100%;
  height: 48px;
  background: #0071e3;
  border: none;
  border-radius: 12px;
  font-size: 17px;
  font-weight: 500;
  transition: all 0.3s;
}

.login-btn:hover {
  background: #0077ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
}

.login-btn:active {
  transform: translateY(0);
}

.tips {
  margin-top: 24px;
  padding: 16px;
  background: #f5f5f7;
  border-radius: 12px;
  text-align: center;
}

.tips p {
  margin: 0;
  font-size: 13px;
  color: #86868b;
}
</style>
