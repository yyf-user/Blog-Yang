<template>
  <div class="api-stats-view">
    <h2>API调用统计</h2>
    
    <!-- API路径页面链接 -->
    <div class="api-paths-link">
      <router-link to="/admin/api-paths" class="view-paths-button">
        <list-icon size="16" class="btn-icon" />
        查看所有API路径
      </router-link>
    </div>
    
    <!-- 固定位置的通知提示 -->
    <div v-if="error || success" class="notification-container">
      <div class="notification" :class="{ 'error': error, 'success': success }">
        <div class="notification-icon">
          <check-circle-icon v-if="success" size="20" />
          <alert-circle-icon v-if="error" size="20" />
        </div>
        <div class="notification-content">
          {{ error || success }}
        </div>
        <button class="notification-close" @click="closeNotification">
          <x-icon size="16" />
        </button>
      </div>
    </div>
    
    <div class="stats-overview" v-if="!isLoading">
      <div class="stats-card">
        <div class="stats-icon">
          <activity-icon size="32" />
        </div>
        <div class="stats-info">
          <h3>{{ totalCalls || 0 }}</h3>
          <p>总调用次数</p>
        </div>
      </div>
      
      <div class="stats-card">
        <div class="stats-icon">
          <users-icon size="32" />
        </div>
        <div class="stats-info">
          <h3>{{ uniqueUsers || 0 }}</h3>
          <p>独立用户数</p>
        </div>
      </div>
      
      <div class="stats-card">
        <div class="stats-icon">
          <clock-icon size="32" />
        </div>
        <div class="stats-info">
          <h3>{{ averageResponseTime || 0 }}ms</h3>
          <p>平均响应时间</p>
        </div>
      </div>
      
      <div class="stats-card">
        <div class="stats-icon">
          <alert-triangle-icon size="32" />
        </div>
        <div class="stats-info">
          <h3>{{ errorRate || 0 }}%</h3>
          <p>错误率</p>
        </div>
      </div>
    </div>
    
    <!-- 加载失败重试按钮 -->
    <div v-if="loadFailed" class="retry-container">
      <div class="error-message">加载API统计数据失败</div>
      <button @click="retryLoading" class="retry-button">
        <refresh-cw-icon size="16" class="retry-icon" />
        重新加载
      </button>
    </div>
    
    <div class="chart-container" v-if="!isLoading">
      <div class="chart-header">
        <h3>API调用趋势 (最近7天)</h3>
        <div class="chart-controls">
          <select v-model="chartPeriod" @change="loadApiTrends">
            <option value="day">按天</option>
            <option value="week">按周</option>
            <option value="month">按月</option>
          </select>
        </div>
      </div>
      <div class="chart-content">
        <div class="chart">
          <div 
            v-for="(day, index) in apiTrends" 
            :key="index" 
            class="chart-bar"
            :style="{ height: `${(day.count / maxTrendValue) * 100}%` }"
          >
            <div class="bar-tooltip">
              <div class="tooltip-date">{{ day.date }}</div>
              <div class="tooltip-value">{{ day.count }} 次调用</div>
            </div>
          </div>
        </div>
        <div class="chart-labels">
          <div 
            v-for="(day, index) in apiTrends" 
            :key="index" 
            class="chart-label"
          >
            {{ formatDate(day.date) }}
          </div>
        </div>
      </div>
    </div>
    
    <div class="table-container" v-if="!isLoading">
      <div class="table-header">
        <h3>热门API端点</h3>
        <div class="search-bar">
          <search-icon size="16" class="search-icon" />
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="搜索API端点..." 
            @input="filterEndpoints"
          />
        </div>
      </div>
      
      <table class="data-table">
        <thead>
          <tr>
            <th>端点</th>
            <th>调用次数</th>
            <th>平均响应时间</th>
            <th>错误率</th>
            <th>最后调用</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="endpoint in filteredEndpoints" :key="endpoint.path">
            <td class="endpoint-cell">
              <div class="endpoint-method" :class="endpoint.method.toLowerCase()">{{ endpoint.method }}</div>
              <div class="endpoint-path">{{ endpoint.path }}</div>
            </td>
            <td>{{ endpoint.calls || 0 }}</td>
            <td>{{ endpoint.avg_response_time || 0 }}ms</td>
            <td>
              <span 
                class="error-rate" 
                :class="{
                  'low': endpoint.error_rate < 1,
                  'medium': endpoint.error_rate >= 1 && endpoint.error_rate < 5,
                  'high': endpoint.error_rate >= 5
                }"
              >
                {{ endpoint.error_rate || 0 }}%
              </span>
            </td>
            <td>{{ formatDateTime(endpoint.last_call) }}</td>
          </tr>
          <tr v-if="filteredEndpoints.length === 0">
            <td colspan="5" class="no-data">没有找到匹配的API端点</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="loading-state" v-if="isLoading">
      <div class="loading-spinner large"></div>
      <p>加载中...</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { statsApi } from '@/api';
