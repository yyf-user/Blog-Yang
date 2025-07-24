<template>
  <div class="settings-manager">
    <h2>系统设置</h2>
    
    <!-- 固定位置的通知提示 -->
    <div v-if="error || success" class="notification-container">
      <div class="notification" :class="{ 'error': error, 'success': success }">
        <div class="notification-icon">
          <check-circle-icon v-if="success" size="20" />
          <alert-circle-icon v-if="error" size="20" />
        </div>
        <div class="notification-content">
          {{ error || success }}
        </div>
        <button class="notification-close" @click="closeNotification">
          <x-icon size="16" />
        </button>
      </div>
    </div>
    
    <div class="settings-tabs">
      <button 
        v-for="tab in tabs" 
        :key="tab.id"
        class="tab-button"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        <component :is="tab.icon" class="tab-icon" />
        <span>{{ tab.name }}</span>
      </button>
    </div>
    
    <!-- 密码修改 -->
    <div class="settings-section" v-if="activeTab === 'password'">
      <h3>修改密码</h3>
      <form @submit.prevent="updatePassword">
        <div class="form-group">
          <label for="current_password">当前密码</label>
          <input 
            type="password" 
            id="current_password" 
            v-model="passwordForm.current_password" 
            placeholder="当前密码"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="new_password">新密码</label>
          <input 
            type="password" 
            id="new_password" 
            v-model="passwordForm.new_password" 
            placeholder="新密码"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="confirm_password">确认新密码</label>
          <input 
            type="password" 
            id="confirm_password" 
            v-model="passwordForm.confirm_password" 
            placeholder="确认新密码"
            required
          />
          <div v-if="passwordMismatch" class="form-error">
            两次输入的密码不一致
          </div>
        </div>
        
        <button 
          type="submit" 
          class="primary-button"
          :disabled="isUpdatingPassword || passwordMismatch"
        >
          <span v-if="isUpdatingPassword" class="loading-spinner"></span>
          <span v-else>修改密码</span>
        </button>
      </form>
    </div>
    
    <!-- 网站设置 -->
    <div class="settings-section" v-if="activeTab === 'site'">
      <h3>网站设置</h3>
      <form @submit.prevent="updateSiteSettings">
        <div class="form-group">
          <label for="site_title">网站标题</label>
          <input 
            type="text" 
            id="site_title" 
            v-model="siteSettings.site_title" 
            placeholder="网站标题"
          />
        </div>
        
        <div class="form-group">
          <label for="site_description">网站描述</label>
          <textarea 
            id="site_description" 
            v-model="siteSettings.site_description" 
            placeholder="网站描述"
            rows="2"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="footer_text">页脚文本</label>
          <input 
            type="text" 
            id="footer_text" 
            v-model="siteSettings.footer_text" 
            placeholder="页脚文本"
          />
        </div>
        
        <button 
          type="submit" 
          class="primary-button"
          :disabled="isUpdatingSiteSettings"
        >
          <span v-if="isUpdatingSiteSettings" class="loading-spinner"></span>
          <span v-else>保存网站设置</span>
        </button>
      </form>
    </div>
    
    <!-- 邮件设置 -->
    <div class="settings-section" v-if="activeTab === 'email'">
      <h3>邮件设置</h3>
      <form @submit.prevent="updateEmailSettings">
        <div class="form-group">
          <label for="smtp_server">SMTP服务器</label>
          <input 
            type="text" 
            id="smtp_server" 
            v-model="emailSettings.smtp_server" 
            placeholder="smtp.example.com"
          />
        </div>
        
        <div class="form-group">
          <label for="smtp_port">SMTP端口</label>
          <input 
            type="number" 
            id="smtp_port" 
            v-model="emailSettings.smtp_port" 
            placeholder="587"
          />
        </div>
        
        <div class="form-group">
          <label for="smtp_username">SMTP用户名</label>
          <input 
            type="text" 
            id="smtp_username" 
            v-model="emailSettings.smtp_username" 
            placeholder="user@example.com"
          />
        </div>
        
        <div class="form-group">
          <label for="smtp_password">SMTP密码</label>
          <input 
            type="password" 
            id="smtp_password" 
            v-model="emailSettings.smtp_password" 
            placeholder="密码"
          />
        </div>
        
        <div class="form-group">
          <label for="email_from">发件人地址</label>
          <input 
            type="email" 
            id="email_from" 
            v-model="emailSettings.email_from" 
            placeholder="noreply@example.com"
          />
        </div>
        
        <button 
          type="submit" 
          class="primary-button"
          :disabled="isUpdatingEmailSettings"
        >
          <span v-if="isUpdatingEmailSettings" class="loading-spinner"></span>
          <span v-else>保存邮件设置</span>
        </button>
      </form>
    </div>
    
    <!-- 安全设置 -->
    <div class="settings-section" v-if="activeTab === 'security'">
      <h3>安全设置</h3>
      <form @submit.prevent="updateSecuritySettings">
        <div class="form-group checkbox-group">
          <input 
            type="checkbox" 
            id="enable_two_factor" 
            v-model="securitySettings.enable_two_factor"
          />
          <label for="enable_two_factor">启用两步验证</label>
        </div>
        
        <div class="form-group checkbox-group">
          <input 
            type="checkbox" 
            id="enable_captcha" 
            v-model="securitySettings.enable_captcha"
          />
          <label for="enable_captcha">启用验证码</label>
        </div>
        
        <div class="form-group">
          <label for="session_timeout">会话超时（分钟）</label>
          <input 
            type="number" 
            id="session_timeout" 
            v-model="securitySettings.session_timeout" 
            min="5"
            max="1440"
          />
        </div>
        
        <div class="form-group">
          <label for="max_login_attempts">最大登录尝试次数</label>
          <input 
            type="number" 
            id="max_login_attempts" 
            v-model="securitySettings.max_login_attempts" 
            min="3"
            max="10"
          />
        </div>
        
        <button 
          type="submit" 
          class="primary-button"
          :disabled="isUpdatingSecuritySettings"
        >
          <span v-if="isUpdatingSecuritySettings" class="loading-spinner"></span>
          <span v-else>保存安全设置</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { usersApi } from '@/api';
