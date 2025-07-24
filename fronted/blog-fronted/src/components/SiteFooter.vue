<template>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-logo">
          <div class="logo">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lightning-icon">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
            <span>博客Yang</span>
          </div>
          <p class="footer-description">
            探索前沿技术，分享编程智慧，记录数字时代的创新之路
          </p>
        </div>
        
        <div class="footer-links">
          <div class="footer-links-column">
            <h4>页面导航</h4>
            <ul>
              <li><a href="#home">首页</a></li>
              <li><a href="#about">关于</a></li>
              <li><a href="#blog">博客</a></li>
              <li><a href="#projects">项目</a></li>
              <li><a href="#contact">联系</a></li>
            </ul>
          </div>
          
          <div class="footer-links-column">
            <h4>资源链接</h4>
            <ul>
              <li><router-link to="/articles">所有文章</router-link></li>
              <li><router-link to="/projects">所有项目</router-link></li>
              <li><router-link to="/archives">归档</router-link></li>
              <li><router-link to="/tags">标签</router-link></li>
            </ul>
          </div>
          
          <div class="footer-links-column">
            <h4>联系方式</h4>
            <ul class="contact-links">
              <li>
                <mail-icon />
                <span>3560543799@qq.com</span>
              </li>
              <li>
                <map-pin-icon />
                <span>中国</span>
              </li>
              <li>
                <github-icon />
                <a href="https://github.com/" target="_blank" rel="noopener noreferrer">GitHub</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <div class="copyright">
          &copy; {{ new Date().getFullYear() }} 科技博客. 保留所有权利.
        </div>
        
        <div class="social-links">
          <a href="https://github.com/yyf-user/nebula-background-forge" target="_blank" rel="noopener noreferrer" class="social-link">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="social-icon">
              <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
            </svg>
          </a>
          <a href="https://linkedin.com/" target="_blank" rel="noopener noreferrer" class="social-link">
            <linkedin-icon />
          </a>
          <a href="https://twitter.com/" target="_blank" rel="noopener noreferrer" class="social-link">
            <twitter-icon />
          </a>
        </div>
      </div>
    </div>
    
    <div class="footer-decoration">
      <div class="footer-grid"></div>
      <div class="footer-glow"></div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { 
  Mail as MailIcon, 
  MapPin as MapPinIcon,
  Github as GithubIcon,
  Linkedin as LinkedinIcon,
  Twitter as TwitterIcon
} from 'lucide-vue-next';
</script>

<style scoped>
.site-footer {
  background-color: rgba(15, 23, 42, 0.8);
  position: relative;
  overflow: hidden;
  border-top: 1px solid rgba(99, 102, 241, 0.2);
  padding: 4rem 2rem 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  position: relative;
  z-index: 2;
}

.footer-content {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-logo {
  display: flex;
  flex-direction: column;
}

.logo {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1.25rem;
}

.lightning-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #3b82f6;
}

.logo span {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.footer-description {
  color: #94a3b8;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  max-width: 350px;
}

.footer-links {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 2rem;
}

.footer-links-column h4 {
  color: #f8fafc;
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 1.25rem;
  position: relative;
}

.footer-links-column h4::after {
  content: '';
  position: absolute;
  bottom: -0.5rem;
  left: 0;
  width: 2rem;
  height: 2px;
  background: linear-gradient(90deg, #3b82f6, transparent);
}

.footer-links-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links-column ul li {
  margin-bottom: 0.75rem;
}

.footer-links-column ul li a {
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.3s;
  display: inline-block;
}

.footer-links-column ul li a:hover {
  color: #3b82f6;
  transform: translateX(3px);
}

.contact-links li {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.contact-links li svg {
  width: 1rem;
  height: 1rem;
  color: #3b82f6;
}

.contact-links li span, .contact-links li a {
  color: #94a3b8;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.copyright {
  color: #64748b;
  font-size: 0.875rem;
}

.social-links {
  display: flex;
  gap: 1rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  background: rgba(30, 41, 59, 0.5);
  color: #94a3b8;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: #3b82f6;
  color: white;
  transform: translateY(-3px);
}

.social-link svg {
  width: 1rem;
  height: 1rem;
}

.footer-decoration {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
  z-index: 1;
}

.footer-grid {
  position: absolute;
  width: 200%;
  height: 100%;
  top: 0;
  left: -50%;
  background-image: 
    linear-gradient(rgba(59, 130, 246, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.05) 1px, transparent 1px);
  background-size: 30px 30px;
  opacity: 0.5;
}

.footer-glow {
  position: absolute;
  bottom: -150px;
  left: 50%;
  transform: translateX(-50%);
  width: 500px;
  height: 300px;
  background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
  filter: blur(50px);
}

@media (max-width: 992px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .footer-description {
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .footer-links {
    grid-template-columns: 1fr 1fr;
  }
  
  .footer-bottom {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }
}

@media (max-width: 576px) {
  .footer-links {
    grid-template-columns: 1fr;
  }
}
</style> 