import { 
  Activity as ActivityIcon,
  Users as UsersIcon,
  Clock as ClockIcon,
  AlertTriangle as AlertTriangleIcon,
  Search as SearchIcon,
  CheckCircle as CheckCircleIcon,
  AlertCircle as AlertCircleIcon,
  X as XIcon,
  List as ListIcon,
  RefreshCw as RefreshCwIcon
} from 'lucide-vue-next';

// 状态
const isLoading = ref(true);
const error = ref('');
const success = ref('');
const totalCalls = ref(0);
const uniqueUsers = ref(0);
const averageResponseTime = ref(0);
const errorRate = ref(0);
const apiEndpoints = ref<any[]>([]);
const filteredEndpoints = ref<any[]>([]);
const apiTrends = ref<any[]>([]);
const chartPeriod = ref('day');
const searchQuery = ref('');
const loadFailed = ref(false); // 新增：用于判断加载是否失败

// 计算属性
const maxTrendValue = computed(() => {
  if (apiTrends.value.length === 0) return 1;
  return Math.max(...apiTrends.value.map(day => day.count));
});

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' });
};

// 格式化日期时间
const formatDateTime = (dateString: string) => {
  if (!dateString) return '未知';
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', { 
    month: 'numeric', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 过滤端点
const filterEndpoints = () => {
  if (!searchQuery.value) {
    filteredEndpoints.value = apiEndpoints.value;
    return;
  }
  
  const query = searchQuery.value.toLowerCase();
  filteredEndpoints.value = apiEndpoints.value.filter(endpoint => 
    endpoint.path.toLowerCase().includes(query) || 
    endpoint.method.toLowerCase().includes(query)
  );
};

// 加载API统计数据
const loadApiStats = async () => {
  try {
    console.log('正在加载API统计数据...');
    const response = await statsApi.getApiStats();
    console.log('API统计数据响应:', response);
    
    const data = response.data;
    
    // 设置统计数据到组件状态
    totalCalls.value = data.total_calls || 0;
    uniqueUsers.value = data.unique_users || 0;
    averageResponseTime.value = data.avg_response_time || 0;
    errorRate.value = data.error_rate || 0;
    
    // 确保endpoints是数组
    if (Array.isArray(data.endpoints)) {
      apiEndpoints.value = data.endpoints;
      console.log(`加载了 ${apiEndpoints.value.length} 个API端点数据`);
    } else {
      apiEndpoints.value = [];
      console.error('endpoints 不是数组:', data.endpoints);
    }
    
    // 初始化过滤后的端点
    filteredEndpoints.value = apiEndpoints.value;
    loadFailed.value = false; // 加载成功，重置失败状态
    
    // 显示成功消息
    if (apiEndpoints.value.length > 0) {
      success.value = `成功加载 ${apiEndpoints.value.length} 个API端点数据`;
      setTimeout(() => { success.value = ''; }, 3000);
    }
  } catch (err: any) {
    console.error('加载API统计数据失败:', err);
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误详情:', err.response.data);
    }
    
    // 设置错误状态
    loadFailed.value = true; // 加载失败，设置失败状态
    error.value = '加载API统计数据失败，请重试';
    
    // 重置值为0，而不是使用模拟数据
    totalCalls.value = 0;
    uniqueUsers.value = 0;
    averageResponseTime.value = 0;
    errorRate.value = 0;
    apiEndpoints.value = [];
    filteredEndpoints.value = [];
  }
};

// 加载API趋势数据
const loadApiTrends = async () => {
  try {
    console.log('正在加载API趋势数据...');
    const response = await statsApi.getApiTrends();
    console.log('API趋势数据响应:', response);
    
    // 确保返回的是数组
    if (Array.isArray(response.data)) {
      apiTrends.value = response.data;
      console.log(`加载了 ${apiTrends.value.length} 天的API趋势数据`);
    } else {
      console.error('API趋势数据不是数组:', response.data);
      // 生成空数据
      apiTrends.value = [];
    }
  } catch (err: any) {
    console.error('加载API趋势数据失败:', err);
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误详情:', err.response.data);
    }
    
    // 生成空趋势数据
    apiTrends.value = [];
    
    // 设置错误消息
    error.value = '加载API趋势数据失败，请重试';
  }
};

// 关闭通知
const closeNotification = () => {
  error.value = '';
  success.value = '';
};

// 重试加载API统计数据
const retryLoading = () => {
  loadApiStats();
};

// 初始化
onMounted(async () => {
  isLoading.value = true;
  
  try {
    await Promise.all([
      loadApiStats(),
      loadApiTrends()
    ]);
  } finally {
    isLoading.value = false;
  }
});
</script>

<style scoped>
.api-stats-view {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.api-stats-view h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #1e293b;
  font-size: 1.25rem;
}

