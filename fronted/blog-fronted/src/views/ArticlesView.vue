<template>
  <div class="articles-container">
    <Navigation />
    
    <main class="articles-content">
      <div class="container">
        <div class="articles-header">
          <h1 class="articles-title">我的<span class="text-gradient">博客</span></h1>
          <p class="articles-subtitle">探索我的技术文章、教程和心得体会</p>
          
          <!-- 调试信息，帮助排查问题 -->
          <div v-if="debug" class="debug-info">
            <p><strong>当前筛选:</strong> {{ selectedTags.length ? `标签ID: ${selectedTags[0]}` : '无标签筛选' }}</p>
            <p><strong>标签列表:</strong> {{ tags.map(t => `${t.name}(${t.id})`) }}</p>
            <p><strong>原文章数:</strong> {{ articles.length }}</p>
            <p><strong>筛选后文章数:</strong> {{ filteredArticles.length }}</p>
          </div>
        </div>
        
        <!-- 文章筛选和搜索 -->
        <div class="articles-filters">
          <div class="search-box">
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="搜索文章..." 
              class="search-input"
              @keyup.enter="searchArticles"
            />
            <button class="search-button" @click="searchArticles">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
            </button>
          </div>
          
          <div class="tag-filters">
            <span 
              class="tag-filter"
              :class="{ active: selectedTags.length === 0 }"
              @click="clearTagFilters"
            >
              全部
            </span>
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
        
        <!-- 文章列表 -->
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载文章列表...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <h2>抱歉，加载失败</h2>
          <p>{{ error }}</p>
          <button @click="fetchArticles" class="retry-button">重试</button>
        </div>
        
        <div v-else-if="filteredArticles.length === 0" class="empty-state">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="empty-icon">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <h3>没有找到相关文章</h3>
          <p>尝试使用其他关键词或清除筛选条件</p>
          <button class="retry-button" @click="clearTagFilters">显示全部文章</button>
        </div>
        
        <div v-else class="articles-grid">
          <article 
            v-for="article in filteredArticles" 
            :key="article.id" 
            class="article-card"
            @click="navigateToArticle(article.slug)"
          >
            <div class="article-image" :style="{ backgroundImage: `url(${article.cover_image || '/placeholder-cover.jpg'})` }"></div>
            <div class="article-content">
              <div class="article-meta">
                <span class="article-date">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="meta-icon">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="16" y1="2" x2="16" y2="6"></line>
                    <line x1="8" y1="2" x2="8" y2="6"></line>
                    <line x1="3" y1="10" x2="21" y2="10"></line>
                  </svg>
                  {{ formatDate(article.published_at) }}
                </span>
                <span class="article-read-time">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="meta-icon">
                    <circle cx="12" cy="12" r="10"></circle>
                    <polyline points="12 6 12 12 16 14"></polyline>
                  </svg>
                  {{ article.read_time }} 分钟阅读
                </span>
              </div>
              
              <h2 class="article-title">{{ article.title }}</h2>
              <p class="article-excerpt">{{ article.excerpt }}</p>
              
              <div class="article-tags">
                <span 
                  v-for="tag in article.tags" 
                  :key="tag.id" 
                  class="article-tag"
                  @click.stop="toggleTag(tag.id)"
                >
                  {{ tag.name }}
                </span>
              </div>
              
              <div class="article-footer">
                <router-link :to="`/articles/${article.slug}`" class="read-more">
                  阅读全文
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="read-more-icon">
                    <line x1="5" y1="12" x2="19" y2="12"></line>
                    <polyline points="12 5 19 12 12 19"></polyline>
                  </svg>
                </router-link>
              </div>
            </div>
          </article>
        </div>
        
        <!-- 分页控件 -->
        <div v-if="totalPages > 1" class="pagination">
          <button 
            class="pagination-button" 
            :disabled="currentPage === 1"
            @click="changePage(currentPage - 1)"
          >
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            上一页
          </button>
          
          <div class="pagination-info">
            第 {{ currentPage }} 页，共 {{ totalPages }} 页
          </div>
          
          <button 
            class="pagination-button" 
            :disabled="currentPage === totalPages"
            @click="changePage(currentPage + 1)"
          >
            下一页
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </div>
    </div>
    </main>
    
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import Navigation from '@/components/Navigation.vue';
import SiteFooter from '@/components/SiteFooter.vue';
import { articlesApi, tagsApi } from '@/api';

// 接口定义
interface Tag {
  id: number;
  name: string;
  slug: string;
}

interface Article {
  id: number;
  title: string;
  slug: string;
  excerpt: string;
  content: string;
  cover_image: string;
  read_time: number;
  published_at: string;
  tags: Tag[];
}

// 状态
const router = useRouter();
const route = useRoute();
const articles = ref<Article[]>([]);
const allArticles = ref<Article[]>([]); // 存储所有文章，不受分页影响
const isLoading = ref(true);
const error = ref<string | null>(null);
const searchQuery = ref('');
const selectedTags = ref<number[]>([]);
const currentPage = ref(1);
const itemsPerPage = 6;
const totalPages = ref(1);
const totalArticles = ref(0);
const debug = ref(true); // 调试模式，便于排查问题

