<template>
  <div class="dashboard">
    <h2>数据概览</h2>
    <div class="stats-grid">
      <div class="stat-card article-card">
        <div class="stat-icon-container">
          <file-text-icon class="stat-icon" />
          <div class="stat-count">{{ stats.articles }}</div>
        </div>
        <div class="stat-info">
          <p>文章数量</p>
        </div>
      </div>
      
      <div class="stat-card project-card">
        <div class="stat-icon-container">
          <folder-icon class="stat-icon" />
          <div class="stat-count">{{ stats.projects }}</div>
        </div>
        <div class="stat-info">
          <p>项目数量</p>
        </div>
      </div>
      
      <div class="stat-card message-card">
        <div class="stat-icon-container">
          <message-square-icon class="stat-icon" />
          <div class="stat-count">{{ stats.messages }}</div>
        </div>
        <div class="stat-info">
          <p>消息数量</p>
        </div>
      </div>
      
      <div class="stat-card visitor-card">
        <div class="stat-icon-container">
          <users-icon class="stat-icon" />
          <div class="stat-count">{{ stats.visitors }}</div>
        </div>
        <div class="stat-info">
          <p>访问人数</p>
        </div>
      </div>
    </div>
    
    <div class="dashboard-row">
      <div class="dashboard-card">
        <div class="card-header">
          <h3>最近活动</h3>
        </div>
        <ul class="activity-list" v-if="!isLoading">
          <li v-for="(activity, index) in recentActivities" :key="index" class="activity-item">
            <span class="activity-time">{{ activity.time }}</span>
            <span class="activity-text">{{ activity.text }}</span>
          </li>
        </ul>
        <div class="loading-placeholder" v-else>
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
      
      <div class="dashboard-card">
        <div class="card-header">
          <h3>最新文章</h3>
          <router-link to="/admin/articles" class="view-all">查看全部</router-link>
        </div>
        <ul class="articles-list" v-if="!isLoading">
          <li v-for="article in recentArticles" :key="article.id" class="article-item">
            <div class="article-info">
              <router-link :to="`/admin/articles/edit/${article.id}`" class="article-title">
                {{ article.title }}
              </router-link>
              <span :class="['status-badge', article.status]">
                {{ article.status === 'published' ? '已发布' : '草稿' }}
              </span>
            </div>
            <span class="article-date">{{ formatDate(article.published_at || article.created_at) }}</span>
          </li>
        </ul>
        <div class="loading-placeholder" v-else>
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
    </div>
    
    <div class="dashboard-row">
      <div class="dashboard-card">
        <div class="card-header">
          <h3>最新项目</h3>
          <router-link to="/admin/projects" class="view-all">查看全部</router-link>
        </div>
        <ul class="projects-list" v-if="!isLoading">
          <li v-for="project in recentProjects" :key="project.id" class="project-item">
            <div class="project-info">
              <router-link :to="`/admin/projects/edit/${project.id}`" class="project-title">
                {{ project.title }}
              </router-link>
              <div class="project-stats">
                <span class="project-stat">
                  <star-icon size="14" />
                  {{ project.stars_count || 0 }}
                </span>
                <span class="project-stat">
                  <git-fork-icon size="14" />
                  {{ project.forks_count || 0 }}
                </span>
              </div>
            </div>
            <span class="project-date">{{ formatDate(project.created_at) }}</span>
          </li>
        </ul>
        <div class="loading-placeholder" v-else>
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
      
      <div class="dashboard-card">
        <div class="card-header">
          <h3>未读消息</h3>
          <router-link to="/admin/messages" class="view-all">查看全部</router-link>
        </div>
        <ul class="messages-list" v-if="!isLoading">
          <li v-for="message in unreadMessages" :key="message.id" class="message-item">
            <div class="message-info">
              <span class="message-name">{{ message.name }}</span>
              <p class="message-preview">{{ truncateMessage(message.message) }}</p>
            </div>
            <span class="message-date">{{ formatDate(message.created_at) }}</span>
          </li>
          <li v-if="unreadMessages.length === 0" class="empty-list">
            <p>没有未读消息</p>
          </li>
        </ul>
        <div class="loading-placeholder" v-else>
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { articlesApi, projectsApi, messagesApi, statsApi } from '@/api';
import { 
  FileText as FileTextIcon,
  Folder as FolderIcon,
  MessageSquare as MessageSquareIcon,
  Users as UsersIcon,
  Star as StarIcon,
  GitFork as GitForkIcon
} from 'lucide-vue-next';

// 状态
const stats = ref({
  articles: 0,
  projects: 0,
  messages: 0,
  visitors: 0
});
const recentActivities = ref<any[]>([]);
const recentArticles = ref<any[]>([]);
const recentProjects = ref<any[]>([]);
const unreadMessages = ref<any[]>([]);
const isLoading = ref(true);

