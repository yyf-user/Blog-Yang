import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: false }
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { guest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { guest: true }
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/articles',
      name: 'articles',
      component: () => import('../views/ArticlesView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/articles/tag/:tag',
      name: 'articles-by-tag',
      component: () => import('../views/ArticlesView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/articles/search/:query',
      name: 'articles-search',
      component: () => import('../views/ArticlesView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/articles/:id',
      name: 'article-detail',
      component: () => import('../views/ArticleDetailView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/projects',
      name: 'projects',
      component: () => import('../views/ProjectsView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/projects/:slug',
      name: 'project-detail',
      component: () => import('../views/ProjectDetailView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue'),
      meta: { requiresAuth: false }
    },
    {
      path: '/admin',
      name: 'admin',
      component: () => import('../views/admin/AdminView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true },
      children: [
        {
          path: '',
          name: 'admin-dashboard',
          component: () => import('../views/admin/DashboardView.vue'),
        },
        {
          path: 'articles',
          name: 'admin-articles',
          component: () => import('../views/admin/ArticlesManager.vue'),
        },
        {
          path: 'articles/create',
          name: 'admin-article-create',
          component: () => import('../views/admin/ArticleEditor.vue'),
        },
        {
          path: 'articles/edit/:id',
          name: 'admin-article-edit',
          component: () => import('../views/admin/ArticleEditor.vue'),
        },
        {
          path: 'projects',
          name: 'admin-projects',
          component: () => import('../views/admin/ProjectsManager.vue'),
        },
        {
          path: 'projects/create',
          name: 'admin-project-create',
          component: () => import('../views/admin/ProjectEditor.vue'),
        },
        {
          path: 'projects/edit/:id',
          name: 'admin-project-edit',
          component: () => import('../views/admin/ProjectEditor.vue'),
        },
        {
          path: 'messages',
          name: 'admin-messages',
          component: () => import('../views/admin/MessagesManager.vue'),
        },
        {
          path: 'tags',
          name: 'admin-tags',
          component: () => import('../views/admin/TagsManager.vue'),
        },
        {
          path: 'api-stats',
          name: 'admin-api-stats',
          component: () => import('../views/admin/ApiStatsView.vue'),
        },
        {
          path: 'api-paths',
          name: 'admin-api-paths',
          component: () => import('../views/admin/ApiPathsView.vue'),
        },
        {
          path: 'profile',
          name: 'admin-profile',
          component: () => import('../views/admin/ProfileView.vue'),
        },
        {
          path: 'settings',
          name: 'admin-settings',
          component: () => import('../views/admin/SettingsManager.vue'),
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'not-found',
      component: () => import('../views/NotFoundView.vue')
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    }
    
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
        top: 80 // 考虑固定导航栏的高度
      };
    }
    
    return { top: 0, behavior: 'smooth' };
  }
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const requiresAdmin = to.matched.some(record => record.meta.requiresAdmin)
  const isGuestRoute = to.matched.some(record => record.meta.guest)
  
  // 检查认证状态
  await authStore.checkAuth()
  
  // 如果需要管理员权限，检查用户是否是管理员
  if (requiresAdmin && authStore.user?.role !== 'admin') {
    return next({ name: 'home' })
  }
  
  // 如果需要认证但未登录，重定向到登录页面
  if (requiresAuth && !authStore.isAuthenticated) {
    return next({ name: 'login' })
  }
  
  // 如果已登录但访问游客页面（如登录、注册），重定向到首页
  if (isGuestRoute && authStore.isAuthenticated) {
    return next({ name: 'home' })
  }
  
  next()
})

// 导航后处理
router.afterEach((to, from) => {
  // 处理导航栏高亮
  if (to.path === '/') {
    // 如果有hash，则高亮对应的导航项
    if (to.hash) {
      const sectionId = to.hash.substring(1); // 去掉#号
      setTimeout(() => {
        const navLinks = document.querySelectorAll('.nav-links a');
        navLinks.forEach(link => {
          link.classList.remove('active');
          if (link.getAttribute('href') === to.hash) {
            link.classList.add('active');
          }
        });
      }, 100);
    }
  }
});

export default router
