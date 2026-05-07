<template>
  <div class="contracts">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>合同列表</span>
          <el-button type="primary" class="upload-btn" @click="$router.push('/upload')">
            <el-icon><Plus /></el-icon>
            上传合同
          </el-button>
        </div>
      </template>

      <el-form :inline="true" :model="searchForm" class="search-form" v-if="userStore.userInfo?.role === 'admin'">
        <el-form-item label="科室">
          <el-select v-model="searchForm.department" placeholder="全部科室" clearable @change="loadContracts">
            <el-option label="全部" value="" />
            <el-option label="地面科" value="地面科" />
            <el-option label="指挥科" value="指挥科" />
            <el-option label="作业科" value="作业科" />
            <el-option label="办公室" value="办公室" />
            <el-option label="保障科" value="保障科" />
          </el-select>
        </el-form-item>
      </el-form>

      <el-table :data="contracts" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="合同名称" min-width="180" />
        <el-table-column prop="department" label="所属科室" width="120" />
        <el-table-column prop="amount" label="合同金额" width="130" :formatter="formatAmount" />
        <el-table-column prop="execution_date" label="履行时间" width="120" :formatter="formatExecutionDate" />
        <el-table-column prop="download_count" label="下载次数" width="100" />
        <el-table-column prop="uploader_name" label="上传人" width="100" />
        <el-table-column prop="created_at" label="上传时间" width="180" :formatter="formatDate" />
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="success" size="small" @click="handleDownload(row)">
              <el-icon><Download /></el-icon>
              下载
            </el-button>
            <el-button type="primary" size="small" @click="viewContract(row)">查看</el-button>
            <el-button type="warning" size="small" @click="editContract(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 查看合同对话框 -->
    <el-dialog v-model="viewDialogVisible" title="合同详情" width="800px" class="apple-dialog">
      <el-descriptions :column="2" border v-if="currentContract">
        <el-descriptions-item label="合同名称">{{ currentContract.name }}</el-descriptions-item>
        <el-descriptions-item label="合同金额">{{ formatAmount(currentContract) }}</el-descriptions-item>
        <el-descriptions-item label="所属科室">{{ currentContract.department }}</el-descriptions-item>
        <el-descriptions-item label="上传人">{{ currentContract.uploader_name }}</el-descriptions-item>
        <el-descriptions-item label="履行时间">{{ formatExecutionDate(currentContract) }}</el-descriptions-item>
        <el-descriptions-item label="下载次数">{{ currentContract.download_count }}</el-descriptions-item>
        <el-descriptions-item label="上传时间">{{ formatDate(currentContract) }}</el-descriptions-item>
        <el-descriptions-item label="文件类型">{{ currentContract.file_type }}</el-descriptions-item>
        <el-descriptions-item label="描述" :span="2">{{ currentContract.description || '无' }}</el-descriptions-item>
      </el-descriptions>
      <div style="margin-top: 20px;" v-if="currentContract">
        <el-button type="primary" @click="handleDownload(currentContract)">
          <el-icon><Download /></el-icon>
          下载文件
        </el-button>
      </div>
    </el-dialog>

    <!-- 编辑合同对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑合同" width="500px" class="apple-dialog">
      <el-form :model="editForm" label-width="100px">
        <el-form-item label="合同名称">
          <el-input v-model="editForm.name" />
        </el-form-item>
        <el-form-item label="合同金额">
          <el-input-number v-model="editForm.amount" :min="0" :precision="2" style="width: 100%;" />
        </el-form-item>
        <el-form-item label="履行开始">
          <el-date-picker
            v-model="editForm.execution_start_date"
            type="date"
            placeholder="请选择开始时间"
            style="width: 100%;"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="履行结束">
          <el-date-picker
            v-model="editForm.execution_end_date"
            type="date"
            placeholder="请选择结束时间"
            style="width: 100%;"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="editForm.description" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUpdate">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getContracts, deleteContract, updateContract, downloadContractFile } from '@/api/contract'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/store/user'

const userStore = useUserStore()
const contracts = ref([])
const loading = ref(false)
const searchForm = ref({
  department: ''
})

const viewDialogVisible = ref(false)
const editDialogVisible = ref(false)
const currentContract = ref(null)
const editForm = ref({
  name: '',
  amount: 0,
  description: '',
  execution_date: ''
})