// 格式化日期
const formatDate = (dateString: string) => {
  if (!dateString) return '未知时间';
  
  const date = new Date(dateString);
  const now = new Date();
  const diffDays = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60 * 24));
  
  if (diffDays === 0) {
    return '今天';
  } else if (diffDays === 1) {
    return '昨天';
  } else if (diffDays < 7) {
    return `${diffDays}天前`;
  } else {
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  }
};

// 截断消息
const truncateMessage = (message: string) => {
  if (message.length > 50) {
    return message.substring(0, 50) + '...';
  }
  return message;
};

// 加载统计数据
const loadStats = async () => {
  try {
    console.log('加载统计数据...');
    const response = await statsApi.getStats();
    
    if (response.data) {
      // 使用后端返回的真实统计数据
      stats.value = response.data;
      console.log('成功加载统计数据:', stats.value);
    } else {
      // 后端返回为空时，显示0值
      stats.value = {
        articles: 0,
        projects: 0,
        messages: 0,
        visitors: 0
      };
    }
    
    // 同时获取实时的文章、项目和消息数量
    try {
      // 获取文章数量
      const articlesResponse = await articlesApi.getArticles({ limit: 1 });
      if (articlesResponse.data && articlesResponse.headers['x-total-count']) {
        stats.value.articles = parseInt(articlesResponse.headers['x-total-count']);
      }
      
      // 获取项目数量
      const projectsResponse = await projectsApi.getProjects({ limit: 1 });
      if (projectsResponse.data && projectsResponse.headers['x-total-count']) {
        stats.value.projects = parseInt(projectsResponse.headers['x-total-count']);
      }
      
      // 获取消息数量
      const messagesResponse = await messagesApi.getMessages({ limit: 1 });
      if (messagesResponse.data && messagesResponse.headers['x-total-count']) {
        stats.value.messages = parseInt(messagesResponse.headers['x-total-count']);
      }
    } catch (countErr) {
      console.error('获取数量统计出错:', countErr);
    }
  } catch (err) {
    console.error('加载统计数据失败:', err);
    // 显示0值，不使用模拟数据
    stats.value = {
      articles: 0,
      projects: 0,
      messages: 0,
      visitors: 0
    };
  }
};

// 加载最近文章
const loadRecentArticles = async () => {
  try {
    console.log('加载最近文章...');
    const response = await articlesApi.getArticles({ limit: 5 });
    
    if (response.data && Array.isArray(response.data)) {
      recentArticles.value = response.data;
      console.log(`成功加载 ${recentArticles.value.length} 篇最近文章`);
      
      // 添加活动记录
      if (response.data.length > 0) {
        const latestArticle = response.data[0];
        if (latestArticle.status === 'published') {
          recentActivities.value.push({
            time: formatDate(latestArticle.published_at),
            text: `发布了新文章《${latestArticle.title}》`
          });
        } else {
          recentActivities.value.push({
            time: formatDate(latestArticle.created_at),
            text: `创建了新草稿《${latestArticle.title}》`
          });
        }
      }
    } else {
      recentArticles.value = [];
    }
  } catch (err) {
    console.error('加载最近文章失败:', err);
    // 设置为空数组，不使用模拟数据
    recentArticles.value = [];
  }
};

// 加载最近项目
const loadRecentProjects = async () => {
  try {
    console.log('加载最近项目...');
    const response = await projectsApi.getProjects({ limit: 5 });
    
    if (response.data && Array.isArray(response.data)) {
      recentProjects.value = response.data;
      console.log(`成功加载 ${recentProjects.value.length} 个最近项目`);
      
      // 添加活动记录
      if (response.data.length > 0) {
        const latestProject = response.data[0];
        recentActivities.value.push({
          time: formatDate(latestProject.created_at),
          text: `创建了新项目"${latestProject.title}"`
        });
      }
    } else {
      recentProjects.value = [];
    }
  } catch (err) {
    console.error('加载最近项目失败:', err);
    // 设置为空数组，不使用模拟数据
    recentProjects.value = [];
  }
};

// 加载未读消息
const loadUnreadMessages = async () => {
  try {
    console.log('加载未读消息...');
    const response = await messagesApi.getMessages({ is_read: false, limit: 5 });
    
    if (response.data && Array.isArray(response.data)) {
      unreadMessages.value = response.data;
      console.log(`成功加载 ${unreadMessages.value.length} 条未读消息`);
      
      // 添加活动记录
      if (response.data.length > 0) {
        recentActivities.value.push({
          time: '今天',
          text: `收到了${response.data.length}条新消息`
        });
      }
    } else {
      unreadMessages.value = [];
    }
  } catch (err) {
    console.error('加载未读消息失败:', err);
    // 设置为空数组，不使用模拟数据
    unreadMessages.value = [];
  }
};