// 标签列表
const tags = ref<Tag[]>([]);
const isTagsLoading = ref(false);

// 获取标签列表
const fetchTags = async () => {
  isTagsLoading.value = true;
  
  try {
    console.log('开始获取标签数据...');
    const response = await tagsApi.getTags();
    
    if (response && response.data) {
      tags.value = response.data;
      console.log(`成功获取 ${tags.value.length} 个标签:`, tags.value);
    } else {
      console.warn('获取标签返回空数据');
    }
  } catch (err) {
    console.error('获取标签失败:', err);
  } finally {
    isTagsLoading.value = false;
  }
};

// 强制本地筛选文章
const applyLocalFilters = () => {
  let filtered = [...allArticles.value];
  
  // 应用标签筛选
  if (selectedTags.value.length > 0) {
    const tagId = selectedTags.value[0];
    filtered = filtered.filter(article => 
      article.tags && article.tags.some(tag => tag.id === tagId)
    );
    console.log(`应用本地标签筛选 (ID: ${tagId})，结果: ${filtered.length} 篇文章`);
  }
  
  // 应用搜索筛选
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(article => 
      article.title.toLowerCase().includes(query) || 
      article.excerpt.toLowerCase().includes(query)
    );
    console.log(`应用本地搜索筛选 (关键词: ${query})，结果: ${filtered.length} 篇文章`);
  }
  
  // 应用分页
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  articles.value = filtered.slice(start, end);
  
  // 更新总页数
  totalArticles.value = filtered.length;
  totalPages.value = Math.max(1, Math.ceil(totalArticles.value / itemsPerPage));
  
  console.log(`分页结果: 第 ${currentPage.value}/${totalPages.value} 页，显示 ${articles.value.length} 篇文章`);
};

// 过滤文章的计算属性
const filteredArticles = computed(() => {
  return articles.value;
});

// 清除所有标签筛选
const clearTagFilters = () => {
  console.log('清除所有标签筛选');
  selectedTags.value = [];
  router.push('/articles');
  applyLocalFilters();
};

// 格式化日期
const formatDate = (dateString: string): string => {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

// 切换标签选择
const toggleTag = (tagId: number) => {
  console.log(`点击标签ID: ${tagId}`);
  
  // 始终只保留一个标签
  selectedTags.value = selectedTags.value.includes(tagId) ? [] : [tagId];
  
  // 重置页码
  currentPage.value = 1;
  
  // 通过路由跳转到标签筛选页面
  const selectedTag = tags.value.find(tag => tag.id === tagId);
  if (selectedTag && selectedTags.value.length > 0) {
    console.log(`跳转到标签筛选页面: ${selectedTag.slug}`);
    router.push(`/articles/tag/${selectedTag.slug}`);
  } else {
    console.log('跳转到文章列表页');
    router.push('/articles');
  }
  
  // 立即应用本地筛选
  applyLocalFilters();
};

// 切换页码
const changePage = (page: number) => {
  currentPage.value = page;
  window.scrollTo({ top: 0, behavior: 'smooth' });
  applyLocalFilters(); // 本地分页
};

// 导航到文章详情页
const navigateToArticle = (slug: string) => {
  router.push(`/articles/${slug}`);
};

// 搜索文章
const searchArticles = () => {
  currentPage.value = 1; // 重置页码
  
  if (searchQuery.value.trim()) {
    router.push(`/articles/search/${encodeURIComponent(searchQuery.value.trim())}`);
  } else {
    router.push('/articles');
  }
  
  // 立即应用本地筛选
  applyLocalFilters();
};

// 获取所有文章数据（一次性获取所有文章）
const fetchAllArticles = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    console.log('获取所有文章数据...');
    
    const response = await articlesApi.getArticles({
      status: 'published',
      limit: 100 // 获取足够多的文章
    });
    
    if (response.data) {
      if (Array.isArray(response.data)) {
        allArticles.value = response.data;
      } else if (response.data.items && Array.isArray(response.data.items)) {
        allArticles.value = response.data.items;
      } else {
        allArticles.value = [];
        console.warn('文章数据格式不符合预期');
      }
      
      console.log(`获取到 ${allArticles.value.length} 篇文章`);
      
      // 应用筛选和分页
      applyLocalFilters();
    }
  } catch (err) {
    console.error('获取文章列表失败:', err);
    error.value = '获取文章列表失败，请稍后再试';
    articles.value = [];
    allArticles.value = [];
  } finally {
    isLoading.value = false;
  }
};

// 监听搜索输入框变化
watch(searchQuery, () => {
  // 当搜索关键词变化时，重新应用筛选
  applyLocalFilters();
});

