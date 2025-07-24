<template>
  <div class="article-detail">
    <Navigation />
    
    <main class="article-content">
      <div class="container">
        <div v-if="isLoading" class="loading-state">
          <div class="loading-spinner"></div>
          <p>加载文章内容...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <h2>抱歉，加载失败</h2>
          <p>{{ error }}</p>
          <router-link to="/articles" class="back-button">返回文章列表</router-link>
        </div>
        
        <article v-else class="article">
          <header class="article-header">
            <div class="article-meta">
              <span class="article-date">
                <CalendarIcon />
                {{ formatDate(article.published_at) }}
              </span>
              <span class="article-read-time">
                <ClockIcon />
                {{ article.read_time }} 分钟阅读
              </span>
            </div>
            
            <h1 class="article-title">{{ article.title }}</h1>
            
            <div class="article-tags">
              <span class="tag" v-for="tag in article.tags" :key="tag.id">
                {{ tag.name }}
              </span>
            </div>
            
            <div class="article-cover" v-if="article.cover_image">
              <img :src="article.cover_image" :alt="article.title">
            </div>
          </header>
          
          <div class="article-body">
            <!-- 使用安全的方式渲染内容 -->
            <div class="markdown-content">
              <div v-for="(paragraph, index) in formattedParagraphs" :key="index">
                <p v-if="!paragraph.startsWith('#')">{{ paragraph }}</p>
                <h2 v-else-if="paragraph.startsWith('## ')">{{ paragraph.substring(3) }}</h2>
                <h3 v-else-if="paragraph.startsWith('### ')">{{ paragraph.substring(4) }}</h3>
                <h4 v-else-if="paragraph.startsWith('#### ')">{{ paragraph.substring(5) }}</h4>
              </div>
            </div>
          </div>
          
          <footer class="article-footer">
            <div class="article-author" v-if="article.author">
              <img :src="article.author.avatar_url || '/default-avatar.jpg'" :alt="article.author.full_name || article.author.username" class="author-avatar">
              <div class="author-info">
                <h3>{{ article.author.full_name || article.author.username }}</h3>
                <p>{{ article.author.bio || '博客作者' }}</p>
              </div>
            </div>
            
            <div class="article-share">
              <h3>分享文章</h3>
              <div class="share-buttons">
                <a href="#" @click.prevent="shareTwitter" class="share-button twitter">
                  <TwitterIcon />
                </a>
                <a href="#" @click.prevent="shareFacebook" class="share-button facebook">
                  <FacebookIcon />
                </a>
                <a href="#" @click.prevent="shareLinkedIn" class="share-button linkedin">
                  <LinkedinIcon />
                </a>
              </div>
            </div>
          </footer>
        </article>
        
        <!-- 相关文章 -->
        <div class="related-articles" v-if="relatedArticles.length">
          <h2>相关文章</h2>
          <div class="articles-grid">
            <div class="article-card" v-for="relatedArticle in relatedArticles" :key="relatedArticle.id">
              <div class="article-image" :style="{ backgroundImage: `url(${relatedArticle.cover_image || '/placeholder-cover.jpg'})` }"></div>
              <div class="article-content">
                <h4 class="article-title">{{ relatedArticle.title }}</h4>
                <p class="article-excerpt">{{ relatedArticle.excerpt }}</p>
                <router-link :to="`/articles/${relatedArticle.slug}`" class="read-more">
                  阅读全文
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { 
  Calendar as CalendarIcon,
  Clock as ClockIcon,
  Twitter as TwitterIcon,
  Facebook as FacebookIcon,
  Linkedin as LinkedinIcon 
} from 'lucide-vue-next';
import Navigation from '../components/Navigation.vue';
import SiteFooter from '../components/SiteFooter.vue';
import { articlesApi } from '@/api';

// 接口定义
interface Author {
  id: number;
  username: string;
  full_name?: string;
  bio?: string;
  avatar_url?: string;
}

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
  author: Author;
  read_time: number;
  view_count: number;
  published_at: string;
  tags: Tag[];
}

// 状态
const route = useRoute();
const article = ref<Article | any>({});
const relatedArticles = ref<Article[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);

// 从URL获取文章slug
const slug = computed(() => route.params.id as string);

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

// 格式化文章内容（分割成段落和标题）
const formattedParagraphs = computed(() => {
  if (!article.value.content) return [];
  
  // 简单的段落处理，按两个换行符分割
  return article.value.content.split('\n\n').filter(p => p.trim() !== '');
});

