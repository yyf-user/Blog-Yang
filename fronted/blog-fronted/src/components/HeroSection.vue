<template>
  <section id="home" class="hero-section">
    <div class="container">
      <div class="hero-content">
        <div class="tech-icons">
          <div class="tech-icon"><code-icon /></div>
          <div class="tech-icon"><cpu-icon /></div>
          <div class="tech-icon"><zap-icon /></div>
        </div>
        
        <h1 class="hero-title">
          构建
          <span class="gradient-text">未来</span>
          科技
        </h1>
        
        <p class="hero-subtitle">
          探索前沿技术，分享编程智慧，记录数字时代的创新之路
        </p>
        
        <div class="cta-buttons">
          <a href="#blog" class="primary-button">开始阅读</a>
          <a href="#about" class="secondary-button">关于我</a>
        </div>
        
        <div class="stats">
          <div class="stat">
            <div class="stat-number">50+</div>
            <div class="stat-label">技术文章</div>
          </div>
          <div class="stat">
            <div class="stat-number">12+</div>
            <div class="stat-label">开源项目</div>
          </div>
          <div class="stat">
            <div class="stat-number">3+</div>
            <div class="stat-label">年经验</div>
          </div>
        </div>
      </div>
      
      <div class="scroll-indicator">
        <arrow-down-icon />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Code as CodeIcon, Cpu as CpuIcon, Zap as ZapIcon, ArrowDown as ArrowDownIcon } from 'lucide-vue-next';
</script>

<style scoped>
.hero-section {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  padding: 6rem 2rem;
  overflow: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
  position: relative;
  z-index: 2;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  animation: fadeInUp 1s ease-out;
}

.tech-icons {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-bottom: 2rem;
}

.tech-icon {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  opacity: 0.7;
  animation: float 3s ease-in-out infinite;
}

.tech-icon:nth-child(2) {
  animation-delay: 1s;
  color: #6366f1;
}

.tech-icon:nth-child(3) {
  animation-delay: 2s;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  color: #f8fafc;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.gradient-text {
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  padding: 0 0.5rem;
}

.hero-subtitle {
  font-size: 1.25rem;
  color: #94a3b8;
  margin-bottom: 2.5rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 3rem;
}

.primary-button, .secondary-button {
  padding: 0.75rem 2rem;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
  text-decoration: none;
}

.primary-button {
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  color: white;
  border: none;
}

.primary-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(59, 130, 246, 0.4);
}

.secondary-button {
  background: rgba(99, 102, 241, 0.1);
  color: #6366f1;
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.secondary-button:hover {
  background: rgba(99, 102, 241, 0.2);
  transform: translateY(-2px);
}

.stats {
  display: flex;
  justify-content: center;
  gap: 3rem;
}

.stat {
  text-align: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.stat-label {
  font-size: 0.875rem;
  color: #94a3b8;
}

.scroll-indicator {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  color: #94a3b8;
  animation: bounce 2s infinite;
}

@keyframes fadeInUp {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-10px);
  }
  100% {
    transform: translateY(0px);
  }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {
    transform: translateY(0);
  }
  40% {
    transform: translateY(-10px);
  }
  60% {
    transform: translateY(-5px);
  }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 3rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .cta-buttons {
    flex-direction: column;
    gap: 0.75rem;
    max-width: 250px;
    margin-left: auto;
    margin-right: auto;
  }
  
  .stats {
    flex-direction: column;
    gap: 1.5rem;
  }
}
</style> 