// 初始化
onMounted(async () => {
  isLoading.value = true;
  
  // 添加一些基本活动
  recentActivities.value = [
    { time: '今天', text: '登录了管理控制台' }
  ];
  
  // 并行加载数据
  await Promise.all([
    loadStats(),
    loadRecentArticles(),
    loadRecentProjects(),
    loadUnreadMessages()
  ]);
  
  // 按时间排序活动
  recentActivities.value.sort((a, b) => {
    const timeOrder = { '今天': 0, '昨天': 1, '2天前': 2, '3天前': 3 };
    const aOrder = timeOrder[a.time as keyof typeof timeOrder] ?? 999;
    const bOrder = timeOrder[b.time as keyof typeof timeOrder] ?? 999;
    return aOrder - bOrder;
  });
  
  isLoading.value = false;
});
</script>

<style scoped>
.dashboard {
  padding: 1.5rem;
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.dashboard h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #1e293b;
  font-size: 1.25rem;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background-color: white;
  border-radius: 0.5rem;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
}

.stat-icon-container {
  position: relative;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-icon {
  width: 3rem;
  height: 3rem;
  margin-bottom: 0.5rem;
}

.article-card .stat-icon {
  color: #3b82f6;
}

.project-card .stat-icon {
  color: #10b981;
}

.message-card .stat-icon {
  color: #f59e0b;
}

.visitor-card .stat-icon {
  color: #8b5cf6;
}

.stat-count {
  font-size: 2rem;
  font-weight: 700;
  margin-top: 0.5rem;
  margin-bottom: 0.25rem;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.article-card .stat-count {
  color: #2563eb;
}

.project-card .stat-count {
  color: #059669;
}

.message-card .stat-count {
  color: #d97706;
}

.visitor-card .stat-count {
  color: #6d28d9;
}

.stat-info p {
  margin: 0;
  color: #64748b;
  font-size: 1rem;
  font-weight: 500;
}

.article-card {
  border-left: 4px solid #3b82f6;
}

.project-card {
  border-left: 4px solid #10b981;
}

.message-card {
  border-left: 4px solid #f59e0b;
}

.visitor-card {
  border-left: 4px solid #8b5cf6;
}

/* 仪表盘行 */
.dashboard-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.dashboard-card {
  background-color: white;
  border-radius: 0.5rem;
  border: 1px solid #e2e8f0;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f8fafc;
}

.card-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1rem;
}

.view-all {
  color: #3b82f6;
  font-size: 0.875rem;
  text-decoration: none;
}

.view-all:hover {
  text-decoration: underline;
}

/* 活动列表 */
.activity-list,
.articles-list,
.projects-list,
.messages-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.activity-item {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  gap: 1rem;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-time {
  color: #64748b;
  font-size: 0.875rem;
  min-width: 60px;
}

.activity-text {
  color: #1e293b;
  font-size: 0.875rem;
}

/* 文章列表 */
.article-item,
.project-item,
.message-item {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.article-item:last-child,
.project-item:last-child,
.message-item:last-child {
  border-bottom: none;
}

.article-info,
.project-info,
.message-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.article-title,
.project-title {
  color: #1e293b;
  text-decoration: none;
  font-weight: 500;
}

.article-title:hover,
.project-title:hover {
  color: #3b82f6;
}

.article-date,
.project-date,
.message-date {
  color: #94a3b8;
  font-size: 0.75rem;
}

.status-badge {
  display: inline-block;
  padding: 0.125rem 0.375rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  margin-top: 0.25rem;
}

.status-badge.published {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.status-badge.draft {
  background-color: rgba(100, 116, 139, 0.1);
  color: #64748b;
}

/* 项目统计 */
.project-stats {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.project-stat {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: #64748b;
  font-size: 0.75rem;
}

/* 消息预览 */
.message-name {
  font-weight: 500;
  color: #1e293b;
}

.message-preview {
  color: #64748b;
  font-size: 0.875rem;
  margin: 0.25rem 0 0;
}

/* 加载状态 */
.loading-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 0;
}

.loading-spinner {
  width: 2rem;
  height: 2rem;
  border: 3px solid rgba(59, 130, 246, 0.3);
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-placeholder p {
  color: #64748b;
  margin: 0;
}

/* 空列表 */
.empty-list {
  display: flex;
  justify-content: center;
  padding: 2rem 0;
}

.empty-list p {
  color: #94a3b8;
  margin: 0;
}

/* 响应式 */
@media (max-width: 768px) {
  .dashboard-row {
    grid-template-columns: 1fr;
  }
}
</style> 