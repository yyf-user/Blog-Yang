<template>
  <div class="projects-manager">
    <div class="content-header">
      <h2>项目管理</h2>
      <router-link to="/admin/projects/create" class="primary-button">
        <plus-icon size="16" />
        新建项目
      </router-link>
    </div>
    
    <div v-if="error" class="error-alert">{{ error }}</div>
    
    <!-- 过滤和搜索 -->
    <div class="filter-container">
      <div class="filter-tabs">
        <button 
          v-for="filter in ['all', 'featured']" 
          :key="filter"
          class="filter-tab"
          :class="{ active: filterFeatured === filter }"
          @click="setFilter(filter)"
        >
          {{ filterLabels[filter] }}
        </button>
      </div>
      
      <div class="search-bar">
        <search-icon size="18" class="search-icon" />
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="搜索项目..." 
          @input="handleSearch"
        />
      </div>
    </div>
    
    <!-- 项目列表 -->
    <div class="projects-grid" v-if="!isLoading && filteredProjects.length > 0">
      <div 
        v-for="project in filteredProjects" 
        :key="project.id" 
        class="project-card"
      >
        <div class="project-image">
          <img :src="project.image_url" :alt="project.title" />
          <div class="project-actions">
            <router-link 
              :to="`/admin/projects/edit/${project.id}`" 
              class="icon-button"
              title="编辑"
            >
              <edit-icon size="16" />
            </router-link>
            <a 
              :href="`/projects/${project.slug}`" 
              target="_blank"
              class="icon-button"
              title="查看"
            >
              <eye-icon size="16" />
            </a>
            <button 
              class="icon-button danger"
              title="删除"
              @click="confirmDelete(project)"
            >
              <trash-icon size="16" />
            </button>
          </div>
          <div v-if="project.featured" class="featured-badge">精选</div>
          <div class="project-id-badge">ID: {{ project.id }}</div>
        </div>
        
        <div class="project-info">
          <h3 class="project-title">{{ project.title }}</h3>
          <p class="project-description">{{ truncateDescription(project.description) }}</p>
          
          <div class="project-meta">
            <div class="project-stats">
              <div class="stat">
                <star-icon size="14" />
                <span>{{ project.stars_count || 0 }}</span>
              </div>
              <div class="stat">
                <git-fork-icon size="14" />
                <span>{{ project.forks_count || 0 }}</span>
              </div>
            </div>
            
            <div class="project-tags" v-if="project.tags && project.tags.length > 0">
              <span 
                v-for="tag in project.tags.slice(0, 3)" 
                :key="tag.id" 
                class="tag"
              >
                {{ tag.name }}
              </span>
              <span v-if="project.tags.length > 3" class="tag more">
                +{{ project.tags.length - 3 }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <div class="empty-state" v-else-if="!isLoading && filteredProjects.length === 0">
      <folder-icon size="48" class="empty-icon" />
      <h3>暂无项目</h3>
      <p v-if="searchQuery">没有找到符合条件的项目，请尝试其他搜索词</p>
      <p v-else-if="filterFeatured === 'featured'">没有精选项目</p>
      <p v-else>开始创建您的第一个项目吧</p>
      <router-link to="/admin/projects/create" class="primary-button">
        <plus-icon size="16" />
        新建项目
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
          <p>确定要删除项目 <strong>{{ projectToDelete?.title }}</strong> 吗？</p>
          <p class="warning-text">此操作无法撤销。</p>
        </div>
        <div class="modal-footer">
          <button class="text-button" @click="showDeleteModal = false">取消</button>
          <button 
            class="danger-button" 
            @click="deleteProject"
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
import { projectsApi } from '@/api';
import { 
  Plus as PlusIcon,
  Folder as FolderIcon,
  Edit as EditIcon,
  Eye as EyeIcon,
  Trash as TrashIcon,
  Search as SearchIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Star as StarIcon,
  GitFork as GitForkIcon,
  X as XIcon
} from 'lucide-vue-next';

// 状态
const projects = ref<any[]>([]);
const isLoading = ref(false);
const error = ref('');
const filterFeatured = ref('all'); // all, featured
const searchQuery = ref('');
const currentPage = ref(1);
const totalProjects = ref(0);
const pageSize = 12;

// 删除相关
const showDeleteModal = ref(false);
const projectToDelete = ref<any>(null);
const isDeleting = ref(false);

// 过滤标签映射
const filterLabels = {
  all: '全部项目',
  featured: '精选项目'
};

// 计算属性
const totalPages = computed(() => Math.ceil(totalProjects.value / pageSize));

const filteredProjects = computed(() => {
  let result = projects.value;
  
  // 按精选状态过滤
  if (filterFeatured.value === 'featured') {
    result = result.filter(project => project.featured);
  }
  
  // 按搜索词过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(project => 
      project.title.toLowerCase().includes(query) || 
      project.description.toLowerCase().includes(query) ||
      project.tags.some((tag: any) => tag.name.toLowerCase().includes(query))
    );
  }
  
  return result;
});