/* API路径页面链接 */
.api-paths-link {
  margin-bottom: 1.5rem;
  text-align: right;
}

.view-paths-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background-color: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.2s ease;
  border: none;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.view-paths-button:hover {
  background-color: #2563eb;
}

.view-paths-button .btn-icon {
  color: white;
}

/* 统计概览 */
.stats-overview {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stats-card {
  background-color: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
}

.stats-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  background-color: rgba(59, 130, 246, 0.1);
  border-radius: 0.5rem;
  color: #3b82f6;
}

.stats-info h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #1e293b;
}

.stats-info p {
  margin: 0.25rem 0 0;
  color: #64748b;
  font-size: 0.875rem;
}

/* 图表 */
.chart-container {
  background-color: white;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  overflow: hidden;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

.chart-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1rem;
}

.chart-controls select {
  padding: 0.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  background-color: white;
  color: #1e293b;
  font-size: 0.875rem;
}

.chart-content {
  padding: 1.5rem;
}

.chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  height: 200px;
  margin-bottom: 1rem;
}

.chart-bar {
  width: 40px;
  background-color: #3b82f6;
  border-radius: 4px 4px 0 0;
  position: relative;
  transition: all 0.3s;
}

.chart-bar:hover {
  background-color: #2563eb;
}

.chart-bar:hover .bar-tooltip {
  display: block;
}

.bar-tooltip {
  display: none;
  position: absolute;
  bottom: calc(100% + 10px);
  left: 50%;
  transform: translateX(-50%);
  background-color: #1e293b;
  color: white;
  padding: 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  white-space: nowrap;
  z-index: 10;
}

.bar-tooltip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border-width: 5px;
  border-style: solid;
  border-color: #1e293b transparent transparent transparent;
}

.tooltip-date {
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.chart-labels {
  display: flex;
  justify-content: space-between;
}

.chart-label {
  width: 40px;
  text-align: center;
  color: #64748b;
  font-size: 0.75rem;
}

/* 表格 */
.table-container {
  background-color: white;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

.table-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1rem;
}

.search-bar {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
}

.search-bar input {
  width: 100%;
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.75rem 1.5rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  background-color: #f8fafc;
  color: #64748b;
  font-weight: 500;
  font-size: 0.875rem;
}

.data-table tr:last-child td {
  border-bottom: none;
}

.endpoint-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.endpoint-method {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.endpoint-method.get {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.endpoint-method.post {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.endpoint-method.put {
  background-color: rgba(234, 179, 8, 0.1);
  color: #eab308;
}

.endpoint-method.delete {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.endpoint-path {
  font-family: monospace;
  font-size: 0.875rem;
}

.error-rate {
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.error-rate.low {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.error-rate.medium {
  background-color: rgba(234, 179, 8, 0.1);
  color: #eab308;
}

.error-rate.high {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.no-data {
  text-align: center;
  color: #94a3b8;
  padding: 2rem 0;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.loading-spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(59, 130, 246, 0.3);
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s ease-in-out infinite;
}

.loading-spinner.large {
  width: 2rem;
  height: 2rem;
  border-width: 3px;
  margin-bottom: 1rem;
}

.loading-state p {
  color: #64748b;
  margin: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-alert {
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background-color: rgba(239, 68, 68, 0.1);
  border-left: 3px solid #ef4444;
  color: #b91c1c;
  border-radius: 0.25rem;
}

/* 加载失败重试样式 */
.retry-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
  background-color: #f8fafc;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  margin-bottom: 2rem;
}

.error-message {
  color: #ef4444;
  font-size: 1rem;
  font-weight: 500;
  margin-bottom: 1rem;
  text-align: center;
}

.retry-button {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  background-color: #3b82f6;
  color: white;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.2s ease;
  border: none;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.retry-button:hover {
  background-color: #2563eb;
}

.retry-button .retry-icon {
  color: white;
}

/* 固定位置的通知样式 */
.notification-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  width: auto;
  max-width: 90%;
}

.notification {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background-color: white;
  animation: fadeIn 0.3s ease-out;
}

.notification.success {
  border-left: 4px solid #22c55e;
}

.notification.error {
  border-left: 4px solid #ef4444;
}

.notification-icon {
  margin-right: 0.75rem;
  display: flex;
  align-items: center;
}

.notification-icon svg {
  color: #22c55e;
}

.notification.error .notification-icon svg {
  color: #ef4444;
}

.notification-content {
  flex: 1;
  font-size: 0.875rem;
  color: #1e293b;
}

.notification-close {
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.75rem;
  border-radius: 0.25rem;
}

.notification-close:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 768px) {
  .stats-overview {
    grid-template-columns: 1fr;
  }
  
  .table-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .search-bar {
    width: 100%;
  }
  
  .data-table {
    display: block;
    overflow-x: auto;
  }
}
</style> 