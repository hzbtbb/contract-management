import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue')
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '仪表板' }
      },
      {
        path: 'contracts',
        name: 'Contracts',
        component: () => import('@/views/Contracts.vue'),
        meta: { title: '合同管理' }
      },
      {
        path: 'upload',
        name: 'Upload',
        component: () => import('@/views/Upload.vue'),
        meta: { title: '上传合同' }
      },
      {
        path: 'users',
        name: 'Users',
        component: () => import('@/views/Users.vue'),
        meta: { title: '用户管理', requireAdmin: true }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()

  if (to.path === '/login') {
    if (userStore.token) {
      next('/')
    } else {
      next()
    }
    return
  }

  if (!userStore.token) {
    next('/login')
    return
  }

  if (!userStore.userInfo) {
    await userStore.getUserInfo()
  }

  if (to.meta.requireAdmin && userStore.userInfo?.role !== 'admin') {
    next('/')
    return
  }

  next()
})

export default router
