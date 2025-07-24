<template>
  <div class="project-detail">
    <navigation />
    
    <main class="project-content">
      <div class="container">
        <!-- 加载和错误状态 -->
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载项目信息...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <h2>抱歉，加载失败</h2>
          <p>{{ error }}</p>
          <router-link to="/projects" class="back-button">返回项目列表</router-link>
        </div>
        
        <!-- 项目内容 -->
        <div v-else class="project-container">
          <!-- 项目头部 -->
          <div class="project-header">
            <div class="emoji-title-container">
              <span class="project-emoji">{{ project.emoji }}</span>
              <h1 class="project-title">{{ project.title }}</h1>
            </div>
            
            <div class="project-meta">
              <!-- 标签列表 -->
              <div class="project-tags">
                <span class="tag" v-for="tag in project.tags" :key="tag.id">{{ tag.name }}</span>
              </div>
              
              <!-- 项目统计 -->
              <div class="project-stats">
                <div class="stat">
                  <star-icon />
                  <span>{{ formatStarCount(project.stars_count) }} 星标</span>
                </div>
                <div class="stat">
                  <git-fork-icon />
                  <span>{{ formatForkCount(project.forks_count) }} 分支</span>
                </div>
              </div>
            </div>
            
            <!-- 项目链接 -->
            <div class="project-links">
              <a v-if="project.github_url" :href="project.github_url" target="_blank" rel="noopener noreferrer" class="link-button github-link">
                <github-icon /> 查看源代码
              </a>
              <a v-if="project.live_url" :href="project.live_url" target="_blank" rel="noopener noreferrer" class="link-button demo-link">
                <external-link-icon /> 在线演示
              </a>
            </div>
          </div>
          
          <!-- 项目图片 -->
          <div v-if="project.image_url" class="project-image-container">
            <img :src="project.image_url" :alt="project.title" class="project-image">
          </div>
          
          <!-- 项目描述 -->
          <div class="project-content-section">
            <h2 class="section-title">项目介绍</h2>
            <div class="project-description markdown-content" v-html="formattedDescription"></div>
          </div>
          
          <!-- 技术栈 -->
          <div v-if="project.tags && project.tags.length > 0" class="project-content-section">
            <h2 class="section-title">技术栈</h2>
            <div class="tech-tags">
              <div class="tech-tag" v-for="tag in project.tags" :key="tag.id">
                {{ tag.name }}
              </div>
            </div>
          </div>
          
          <!-- 相关项目 -->
          <div v-if="relatedProjects && relatedProjects.length > 0" class="project-content-section">
            <h2 class="section-title">相关项目</h2>
            <div class="related-projects">
              <router-link 
                v-for="relatedProject in relatedProjects" 
                :key="relatedProject.id" 
                :to="`/projects/${relatedProject.slug}`" 
                class="related-project-card"
              >
                <div class="related-emoji">{{ relatedProject.emoji }}</div>
                <div class="related-content">
                  <h3 class="related-title">{{ relatedProject.title }}</h3>
                  <p class="related-description">{{ truncateText(relatedProject.description, 80) }}</p>
                </div>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <site-footer />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
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
import { marked } from 'marked';

// 添加显示调试信息的标志
const debug = ref(false);

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

// 截断文本方法
const truncateText = (text: string, maxLength: number): string => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  return text.substring(0, maxLength) + '...';
};

// 格式化星标数量，确保显示为数字
const formatStarCount = (value: any): number => {
  if (value === null || value === undefined || value === '') return 0;
  const num = Number(value);
  return isNaN(num) ? 0 : num;
};

// 格式化分支数量，确保显示为数字
const formatForkCount = (value: any): number => {
  if (value === null || value === undefined || value === '') return 0;
  const num = Number(value);
  return isNaN(num) ? 0 : num;
};

// 将Markdown格式的描述转换为HTML
const formattedDescription = computed(() => {
  if (!project.value.description) return '';
  try {
    return marked(project.value.description);
  } catch (e) {
    console.error('解析Markdown失败:', e);
    return project.value.description;
  }
});

// 项目获取函数
const fetchProject = async () => {
  const slug = route.params.slug as string;
  isLoading.value = true;
  error.value = null;
  
  try {
    console.log('正在获取项目详情:', slug);
    // 从API获取项目详情
    const projectResponse = await projectsApi.getProjectBySlug(slug);
    console.log('项目详情原始响应:', projectResponse.data);
    
    if (projectResponse.data) {
      // 手动转换数值字段
      const data = projectResponse.data;
      
      // 确保project.value是一个新对象
      project.value = {
        ...data,
        // 强制转换数值字段
        stars_count: Number(data.stars_count || 0),
        forks_count: Number(data.forks_count || 0)
      };
      
      // 如果项目有标签，获取相关项目
      if (project.value.tags && project.value.tags.length > 0) {
        try {
          // 获取相关项目 - 使用第一个标签作为筛选条件
          const tagSlug = project.value.tags[0].slug;
          const relatedResponse = await projectsApi.getProjectsByTag(tagSlug, 3);
          
          if (relatedResponse.data) {
            // 处理相关项目数据
            let relatedItems = [];
            if (Array.isArray(relatedResponse.data)) {
              relatedItems = relatedResponse.data;
            } else if (relatedResponse.data.items && Array.isArray(relatedResponse.data.items)) {
              relatedItems = relatedResponse.data.items;
            }
            
            // 过滤掉当前项目，并确保数字字段被正确处理
            relatedProjects.value = relatedItems
              .filter(p => p.id !== project.value.id)
              .slice(0, 3)
              .map(p => ({
                ...p,
                stars_count: Number(p.stars_count || 0),
                forks_count: Number(p.forks_count || 0)
              }));
          }
        } catch (relatedErr) {
          console.error('获取相关项目失败:', relatedErr);
          // 非致命错误，继续显示主项目
        }
      }
    } else {
      error.value = '找不到该项目';
    }
  } catch (err: any) {
    console.error('获取项目详情失败:', err);
    error.value = err.response?.status === 404 ? '找不到该项目' : '加载项目信息失败';
  } finally {
    isLoading.value = false;
  }
};

