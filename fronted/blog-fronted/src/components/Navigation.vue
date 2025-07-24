<template>
  <header class="site-header" :class="{ 'scrolled': isScrolled }">
    <div class="container">
      <div class="logo">
        <router-link to="/">
          <div class="logo-icon">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-zap">
              <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
            </svg>
          </div>
          <span class="logo-text">博客Yang</span>
        </router-link>
      </div>
      
      <nav class="main-nav" :class="{ 'active': navActive }">
        <ul class="nav-links">
          <li><router-link to="/" @click="scrollToSection('home')">首页</router-link></li>
          <li><router-link to="/#about" @click="scrollToSection('about')">关于</router-link></li>
          <li><router-link to="/#blog" @click="scrollToSection('blog')">博客</router-link></li>
          <li><router-link to="/#projects" @click="scrollToSection('projects')">项目</router-link></li>
          <li><router-link to="/contact">联系</router-link></li>
          <li v-if="!isAuthenticated">
            <router-link to="/login" class="login-button">登录</router-link>
          </li>
          <li v-else-if="isAuthenticated && isAdmin">
            <button class="admin-button" @click="openAdminPanel">管理后台</button>
            <button class="logout-button" @click="handleLogout">登出</button>
          </li>
          <li v-else>
            <button class="logout-button" @click="handleLogout">登出</button>
          </li>
          <li>
            <a href="https://github.com/yyf-user/nebula-background-forge" target="_blank" class="github-link">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="github-icon">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
              </svg>
              GitHub
            </a>
          </li>
        </ul>
      </nav>
      
      <button class="mobile-nav-toggle" @click="toggleNav" aria-label="切换导航">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const isAuthenticated = ref(authStore.isAuthenticated);
const isScrolled = ref(false);
const navActive = ref(false);

// 判断当前用户是否为管理员
const isAdmin = computed(() => {
  return authStore.user?.role === 'admin';
});

// 在新标签页中打开管理后台
const openAdminPanel = () => {
  const adminUrl = `${window.location.origin}/admin`;
  window.open(adminUrl, '_blank');
};

// 处理滚动事件
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50;
};

// 切换导航菜单
const toggleNav = () => {
  navActive.value = !navActive.value;
  document.body.classList.toggle('nav-open');
};

// 关闭导航菜单
const closeNav = () => {
  navActive.value = false;
  document.body.classList.remove('nav-open');
};

// 滚动到指定区域
const scrollToSection = (sectionId: string) => {
  closeNav();
  
  // 如果当前不在首页，先导航到首页
  if (route.path !== '/') {
    router.push('/').then(() => {
      setTimeout(() => {
        const element = document.getElementById(sectionId);
        if (element) {
          element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }, 100);
    });
  } else {
    // 如果已经在首页，直接滚动
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
      });
    }
  }
};

// 处理登出
const handleLogout = () => {
  authStore.logout();
  router.push('/login');
};

// 监听认证状态变化
watch(() => authStore.isAuthenticated, (newVal) => {
  isAuthenticated.value = newVal;
});

// 监听路由变化
watch(() => route.path, () => {
  // 关闭移动端菜单
  closeNav();
});

// 监听路由变化，更新导航栏高亮
watch(() => route.path, (newPath) => {
  // 更新导航高亮
  setTimeout(() => {
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
      link.classList.remove('active');
      
      const href = link.getAttribute('href');
      if (href) {
        if (href === '/' && newPath === '/') {
          link.classList.add('active');
        } else if (href.startsWith('/#') && newPath === '/' && route.hash === href.substring(1)) {
          link.classList.add('active');
        } else if (href === newPath) {
          link.classList.add('active');
        }
      }
    });
  }, 100);
});