import { 
  Lock as LockIcon,
  Globe as GlobeIcon,
  Mail as MailIcon,
  Shield as ShieldIcon,
  CheckCircle as CheckCircleIcon,
  AlertCircle as AlertCircleIcon,
  X as XIcon
} from 'lucide-vue-next';

// 标签页
const tabs = [
  { id: 'password', name: '密码修改', icon: LockIcon },
  { id: 'site', name: '网站设置', icon: GlobeIcon },
  { id: 'email', name: '邮件设置', icon: MailIcon },
  { id: 'security', name: '安全设置', icon: ShieldIcon }
];

const activeTab = ref('password');

// 密码表单
const passwordForm = ref({
  current_password: '',
  new_password: '',
  confirm_password: ''
});

// 网站设置
const siteSettings = ref({
  site_title: '博客Yang - 个人技术博客',
  site_description: '分享Web开发、人工智能和技术趋势的个人博客',
  footer_text: '© 2023 博客Yang. All rights reserved.'
});

// 邮件设置
const emailSettings = ref({
  smtp_server: '',
  smtp_port: 587,
  smtp_username: '',
  smtp_password: '',
  email_from: ''
});

// 安全设置
const securitySettings = ref({
  enable_two_factor: false,
  enable_captcha: true,
  session_timeout: 60,
  max_login_attempts: 5
});

// 状态
const isUpdatingPassword = ref(false);
const isUpdatingSiteSettings = ref(false);
const isUpdatingEmailSettings = ref(false);
const isUpdatingSecuritySettings = ref(false);
const error = ref('');
const success = ref('');

// 计算属性
const passwordMismatch = computed(() => {
  return passwordForm.value.new_password !== passwordForm.value.confirm_password && 
         passwordForm.value.confirm_password !== '';
});

// 更新密码
const updatePassword = async () => {
  // 验证密码
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    error.value = '两次输入的密码不一致';
    return;
  }
  
  isUpdatingPassword.value = true;
  error.value = '';
  success.value = '';
  
  try {
    console.log('正在调用密码修改接口...');
    
    // 使用正确的API调用
    const response = await usersApi.updatePassword({
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password
    });
    
    console.log('密码修改成功，响应:', response);
    
    success.value = '密码修改成功';
    
    // 重置表单
    passwordForm.value = {
      current_password: '',
      new_password: '',
      confirm_password: ''
    };
    
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('修改密码失败:', err);
    
    // 详细记录错误信息以便调试
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误信息:', err.response.data);
    }
    
    error.value = err.response?.data?.detail || '修改密码失败，请稍后再试';
  } finally {
    isUpdatingPassword.value = false;
  }
};

