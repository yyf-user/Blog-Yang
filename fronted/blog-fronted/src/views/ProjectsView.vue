<template>
  <div class="projects-container">
    <Navigation />
    
    <main class="projects-content">
      <div class="container">
        <div class="projects-header">
          <h1 class="projects-title">我的<span class="text-gradient">项目</span></h1>
          <p class="projects-subtitle">探索我开发的各类项目和开源贡献</p>
        </div>
        
        <!-- 项目筛选 -->
        <div class="projects-filters">
          <div class="tag-filters">
            <span 
              v-for="tag in tags" 
              :key="tag.id" 
              class="tag-filter"
              :class="{ active: selectedTags.includes(tag.id) }"
              @click="toggleTag(tag.id)"
            >
              {{ tag.name }}
            </span>
          </div>
        </div>
        
        <!-- 项目列表 -->
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载项目列表...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <h2>抱歉，加载失败</h2>
          <p>{{ error }}</p>
          <button @click="retryLoading" class="retry-button">重试</button>
        </div>
        
        <div v-else-if="filteredProjects.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-icon">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <h3>没有找到相关项目</h3>
          <p>尝试清除筛选条件</p>
        </div>
        
        <div v-else class="projects-grid">
          <div 
            v-for="project in filteredProjects" 
            :key="project.id" 
            class="project-card"
            @click="navigateToProject(project.slug)"
          >
            <div class="project-header">
              <div class="project-emoji">{{ project.emoji }}</div>
              <div class="project-links">
                <a v-if="project.github_url" :href="project.github_url" target="_blank" class="project-link github" @click.stop>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
                  </svg>
                </a>
                <a v-if="project.live_url" :href="project.live_url" target="_blank" class="project-link live" @click.stop>
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="2" y1="12" x2="22" y2="12"></line>
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
                  </svg>
                </a>
              </div>
            </div>
            
            <div class="project-image" :style="{ backgroundImage: `url(${project.image_url || '/placeholder-project.jpg'})` }"></div>
            
            <div class="project-content">
              <h3 class="project-title">{{ project.title }}</h3>
              <p class="project-description">{{ project.description }}</p>
              
              <div class="project-tags">
                <span 
                  v-for="tag in project.tags" 
                  :key="tag.id" 
                  class="project-tag"
                  @click.stop="toggleTag(tag.id)"
                >
                  {{ tag.name }}
                </span>
              </div>
              
              <div class="project-stats">
                <div class="project-stat" v-if="project.stars_count !== undefined">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="stat-icon">
                    <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
                  </svg>
                  <span>{{ project.stars_count }}</span>
                </div>
                <div class="project-stat" v-if="project.forks_count !== undefined">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="stat-icon">
                    <path d="M5 3v4M9 3v4M5 7h4M17 7h.01M17 11h.01M17 15h.01M17 19h.01M5 11h4M9 15v4M5 19h4M5 15v4M5 11v4"></path>
                  </svg>
                  <span>{{ project.forks_count }}</span>
                </div>
              </div>
              
              <router-link :to="`/projects/${project.slug}`" class="view-details">
                查看详情
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="details-icon">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                  <polyline points="12 5 19 12 12 19"></polyline>
                </svg>
              </router-link>
            </div>
          </div>
        </div>
    </div>
    </main>
    
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import Navigation from '@/components/Navigation.vue';
import SiteFooter from '@/components/SiteFooter.vue';
import { projectsApi, tagsApi } from '@/api'; // 导入API

// 接口定义
interface Tag {
  id: number;
  name: string;
  slug: string;
}

interface Project {
  id: number;
  title: string;
  slug: string;
  description: string;
  image_url: string;
  github_url?: string;
  live_url?: string;
  stars_count?: number;
  forks_count?: number;
  emoji: string;
  tags: Tag[];
}

// 状态
const router = useRouter();
const projects = ref<Project[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);
const selectedTags = ref<number[]>([]);

// 标签列表
const tags = ref<Tag[]>([]);

// 过滤项目
const filteredProjects = computed(() => {
  if (selectedTags.value.length === 0) {
    return projects.value;
  }
  
  return projects.value.filter(project => 
    project.tags.some(tag => selectedTags.value.includes(tag.id))
  );
});

// 切换标签选择
const toggleTag = (tagId: number) => {
  const index = selectedTags.value.indexOf(tagId);
  if (index === -1) {
    selectedTags.value.push(tagId);
  } else {
    selectedTags.value.splice(index, 1);
  }
};

// 导航到项目详情页
const navigateToProject = (slug: string) => {
  router.push(`/projects/${slug}`);
};

// 获取标签列表
const fetchTags = async () => {
  try {
    const response = await tagsApi.getTags();
    tags.value = response.data || [];
    console.log('获取标签成功:', tags.value.length);
  } catch (err: any) {
    console.error('获取标签失败:', err);
  }
};

