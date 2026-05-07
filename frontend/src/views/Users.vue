<template>
  <div class="users">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加用户
          </el-button>
        </div>
      </template>

      <el-table :data="users" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="department" label="所属科室" width="150">
          <template #default="{ row }">
            {{ row.department || '管理员' }}
          </template>
        </el-table-column>
        <el-table-column prop="role" label="角色" width="120">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'success'">
              {{ row.role === 'admin' ? '管理员' : '普通用户' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" :formatter="formatDate" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="showEditDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑用户对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑用户' : '添加用户'" width="500px">
      <el-form :model="userForm" :rules="rules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" placeholder="请输入用户名" :disabled="isEdit" />
        </el-form-item>
        <el-form-item label="密码" prop="password" v-if="!isEdit">
          <el-input v-model="userForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" placeholder="请选择角色" style="width: 100%;">
            <el-option label="管理员" value="admin" />
            <el-option label="普通用户" value="user" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属科室" prop="department" v-if="userForm.role === 'user'">
          <el-select v-model="userForm.department" placeholder="请选择科室" style="width: 100%;">
            <el-option label="地面科" value="地面科" />
            <el-option label="指挥科" value="指挥科" />
            <el-option label="作业科" value="作业科" />
            <el-option label="办公室" value="办公室" />
            <el-option label="保障科" value="保障科" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="isEdit ? handleEditUser() : handleAddUser()">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getUsers, register, updateUser, deleteUser } from '@/api/auth'
import { ElMessage, ElMessageBox } from 'element-plus'

const users = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const userFormRef = ref(null)
const isEdit = ref(false)

const userForm = ref({
  id: null,
  username: '',
  password: '',
  role: 'user',
  department: ''
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
  department: [{ required: true, message: '请选择科室', trigger: 'change' }]
}

const formatDate = (row) => {
  return new Date(row.created_at).toLocaleString('zh-CN')
}

const loadUsers = async () => {
  loading.value = true
  try {
    const data = await getUsers()
    users.value = data
  } catch (error) {
    console.error('加载用户列表失败:', error)
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  isEdit.value = false
  userForm.value = {
    id: null,
    username: '',
    password: '',
    role: 'user',
    department: ''
  }
  dialogVisible.value = true
}

const showEditDialog = (row) => {
  isEdit.value = true
  userForm.value = {
    id: row.id,
    username: row.username,
    password: '',
    role: row.role,
    department: row.department || ''
  }
  dialogVisible.value = true
}

const handleAddUser = async () => {
  await userFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await register(userForm.value)
        ElMessage.success('添加用户成功')
        dialogVisible.value = false
        loadUsers()
      } catch (error) {
        console.error('添加用户失败:', error)
      }
    }
  })
}

const handleEditUser = async () => {
  await userFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await updateUser(userForm.value.id, {
          role: userForm.value.role,
          department: userForm.value.department
        })
        ElMessage.success('修改用户成功')
        dialogVisible.value = false
        loadUsers()
      } catch (error) {
        console.error('修改用户失败:', error)
      }
    }
  })
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该用户吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteUser(row.id)
    ElMessage.success('删除成功')
    loadUsers()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除用户失败:', error)
    }
  }
}

onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
