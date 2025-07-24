<template>
  <section id="projects" class="projects-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">我的<span class="highlight">项目</span></h2>
        <p class="section-subtitle">探索我的开源项目和技术实践</p>
      </div>
      
      <!-- 加载状态 -->
      <div class="loading-state" v-if="isLoading">
        <div class="loading-spinner"></div>
        <p>加载项目...</p>
      </div>
      
      <!-- 错误状态 -->
      <div class="error-state" v-else-if="error">
        <p>{{ error }}</p>
        <button @click="fetchProjects" class="retry-button">重试</button>
      </div>
      
      <div v-else>
        <!-- 精选项目 -->
        <div class="featured-project" v-if="featuredProject" @click="navigateToProject(featuredProject.slug)">
          <div class="featured-content">
            <h3 class="featured-title">
              {{ featuredProject.emoji }} {{ featuredProject.title }}
            </h3>
            <p class="featured-description">{{ featuredProject.description }}</p>
            
            <div class="project-tags">
              <span class="project-tag" v-for="tag in featuredProject.tags" :key="tag.id">
                {{ tag.name }}
              </span>
            </div>
            
            <div class="project-stats">
              <div class="stat">
                <github-icon />
                <span>{{ featuredProject.stars_count }} 星标</span>
              </div>
              <div class="stat">
                <git-fork-icon />
                <span>{{ featuredProject.forks_count }} 分支</span>
              </div>
            </div>
            
            <div class="project-links">
              <a :href="featuredProject.github_url" target="_blank" rel="noopener noreferrer" class="github-link" @click.stop>
                <github-icon /> 源代码
              </a>
              <a v-if="featuredProject.live_url" :href="featuredProject.live_url" target="_blank" rel="noopener noreferrer" class="demo-link" @click.stop>
                <external-link-icon /> 在线演示
              </a>
            </div>
          </div>
          <div class="featured-image" :style="{ backgroundImage: `url(${featuredProject.image_url || '/project-placeholder.jpg'})` }">
            <div class="featured-badge">精选项目</div>
          </div>
        </div>
        
        <!-- 项目列表 -->
        <div class="projects-grid">
          <div class="project-card" v-for="project in projects" :key="project.id" @click="navigateToProject(project.slug)">
            <div class="project-emoji">{{ project.emoji }}</div>
            <h4 class="project-title">{{ project.title }}</h4>
            <p class="project-description">{{ project.description }}</p>
            
            <div class="project-tags">
              <span class="project-tag" v-for="tag in project.tags" :key="tag.id">
                {{ tag.name }}
              </span>
            </div>
            
            <div class="project-meta">
              <div class="project-stats">
                <div class="stat">
                  <star-icon />
                  <span>{{ project.stars_count }}</span>
                </div>
                <div class="stat">
                  <git-fork-icon />
                  <span>{{ project.forks_count }}</span>
                </div>
              </div>
              
              <div class="project-links">
                <a :href="project.github_url" target="_blank" rel="noopener noreferrer" class="github-button" @click.stop>
                  <github-icon />
                </a>
                <a v-if="project.live_url" :href="project.live_url" target="_blank" rel="noopener noreferrer" class="demo-button" @click.stop>
                  <external-link-icon />
                </a>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 查看所有项目按钮 -->
        <div class="view-all">
          <router-link to="/projects" class="view-all-button">
            查看所有项目
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { 
  Github as GithubIcon,
  ExternalLink as ExternalLinkIcon,
  Star as StarIcon,
  GitFork as GitForkIcon
} from 'lucide-vue-next';
import { projectsApi } from '@/api';
import { useRouter } from 'vue-router';

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
  github_url: string;
  live_url?: string;
  stars_count: number;
  forks_count: number;
  emoji: string;
  tags: Tag[];
}

