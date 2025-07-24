<template>
  <div class="login-container">
    <div class="login-card">
      <div class="logo-container">
        <div class="logo">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lightning-icon">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
          </svg>
        </div>
      </div>
      <h1 class="welcome-text">欢迎回来</h1>
      <p class="login-subtitle">登录您的账户以继续访问系统</p>
      
      <div v-if="error" class="error-alert">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">用户名</label>
          <div class="input-container">
            <span class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                <circle cx="12" cy="7" r="4" />
              </svg>
            </span>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              placeholder="请输入用户名"
              required
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="password">密码</label>
          <div class="input-container">
            <span class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
            </span>
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              v-model="password" 
              placeholder="请输入密码"
              required
            />
            <span class="toggle-password" @click="togglePasswordVisibility">
              <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                <circle cx="12" cy="12" r="3" />
              </svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                <line x1="1" y1="1" x2="23" y2="23" />
              </svg>
            </span>
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="login-button" :disabled="isLoading ? true : false">
            <span v-if="isLoading" class="loading-spinner"></span>
            <span v-else>登录系统</span>
          </button>
        </div>
      </form>
      
      <div class="register-link">
        还没有账户？ <router-link to="/register">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const error = ref('')

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const handleLogin = async () => {
  try {
    isLoading.value = true
    error.value = ''
    
    console.log('开始登录流程，用户名:', username.value)
    
    // 检查输入
    if (!username.value || !password.value) {
      error.value = '请输入用户名和密码'
      return
    }
    
    console.log('调用authStore.login...')
    
    // 尝试登录
    try {
      await authStore.login(username.value, password.value)
      console.log('authStore.login调用成功')
    } catch (loginError) {
      console.error('authStore.login调用失败:', loginError)
      throw loginError
    }
    
    console.log('检查登录状态:', authStore.isAuthenticated)
    
    // 登录成功后检查认证状态
    if (!authStore.isAuthenticated) {
      console.error('登录后认证状态为false')
      error.value = '登录失败，请检查用户名和密码'
      return
    }
    
    // 登录成功后检查用户信息
    console.log('登录后用户信息:', authStore.user)
    
    if (authStore.user) {
      console.log('登录成功，用户信息:', authStore.user)
      console.log('用户角色:', authStore.user.role)
      
      // 根据用户角色导航到不同页面
      if (authStore.user.role === 'admin') {
        console.log('管理员登录，导航到管理页面')
        // 在新标签页中打开后台管理页面
        const adminUrl = `${window.location.origin}/admin`
        window.open(adminUrl, '_blank')
        // 可选：在当前页面返回首页
        router.push('/')
      } else {
        console.log('普通用户登录，导航到首页')
        router.push('/')
      }
    } else {
      console.warn('登录成功但未获取到用户信息，尝试手动获取')
      
      try {
        await authStore.getCurrentUser()
        console.log('手动获取用户信息成功:', authStore.user)
        
        if (authStore.user && authStore.user.role === 'admin') {
          // 在新标签页中打开后台管理页面
          const adminUrl = `${window.location.origin}/admin`
          window.open(adminUrl, '_blank')
          // 可选：在当前页面返回首页
          router.push('/')
        } else {
          router.push('/')
        }
      } catch (userError) {
        console.error('手动获取用户信息失败:', userError)
        console.warn('使用默认导航到首页')
        router.push('/')
      }
    }
  } catch (err: any) {
    console.error('登录错误详情:', err)
    
    // 显示友好的错误信息
    if (err.message && err.message.includes('Network Error')) {
      error.value = '网络错误，请检查网络连接'
    } else if (err.response && err.response.status === 401) {
      error.value = '用户名或密码错误'
    } else if (err.response && err.response.status === 403) {
      error.value = '账户已被禁用'
    } else {
      error.value = err.message || '登录失败，请检查用户名和密码'
    }
    
    // 显示更详细的错误信息
    if (err.response) {
      console.error('服务器响应状态:', err.response.status)
      console.error('服务器响应数据:', err.response.data)
    }
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
  position: relative;
}

.login-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.1) 0%, transparent 20%),
    radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.1) 0%, transparent 20%);
  pointer-events: none;
}

.login-card {
  width: 100%;
  max-width: 450px;
  padding: 2.5rem;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border-radius: 1rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  border: 1px solid rgba(99, 102, 241, 0.2);
}

.logo-container {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.logo {
  width: 4rem;
  height: 4rem;
  background: rgba(59, 130, 246, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0.75rem;
  border: 1px solid rgba(59, 130, 246, 0.4);
}

.lightning-icon {
  width: 2.5rem;
  height: 2.5rem;
  color: #3b82f6;
  filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.6));
}

.welcome-text {
  font-size: 1.875rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 0.5rem;
  color: #f8fafc;
}

.login-subtitle {
  text-align: center;
  color: #94a3b8;
  margin-bottom: 2rem;
}

.error-alert {
  padding: 0.75rem 1rem;
  margin-bottom: 1.5rem;
  background-color: rgba(239, 68, 68, 0.2);
  border: 1px solid rgba(239, 68, 68, 0.5);
  color: #fca5a5;
  border-radius: 0.5rem;
  text-align: center;
  font-size: 0.875rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #e2e8f0;
  font-weight: 500;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: #64748b;
  width: 1.25rem;
  height: 1.25rem;
}

.input-container input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  background: rgba(30, 41, 59, 0.8);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 0.5rem;
  color: #e2e8f0;
  font-size: 1rem;
  transition: all 0.3s;
}

.input-container input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

.input-container input::placeholder {
  color: #64748b;
}

.toggle-password {
  position: absolute;
  right: 1rem;
  cursor: pointer;
  color: #64748b;
  width: 1.25rem;
  height: 1.25rem;
}

.form-actions {
  margin-top: 2rem;
}

.login-button {
  width: 100%;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.login-button:hover {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
}

.login-button:active {
  transform: translateY(0);
  box-shadow: none;
}

.login-button:disabled {
  background: #475569;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 1.25rem;
  height: 1.25rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.register-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #94a3b8;
  font-size: 0.875rem;
}

.register-link a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.register-link a:hover {
  color: #60a5fa;
  text-decoration: underline;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
</style> 