// 截断描述
const truncateDescription = (description: string) => {
  if (description.length > 100) {
    return description.substring(0, 100) + '...';
  }
  return description;
};

// 设置过滤器
const setFilter = (filter: string) => {
  filterFeatured.value = filter;
};

// 加载项目
const loadProjects = async () => {
  isLoading.value = true;
  error.value = '';
  
  try {
    // 构建查询参数
    const params: any = {
      skip: (currentPage.value - 1) * pageSize,
      limit: pageSize
    };
    
    // 如果有过滤条件，添加到参数
    if (filterFeatured.value === 'featured') {
      params.featured = true;
    }
    
    const response = await projectsApi.getProjects(params);
    projects.value = response.data;
    
    // 假设总数从响应头中获取，如果后端没有提供，则使用当前页面项目数
    totalProjects.value = parseInt(response.headers['x-total-count'] || '0') || projects.value.length;
  } catch (err: any) {
    console.error('加载项目失败:', err);
    error.value = '加载项目失败，请稍后再试';
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
    loadProjects();
  }, 300);
};

// 确认删除
const confirmDelete = (project: any) => {
  projectToDelete.value = project;
  showDeleteModal.value = true;
};

// 删除项目
const deleteProject = async () => {
  if (!projectToDelete.value) return;
  
  isDeleting.value = true;
  try {
    await projectsApi.deleteProject(projectToDelete.value.id);
    
    // 从列表中移除
    projects.value = projects.value.filter(project => project.id !== projectToDelete.value.id);
    totalProjects.value--;
    
    // 关闭弹窗
    showDeleteModal.value = false;
    projectToDelete.value = null;
  } catch (err: any) {
    console.error('删除项目失败:', err);
    error.value = '删除项目失败，请稍后再试';
  } finally {
    isDeleting.value = false;
  }
};

// 切换页面
const changePage = (page: number) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
};

// 监听过滤器变化，重新加载项目
watch(filterFeatured, () => {
  currentPage.value = 1; // 重置页码
  loadProjects();
});

// 监听页码变化，重新加载项目
watch(currentPage, () => {
  loadProjects();
});

// 初始化
onMounted(() => {
  loadProjects();
});
</script>

<style scoped>
.projects-manager {
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

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.project-card {
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  overflow: hidden;
  transition: all 0.2s;
}

.project-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  transform: translateY(-2px);
}

.project-image {
  position: relative;
  height: 160px;
  overflow: hidden;
}

.project-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.project-card:hover .project-image img {
  transform: scale(1.05);
}

.project-actions {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: flex;
  gap: 0.25rem;
  opacity: 0;
  transition: opacity 0.2s;
}

.project-card:hover .project-actions {
  opacity: 1;
}

.featured-badge {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  background-color: rgba(59, 130, 246, 0.9);
  color: white;
  font-size: 0.75rem;
  font-weight: 500;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
}

.project-id-badge {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  background-color: #3b82f6;
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 0.25rem;
  z-index: 10;
}

.project-info {
  padding: 1rem;
}

.project-title {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  color: #1e293b;
}

.project-description {
  color: #64748b;
  font-size: 0.875rem;
  margin-bottom: 1rem;
  line-height: 1.5;
}

.project-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.project-stats {
  display: flex;
  gap: 1rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #64748b;
  font-size: 0.75rem;
}

.project-tags {
  display: flex;
  gap: 0.25rem;
}

.tag {
  background-color: #f1f5f9;
  color: #64748b;
  font-size: 0.75rem;
  padding: 0.125rem 0.375rem;
  border-radius: 9999px;
}

.tag.more {
  background-color: #e2e8f0;
}

.icon-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.9);
  border: none;
  color: #64748b;
  cursor: pointer;
  width: 2rem;
  height: 2rem;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.icon-button:hover {
  background-color: white;
  color: #1e293b;
}

.icon-button.danger:hover {
  background-color: white;
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