// 状态
const router = useRouter();
const featuredProject = ref<Project | null>(null);
const projects = ref<Project[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

// 导航到项目详情页
const navigateToProject = (slug: string) => {
  router.push(`/projects/${slug}`);
};

// 获取项目数据
const fetchProjects = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    // 获取精选项目
    const featuredResponse = await projectsApi.getProjects({
      featured: true,
      limit: 1
    });
    console.log('精选项目API响应:', featuredResponse);
    
    // 检查响应结构并处理精选项目
    if (featuredResponse.data) {
      if (Array.isArray(featuredResponse.data) && featuredResponse.data.length > 0) {
        featuredProject.value = featuredResponse.data[0];
      } else if (featuredResponse.data.items && Array.isArray(featuredResponse.data.items) && featuredResponse.data.items.length > 0) {
        featuredProject.value = featuredResponse.data.items[0];
      } else {
        console.log('没有找到精选项目');
        featuredProject.value = null;
      }
    }
    
    // 获取普通项目
    const projectsResponse = await projectsApi.getProjects({
      limit: 6
    });
    console.log('普通项目API响应:', projectsResponse);
    
    // 处理普通项目数据
    if (projectsResponse.data) {
      // 处理不同的返回格式
      if (Array.isArray(projectsResponse.data)) {
        // 如果精选项目已经存在，需要过滤掉
        if (featuredProject.value) {
          projects.value = projectsResponse.data.filter(
            project => project.id !== featuredProject.value?.id
          ).slice(0, 6);
        } else {
          projects.value = projectsResponse.data.slice(0, 6);
        }
      } 
      else if (projectsResponse.data.items && Array.isArray(projectsResponse.data.items)) {
        // 如果精选项目已经存在，需要过滤掉
        if (featuredProject.value) {
          projects.value = projectsResponse.data.items.filter(
            project => project.id !== featuredProject.value?.id
          ).slice(0, 6);
        } else {
          projects.value = projectsResponse.data.items.slice(0, 6);
        }
      } else {
        console.warn('项目数据格式不符合预期');
        projects.value = [];
      }
      
      console.log(`加载了 ${projects.value.length} 个普通项目`);
    } else {
      projects.value = [];
      console.warn('获取项目返回空数据');
    }
  } catch (err: any) {
    console.error('获取项目失败:', err);
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误详情:', err.response.data);
    }
    error.value = '获取项目列表失败';
    featuredProject.value = null;
    projects.value = [];
  } finally {
    isLoading.value = false;
  }
};

// 页面加载时获取数据
onMounted(() => {
  fetchProjects();
});
</script>

<style scoped>
.projects-section {
  padding: 6rem 2rem;
  background-color: rgba(15, 23, 42, 0.3);
  position: relative;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #f8fafc;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #94a3b8;
  max-width: 600px;
  margin: 0 auto;
}

.highlight {
  color: #3b82f6;
}

/* 加载状态 */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
  color: #94a3b8;
}

.loading-spinner {
  width: 2rem;
  height: 2rem;
  border: 2px solid rgba(59, 130, 246, 0.1);
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 0.75rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 错误状态 */
.error-state {
  text-align: center;
  padding: 2rem 0;
}

.error-state p {
  color: #ef4444;
  margin-bottom: 1rem;
}

.retry-button {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background: #2563eb;
}

/* 精选项目 */
.featured-project {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 4rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.1);
  animation: fadeIn 1s ease-out;
  cursor: pointer; /* 添加手型光标 */
}

.featured-content {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
}

.featured-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #f8fafc;
}

.featured-description {
  color: #94a3b8;
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.featured-image {
  background-size: cover;
  background-position: center;
  position: relative;
}

.featured-badge {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 2rem;
  font-weight: 600;
  font-size: 0.875rem;
  box-shadow: 0 4px 10px rgba(59, 130, 246, 0.5);
}

/* 项目列表 */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.project-card {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 1.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  flex-direction: column;
  height: 100%;
  animation: fadeIn 1s ease-out;
  animation-fill-mode: both;
  cursor: pointer; /* 添加手型光标 */
}

.project-card:nth-child(2) {
  animation-delay: 0.2s;
}

.project-card:nth-child(3) {
  animation-delay: 0.3s;
}

.project-card:nth-child(4) {
  animation-delay: 0.4s;
}

.project-card:nth-child(5) {
  animation-delay: 0.5s;
}

.project-card:nth-child(6) {
  animation-delay: 0.6s;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.project-emoji {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.project-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #f8fafc;
}

.project-description {
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 1.25rem;
  flex-grow: 1;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.project-tag {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.project-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.project-stats {
  display: flex;
  gap: 1rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
  font-size: 0.875rem;
}

.stat svg {
  width: 1rem;
  height: 1rem;
  color: #3b82f6;
}

.project-links {
  display: flex;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.github-link, .demo-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.3s;
  text-decoration: none;
}

.github-link {
  background: rgba(15, 23, 42, 0.8);
  color: #f8fafc;
}

.demo-link {
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  color: white;
}

.github-link:hover, .demo-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.github-button, .demo-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.25rem;
  height: 2.25rem;
  border-radius: 0.5rem;
  transition: all 0.3s;
}

.github-button {
  background: rgba(15, 23, 42, 0.8);
  color: #f8fafc;
}

.demo-button {
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  color: white;
}

.github-button:hover, .demo-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* 查看所有按钮 */
.view-all {
  text-align: center;
  margin-top: 3rem;
}

.view-all-button {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
  border: 1px solid rgba(59, 130, 246, 0.2);
  display: inline-block;
}

.view-all-button:hover {
  background: rgba(59, 130, 246, 0.2);
  transform: translateY(-2px);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 992px) {
  .featured-project {
    grid-template-columns: 1fr;
  }
  
  .featured-image {
    height: 300px;
    order: -1;
  }
}

@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
}
</style> 