// 页面加载时获取数据
onMounted(() => {
  fetchProject();
});
</script>

<style>
/* 全局Markdown样式 - 不使用scoped以确保样式应用到v-html内容 */
.markdown-content {
  color: #94a3b8;
  line-height: 1.8;
  font-size: 1.05rem;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3,
.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  font-weight: 600;
  color: #f8fafc;
  line-height: 1.4;
}

.markdown-content h1 {
  font-size: 1.8rem;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  padding-bottom: 0.5rem;
}

.markdown-content h2 {
  font-size: 1.6rem;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  padding-bottom: 0.3rem;
}

.markdown-content h3 {
  font-size: 1.4rem;
}

.markdown-content h4 {
  font-size: 1.2rem;
}

.markdown-content p {
  margin-bottom: 1.25rem;
}

.markdown-content ul,
.markdown-content ol {
  margin-bottom: 1.25rem;
  padding-left: 1.5rem;
}

.markdown-content ul li,
.markdown-content ol li {
  margin-bottom: 0.5rem;
}

.markdown-content a {
  color: #3b82f6;
  text-decoration: none;
  border-bottom: 1px solid transparent;
  transition: border-color 0.2s;
}

.markdown-content a:hover {
  border-bottom-color: #3b82f6;
}

.markdown-content blockquote {
  border-left: 4px solid #3b82f6;
  padding-left: 1rem;
  margin-left: 0;
  margin-right: 0;
  margin-bottom: 1.25rem;
  font-style: italic;
  color: #94a3b8;
}

.markdown-content code {
  background-color: rgba(99, 102, 241, 0.1);
  padding: 0.2rem 0.4rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

.markdown-content pre {
  background-color: rgba(15, 23, 42, 0.8);
  padding: 1rem;
  border-radius: 0.5rem;
  overflow-x: auto;
  margin-bottom: 1.25rem;
}

.markdown-content pre code {
  background-color: transparent;
  padding: 0;
  color: #e2e8f0;
  font-family: monospace;
}

.markdown-content img {
  max-width: 100%;
  height: auto;
  border-radius: 0.5rem;
  margin: 1rem 0;
}

.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1.25rem;
}

.markdown-content table th,
.markdown-content table td {
  padding: 0.5rem;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.markdown-content table th {
  background-color: rgba(99, 102, 241, 0.1);
  font-weight: 600;
}
</style>

<style scoped>
.project-detail {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #0f172a;
  color: #f8fafc;
}

.project-content {
  flex: 1;
  padding: 5rem 0;
}

.container {
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  padding: 0 1.5rem;
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
  width: 3rem;
  height: 3rem;
  border: 3px solid rgba(59, 130, 246, 0.1);
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p {
  color: #94a3b8;
  font-size: 1.1rem;
}

/* 错误状态 */
.error-state {
  text-align: center;
  padding: 4rem 0;
}

.error-state h2 {
  color: #ef4444;
  font-size: 1.75rem;
  margin-bottom: 1rem;
}

.error-state p {
  color: #94a3b8;
  margin-bottom: 2rem;
}

.back-button {
  display: inline-block;
  background-color: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.back-button:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}

/* 项目容器 */
.project-container {
  animation: fade-in 0.5s ease-out;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 项目头部 */
.project-header {
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
}

.emoji-title-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.project-emoji {
  font-size: 3rem;
  line-height: 1;
}

.project-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin: 0;
  color: #f8fafc;
}

.project-meta {
  margin-bottom: 1.5rem;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.tag {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  padding: 0.3rem 0.8rem;
  border-radius: 9999px;
  font-size: 0.85rem;
  font-weight: 500;
}

.project-stats {
  display: flex;
  gap: 2rem;
  margin-top: 1rem;
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #94a3b8;
}

.stat svg {
  width: 1.25rem;
  height: 1.25rem;
  color: #3b82f6;
}

.project-links {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.link-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 0.5rem;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s;
}

.github-link {
  background-color: rgba(15, 23, 42, 0.8);
  color: #f8fafc;
}

.demo-link {
  background-color: #3b82f6;
  color: white;
}

.link-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* 项目图片 */
.project-image-container {
  margin-bottom: 2rem;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.project-image {
  width: 100%;
  height: auto;
  display: block;
}

/* 内容区块 */
.project-content-section {
  margin-bottom: 3rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #f8fafc;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
  padding-bottom: 0.75rem;
}

/* 技术标签 */
.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tech-tag {
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.1), rgba(99, 102, 241, 0.1));
  color: #60a5fa;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(99, 102, 241, 0.1);
}

/* 相关项目 */
.related-projects {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1rem;
}

.related-project-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: 0.75rem;
  background-color: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(99, 102, 241, 0.1);
  text-decoration: none;
  transition: all 0.3s;
}

.related-project-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  background-color: rgba(30, 41, 59, 0.7);
}

.related-emoji {
  font-size: 2rem;
}

.related-content {
  flex: 1;
}

.related-title {
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: #f8fafc;
}

.related-description {
  color: #94a3b8;
  font-size: 0.9rem;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 640px) {
  .project-title {
    font-size: 2rem;
  }
  
  .project-emoji {
    font-size: 2.5rem;
  }
  
  .project-links {
    flex-direction: column;
  }
  
  .section-title {
    font-size: 1.35rem;
  }
}
</style> 