// 获取文章数据
const fetchArticle = async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    // 获取文章详情
    const articleResponse = await articlesApi.getArticleBySlug(slug.value);
    article.value = articleResponse.data;
    
    // 获取相关文章（同一标签的其他文章）
    if (article.value && article.value.tags && article.value.tags.length > 0) {
      const tagId = article.value.tags[0].id;
      const relatedResponse = await articlesApi.getArticles({
        status: 'published',
        tag: tagId,
        limit: 2
      });
      
      // 排除当前文章
      if (relatedResponse.data) {
        relatedArticles.value = relatedResponse.data.filter(
          (a: Article) => a.id !== article.value.id
        );
      }
    }
  } catch (err: any) {
    console.error('Failed to fetch article:', err);
    error.value = '无法加载文章，请稍后再试';
  } finally {
    isLoading.value = false;
  }
};

// 分享功能
const shareTwitter = () => {
  const text = encodeURIComponent(`${article.value.title} | 科技博客`);
  const url = encodeURIComponent(window.location.href);
  window.open(`https://twitter.com/intent/tweet?text=${text}&url=${url}`, '_blank');
};

const shareFacebook = () => {
  const url = encodeURIComponent(window.location.href);
  window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}`, '_blank');
};

const shareLinkedIn = () => {
  const url = encodeURIComponent(window.location.href);
  const title = encodeURIComponent(article.value.title);
  window.open(`https://www.linkedin.com/shareArticle?mini=true&url=${url}&title=${title}`, '_blank');
};

// 页面加载时获取数据
onMounted(() => {
  fetchArticle();
});
</script>

<style scoped>
.article-detail {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.article-content {
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

/* 文章样式 */
.article {
  animation: fadeIn 0.8s ease-out;
}

.article-header {
  margin-bottom: 2.5rem;
}

.article-meta {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--color-text-muted);
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
  color: var(--color-primary);
}

.article-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  color: var(--color-text);
  line-height: 1.2;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.tag {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary);
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
}

.article-cover {
  margin-bottom: 2.5rem;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.article-cover img {
  width: 100%;
  height: auto;
  display: block;
}

/* 文章内容 */
.article-body {
  margin-bottom: 3rem;
  color: var(--color-text-light);
  font-size: 1.125rem;
  line-height: 1.8;
}

.markdown-content h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin: 2rem 0 1rem;
  color: var(--color-text);
}

.markdown-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin: 1.75rem 0 1rem;
  color: var(--color-text);
}

.markdown-content p {
  margin-bottom: 1.25rem;
}

/* 文章页脚 */
.article-footer {
  display: flex;
  flex-direction: column;
  gap: 2rem;
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.article-author {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.author-avatar {
  width: 5rem;
  height: 5rem;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid rgba(59, 130, 246, 0.2);
}

.author-info h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.author-info p {
  color: var(--color-text-muted);
}

.article-share {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.article-share h3 {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 0.75rem;
}

.share-buttons {
  display: flex;
  gap: 1rem;
}

.share-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.share-button.twitter {
  background-color: #1DA1F2;
  color: white;
}

.share-button.facebook {
  background-color: #1877F2;
  color: white;
}

.share-button.linkedin {
  background-color: #0A66C2;
  color: white;
}

.share-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.share-button svg {
  width: 1.25rem;
  height: 1.25rem;
}

/* 相关文章 */
.related-articles {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.related-articles h2 {
  font-size: 1.75rem;
  font-weight: 700;
  margin-bottom: 2rem;
  color: var(--color-text);
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
}

.article-card {
  background: var(--color-surface);
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
  animation: fadeIn 1s ease-out;
  animation-fill-mode: both;
  border: 1px solid rgba(99, 102, 241, 0.1);
}

.article-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.article-image {
  height: 160px;
  background-size: cover;
  background-position: center;
}

.article-content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.article-card .article-title {
  font-size: 1.125rem;
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
  font-size: 0.875rem;
}

.read-more {
  display: inline-block;
  color: var(--color-primary);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s;
  font-size: 0.875rem;
}

.read-more:hover {
  color: var(--color-secondary);
}

@media (max-width: 768px) {
  .article-content {
    padding: 2rem 1.5rem;
  }
  
  .article-title {
    font-size: 2rem;
  }
  
  .article-body {
    font-size: 1rem;
  }
  
  .article-footer {
    flex-direction: column;
  }
  
  .articles-grid {
    grid-template-columns: 1fr;
  }
}
</style> 