<template>
  <div class="articles-manager">
    <div class="content-header">
      <h2>文章管理</h2>
      <router-link to="/admin/articles/create" class="primary-button">
        <plus-icon size="16" />
        新建文章
      </router-link>
    </div>
    
    <div v-if="error" class="error-alert">{{ error }}</div>
    
    <!-- 过滤和搜索 -->
    <div class="filter-container">
      <div class="filter-tabs">
        <button 
          v-for="status in ['all', 'published', 'draft']" 
          :key="status"
          class="filter-tab"
          :class="{ active: filterStatus === status }"
          @click="filterStatus = status"
        >
          {{ statusLabels[status] }}
        </button>
      </div>
      
      <div class="search-bar">
        <search-icon size="18" class="search-icon" />
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索文章..." 
          @input="handleSearch"
        />
      </div>
    </div>
    
    <!-- 文章列表 -->
    <div class="table-container" v-if="!isLoading && filteredArticles.length > 0">
      <table class="data-table">
        <thead>
          <tr>
            <th width="60">ID</th>
            <th>标题</th>
            <th width="100">状态</th>
            <th width="150">发布日期</th>
            <th width="100">阅读量</th>
            <th width="120">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in filteredArticles" :key="article.id">
            <td class="id-cell">{{ article.id }}</td>
            <td class="title-cell">
              <div class="article-title">{{ article.title }}</div>
              <div class="article-slug">{{ article.slug }}</div>
            </td>
            <td>
              <span :class="['status-badge', article.status]">
                {{ statusLabels[article.status] }}
              </span>
            </td>
            <td>{{ formatDate(article.published_at) }}</td>
            <td>{{ article.view_count }}</td>
            <td class="actions">
              <router-link 
                :to="`/admin/articles/edit/${article.id}`" 
                class="icon-button"
                title="编辑"
              >
                <edit-icon size="16" />
              </router-link>
              <a 
                :href="`/articles/${article.slug}`" 
                target="_blank"
                class="icon-button"
                title="查看"
              >
                <eye-icon size="16" />
              </a>
              <button 
                class="icon-button danger"
                title="删除"
                @click="confirmDelete(article)"
              >
                <trash-icon size="16" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- 空状态 -->
    <div class="empty-state" v-else-if="!isLoading && filteredArticles.length === 0">
      <file-text-icon size="48" class="empty-icon" />
      <h3>暂无文章</h3>
      <p v-if="searchQuery">没有找到符合条件的文章，请尝试其他搜索词</p>
      <p v-else-if="filterStatus !== 'all'">没有{{ statusLabels[filterStatus] }}的文章</p>
      <p v-else>开始创建您的第一篇文章吧</p>
      <router-link to="/admin/articles/create" class="primary-button">
        <plus-icon size="16" />
        新建文章
      </router-link>
    </div>
    
    <!-- 加载状态 -->
    <div class="loading-state" v-if="isLoading">
      <div class="loading-spinner large"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 分页控制 -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        class="pagination-button" 
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        <chevron-left-icon size="16" />
      </button>
      
      <div class="page-info">
        第 {{ currentPage }} 页，共 {{ totalPages }} 页
      </div>
      
      <button 
        class="pagination-button" 
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        <chevron-right-icon size="16" />
      </button>
    </div>
    
    <!-- 确认删除弹窗 -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>确认删除</h3>
          <button class="icon-button" @click="showDeleteModal = false">
            <x-icon size="16" />
          </button>
        </div>
        <div class="modal-body">
          <p>确定要删除文章 <strong>{{ articleToDelete?.title }}</strong> 吗？</p>
          <p class="warning-text">此操作无法撤销。</p>
        </div>
        <div class="modal-footer">
          <button class="text-button" @click="showDeleteModal = false">取消</button>
          <button 
            class="danger-button" 
            @click="deleteArticle"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="loading-spinner"></span>
            <span v-else>删除</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { articlesApi } from '@/api';
import { 
  Plus as PlusIcon,
  FileText as FileTextIcon,
  Edit as EditIcon,
  Eye as EyeIcon,
  Trash as TrashIcon,
  Search as SearchIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  X as XIcon
} from 'lucide-vue-next';

// 状态
const articles = ref<any[]>([]);
const isLoading = ref(false);
const error = ref('');
const filterStatus = ref('all'); // all, published, draft
const searchQuery = ref('');
const currentPage = ref(1);
const totalArticles = ref(0);
const pageSize = 10;

// 删除相关
const showDeleteModal = ref(false);
const articleToDelete = ref<any>(null);
const isDeleting = ref(false);

// 状态标签映射
const statusLabels = {
  all: '全部',
  published: '已发布',
  draft: '草稿'
};

// 计算属性
const totalPages = computed(() => Math.ceil(totalArticles.value / pageSize));