// 生命周期钩子
onMounted(() => {
  window.addEventListener('scroll', handleScroll);
  
  // 初始化时检查认证状态
  isAuthenticated.value = authStore.isAuthenticated;
  
  // 如果有hash，滚动到对应区域
  if (route.hash) {
    setTimeout(() => {
      const element = document.getElementById(route.hash.substring(1));
      if (element) {
        element.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    }, 100);
  }
  
  // 如果是管理员用户，确保使用正确的头像
  if (authStore.user && authStore.user.role === 'admin') {
    const userData = JSON.parse(localStorage.getItem('user') || '{}');
    userData.avatar_url = '/touxiang.png';
    localStorage.setItem('user', JSON.stringify(userData));
  }
});

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.site-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  padding: 1.5rem 0;
  transition: all 0.3s ease;
  z-index: 100;
  background: transparent;
}

.site-header.scrolled {
  background-color: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  padding: 1rem 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo a {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #f8fafc;
}

.logo-icon {
  width: 2rem;
  height: 2rem;
  color: #3b82f6;
  margin-right: 0.5rem;
}

.logo-text {
  font-size: 1.5rem;
  font-weight: 700;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.main-nav {
  display: flex;
  align-items: center;
}

.nav-links {
  display: flex;
  list-style: none;
  margin: 0;
  padding: 0;
  gap: 2rem;
}

.nav-links a {
  color: #e2e8f0;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
  display: block;
}

.nav-links a:hover,
.nav-links a.active {
  color: #3b82f6;
}

/* 下拉菜单样式 */
.dropdown {
  position: relative;
}

.dropdown-toggle {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  cursor: pointer;
}

.dropdown-toggle svg {
  transition: transform 0.3s;
}

.dropdown.active .dropdown-toggle svg {
  transform: rotate(180deg);
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  background-color: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 0.5rem;
  padding: 0.5rem 0;
  min-width: 160px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
  opacity: 0;
  visibility: hidden;
  transform: translateY(10px);
  transition: all 0.3s;
  z-index: 100;
}

.dropdown-menu.active {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu li {
  display: block;
}

.dropdown-menu a {
  padding: 0.5rem 1rem;
  white-space: nowrap;
}

.dropdown-menu a:hover {
  background-color: rgba(59, 130, 246, 0.1);
}

.login-button, .logout-button, .admin-button {
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  display: inline-block;
  text-decoration: none;
  margin-left: 0.5rem;
}

.login-button:hover, .logout-button:hover, .admin-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
  color: white;
}

.admin-button {
  background: linear-gradient(90deg, #10b981, #059669);
}

.admin-button:hover {
  background: linear-gradient(90deg, #059669, #047857);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.5);
}

.github-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #e2e8f0;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.github-link:hover {
  color: #3b82f6;
}

.github-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.mobile-nav-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  width: 30px;
  height: 24px;
  position: relative;
  z-index: 1001;
}

.mobile-nav-toggle span {
  display: block;
  width: 30px;
  height: 2px;
  background-color: #f8fafc;
  margin: 5px 0;
  transition: all 0.3s;
}

@media (max-width: 1024px) {
  .nav-links {
    gap: 1.5rem;
  }
}

@media (max-width: 768px) {
  .mobile-nav-toggle {
    display: block;
  }
  
  .main-nav {
    position: fixed;
    top: 0;
    right: 0;
    width: 70%;
    height: 100vh;
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(10px);
    transform: translateX(100%);
    transition: transform 0.3s ease;
    z-index: 1000;
    padding-top: 5rem;
  }
  
  .main-nav.active {
    transform: translateX(0);
  }
  
  .nav-links {
    flex-direction: column;
    align-items: center;
    gap: 1.5rem;
    width: 100%;
  }
  
  body.nav-open {
    overflow: hidden;
  }
  
  .mobile-nav-toggle.active span:nth-child(1) {
    transform: rotate(45deg) translate(5px, 5px);
  }
  
  .mobile-nav-toggle.active span:nth-child(2) {
    opacity: 0;
  }
  
  .mobile-nav-toggle.active span:nth-child(3) {
    transform: rotate(-45deg) translate(7px, -7px);
  }
}
</style> 