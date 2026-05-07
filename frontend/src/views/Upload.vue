<template>
  <div class="upload">
    <el-card>
      <template #header>
        <span>上传合同</span>
      </template>

      <el-form :model="uploadForm" :rules="rules" ref="uploadFormRef" label-width="120px">
        <el-form-item label="合同名称" prop="name">
          <el-input v-model="uploadForm.name" placeholder="请输入合同名称" />
        </el-form-item>

        <el-form-item label="合同金额" prop="amount">
          <el-input-number v-model="uploadForm.amount" :min="0" :precision="2" placeholder="请输入合同金额" style="width: 100%;" />
        </el-form-item>

        <el-form-item label="所属科室" prop="department">
          <el-select v-model="uploadForm.department" placeholder="请选择科室" style="width: 100%;" :disabled="!isAdmin">
            <el-option label="地面科" value="地面科" />
            <el-option label="指挥科" value="指挥科" />
            <el-option label="作业科" value="作业科" />
            <el-option label="办公室" value="办公室" />
            <el-option label="保障科" value="保障科" />
          </el-select>
        </el-form-item>

        <el-form-item label="甲方" prop="party_a">
          <el-input v-model="uploadForm.party_a" placeholder="请输入甲方名称" />
        </el-form-item>

        <el-form-item label="乙方" prop="party_b">
          <el-input v-model="uploadForm.party_b" placeholder="请输入乙方名称" />
        </el-form-item>

        <el-form-item label="合同签订日期" prop="signing_date">
          <el-date-picker
            v-model="uploadForm.signing_date"
            type="date"
            placeholder="请选择合同签订日期"
            style="width: 100%;"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <el-form-item label="履行时间" prop="execution_dates">
          <el-date-picker
            v-model="uploadForm.execution_dates"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            style="width: 100%;"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>

        <el-form-item label="合同文件" prop="file">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            :on-change="handleFileChange"
            :on-exceed="handleExceed"
            accept=".pdf,.jpg,.jpeg,.png"
            drag
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              将文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 PDF、JPG、PNG 格式
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit" :loading="uploading">
            <el-icon><Upload /></el-icon>
            提交上传
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/store/user'
import { uploadContract } from '@/api/contract'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const uploadFormRef = ref(null)
const uploadRef = ref(null)
const uploading = ref(false)

const uploadForm = ref({
  name: '',
  amount: 0,
  department: '',
  file: null,
  party_a: '',
  party_b: '',
  signing_date: '',
  execution_dates: []
})

const isAdmin = computed(() => userStore.userInfo?.role === 'admin')

const rules = {
  name: [{ required: true, message: '请输入合同名称', trigger: 'blur' }],
  amount: [{ required: true, message: '请输入合同金额', trigger: 'blur' }],
  department: [{ required: true, message: '请选择科室', trigger: 'change' }],
  party_a: [{ required: true, message: '请输入甲方名称', trigger: 'blur' }],
  party_b: [{ required: true, message: '请输入乙方名称', trigger: 'blur' }],
  signing_date: [{ required: true, message: '请选择合同签订日期', trigger: 'change' }],
  execution_dates: [{ required: true, message: '请选择履行时间', trigger: 'change' }],
  file: [{ required: true, message: '请上传合同文件', trigger: 'change' }]
}

const handleFileChange = (file) => {
  uploadForm.value.file = file.raw
}

const handleExceed = () => {
  ElMessage.warning('只能上传一个文件')
}

const handleSubmit = async () => {
  await uploadFormRef.value.validate(async (valid) => {
    if (valid) {
      if (!uploadForm.value.file) {
        ElMessage.error('请选择要上传的文件')
        return
      }

      uploading.value = true
      try {
        const formData = new FormData()
        formData.append('name', uploadForm.value.name)
        formData.append('amount', uploadForm.value.amount)
        formData.append('department', uploadForm.value.department)
        formData.append('party_a', uploadForm.value.party_a)
        formData.append('party_b', uploadForm.value.party_b)
        formData.append('signing_date', uploadForm.value.signing_date)
        formData.append('execution_start_date', uploadForm.value.execution_dates[0])
        formData.append('execution_end_date', uploadForm.value.execution_dates[1])
        formData.append('file', uploadForm.value.file)

        await uploadContract(formData)
        ElMessage.success('上传成功')
        handleReset()
        router.push('/contracts')
      } catch (error) {
        console.error('上传失败:', error)
      } finally {
        uploading.value = false
      }
    }
  })
}

const handleReset = () => {
  uploadFormRef.value.resetFields()
  uploadRef.value.clearFiles()
  uploadForm.value.file = null
  uploadForm.value.execution_dates = []
}

onMounted(() => {
  if (!isAdmin.value && userStore.userInfo?.department) {
    uploadForm.value.department = userStore.userInfo.department
  }
})
</script>

<style scoped>
.upload {
  max-width: 800px;
}

:deep(.el-card__header) {
  padding: 24px;
}

:deep(.el-card__header span) {
  font-size: 20px;
  font-weight: 600;
  color: #1d1d1f;
}

:deep(.el-form-item__label) {
  color: #1d1d1f;
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  background: #f5f5f7;
  border: 1px solid transparent;
  transition: all 0.3s;
}

:deep(.el-input__wrapper:hover) {
  background: #e8e8ed;
}

:deep(.el-input__wrapper.is-focus) {
  background: #fff;
  border-color: #0071e3;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

:deep(.el-textarea__inner) {
  border-radius: 10px;
  background: #f5f5f7;
  border: 1px solid transparent;
  transition: all 0.3s;
}

:deep(.el-textarea__inner:hover) {
  background: #e8e8ed;
}

:deep(.el-textarea__inner:focus) {
  background: #fff;
  border-color: #0071e3;
  box-shadow: 0 0 0 4px rgba(0, 113, 227, 0.1);
}

.el-upload {
  width: 100%;
}

:deep(.el-upload-dragger) {
  width: 100%;
  border-radius: 12px;
  border: 2px dashed #d1d1d6;
  background: #f5f5f7;
  transition: all 0.3s;
}

:deep(.el-upload-dragger:hover) {
  border-color: #0071e3;
  background: #fff;
}

:deep(.el-button--primary) {
  background: #0071e3;
  border: none;
  border-radius: 10px;
  height: 44px;
  font-weight: 500;
  transition: all 0.3s;
}

:deep(.el-button--primary:hover) {
  background: #0077ed;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3);
}

:deep(.el-button--default) {
  border-radius: 10px;
  height: 44px;
  background: #f5f5f7;
  border: 1px solid transparent;
  color: #1d1d1f;
  font-weight: 500;
}

:deep(.el-button--default:hover) {
  background: #e8e8ed;
}
</style>
