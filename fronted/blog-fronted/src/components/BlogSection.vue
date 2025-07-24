<template>
  <section id="blog" class="blog-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">我的<span class="highlight">博客</span></h2>
        <p class="section-subtitle">分享我的技术观点和学习心得</p>
      </div>
      
      <!-- 加载状态 -->
      <div class="loading-state" v-if="isLoading">
        <div class="loading-spinner"></div>
        <p>加载文章...</p>
      </div>
      
      <!-- 错误状态 -->
      <div class="error-state" v-else-if="error">
        <p>{{ error }}</p>
        <button @click="fetchArticles" class="retry-button">重试</button>
      </div>
      
      <div v-else>
        <!-- 精选文章 -->
        <div class="featured-article" v-if="featuredArticle">
          <div class="featured-article-content">
            <div class="article-meta">
              <span class="article-date">
                <calendar-icon />
                {{ formatDate(featuredArticle.published_at) }}
              </span>
              <span class="article-read-time">
                <clock-icon />
                {{ featuredArticle.read_time }} 分钟阅读
              </span>
            </div>
            
            <h3 class="featured-article-title">{{ featuredArticle.title }}</h3>
            <p class="featured-article-excerpt">{{ featuredArticle.excerpt }}</p>
            
            <div class="article-tags">
              <span 
                class="tag" 
                v-for="tag in featuredArticle.tags" 
                :key="tag.id"
                @click.stop="navigateToTagArticles(tag.slug)"
              >
                {{ tag.name }}
              </span>
            </div>
            
            <router-link :to="`/articles/${featuredArticle.slug}`" class="read-more">
              阅读全文 <arrow-right-icon />
            </router-link>
          </div>
          <div class="featured-article-image" :style="{ backgroundImage: `url(${featuredArticle.cover_image || '/placeholder-cover.jpg'})` }">
            <div class="featured-badge">精选</div>
          </div>
        </div>
        
        <!-- 文章列表 -->
        <div class="articles-grid">
          <div class="article-card" v-for="article in articles" :key="article.id">
            <div class="article-image" :style="{ backgroundImage: `url(${article.cover_image || '/placeholder-cover.jpg'})` }"></div>
            
            <div class="article-content">
              <div class="article-meta">
                <span class="article-date">
                  <calendar-icon />
                  {{ formatDate(article.published_at) }}
                </span>
                <span class="article-read-time">
                  <clock-icon />
                  {{ article.read_time }} 分钟阅读
                </span>
              </div>
              
              <h4 class="article-title">{{ article.title }}</h4>
              <p class="article-excerpt">{{ article.excerpt }}</p>
              
              <div class="article-tags">
                <span 
                  class="tag" 
                  v-for="tag in article.tags" 
                  :key="tag.id"
                  @click.stop="navigateToTagArticles(tag.slug)"
                >
                  {{ tag.name }}
                </span>
              </div>
              
              <router-link :to="`/articles/${article.slug}`" class="read-more">
                阅读全文 <arrow-right-icon />
              </router-link>
            </div>
          </div>
        </div>
        
        <!-- 查看所有文章按钮 -->
        <div class="view-all">
          <router-link to="/articles" class="view-all-button">
            查看所有文章
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Calendar as CalendarIcon, Clock as ClockIcon, ArrowRight as ArrowRightIcon } from 'lucide-vue-next';
import { articlesApi } from '@/api';
import { useRouter } from 'vue-router';

const router = useRouter();

// 标签导航功能
const navigateToTagArticles = (tagSlug: string) => {
  router.push(`/articles/tag/${tagSlug}`);
};

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
  cover_image: string;
  read_time: number;
  published_at: string;
  tags: Tag[];
}

// 状态
const featuredArticle = ref<Article | null>(null);
const articles = ref<Article[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

// 获取文章数据
const fetchArticles = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    // 获取精选文章
    const featuredResponse = await articlesApi.getArticles({
      featured: true,
      status: 'published',
      limit: 1
    });
    
    if (featuredResponse.data && featuredResponse.data.length > 0) {
      featuredArticle.value = featuredResponse.data[0];
    }
    
    // 获取普通文章（排除精选文章）
    const articlesResponse = await articlesApi.getArticles({
      featured: false,
      status: 'published',
      limit: 3
    });
    
    if (articlesResponse.data) {
      articles.value = articlesResponse.data;
    }
  } catch (err: any) {
    console.error('Failed to fetch articles:', err);
    error.value = '获取文章列表失败';
  } finally {
    isLoading.value = false;
  }
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

// 页面加载时获取数据
onMounted(() => {
  fetchArticles();
});
</script>

<style scoped>
.blog-section {
  padding: 6rem 2rem;
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

/* 精选文章 */
.featured-article {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 2rem;
  margin-bottom: 4rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.1);
  animation: fadeIn 1s ease-out;
}

.featured-article-content {
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
}

.featured-article-title {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #f8fafc;
}

.featured-article-excerpt {
  color: #94a3b8;
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.featured-article-image {
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

/* 文章列表 */
.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
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
  display: flex;
  flex-direction: column;
  animation: fadeIn 1s ease-out;
  animation-fill-mode: both;
}

.article-card:nth-child(2) {
  animation-delay: 0.2s;
}

.article-card:nth-child(3) {
  animation-delay: 0.4s;
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
  color: #94a3b8;
  font-size: 0.875rem;
}

.article-date,
.article-read-time {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.article-date svg,
.article-read-time svg {
  width: 1rem;
  height: 1rem;
  color: #3b82f6;
}

.article-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #f8fafc;
}

.article-excerpt {
  color: #94a3b8;
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

.tag {
  background: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

.tag:hover {
  background: rgba(59, 130, 246, 0.2);
  transform: translateY(-2px);
}

.read-more {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #3b82f6;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s;
  margin-top: auto;
}

.read-more svg {
  width: 1rem;
  height: 1rem;
  transition: transform 0.3s;
}

.read-more:hover {
  color: #60a5fa;
}

.read-more:hover svg {
  transform: translateX(3px);
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
  .featured-article {
    grid-template-columns: 1fr;
  }
  
  .featured-article-image {
    height: 300px;
    order: -1;
  }
}

@media (max-width: 768px) {
  .articles-grid {
    grid-template-columns: 1fr;
  }
  
  .article-image {
    height: 250px;
  }
}
</style> 