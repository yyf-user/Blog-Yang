<template>
  <div class="api-paths-view">
    <h2>API接口路径一览</h2>
    
    <div class="section-description">
      该页面展示了系统所有可用的API接口路径，方便管理员查阅和使用。
    </div>
    
    <div class="search-filter">
      <div class="search-box">
        <search-icon class="search-icon" />
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索API路径..." 
          @input="filterApiPaths"
        />
      </div>
      
      <div class="filter-methods">
        <button 
          class="method-filter" 
          :class="{ active: selectedMethods.includes('GET') }"
          @click="toggleMethod('GET')"
        >
          GET
        </button>
        <button 
          class="method-filter" 
          :class="{ active: selectedMethods.includes('POST') }"
          @click="toggleMethod('POST')"
        >
          POST
        </button>
        <button 
          class="method-filter" 
          :class="{ active: selectedMethods.includes('PUT') }"
          @click="toggleMethod('PUT')"
        >
          PUT
        </button>
        <button 
          class="method-filter" 
          :class="{ active: selectedMethods.includes('DELETE') }"
          @click="toggleMethod('DELETE')"
        >
          DELETE
        </button>
      </div>
    </div>
    
    <div class="api-groups">
      <div v-for="group in filteredApiGroups" :key="group.name" class="api-group">
        <div class="group-header" @click="toggleGroup(group.name)">
          <h3>{{ group.name }}</h3>
          <chevron-down-icon 
            class="group-icon" 
            :class="{ 'rotate': expandedGroups.includes(group.name) }" 
          />
        </div>
        
        <div class="group-content" v-show="expandedGroups.includes(group.name)">
          <table class="api-table">
            <thead>
              <tr>
                <th class="method-col">方法</th>
                <th class="path-col">路径</th>
                <th class="desc-col">描述</th>
                <th class="auth-col">认证</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(api, index) in group.apis" :key="index">
                <td class="method-cell">
                  <span class="method-badge" :class="api.method.toLowerCase()">
                    {{ api.method }}
                  </span>
                </td>
                <td class="path-cell">
                  <code>{{ api.path }}</code>
                </td>
                <td class="desc-cell">
                  {{ api.description }}
                </td>
                <td class="auth-cell">
                  <lock-icon v-if="api.requiresAuth" class="auth-icon" />
                  <check-icon v-else class="public-icon" />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { 
  Search as SearchIcon,
  ChevronDown as ChevronDownIcon,
  Lock as LockIcon,
  Check as CheckIcon
} from 'lucide-vue-next';

// API路径数据结构
interface ApiPath {
  method: string;
  path: string;
  description: string;
  requiresAuth: boolean;
}

interface ApiGroup {
  name: string;
  apis: ApiPath[];
}

// 状态
const searchQuery = ref('');
const selectedMethods = ref<string[]>(['GET', 'POST', 'PUT', 'DELETE']);
const expandedGroups = ref<string[]>([]);
const apiGroups = ref<ApiGroup[]>([]);