const formatAmount = (row) => {
  return '¥' + row.amount.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatDate = (row) => {
  return new Date(row.created_at).toLocaleString('zh-CN')
}

const formatExecutionDate = (row) => {
  if (!row.execution_start_date || !row.execution_end_date) return '未设置'
  const start = new Date(row.execution_start_date).toLocaleDateString('zh-CN')
  const end = new Date(row.execution_end_date).toLocaleDateString('zh-CN')
  return `${start} 至 ${end}`
}

const loadContracts = async () => {
  loading.value = true
  try {
    const params = {}
    if (searchForm.value.department) {
      params.department = searchForm.value.department
    }
    const data = await getContracts(params)
    contracts.value = data
  } catch (error) {
    console.error('加载合同列表失败:', error)
  } finally {
    loading.value = false
  }
}

const viewContract = (row) => {
  currentContract.value = row
  viewDialogVisible.value = true
}

const editContract = (row) => {
  currentContract.value = row
  editForm.value = {
    name: row.name,
    amount: row.amount,
    description: row.description || '',
    execution_start_date: row.execution_start_date ? new Date(row.execution_start_date).toISOString().split('T')[0] : '',
    execution_end_date: row.execution_end_date ? new Date(row.execution_end_date).toISOString().split('T')[0] : ''
  }
  editDialogVisible.value = true
}

const handleUpdate = async () => {
  try {
    await updateContract(currentContract.value.id, editForm.value)
    ElMessage.success('更新成功')
    editDialogVisible.value = false
    loadContracts()
  } catch (error) {
    console.error('更新失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这个合同吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await deleteContract(row.id)
    ElMessage.success('删除成功')
    loadContracts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
    }
  }
}

const handleDownload = async (row) => {
  try {
    const response = await downloadContractFile(row.id)
    const url = window.URL.createObjectURL(new Blob([response]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', row.name + (row.file_type || '.pdf'))
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('下载成功')
    loadContracts()
  } catch (error) {
    console.error('下载失败:', error)
    ElMessage.error('下载失败')
  }
}

onMounted(() => {
  loadContracts()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header span {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
}

.upload-btn {
  background: #0071e3;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-weight: 500;
  transition: all 0.3s;
}

.upload-btn:hover {
  background: #0077ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
}

.search-form {
  margin-bottom: 20px;
}

.search-form :deep(.el-select) {
  width: 200px;
}

.search-form :deep(.el-input__wrapper) {
  border-radius: 10px;
  background: #f5f5f7;
  border: 1px solid transparent;
  transition: all 0.3s;
}

.search-form :deep(.el-input__wrapper:hover) {
  background: #e8e8ed;
}

.search-form :deep(.el-input__wrapper.is-focus) {
  background: #fff;
  border-color: #0071e3;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.el-table th) {
  background: #f5f5f7;
  color: #1d1d1f;
  font-weight: 600;
}

:deep(.el-table td) {
  color: #1d1d1f;
}

:deep(.el-button) {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s;
}

:deep(.el-button--success) {
  background: #34c759;
  border-color: #34c759;
}

:deep(.el-button--success:hover) {
  background: #30b350;
  transform: translateY(-1px);
}

:deep(.el-button--primary) {
  background: #0071e3;
  border-color: #0071e3;
}

:deep(.el-button--primary:hover) {
  background: #0077ed;
  transform: translateY(-1px);
}

:deep(.el-button--warning) {
  background: #ff9500;
  border-color: #ff9500;
}

:deep(.el-button--warning:hover) {
  background: #ff9f0a;
  transform: translateY(-1px);
}

:deep(.el-button--danger) {
  background: #ff3b30;
  border-color: #ff3b30;
}

:deep(.el-button--danger:hover) {
  background: #ff453a;
  transform: translateY(-1px);
}

.apple-dialog :deep(.el-dialog) {
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}

.apple-dialog :deep(.el-dialog__header) {
  padding: 24px 24px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.apple-dialog :deep(.el-dialog__title) {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
}

.apple-dialog :deep(.el-dialog__body) {
  padding: 24px;
}

.apple-dialog :deep(.el-descriptions__label) {
  background: #f5f5f7;
  color: #1d1d1f;
  font-weight: 500;
}
</style>