// 获取项目数据
const fetchProjects = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    // 从后端API获取真实数据
    const response = await projectsApi.getProjects();
    console.log('API响应数据:', response);
    
    // 检查响应结构
    if (response.data) {
      // 如果数据是数组，直接使用
      if (Array.isArray(response.data)) {
        projects.value = response.data;
      } 
      // 如果数据包含items数组，使用items
      else if (response.data.items && Array.isArray(response.data.items)) {
        projects.value = response.data.items;
      }
      // 其他情况尝试把整个对象当作单个项目处理
      else {
        console.warn('数据格式不符合预期，尝试解析:', response.data);
        projects.value = [];
      }
      
      console.log(`加载了 ${projects.value.length} 个项目:`, projects.value);
    } else {
      projects.value = [];
      console.warn('获取项目返回空数据');
    }
    isLoading.value = false;
  } catch (err: any) {
    console.error('获取项目列表失败:', err);
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误详情:', err.response.data);
    }
    error.value = '获取项目列表失败，请重试';
    isLoading.value = false;
    projects.value = [];
  }
};

// 重试加载
const retryLoading = () => {
  fetchProjects();
};

// 页面加载时获取数据
onMounted(async () => {
  await Promise.all([
    fetchTags(),
    fetchProjects()
  ]);
});
</script>

<style scoped>
.projects-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.projects-content {
  flex: 1;
  padding: 6rem 0;
}

.projects-header {
  text-align: center;
  margin-bottom: 3rem;
}

.projects-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--color-text);
}

.projects-subtitle {
  font-size: 1.25rem;
  color: var(--color-text-muted);
  max-width: 600px;
  margin: 0 auto;
}

/* 筛选样式 */
.projects-filters {
  margin-bottom: 2.5rem;
}

.tag-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}

.tag-filter {
  background: rgba(30, 41, 59, 0.5);
  color: var(--color-text-muted);
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.tag-filter:hover {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
}

.tag-filter.active {
  background: rgba(59, 130, 246, 0.2);
  color: var(--color-primary);
  border-color: var(--color-primary);
}

/* 项目卡片样式 */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
}

.project-card {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(99, 102, 241, 0.1);
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.project-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
}

.project-emoji {
  font-size: 1.5rem;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 0.5rem;
}

.project-links {
  display: flex;
  gap: 0.75rem;
}

.project-link {
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 50%;
  transition: all 0.3s;
}

.project-link svg {
  width: 1rem;
  height: 1rem;
  color: var(--color-text-muted);
  transition: color 0.3s;
}

.project-link:hover {
  background: rgba(59, 130, 246, 0.2);
}

.project-link:hover svg {
  color: var(--color-primary);
}

.project-image {
  height: 180px;
  background-size: cover;
  background-position: center;
}

.project-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.project-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: var(--color-text);
}

.project-description {
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-bottom: 1.25rem;
  flex-grow: 1;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.project-tag {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.3s;
}

.project-tag:hover {
  background: rgba(59, 130, 246, 0.2);
}

.project-stats {
  display: flex;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.project-stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.stat-icon {
  width: 1rem;
  height: 1rem;
  color: var(--color-text-muted);
}

.view-details {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s;
  margin-top: auto;
}

.view-details:hover {
  color: var(--color-secondary);
}

.details-icon {
  width: 1rem;
  height: 1rem;
  transition: transform 0.3s;
}

.view-details:hover .details-icon {
  transform: translateX(3px);
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  color: var(--color-text-muted);
}

.loading-state .loading-spinner {
  width: 2.5rem;
  height: 2.5rem;
  border: 3px solid rgba(99, 102, 241, 0.1);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 错误状态 */
.error-state {
  text-align: center;
  padding: 4rem 0;
}

.error-state h2 {
  color: var(--color-error);
  margin-bottom: 1rem;
}

.error-state p {
  color: var(--color-text-muted);
  margin-bottom: 2rem;
}

.retry-button {
  background: var(--color-primary);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: background 0.3s;
}

.retry-button:hover {
  background: var(--color-secondary);
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 4rem 0;
  color: var(--color-text-muted);
}

.empty-icon {
  width: 3rem;
  height: 3rem;
  margin-bottom: 1rem;
  color: var(--color-text-muted);
}

.empty-state h3 {
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

/* 响应式调整 */
@media (max-width: 992px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .projects-content {
    padding: 5rem 0;
  }
  
  .projects-title {
    font-size: 2.5rem;
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .tag-filters {
    gap: 0.5rem;
  }
  
  .tag-filter {
    padding: 0.4rem 0.75rem;
    font-size: 0.8rem;
  }
}
</style> 