// 初始化API组
onMounted(() => {
  // 这里定义所有API路径
  apiGroups.value = [
    {
      name: '认证相关',
      apis: [
        { 
          method: 'POST', 
          path: '/api/auth/login', 
          description: '用户登录，获取JWT令牌', 
          requiresAuth: false 
        },
        { 
          method: 'POST', 
          path: '/api/auth/register', 
          description: '注册新用户', 
          requiresAuth: false 
        }
      ]
    },
    {
      name: '用户相关',
      apis: [
        { 
          method: 'GET', 
          path: '/api/users/me', 
          description: '获取当前用户信息', 
          requiresAuth: true 
        },
        { 
          method: 'PUT', 
          path: '/api/users/me', 
          description: '更新当前用户信息', 
          requiresAuth: true 
        },
        { 
          method: 'PUT', 
          path: '/api/users/me/password', 
          description: '修改当前用户密码', 
          requiresAuth: true 
        },
        { 
          method: 'GET', 
          path: '/api/users', 
          description: '获取所有用户列表（仅管理员）', 
          requiresAuth: true 
        },
        { 
          method: 'GET', 
          path: '/api/users/{user_id}', 
          description: '通过ID获取用户信息（仅管理员）', 
          requiresAuth: true 
        },
        { 
          method: 'PUT', 
          path: '/api/users/{user_id}/role', 
          description: '更新用户角色（仅管理员）', 
          requiresAuth: true 
        }
      ]
    },
    {
      name: '文章相关',
      apis: [
        { 
          method: 'GET', 
          path: '/api/articles', 
          description: '获取文章列表', 
          requiresAuth: false 
        },
        { 
          method: 'POST', 
          path: '/api/articles', 
          description: '创建新文章', 
          requiresAuth: true 
        },
        { 
          method: 'GET', 
          path: '/api/articles/{article_id}', 
          description: '通过ID获取文章详情', 
          requiresAuth: false 
        },
        { 
          method: 'GET', 
          path: '/api/articles/by-slug/{slug}', 
          description: '通过slug获取文章详情', 
          requiresAuth: false 
        },
        { 
          method: 'PUT', 
          path: '/api/articles/{article_id}', 
          description: '更新文章', 
          requiresAuth: true 
        },
        { 
          method: 'PUT', 
          path: '/api/articles/{article_id}/publish', 
          description: '发布/取消发布文章', 
          requiresAuth: true 
        },
        { 
          method: 'DELETE', 
          path: '/api/articles/{article_id}', 
          description: '删除文章', 
          requiresAuth: true 
        }
      ]
    },
    {
      name: '标签相关',
      apis: [
        { 
          method: 'GET', 
          path: '/api/tags', 
          description: '获取标签列表', 
          requiresAuth: false 
        },
        { 
          method: 'POST', 
          path: '/api/tags', 
          description: '创建新标签', 
          requiresAuth: true 
        },
        { 
          method: 'GET', 
          path: '/api/tags/{tag_id}', 
          description: '通过ID获取标签详情', 
          requiresAuth: false 
        },
        { 
          method: 'DELETE', 
          path: '/api/tags/{tag_id}', 
          description: '删除标签', 
          requiresAuth: true 
        }
      ]
    },
    {
      name: '项目相关',
      apis: [
        { 
          method: 'GET', 
          path: '/api/projects', 
          description: '获取项目列表', 
          requiresAuth: false 
        },
        { 
          method: 'POST', 
          path: '/api/projects', 
          description: '创建新项目', 
          requiresAuth: true 
        },
        { 
          method: 'GET', 
          path: '/api/projects/{project_id}', 
          description: '通过ID获取项目详情', 
          requiresAuth: false 
        },
        { 
          method: 'GET', 
          path: '/api/projects/by-slug/{slug}', 
          description: '通过slug获取项目详情', 
          requiresAuth: false 
        },
        { 
          method: 'PUT', 
          path: '/api/projects/{project_id}', 
          description: '更新项目', 
          requiresAuth: true 
        },
        { 
          method: 'PUT', 
          path: '/api/projects/{project_id}/stats', 
          description: '更新项目统计信息', 
          requiresAuth: true 
        },
        { 
          method: 'DELETE', 
          path: '/api/projects/{project_id}', 
          description: '删除项目', 
          requiresAuth: true 
        }
      ]
    },
    {
      name: '消息相关',
      apis: [
        { 
          method: 'GET', 
          path: '/api/messages', 
          description: '获取消息列表', 
          requiresAuth: true 
        },
        { 
          method: 'POST', 
          path: '/api/messages', 
          description: '发送新消息（联系表单）', 
          requiresAuth: false 
        },
        { 
          method: 'GET', 
          path: '/api/messages/{message_id}', 
          description: '通过ID获取消息详情', 
          requiresAuth: true 
        },
        { 
          method: 'PUT', 
          path: '/api/messages/{message_id}', 
          description: '更新消息（标记已读）', 
          requiresAuth: true 
        },
        { 
          method: 'DELETE', 
          path: '/api/messages/{message_id}', 
          description: '删除消息', 
          requiresAuth: true 
        }
      ]
    },
    {
      name: '统计相关',
      apis: [
        { 
          method: 'GET', 
          path: '/api/stats', 
          description: '获取所有统计数据', 
          requiresAuth: false 
        },
        { 
          method: 'GET', 
          path: '/api/stats/dashboard', 
          description: '获取仪表盘统计数据', 
          requiresAuth: true 
        },
        { 
          method: 'GET', 
          path: '/api/stats/api', 
          description: '获取API调用统计信息', 
          requiresAuth: true 
        },
        { 
          method: 'GET', 
          path: '/api/stats/api/trends', 
          description: '获取API调用趋势数据', 
          requiresAuth: true 
        },
        { 
          method: 'GET', 
          path: '/api/stats/api/{endpoint}', 
          description: '获取特定API的调用详情', 
          requiresAuth: true 
        }
      ]
    },
    {
      name: '上传相关',
      apis: [
        { 
          method: 'POST', 
          path: '/api/uploads/image', 
          description: '上传图片', 
          requiresAuth: true 
        }
      ]
    },
    {
      name: '订阅者相关',
      apis: [
        { 
          method: 'GET', 
          path: '/api/subscribers', 
          description: '获取订阅者列表', 
          requiresAuth: true 
        },
        { 
          method: 'POST', 
          path: '/api/subscribers', 
          description: '添加新订阅者', 
          requiresAuth: false 
        },
        { 
          method: 'DELETE', 
          path: '/api/subscribers/{subscriber_id}', 
          description: '删除订阅者', 
          requiresAuth: true 
        },
        { 
          method: 'PUT', 
          path: '/api/subscribers/{subscriber_id}/status', 
          description: '更新订阅者状态', 
          requiresAuth: true 
        }
      ]
    }
  ];
  
  // 默认展开第一个组
  if (apiGroups.value.length > 0) {
    expandedGroups.value = [apiGroups.value[0].name];
  }
});

