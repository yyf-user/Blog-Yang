<template>
  <div class="project-detail">
    <navigation />
    
    <main class="project-content">
      <div class="container">
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载项目信息...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <h2>抱歉，加载失败</h2>
          <p>{{ error }}</p>
          <router-link to="/projects" class="back-button">返回项目列表</router-link>
        </div>
        
        <article v-else class="project">
          <div class="project-header">
            <div class="project-emoji">{{ project.emoji }}</div>
            <h1 class="project-title">{{ project.title }}</h1>
            
            <div class="project-tags">
              <span class="tag" v-for="tag in project.tags" :key="tag.id">
                {{ tag.name }}
              </span>
            </div>
            
            <div class="project-stats">
              <div class="stat">
                <star-icon />
                <span>{{ project.stars_count }} 星标</span>
              </div>
              <div class="stat">
                <git-fork-icon />
                <span>{{ project.forks_count }} 分支</span>
              </div>
            </div>
            
            <div class="project-links">
              <a :href="project.github_url" target="_blank" rel="noopener noreferrer" class="github-link">
                <github-icon /> 查看源代码
              </a>
              <a v-if="project.live_url" :href="project.live_url" target="_blank" rel="noopener noreferrer" class="demo-link">
                <external-link-icon /> 在线演示
              </a>
            </div>
          </div>
          
          <div class="project-image" v-if="project.image_url">
            <img :src="project.image_url" :alt="project.title">
          </div>
          
          <div class="project-body">
            <div class="project-description">
              {{ project.description }}
            </div>
          </div>
        </article>
        
        <!-- 相关项目 -->
        <div class="related-projects" v-if="relatedProjects.length">
          <h2>相关项目</h2>
          <div class="projects-grid">
            <div class="project-card" v-for="relatedProject in relatedProjects" :key="relatedProject.id">
              <div class="card-emoji">{{ relatedProject.emoji }}</div>
              <h3 class="card-title">{{ relatedProject.title }}</h3>
              <p class="card-description">{{ relatedProject.description }}</p>
              
              <div class="card-tags">
                <span class="tag" v-for="tag in relatedProject.tags" :key="tag.id">
                  {{ tag.name }}
                </span>
              </div>
              
              <div class="card-footer">
                <div class="card-stats">
                  <div class="stat">
                    <star-icon />
                    <span>{{ relatedProject.stars_count }}</span>
                  </div>
                  <div class="stat">
                    <git-fork-icon />
                    <span>{{ relatedProject.forks_count }}</span>
                  </div>
                </div>
                <router-link :to="`/project/${relatedProject.slug}`" class="view-project">
                  查看项目
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <site-footer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { 
  Star as StarIcon,
  GitFork as GitForkIcon,
  Github as GithubIcon,
  ExternalLink as ExternalLinkIcon
} from 'lucide-vue-next';
import { projectsApi } from '@/api';
import Navigation from '@/components/Navigation.vue';
import SiteFooter from '@/components/SiteFooter.vue';

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
const route = useRoute();
const project = ref<Project | any>({});
const relatedProjects = ref<Project[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);

// 获取项目数据
const fetchProject = async () => {
  const slug = route.params.slug as string;
  isLoading.value = true;
  error.value = null;
  
  try {
    console.log('正在获取项目详情:', slug);
    // 从API获取项目详情
    const projectResponse = await projectsApi.getProjectBySlug(slug);
    console.log('项目详情响应:', projectResponse);
    
    if (projectResponse.data) {
      project.value = projectResponse.data;
      console.log('项目详情:', project.value);
      
      // 如果项目有标签，获取相关项目
      if (project.value.tags && project.value.tags.length > 0) {
        // 获取相关项目 - 使用第一个标签作为筛选条件
        const tagSlug = project.value.tags[0].slug;
        const relatedResponse = await projectsApi.getProjectsByTag(tagSlug, 2);
        console.log('相关项目响应:', relatedResponse);
        
        if (relatedResponse.data) {
          // 处理相关项目数据
          if (Array.isArray(relatedResponse.data)) {
            // 过滤掉当前项目
            relatedProjects.value = relatedResponse.data
              .filter(p => p.id !== project.value.id)
              .slice(0, 2);
          } else if (relatedResponse.data.items && Array.isArray(relatedResponse.data.items)) {
            // 过滤掉当前项目
            relatedProjects.value = relatedResponse.data.items
              .filter(p => p.id !== project.value.id)
              .slice(0, 2);
          }
          console.log(`加载了 ${relatedProjects.value.length} 个相关项目`);
        }
      }
    } else {
      error.value = '找不到该项目';
    }
  } catch (err: any) {
    console.error('获取项目详情失败:', err);
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误详情:', err.response.data);
      
      if (err.response.status === 404) {
        error.value = '找不到该项目';
      } else {
        error.value = '加载项目信息失败';
      }
    } else {
      error.value = '网络错误，请稍后重试';
    }
  } finally {
    isLoading.value = false;
  }
};

// 页面加载时获取数据
onMounted(() => {
  fetchProject();
});
</script>

<style scoped>
.project-detail {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.project-content {
  flex: 1;
  padding: 7rem 0 4rem;
  background-color: var(--color-background);
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 2rem;
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
  margin-bottom: 1rem;
  width: 2rem;
  height: 2rem;
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

.back-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: var(--color-primary);
  color: white;
  border-radius: 0.5rem;
  text-decoration: none;
  transition: all 0.3s;
}

.back-button:hover {
  background: var(--color-secondary);
  transform: translateY(-2px);
}

/* 项目样式 */
.project {
  animation: fadeIn 0.8s ease-out;
}

.project-header {
  margin-bottom: 2.5rem;
  text-align: center;
}

.project-emoji {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.project-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  color: var(--color-text);
  line-height: 1.2;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tag {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.project-stats {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 1.5rem;
  color: var(--color-text-muted);
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.stat svg {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-primary);
}

.project-links {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.github-link, .demo-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.3s;
  text-decoration: none;
}

.github-link {
  background: rgba(15, 23, 42, 0.8);
  color: white;
}

.demo-link {
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  color: white;
}

.github-link:hover, .demo-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.project-image {
  margin-bottom: 2.5rem;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.project-image img {
  width: 100%;
  height: auto;
  display: block;
}

/* 项目内容 */
.project-body {
  color: var(--color-text-light);
  font-size: 1.125rem;
  line-height: 1.8;
}

.project-description {
  margin-bottom: 2rem;
  font-size: 1.25rem;
}

/* 相关项目 */
.related-projects {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.related-projects h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: var(--color-text);
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.project-card {
  background: var(--color-surface);
  border-radius: 0.75rem;
  padding: 1.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  border: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  flex-direction: column;
  animation: fadeIn 1s ease-out;
  animation-fill-mode: both;
}

.project-card:nth-child(2) {
  animation-delay: 0.2s;
}

.project-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.card-emoji {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: var(--color-text);
}

.card-description {
  color: var(--color-text-muted);
  margin-bottom: 1.25rem;
  flex-grow: 1;
  line-height: 1.6;
}

.card-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.card-stats {
  display: flex;
  gap: 1rem;
}

.view-project {
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s;
}

.view-project:hover {
  color: var(--color-secondary);
}

@media (max-width: 768px) {
  .project-content {
    padding: 5rem 0 3rem;
  }
  
  .tech-list {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  .project-links {
    flex-direction: column;
    gap: 1rem;
  }
  
  .github-link, .demo-link {
    width: 100%;
    justify-content: center;
  }
}
</style> 