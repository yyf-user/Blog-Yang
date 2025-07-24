<script setup lang="ts">
import Navigation from '@/components/Navigation.vue';
import HeroSection from '@/components/HeroSection.vue';
import AboutSection from '@/components/AboutSection.vue';
import BlogSection from '@/components/BlogSection.vue';
import ProjectsSection from '@/components/ProjectsSection.vue';
import ContactSection from '@/components/ContactSection.vue';
import SiteFooter from '@/components/SiteFooter.vue';
import { tagsApi } from '@/api';
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

// 获取常用标签以便在首页显示并提供点击筛选功能
const commonTags = ref<any[]>([]);
const router = useRouter();

// 获取常用标签
const fetchCommonTags = async () => {
  try {
    const response = await tagsApi.getTags();
    if (response.data && Array.isArray(response.data)) {
      // 只取前5个标签用于展示
      commonTags.value = response.data.slice(0, 5);
    }
  } catch (error) {
    console.error("获取标签失败:", error);
  }
};

// 点击标签时跳转到文章列表并应用筛选
const navigateToTagArticles = (tagSlug: string) => {
  router.push(`/articles/tag/${tagSlug}`);
};

onMounted(() => {
  fetchCommonTags();
});
</script>

<template>
  <div class="home-container">
    <navigation />
    
    <div id="home">
      <hero-section />
    </div>
    
    <div id="about">
      <about-section />
    </div>
    
    <!-- 常用标签筛选 -->
    <div class="common-tags-section">
      <div class="container">
        <h2 class="tags-title">热门标签</h2>
        <div class="tags-container">
          <div 
            v-for="tag in commonTags" 
            :key="tag.id" 
            class="tag-item"
            @click="navigateToTagArticles(tag.slug)"
          >
            {{ tag.name }}
          </div>
        </div>
      </div>
    </div>
    
    <div id="blog">
      <blog-section />
    </div>
    
    <div id="projects">
      <projects-section />
    </div>
    
    <div id="contact">
      <contact-section />
    </div>
    
    <site-footer />
  </div>
</template>

<style scoped>
.home-container {
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

#home, #about, #blog, #projects, #contact {
  scroll-margin-top: 80px; /* 适应固定导航栏的高度 */
  position: relative;
}

/* 添加半透明背景以提高内容可读性 */
#about, #blog, #projects, #contact {
  background-color: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(5px);
  margin: 2rem 0;
  border-radius: 1rem;
}

/* 常用标签样式 */
.common-tags-section {
  padding: 3rem 0;
  background-color: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(5px);
  margin: 2rem 0;
  border-radius: 1rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.tags-title {
  text-align: center;
  font-size: 1.75rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.tag-item {
  background: rgba(59, 130, 246, 0.1);
  color: var(--color-primary, #3b82f6);
  padding: 0.5rem 1.5rem;
  border-radius: 2rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid rgba(59, 130, 246, 0.2);
  font-size: 1rem;
}

.tag-item:hover {
  background: rgba(59, 130, 246, 0.2);
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
}

@media (max-width: 768px) {
  .tag-item {
    padding: 0.4rem 1rem;
    font-size: 0.875rem;
  }
}
</style>