// 过滤API路径
const filterApiPaths = () => {
  // 搜索查询处理在计算属性中完成
};

// 切换HTTP方法筛选
const toggleMethod = (method: string) => {
  const index = selectedMethods.value.indexOf(method);
  if (index === -1) {
    selectedMethods.value.push(method);
  } else {
    selectedMethods.value.splice(index, 1);
  }
};

// 切换组的展开/折叠状态
const toggleGroup = (groupName: string) => {
  const index = expandedGroups.value.indexOf(groupName);
  if (index === -1) {
    expandedGroups.value.push(groupName);
  } else {
    expandedGroups.value.splice(index, 1);
  }
};

// 过滤后的API组
const filteredApiGroups = computed(() => {
  return apiGroups.value
    .map(group => {
      // 过滤组内的API
      const filteredApis = group.apis.filter(api => {
        // 方法过滤
        if (!selectedMethods.value.includes(api.method)) {
          return false;
        }
        
        // 搜索过滤
        if (searchQuery.value) {
          const query = searchQuery.value.toLowerCase();
          return (
            api.path.toLowerCase().includes(query) ||
            api.description.toLowerCase().includes(query)
          );
        }
        
        return true;
      });
      
      // 返回过滤后的组
      return {
        ...group,
        apis: filteredApis
      };
    })
    .filter(group => group.apis.length > 0); // 只保留有API的组
});
</script>

<style scoped>
.api-paths-view {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.api-paths-view h2 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #1e293b;
  font-size: 1.25rem;
}

.section-description {
  color: #64748b;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}

/* 搜索和过滤 */
.search-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.search-box {
  position: relative;
  width: 300px;
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1rem;
  height: 1rem;
  color: #64748b;
}

.search-box input {
  width: 100%;
  padding: 0.5rem 1rem 0.5rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.filter-methods {
  display: flex;
  gap: 0.5rem;
}

.method-filter {
  padding: 0.4rem 0.75rem;
  border-radius: 0.375rem;
  font-size: 0.75rem;
  font-weight: 600;
  background-color: #f1f5f9;
  color: #64748b;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.2s;
}

.method-filter.active {
  background-color: #3b82f6;
  color: white;
  border-color: #2563eb;
}

.method-filter:hover:not(.active) {
  background-color: #e2e8f0;
}

/* API分组 */
.api-groups {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.api-group {
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  overflow: hidden;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background-color: #f8fafc;
  cursor: pointer;
  border-bottom: 1px solid #e2e8f0;
}

.group-header:hover {
  background-color: #f1f5f9;
}

.group-header h3 {
  margin: 0;
  font-size: 1rem;
  color: #1e293b;
}

.group-icon {
  width: 1.25rem;
  height: 1.25rem;
  color: #64748b;
  transition: transform 0.3s;
}

.group-icon.rotate {
  transform: rotate(180deg);
}

.group-content {
  overflow-x: auto;
}

/* API表格 */
.api-table {
  width: 100%;
  border-collapse: collapse;
}

.api-table th,
.api-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.api-table th {
  background-color: #f8fafc;
  color: #64748b;
  font-weight: 500;
  font-size: 0.75rem;
  text-transform: uppercase;
}

.api-table tr:last-child td {
  border-bottom: none;
}

.method-col {
  width: 100px;
}

.path-col {
  width: 30%;
}

.desc-col {
  width: 50%;
}

.auth-col {
  width: 80px;
  text-align: center;
}

.method-cell {
  text-align: center;
}

.method-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.method-badge.get {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.method-badge.post {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.method-badge.put {
  background-color: rgba(234, 179, 8, 0.1);
  color: #eab308;
}

.method-badge.delete {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.path-cell code {
  font-family: monospace;
  font-size: 0.875rem;
  background-color: #f1f5f9;
  padding: 0.125rem 0.375rem;
  border-radius: 0.25rem;
  color: #334155;
}

.desc-cell {
  color: #64748b;
  font-size: 0.875rem;
}

.auth-cell {
  text-align: center;
}

.auth-icon {
  width: 1rem;
  height: 1rem;
  color: #ef4444;
}

.public-icon {
  width: 1rem;
  height: 1rem;
  color: #22c55e;
}

@media (max-width: 768px) {
  .search-filter {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .search-box {
    width: 100%;
  }
  
  .method-col {
    width: 80px;
  }
  
  .path-col,
  .desc-col {
    width: auto;
  }
}
</style> 