<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="sidebar">
      <div class="logo">
        <h3>合同管理系统</h3>
      </div>
      <el-menu
        :default-active="activeMenu"
        router
        class="sidebar-menu"
      >
        <el-menu-item index="/dashboard">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表板</span>
        </el-menu-item>
        <el-menu-item index="/contracts">
          <el-icon><Document /></el-icon>
          <span>合同管理</span>
        </el-menu-item>
        <el-menu-item index="/upload">
          <el-icon><Upload /></el-icon>
          <span>上传合同</span>
        </el-menu-item>
        <el-menu-item v-if="userStore.userInfo?.role === 'admin'" index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <div class="header-content">
          <span class="title">{{ currentTitle }}</span>
          <div class="user-info">
            <el-dropdown @command="handleCommand" class="user-dropdown">
              <span class="user-name">
                <el-icon class="user-icon"><User /></el-icon>
                {{ userStore.userInfo?.username }}
                <el-icon class="arrow-icon"><arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu class="user-menu">
                  <el-dropdown-item disabled>
                    <div class="user-dept">{{ userStore.userInfo?.department || '管理员' }}</div>
                  </el-dropdown-item>
                  <el-dropdown-item divided command="logout">
                    <el-icon><SwitchButton /></el-icon>
                    退出登录
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const activeMenu = computed(() => route.path)
const currentTitle = computed(() => route.meta.title || '')

const handleCommand = (command) => {
  if (command === 'logout') {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background: #f5f5f7;
}

.sidebar {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.04);
}

.logo {
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.logo h3 {
  margin: 0;
  color: #1d1d1f;
  font-size: 17px;
  font-weight: 600;
  letter-spacing: -0.3px;
}

.sidebar-menu {
  border-right: none;
  background: transparent;
  padding: 12px;
}

.sidebar-menu :deep(.el-menu-item) {
  height: 44px;
  line-height: 44px;
  border-radius: 10px;
  margin-bottom: 4px;
  color: #1d1d1f;
  transition: all 0.3s;
}

.sidebar-menu :deep(.el-menu-item:hover) {
  background: rgba(0, 0, 0, 0.04);
  color: #0071e3;
}

.sidebar-menu :deep(.el-menu-item.is-active) {
  background: #0071e3;
  color: #fff;
}

.sidebar-menu :deep(.el-menu-item .el-icon) {
  font-size: 18px;
}

.header {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  padding: 0 24px;
  height: 64px;
}

.header-content {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.title {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
  letter-spacing: -0.5px;
}

.user-dropdown {
  cursor: pointer;
}

.user-name {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  background: #f5f5f7;
  border-radius: 20px;
  color: #1d1d1f;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s;
}

.user-name:hover {
  background: #e8e8ed;
}

.user-icon {
  font-size: 16px;
}

.arrow-icon {
  font-size: 12px;
  color: #86868b;
}

.user-menu :deep(.el-dropdown-menu__item) {
  padding: 12px 20px;
}

.user-dept {
  color: #86868b;
  font-size: 13px;
}

.main-content {
  background: #f5f5f7;
  padding: 24px;
  overflow-y: auto;
}

.main-content :deep(.el-card) {
  border-radius: 16px;
  border: none;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
}

.main-content :deep(.el-card__header) {
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  padding: 20px 24px;
}

.main-content :deep(.el-card__body) {
  padding: 24px;
}
</style>