// 更新网站设置
const updateSiteSettings = async () => {
  isUpdatingSiteSettings.value = true;
  error.value = '';
  success.value = '';
  
  try {
    // 这里应该调用更新网站设置的API
    // 由于没有相应的API，我们只是模拟成功
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    success.value = '网站设置更新成功';
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('更新网站设置失败:', err);
    error.value = '更新网站设置失败，请稍后再试';
  } finally {
    isUpdatingSiteSettings.value = false;
  }
};

// 更新邮件设置
const updateEmailSettings = async () => {
  isUpdatingEmailSettings.value = true;
  error.value = '';
  success.value = '';
  
  try {
    // 这里应该调用更新邮件设置的API
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    success.value = '邮件设置更新成功';
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('更新邮件设置失败:', err);
    error.value = '更新邮件设置失败，请稍后再试';
  } finally {
    isUpdatingEmailSettings.value = false;
  }
};

// 更新安全设置
const updateSecuritySettings = async () => {
  isUpdatingSecuritySettings.value = true;
  error.value = '';
  success.value = '';
  
  try {
    // 这里应该调用更新安全设置的API
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    success.value = '安全设置更新成功';
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('更新安全设置失败:', err);
    error.value = '更新安全设置失败，请稍后再试';
  } finally {
    isUpdatingSecuritySettings.value = false;
  }
};

// 关闭通知
const closeNotification = () => {
  error.value = '';
  success.value = '';
};

// 初始化
onMounted(() => {
  // 加载设置
  // 由于没有相应的API，我们使用默认值
});
</script>

<style scoped>
.settings-manager {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.settings-manager h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #1e293b;
  font-size: 1.25rem;
}

.settings-tabs {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 1rem;
}

.tab-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: 1px solid #e2e8f0;
  color: #64748b;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-button:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

.tab-button.active {
  background-color: #3b82f6;
  border-color: #3b82f6;
  color: white;
}

.tab-icon {
  width: 1rem;
  height: 1rem;
}

.settings-section {
  margin-bottom: 2.5rem;
  max-width: 600px;
}

.settings-section:last-child {
  margin-bottom: 0;
}

.settings-section h3 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #1e293b;
  font-size: 1.125rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.75rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #1e293b;
  font-weight: 500;
  font-size: 0.875rem;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.checkbox-group label {
  margin-bottom: 0;
}

.form-group input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
}

.form-group input:not([type="checkbox"]),
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

.form-group textarea {
  resize: vertical;
}

.form-error {
  color: #ef4444;
  font-size: 0.75rem;
  margin-top: 0.5rem;
}

.primary-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.primary-button:hover {
  background-color: #2563eb;
}

.primary-button:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.loading-spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-alert {
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background-color: rgba(239, 68, 68, 0.1);
  border-left: 3px solid #ef4444;
  color: #b91c1c;
  border-radius: 0.25rem;
}

.success-alert {
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background-color: rgba(34, 197, 94, 0.1);
  border-left: 3px solid #22c55e;
  color: #166534;
  border-radius: 0.25rem;
}

/* 固定位置的通知样式 */
.notification-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  width: auto;
  max-width: 90%;
}

.notification {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  background-color: white;
  animation: fadeIn 0.3s ease-out;
}

.notification.success {
  border-left: 4px solid #22c55e;
}

.notification.error {
  border-left: 4px solid #ef4444;
}

.notification-icon {
  margin-right: 0.75rem;
  display: flex;
  align-items: center;
}

.notification-icon svg {
  color: #22c55e;
}

.notification.error .notification-icon svg {
  color: #ef4444;
}

.notification-content {
  flex: 1;
  font-size: 0.875rem;
  color: #1e293b;
}

.notification-close {
  background: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 0.75rem;
  border-radius: 0.25rem;
}

.notification-close:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 隐藏原来的提示信息 */
.error-alert, .success-alert {
  display: none;
}

@media (max-width: 768px) {
  .settings-tabs {
    overflow-x: auto;
    padding-bottom: 0.5rem;
    flex-wrap: nowrap;
  }
  
  .tab-button {
    white-space: nowrap;
  }
}
</style> 