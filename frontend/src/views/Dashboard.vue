<template>
  <div class="dashboard">
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="24">
        <el-card>
          <el-select v-model="selectedYear" placeholder="选择年份" @change="loadStats" style="width: 200px;">
            <el-option label="全部年份" :value="null" />
            <el-option v-for="year in years" :key="year" :label="year + '年'" :value="year" />
          </el-select>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #409eff;">
              <el-icon :size="30"><Document /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stats.total_contracts }}</div>
              <div class="stat-label">合同数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" style="background-color: #67c23a;">
              <el-icon :size="30"><Money /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ formatAmount(stats.total_amount) }}</div>
              <div class="stat-label">合同总金额</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>各科室合同数量</span>
          </template>
          <div ref="contractChartRef" style="height: 350px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>各科室合同金额</span>
          </template>
          <div ref="amountChartRef" style="height: 350px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>科室统计详情</span>
          </template>
          <el-table :data="departmentList" stripe>
            <el-table-column prop="department" label="科室" />
            <el-table-column prop="count" label="合同数量" />
            <el-table-column prop="amount" label="合同金额" :formatter="formatTableAmount" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { getDashboardStats } from '@/api/contract'
import * as echarts from 'echarts'

const stats = ref({
  total_contracts: 0,
  total_amount: 0,
  department_stats: {}
})

const selectedYear = ref(null)
const years = ref([])
const contractChartRef = ref(null)
const amountChartRef = ref(null)
const departmentList = ref([])

const formatAmount = (amount) => {
  return '¥' + amount.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

const formatTableAmount = (row) => {
  return formatAmount(row.amount)
}

const loadStats = async () => {
  try {
    const params = selectedYear.value ? { year: selectedYear.value } : {}
    const data = await getDashboardStats(params)
    stats.value = data

    departmentList.value = Object.keys(data.department_stats).map(dept => ({
      department: dept,
      count: data.department_stats[dept].count,
      amount: data.department_stats[dept].amount
    }))

    await nextTick()
    initCharts()
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const initCharts = () => {
  const departments = Object.keys(stats.value.department_stats)
  const counts = departments.map(dept => stats.value.department_stats[dept].count)
  const amounts = departments.map(dept => stats.value.department_stats[dept].amount)

  // 合同数量图表
  const contractChart = echarts.init(contractChartRef.value)
  contractChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    xAxis: {
      type: 'category',
      data: departments
    },
    yAxis: {
      type: 'value'
    },
    series: [{
      data: counts,
      type: 'bar',
      itemStyle: {
        color: '#409eff'
      }
    }]
  })

  // 合同金额图表
  const amountChart = echarts.init(amountChartRef.value)
  amountChart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: ¥{c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [{
      type: 'pie',
      radius: '50%',
      data: departments.map((dept, index) => ({
        name: dept,
        value: amounts[index]
      })),
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }]
  })

  window.addEventListener('resize', () => {
    contractChart.resize()
    amountChart.resize()
  })
}

onMounted(() => {
  // 生成年份列表（最近10年）
  const currentYear = new Date().getFullYear()
  for (let i = 0; i < 10; i++) {
    years.value.push(currentYear - i)
  }
  loadStats()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 16px;
  border: 1px solid #e4e7ed;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.stat-card :deep(.el-card__body) {
  padding: 24px;
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-icon .el-icon {
  color: #fff;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

:deep(.el-card__header) {
  padding: 20px 24px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

:deep(.el-card__header span) {
  font-size: 18px;
  font-weight: 600;
  color: #1d1d1f;
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
</style>
