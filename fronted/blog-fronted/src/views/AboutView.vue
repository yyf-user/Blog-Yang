<template>
  <div class="about-container">
    <Navigation />
    
    <main class="about-content">
      <div class="container">
        <div class="about-header">
          <h1 class="about-title">关于<span class="text-gradient">我</span></h1>
          <p class="about-subtitle">了解我的技术背景、专业技能和职业经历</p>
        </div>
        
        <div class="about-sections">
          <!-- 个人简介 -->
          <section class="about-section">
            <h2>个人简介</h2>
            <div class="about-bio">
              <div class="bio-image">
                <img src="https://picsum.photos/seed/profile/300/300" alt="个人照片" />
              </div>
              <div class="bio-content">
                <p>你好！我是一名充满热情的全栈开发工程师，专注于创建高性能、用户友好的Web应用程序。我热爱技术，并且不断学习新的工具和框架，以提高自己的技能水平。</p>
                <p>我拥有计算机科学学士学位，并且在软件开发领域有5年以上的工作经验。我喜欢解决复杂问题，并且善于将技术解决方案与业务需求相结合。</p>
                <p>在我的空闲时间，我喜欢写技术博客、参与开源项目，并且探索新的编程语言和技术。我相信持续学习和知识分享是成为优秀开发者的关键。</p>
              </div>
            </div>
          </section>
          
          <!-- 专业技能 -->
          <section class="about-section">
            <h2>专业技能</h2>
            <div class="skills-container">
              <div class="skill-category">
                <h3>前端开发</h3>
                <ul class="skill-list">
                  <li class="skill-item">
                    <span class="skill-name">Vue.js</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 90%"></div>
                    </div>
                  </li>
                  <li class="skill-item">
                    <span class="skill-name">TypeScript</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 85%"></div>
                    </div>
                  </li>
                  <li class="skill-item">
                    <span class="skill-name">CSS/SCSS</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 95%"></div>
                    </div>
                  </li>
                </ul>
              </div>
              
              <div class="skill-category">
                <h3>后端开发</h3>
                <ul class="skill-list">
                  <li class="skill-item">
                    <span class="skill-name">Python</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 88%"></div>
                    </div>
                  </li>
                  <li class="skill-item">
                    <span class="skill-name">FastAPI</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 82%"></div>
                    </div>
                  </li>
                  <li class="skill-item">
                    <span class="skill-name">数据库设计</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 80%"></div>
                    </div>
                  </li>
                </ul>
              </div>
              
              <div class="skill-category">
                <h3>DevOps</h3>
                <ul class="skill-list">
                  <li class="skill-item">
                    <span class="skill-name">Docker</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 75%"></div>
                    </div>
                  </li>
                  <li class="skill-item">
                    <span class="skill-name">CI/CD</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 70%"></div>
                    </div>
                  </li>
                  <li class="skill-item">
                    <span class="skill-name">云服务</span>
                    <div class="skill-bar">
                      <div class="skill-progress" style="width: 78%"></div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </section>
          
          <!-- 工作经历 -->
          <section class="about-section">
            <h2>工作经历</h2>
            <div class="timeline">
              <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <h3>高级全栈开发工程师</h3>
                  <p class="timeline-company">科技创新有限公司</p>
                  <p class="timeline-date">2021年 - 至今</p>
                  <ul class="timeline-details">
                    <li>负责公司核心产品的前端和后端开发</li>
                    <li>使用Vue.js和FastAPI构建高性能Web应用</li>
                    <li>优化系统架构，提高应用性能和用户体验</li>
                    <li>指导初级开发人员，组织技术分享会</li>
                  </ul>
                </div>
              </div>
              
              <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <h3>Web开发工程师</h3>
                  <p class="timeline-company">互联网科技有限公司</p>
                  <p class="timeline-date">2018年 - 2021年</p>
                  <ul class="timeline-details">
                    <li>参与多个Web应用项目的开发和维护</li>
                    <li>使用React和Node.js构建响应式Web应用</li>
                    <li>实现RESTful API和数据库设计</li>
                    <li>参与敏捷开发流程，提高团队协作效率</li>
                  </ul>
                </div>
              </div>
              
              <div class="timeline-item">
                <div class="timeline-dot"></div>
                <div class="timeline-content">
                  <h3>初级前端开发工程师</h3>
                  <p class="timeline-company">网络科技有限公司</p>
                  <p class="timeline-date">2016年 - 2018年</p>
                  <ul class="timeline-details">
                    <li>负责公司网站和Web应用的前端开发</li>
                    <li>使用HTML, CSS和JavaScript构建用户界面</li>
                    <li>优化网站性能和跨浏览器兼容性</li>
                    <li>参与UI/UX设计讨论和实现</li>
                  </ul>
                </div>
              </div>
            </div>
          </section>
          
          <!-- 教育背景 -->
          <section class="about-section">
            <h2>教育背景</h2>
            <div class="education">
              <div class="education-item">
                <h3>计算机科学学士学位</h3>
                <p class="education-institution">某知名大学</p>
                <p class="education-date">2012年 - 2016年</p>
                <p class="education-details">
                  主修计算机科学，专注于软件工程和Web开发。参与多个实践项目，并获得优秀毕业生称号。
                </p>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
    
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import Navigation from '@/components/Navigation.vue'
import SiteFooter from '@/components/SiteFooter.vue'
</script>

