<script setup lang="ts">
import Navigation from '@/components/Navigation.vue';
import HeroSection from '@/components/HeroSection.vue';
import AboutSection from '@/components/AboutSection.vue';
import BlogSection from '@/components/BlogSection.vue';
import ProjectsSection from '@/components/ProjectsSection.vue';
import ContactSection from '@/components/ContactSection.vue';
import SiteFooter from '@/components/SiteFooter.vue';
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
</style>