// 监听路由变化
watch(
  () => route.path,
  (newPath) => {
    console.log(`路由变化: ${newPath}`);
    
    // 重置页码
    currentPage.value = 1;
    
    // 根据路由类型设置过滤条件
    if (route.name === 'articles-by-tag' && route.params.tag) {
      const tagSlug = route.params.tag as string;
      const foundTag = tags.value.find(tag => tag.slug === tagSlug);
      if (foundTag) {
        selectedTags.value = [foundTag.id];
        searchQuery.value = '';
        console.log(`根据路由设置标签筛选: ${foundTag.name} (ID: ${foundTag.id})`);
      }
    } else if (route.name === 'articles-search' && route.params.query) {
      searchQuery.value = decodeURIComponent(route.params.query as string);
      selectedTags.value = [];
      console.log(`根据路由设置搜索筛选: ${searchQuery.value}`);
    } else {
      // 普通文章列表，清除所有过滤
      selectedTags.value = [];
      searchQuery.value = '';
    }
    
    // 应用筛选
    applyLocalFilters();
  },
  { immediate: true }
);

// 页面加载时获取数据
onMounted(async () => {
  console.log('组件挂载，当前路由:', route.name, route.params);
  
  // 先获取标签
  await fetchTags();
  
  // 从路由参数中获取标签或搜索关键词
  if (route.name === 'articles-by-tag' && route.params.tag) {
    const tagSlug = route.params.tag as string;
    console.log('按标签过滤:', tagSlug);
    
    const foundTag = tags.value.find(tag => tag.slug === tagSlug);
    if (foundTag) {
      selectedTags.value = [foundTag.id];
      console.log(`找到匹配的标签: ${foundTag.name}`);
    }
  } else if (route.name === 'articles-search' && route.params.query) {
    const query = route.params.query as string;
    searchQuery.value = decodeURIComponent(query);
    console.log('搜索关键词:', searchQuery.value);
  }
  
  // 获取所有文章数据并本地筛选
  await fetchAllArticles();
});
</script>

<style scoped>
.articles-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.articles-content {
  flex: 1;
  padding: 6rem 0;
}

.articles-header {
  text-align: center;
  margin-bottom: 3rem;
}

.articles-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--color-text);
}

.articles-subtitle {
  font-size: 1.25rem;
  color: var(--color-text-muted);
  max-width: 600px;
  margin: 0 auto;
}

/* 筛选和搜索样式 */
.articles-filters {
  margin-bottom: 2.5rem;
}

.search-box {
  position: relative;
  margin-bottom: 1.5rem;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 1rem;
  background: rgba(30, 41, 59, 0.5);
  border: 1px solid rgba(99, 102, 241, 0.2);
  border-radius: 0.5rem;
  color: var(--color-text);
  font-size: 1rem;
  transition: all 0.3s;
  padding-right: 3rem;
}

.search-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

.search-button {
  position: absolute;
  right: 0.5rem;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  padding: 0.5rem;
  cursor: pointer;
  transition: color 0.3s;
}

.search-button:hover {
  color: var(--color-primary);
}

.search-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

.tag-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1rem;
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

/* 文章卡片样式 */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.article-card {
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

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.article-image {
  height: 200px;
  background-size: cover;
  background-position: center;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
}

.article-content {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.article-meta {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

.article-date,
.article-read-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.meta-icon {
  width: 1rem;
  height: 1rem;
  color: var(--color-primary);
}

.article-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: var(--color-text);
  line-height: 1.4;
}

.article-excerpt {
  color: var(--color-text-muted);
  line-height: 1.6;
  margin-bottom: 1.25rem;
  flex-grow: 1;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.article-tag {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.3s;
}

.article-tag:hover {
  background: rgba(59, 130, 246, 0.2);
}

.article-footer {
  margin-top: auto;
}

.read-more {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s;
}

.read-more:hover {
  color: var(--color-secondary);
}

.read-more-icon {
  width: 1rem;
  height: 1rem;
  transition: transform 0.3s;
}

.read-more:hover .read-more-icon {
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

/* 分页控件 */
.pagination {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 3rem;
}

.pagination-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  border: 1px solid rgba(59, 130, 246, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
  font-weight: 500;
  transition: all 0.3s;
}

.pagination-button:hover:not(:disabled) {
  background: rgba(59, 130, 246, 0.2);
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-button svg {
  width: 1rem;
  height: 1rem;
}

.pagination-info {
  color: var(--color-text-muted);
  font-size: 0.875rem;
}

/* 响应式调整 */
@media (max-width: 992px) {
  .articles-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .articles-content {
    padding: 5rem 0;
  }
  
  .articles-title {
    font-size: 2.5rem;
  }
  
  .articles-grid {
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

/* 调试信息样式 */
.debug-info {
  background: rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(0, 0, 0, 0.1);
  border-radius: 0.5rem;
  padding: 1rem;
  margin: 1rem 0;
  font-size: 0.8rem;
  font-family: monospace;
}

.debug-info p {
  margin: 0.25rem 0;
}
</style> 