const filteredArticles = computed(() => {
  let result = articles.value;
  
  // 按状态过滤
  if (filterStatus.value !== 'all') {
    result = result.filter(article => article.status === filterStatus.value);
  }
  
  // 按搜索词过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(article => 
      article.title.toLowerCase().includes(query) || 
      article.slug.toLowerCase().includes(query)
    );
  }
  
  return result;
});

// 格式化日期
const formatDate = (dateString: string | null) => {
  if (!dateString) return '未发布';
  
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// 加载文章
const loadArticles = async () => {
  isLoading.value = true;
  error.value = '';
  
  try {
    // 构建查询参数
    const params: any = {
      skip: (currentPage.value - 1) * pageSize,
      limit: pageSize
    };
    
    // 如果有过滤条件，添加到参数
    if (filterStatus.value !== 'all') {
      params.status = filterStatus.value;
    }
    
    const response = await articlesApi.getArticles(params);
    articles.value = response.data;
    
    // 假设总数从响应头中获取，如果后端没有提供，则使用当前页面文章数
    totalArticles.value = parseInt(response.headers['x-total-count'] || '0') || articles.value.length;
  } catch (err: any) {
    console.error('加载文章失败:', err);
    error.value = '加载文章失败，请稍后再试';
  } finally {
    isLoading.value = false;
  }
};

// 搜索处理（带防抖）
let searchTimeout: number | null = null;
const handleSearch = () => {
  if (searchTimeout) {
    clearTimeout(searchTimeout);
  }
  
  searchTimeout = window.setTimeout(() => {
    currentPage.value = 1; // 重置页码
    loadArticles();
  }, 300);
};

// 确认删除
const confirmDelete = (article: any) => {
  articleToDelete.value = article;
  showDeleteModal.value = true;
};

// 删除文章
const deleteArticle = async () => {
  if (!articleToDelete.value) return;
  
  isDeleting.value = true;
  try {
    await articlesApi.deleteArticle(articleToDelete.value.id);
    
    // 从列表中移除
    articles.value = articles.value.filter(article => article.id !== articleToDelete.value.id);
    totalArticles.value--;
    
    // 关闭弹窗
    showDeleteModal.value = false;
    articleToDelete.value = null;
  } catch (err: any) {
    console.error('删除文章失败:', err);
    error.value = '删除文章失败，请稍后再试';
  } finally {
    isDeleting.value = false;
  }
};

// 切换页面
const changePage = (page: number) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
};

// 监听过滤器变化，重新加载文章
watch(filterStatus, () => {
  currentPage.value = 1; // 重置页码
  loadArticles();
});

// 监听页码变化，重新加载文章
watch(currentPage, () => {
  loadArticles();
});

// 初始化
onMounted(() => {
  loadArticles();
});
</script>

<style scoped>
.articles-manager {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.content-header h2 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
}

.filter-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.filter-tabs {
  display: flex;
  gap: 0.5rem;
}

.filter-tab {
  background-color: white;
  border: 1px solid #e2e8f0;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-tab:hover {
  background-color: #f8fafc;
}

.filter-tab.active {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
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
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.table-container {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid #e2e8f0;
}

.data-table th {
  background-color: #f8fafc;
  color: #64748b;
  font-weight: 600;
  font-size: 0.875rem;
}

.id-cell {
  font-weight: 600;
  color: #3b82f6;
  font-size: 0.875rem;
}

.title-cell {
  max-width: 300px;
}

.article-title {
  font-weight: 500;
  color: #1e293b;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.article-slug {
  color: #94a3b8;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
}

.status-badge.published {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.status-badge.draft {
  background-color: rgba(100, 116, 139, 0.1);
  color: #64748b;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.icon-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.icon-button:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

.icon-button.danger:hover {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  text-align: center;
}

.empty-icon {
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.25rem;
}

.empty-state p {
  color: #64748b;
  margin-bottom: 1.5rem;
}

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
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

.loading-spinner.large {
  width: 2rem;
  height: 2rem;
  border: 3px solid rgba(59, 130, 246, 0.3);
  border-top-color: #3b82f6;
  margin-bottom: 1rem;
}

.loading-state p {
  color: #64748b;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 1rem;
}

.pagination-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: #f8fafc;
  color: #1e293b;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #64748b;
  font-size: 0.875rem;
}

.primary-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  text-decoration: none;
}

.primary-button:hover {
  background-color: #2563eb;
}

.error-alert {
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background-color: rgba(239, 68, 68, 0.1);
  border-left: 3px solid #ef4444;
  color: #b91c1c;
  border-radius: 0.25rem;
}

/* 弹窗 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.125rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.warning-text {
  color: #ef4444;
  font-size: 0.875rem;
}

.text-button {
  background-color: transparent;
  color: #64748b;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.text-button:hover {
  color: #1e293b;
}

.danger-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.danger-button:hover {
  background-color: #dc2626;
}

.danger-button:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}
</style> 