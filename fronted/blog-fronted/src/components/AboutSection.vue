<template>
  <section id="about" class="about-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">关于<span class="highlight">我</span></h2>
        <p class="section-subtitle">探索我的技术旅程与专业领域</p>
      </div>
      
      <div class="about-content">
        <div class="about-text">
          <h3>个人简介</h3>
          <p>
            作为一名全栈开发者，我热衷于构建优雅、高效且用户友好的数字解决方案。我结合了创造性思维和技术专长，将复杂的问题转化为简洁的解决方案。
          </p>
          <p>
            我的技术旅程始于对编程的纯粹好奇，随着时间的推移，这种好奇心转变为对构建可扩展系统和优化用户体验的热情。我不断追求学习和掌握新技术，以保持在这个快速发展的行业的前沿。
          </p>
          
          <h3>核心价值观</h3>
          <div class="values">
            <div class="value-item">
              <div class="value-icon"><zap-icon /></div>
              <div class="value-text">
                <strong>持续学习</strong>
                <span>不断探索新技术和最佳实践</span>
              </div>
            </div>
            <div class="value-item">
              <div class="value-icon"><users-icon /></div>
              <div class="value-text">
                <strong>用户为中心</strong>
                <span>构建以人为本的直观解决方案</span>
              </div>
            </div>
            <div class="value-item">
              <div class="value-icon"><shield-icon /></div>
              <div class="value-text">
                <strong>代码质量</strong>
                <span>注重可维护性、可扩展性和安全性</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="tech-stack">
        <h3 class="tech-stack-title">技术栈</h3>
        
        <div class="stack-grid">
          <div class="stack-category">
            <div class="category-header">
              <code2-icon />
              <h4>前端开发</h4>
            </div>
            <ul class="tech-list">
              <li>Vue.js / React.js</li>
              <li>TypeScript</li>
              <li>Tailwind CSS</li>
              <li>SCSS / CSS3</li>
              <li>Vite / Webpack</li>
              <li>Responsive Design</li>
              <li></li>
            </ul>
          </div>
          
          <div class="stack-category">
            <div class="category-header">
              <database-icon />
              <h4>后端开发</h4>
            </div>
            <ul class="tech-list">
              <li>FastAPI / Flask</li>
              <li>Node.js / Express</li>
              <li>MySQL / PostgreSQL</li>
              <li>MongoDB</li>
              <li>Redis</li>
              <li>RESTful API</li>
              <li></li>
            </ul>
          </div>
          
          <div class="stack-category">
            <div class="category-header">
              <smartphone-icon />
              <h4>移动开发</h4>
            </div>
            <ul class="tech-list">
              <li>React Native</li>
              <li>Flutter</li>
              <li>PWA</li>
              <li>Android SDK</li>
              <li>Xamarin / .NET MAUI</li>
              <li>Cordova/PhoneGap</li>
              <li>AppMaster、Bubble、PowerApps</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { 
  Zap as ZapIcon, 
  Users as UsersIcon, 
  Shield as ShieldIcon,
  Code2 as Code2Icon,
  Database as DatabaseIcon,
  Smartphone as SmartphoneIcon,
  Cloud as CloudIcon
} from 'lucide-vue-next';
</script>

<style scoped>
.about-section {
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

.about-content {
  display: flex;
  flex-direction: column;
  margin-bottom: 4rem;
  animation: fadeIn 1s ease-out;
}

.about-text h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: #e2e8f0;
}

.about-text p {
  color: #94a3b8;
  line-height: 1.7;
  margin-bottom: 1.5rem;
}

.values {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 2rem;
}

.value-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(30, 41, 59, 0.5);
  border-radius: 0.75rem;
  border: 1px solid rgba(99, 102, 241, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.value-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  border-color: rgba(99, 102, 241, 0.3);
}

.value-icon {
  flex-shrink: 0;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 0.5rem;
  color: #3b82f6;
}

.value-text {
  display: flex;
  flex-direction: column;
}

.value-text strong {
  font-size: 1.125rem;
  color: #e2e8f0;
  margin-bottom: 0.25rem;
}

.value-text span {
  color: #94a3b8;
  font-size: 0.875rem;
}

.tech-stack {
  animation: fadeIn 1s ease-out;
  animation-delay: 0.3s;
  opacity: 0;
  animation-fill-mode: forwards;
}

.tech-stack-title {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 2rem;
  text-align: center;
  color: #e2e8f0;
}

.stack-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.stack-category {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 0.75rem;
  padding: 1.5rem;
  border: 1px solid rgba(99, 102, 241, 0.1);
  transition: transform 0.3s ease;
}

.stack-category:hover {
  transform: translateY(-5px);
  border-color: rgba(99, 102, 241, 0.3);
}

.category-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(99, 102, 241, 0.1);
}

.category-header svg {
  width: 1.5rem;
  height: 1.5rem;
  color: #3b82f6;
}

.category-header h4 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: #e2e8f0;
}

.tech-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.tech-list li {
  padding: 0.5rem 0;
  color: #94a3b8;
  position: relative;
  padding-left: 1.5rem;
}

.tech-list li::before {
  content: "•";
  color: #3b82f6;
  position: absolute;
  left: 0.25rem;
  top: 0.5rem;
  font-size: 1.25rem;
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

@media (max-width: 768px) {
  .about-content {
    flex-direction: column;
  }
  
  .about-image {
    width: 100%;
    margin-bottom: 2rem;
  }
  
  .values {
    grid-template-columns: 1fr;
  }
  
  .stack-grid {
    grid-template-columns: 1fr;
  }
}
</style> 