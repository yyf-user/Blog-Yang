<template>
  <div class="register-container">
    <div class="register-card">
      <div class="logo-container">
        <div class="logo">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lightning-icon">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" />
          </svg>
        </div>
      </div>
      <h1 class="welcome-text">创建账户</h1>
      <p class="register-subtitle">注册一个新账户以访问系统</p>
      
      <div v-if="error" class="error-alert">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleRegister" class="register-form">
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
          <label for="email">电子邮箱</label>
          <div class="input-container">
            <span class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                <polyline points="22,6 12,13 2,6" />
              </svg>
            </span>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="请输入电子邮箱"
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
        
        <div class="form-group">
          <label for="confirmPassword">确认密码</label>
          <div class="input-container">
            <span class="input-icon">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
              </svg>
            </span>
            <input 
              :type="showPassword ? 'text' : 'password'" 
              id="confirmPassword" 
              v-model="confirmPassword" 
              placeholder="请再次输入密码"
              required
            />
          </div>
          <div v-if="passwordMismatch" class="error-message">
            两次输入的密码不一致
          </div>
        </div>
        
        <div class="form-actions">
          <button type="submit" class="register-button" :disabled="isLoading || passwordMismatch ? true : false">
            <span v-if="isLoading" class="loading-spinner"></span>
            <span v-else>注册账户</span>
          </button>
        </div>
      </form>
      
      <div class="login-link">
        已有账户？ <router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const isLoading = ref(false)
const error = ref('')

const passwordMismatch = computed(() => {
  return password.value && confirmPassword.value && password.value !== confirmPassword.value
})

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const handleRegister = async () => {
  if (passwordMismatch.value) {
    return
  }
  
  try {
    isLoading.value = true
    error.value = ''
    
    await authStore.register(username.value, email.value, password.value)
    router.push('/login')
  } catch (err: any) {
    error.value = err.message || '注册失败，请稍后再试'
    console.error('Register error:', err)
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
  position: relative;
}

.register-container::before {
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

.register-card {
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

.register-subtitle {
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

.error-message {
  color: #ef4444;
  font-size: 0.875rem;
  margin-top: 0.5rem;
}

.form-actions {
  margin-top: 2rem;
}

.register-button {
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

.register-button:hover {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
}

.register-button:active {
  transform: translateY(0);
  box-shadow: none;
}

.register-button:disabled {
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

.login-link {
  margin-top: 1.5rem;
  text-align: center;
  color: #94a3b8;
  font-size: 0.875rem;
}

.login-link a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

.login-link a:hover {
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