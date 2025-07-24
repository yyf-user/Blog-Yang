<template>
  <div class="admin-container">
    <div class="admin-header">
      <div class="header-left">
        <h1>管理员控制台</h1>
        <router-link to="/" class="home-link">
          <home-icon class="home-icon" />
          <span>返回首页</span>
        </router-link>
      </div>
      <div class="user-info" v-if="user">
        <div class="avatar-container">
          <img 
            src="/touxiang.png" 
            alt="用户头像" 
            class="user-avatar"
          />
        </div>
        <span>欢迎，{{ user.username }}</span>
        <button @click="handleLogout" class="logout-btn">退出登录</button>
      </div>
    </div>
    
    <div class="admin-layout">
      <div class="admin-sidebar">
        <nav class="admin-nav">
          <router-link 
            v-for="tab in tabs" 
            :key="tab.id" 
            :to="tab.path"
            class="tab-button"
            :class="{ active: isActive(tab.path) }"
          >
            <component :is="tab.icon" class="tab-icon" />
            <span>{{ tab.name }}</span>
          </router-link>
        </nav>
      </div>
      
      <div class="admin-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { 
  LayoutDashboard as DashboardIcon,
  FileText as FileTextIcon,
  Folder as FolderIcon,
  MessageSquare as MessageSquareIcon,
  Tag as TagIcon,
  Settings as SettingsIcon,
  User as UserIcon,
  LineChart as ChartIcon,
  Activity as ActivityIcon,
  Home as HomeIcon
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const user = ref(authStore.user);

// 定义管理菜单选项
const tabs = [
  { id: 'dashboard', name: '仪表盘', icon: DashboardIcon, path: '/admin' },
  { id: 'articles', name: '文章管理', icon: FileTextIcon, path: '/admin/articles' },
  { id: 'projects', name: '项目管理', icon: FolderIcon, path: '/admin/projects' },
  { id: 'messages', name: '消息管理', icon: MessageSquareIcon, path: '/admin/messages' },
  { id: 'tags', name: '标签管理', icon: TagIcon, path: '/admin/tags' },
  { id: 'api-stats', name: 'API统计', icon: ChartIcon, path: '/admin/api-stats' },
  { id: 'api-paths', name: 'API路径', icon: ActivityIcon, path: '/admin/api-paths' },
  { id: 'profile', name: '个人资料', icon: UserIcon, path: '/admin/profile' },
  { id: 'settings', name: '系统设置', icon: SettingsIcon, path: '/admin/settings' },
];

// 判断当前路由是否激活
const isActive = (path: string) => {
  if (path === '/admin' && route.path === '/admin') {
    return true;
  }
  return path !== '/admin' && route.path.startsWith(path);
};

// 处理头像加载错误
const handleAvatarError = (e: Event) => {
  const target = e.target as HTMLImageElement;
  target.src = '/default-avatar.png'; // 设置默认头像
};

// 退出登录
const handleLogout = () => {
  authStore.logout();
  router.push('/login');
  
  // 显示退出成功消息
  alert('退出登录成功');
};

// 检查认证状态
onMounted(async () => {
  if (!authStore.isAuthenticated) {
    await authStore.checkAuth();
    if (!authStore.isAuthenticated) {
      router.push('/login');
      return;
    }
  }
  
  // 更新用户信息
  try {
    await authStore.getCurrentUser();
    user.value = authStore.user;
  } catch (error) {
    console.error('获取用户信息失败', error);
  }
  
  // 如果用户不是管理员，重定向到首页
  if (user.value && user.value.role !== 'admin') {
    router.push('/');
  }
});
</script>

<style scoped>
.admin-container {
  min-height: 100vh;
  background-color: #f8fafc;
}

.admin-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  z-index: 100;
  height: 64px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.admin-header h1 {
  font-size: 1.5rem;
  color: #1e293b;
  margin: 0;
}

.home-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #3b82f6;
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  background-color: rgba(59, 130, 246, 0.1);
  transition: all 0.2s;
}

.home-link:hover {
  background-color: rgba(59, 130, 246, 0.2);
}

.home-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info span {
  color: #64748b;
}

.avatar-container {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid #e2e8f0;
}

.user-avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.logout-btn {
  background-color: transparent;
  color: #ef4444;
  border: 1px solid #ef4444;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.logout-btn:hover {
  background-color: #ef4444;
  color: white;
}

.admin-layout {
  display: flex;
  min-height: calc(100vh - 64px);
  margin-top: 64px; /* 为固定的header腾出空间 */
}

.admin-sidebar {
  position: fixed;
  top: 64px; /* 与header底部对齐 */
  left: 0;
  bottom: 0;
  width: 220px;
  background-color: #1e293b;
  padding: 2rem 0;
  overflow-y: auto;
  z-index: 90;
}

.admin-nav {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background-color: transparent;
  border: none;
  color: #94a3b8;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
  border-left: 3px solid transparent;
  text-decoration: none;
}

.tab-button:hover {
  background-color: rgba(255, 255, 255, 0.05);
  color: #e2e8f0;
}

.tab-button.active {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
  border-left-color: #3b82f6;
}

.tab-icon {
  width: 1.25rem;
  height: 1.25rem;
}

.admin-content {
  flex: 1;
  margin-left: 220px; /* 与sidebar宽度相同 */
  padding: 2rem;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .admin-header {
    padding: 1rem;
  }
  
  .header-left {
    gap: 1rem;
  }
  
  .admin-header h1 {
    font-size: 1.25rem;
  }
  
  .home-link {
    padding: 0.375rem 0.75rem;
    font-size: 0.875rem;
  }
  
  .admin-sidebar {
    position: fixed;
    top: 64px;
    left: 0;
    right: 0;
    bottom: auto;
    width: 100%;
    height: auto;
    padding: 0.5rem 0;
    z-index: 90;
  }
  
  .admin-nav {
    flex-direction: row;
    overflow-x: auto;
    padding: 0 1rem;
  }
  
  .tab-button {
    border-left: none;
    border-bottom: 3px solid transparent;
    padding: 0.5rem 1rem;
    white-space: nowrap;
  }
  
  .tab-button.active {
    border-left-color: transparent;
    border-bottom-color: #3b82f6;
  }
  
  .admin-content {
    margin-left: 0;
    margin-top: 60px; /* 为移动端的横向导航栏腾出空间 */
  }
  
  .admin-layout {
    flex-direction: column;
  }
}
</style> 