<style scoped>
.about-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.about-content {
  flex: 1;
  padding: 6rem 0;
}

.about-header {
  text-align: center;
  margin-bottom: 4rem;
}

.about-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--color-text);
}

.about-subtitle {
  font-size: 1.25rem;
  color: var(--color-text-muted);
  max-width: 600px;
  margin: 0 auto;
}

.about-sections {
  display: flex;
  flex-direction: column;
  gap: 5rem;
}

.about-section {
  animation: fadeIn 0.5s ease-out;
}

.about-section h2 {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  position: relative;
  display: inline-block;
}

.about-section h2::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  width: 50%;
  height: 3px;
  background: linear-gradient(90deg, var(--color-primary), transparent);
  border-radius: 3px;
}

/* 个人简介样式 */
.about-bio {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 2rem;
  align-items: start;
}

.bio-image img {
  width: 100%;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  border: 3px solid rgba(99, 102, 241, 0.2);
}

.bio-content {
  font-size: 1.1rem;
  line-height: 1.8;
}

.bio-content p {
  margin-bottom: 1.5rem;
}

/* 技能样式 */
.skills-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 3rem;
}

.skill-category h3 {
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--color-primary);
}

.skill-list {
  list-style: none;
  padding: 0;
}

.skill-item {
  margin-bottom: 1.5rem;
}

.skill-name {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.skill-bar {
  height: 8px;
  background: rgba(99, 102, 241, 0.1);
  border-radius: 4px;
  overflow: hidden;
}

.skill-progress {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  border-radius: 4px;
  transition: width 1s ease-out;
}

/* 工作经历时间线 */
.timeline {
  position: relative;
  padding-left: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--color-primary), var(--color-secondary), transparent);
}

.timeline-item {
  position: relative;
  padding-bottom: 3rem;
}

.timeline-dot {
  position: absolute;
  left: -2.5rem;
  top: 0.5rem;
  width: 1rem;
  height: 1rem;
  border-radius: 50%;
  background: var(--color-primary);
  border: 2px solid var(--color-background);
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.3);
}

.timeline-content {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.timeline-content:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.timeline-content h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.timeline-company {
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: 0.25rem;
}

.timeline-date {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.timeline-details {
  padding-left: 1.5rem;
}

.timeline-details li {
  margin-bottom: 0.5rem;
}

/* 教育背景 */
.education-item {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 1.5rem;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.education-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.education-item h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.education-institution {
  font-weight: 600;
  color: var(--color-primary);
  margin-bottom: 0.25rem;
}

.education-date {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.education-details {
  line-height: 1.6;
}

/* 响应式调整 */
@media (max-width: 992px) {
  .about-bio {
    grid-template-columns: 1fr;
  }
  
  .bio-image {
    max-width: 300px;
    margin: 0 auto 2rem;
  }
  
  .skills-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .about-content {
    padding: 5rem 0;
  }
  
  .about-title {
    font-size: 2.5rem;
  }
  
  .about-sections {
    gap: 4rem;
  }
  
  .about-section h2 {
    font-size: 1.75rem;
  }
  
  .timeline {
    padding-left: 1.5rem;
  }
  
  .timeline-dot {
    left: -2rem;
  }
}
</style>
