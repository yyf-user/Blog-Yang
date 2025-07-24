<template>
  <div class="profile-view">
    <h2>个人资料</h2>
    
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
    
    <div class="profile-container">
      <div class="avatar-section">
        <div class="avatar-preview">
          <img 
            :src="avatarPreview || profile.avatar_url || '/default-avatar.png'" 
            alt="用户头像" 
            class="avatar-image"
            @error="handleAvatarError"
          />
        </div>
        
        <div class="avatar-actions">
          <label for="avatar-upload" class="upload-button">
            <upload-cloud-icon size="16" />
            上传新头像
          </label>
          <input 
            type="file" 
            id="avatar-upload" 
            accept="image/*" 
            @change="handleAvatarChange" 
            class="hidden-input"
          />
          
          <button 
            v-if="avatarFile" 
            class="primary-button" 
            @click="uploadAvatar"
            :disabled="isUploading"
          >
            <span v-if="isUploading" class="loading-spinner"></span>
            <span v-else>保存头像</span>
          </button>
        </div>
      </div>
      
      <div class="profile-details">
        <form @submit.prevent="updateProfile">
          <div class="form-group">
            <label for="username">用户名</label>
            <input 
              type="text" 
              id="username" 
              v-model="profile.username" 
              placeholder="用户名"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="email">电子邮箱</label>
            <input 
              type="email" 
              id="email" 
              v-model="profile.email" 
              placeholder="电子邮箱"
              required
            />
          </div>
          
          <div class="form-group">
            <label for="full_name">全名</label>
            <input 
              type="text" 
              id="full_name" 
              v-model="profile.full_name" 
              placeholder="全名"
            />
          </div>
          
          <div class="form-group">
            <label for="bio">个人简介</label>
            <textarea 
              id="bio" 
              v-model="profile.bio" 
              placeholder="个人简介"
              rows="4"
            ></textarea>
          </div>
          
          <h3>社交媒体链接</h3>
          
          <div class="form-group">
            <label for="github_url">GitHub</label>
            <div class="input-with-icon">
              <github-icon size="16" class="input-icon" />
              <input 
                type="text" 
                id="github_url" 
                v-model="profile.github_url" 
                placeholder="GitHub个人主页链接"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="linkedin_url">LinkedIn</label>
            <div class="input-with-icon">
              <linkedin-icon size="16" class="input-icon" />
              <input 
                type="text" 
                id="linkedin_url" 
                v-model="profile.linkedin_url" 
                placeholder="LinkedIn个人主页链接"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="twitter_url">Twitter</label>
            <div class="input-with-icon">
              <twitter-icon size="16" class="input-icon" />
              <input 
                type="text" 
                id="twitter_url" 
                v-model="profile.twitter_url" 
                placeholder="Twitter个人主页链接"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="website_url">个人网站</label>
            <div class="input-with-icon">
              <globe-icon size="16" class="input-icon" />
              <input 
                type="text" 
                id="website_url" 
                v-model="profile.website_url" 
                placeholder="个人网站链接"
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            class="primary-button"
            :disabled="isUpdatingProfile"
          >
            <span v-if="isUpdatingProfile" class="loading-spinner"></span>
            <span v-else>保存个人信息</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { usersApi } from '@/api';
import { 
  UploadCloud as UploadCloudIcon,
  Github as GithubIcon,
  Linkedin as LinkedinIcon,
  Twitter as TwitterIcon,
  Globe as GlobeIcon,
  CheckCircle as CheckCircleIcon,
  AlertCircle as AlertCircleIcon,
  X as XIcon
} from 'lucide-vue-next';
import axios from 'axios';

// 状态
const profile = ref({
  username: '',
  email: '',
  full_name: '',
  bio: '',
  avatar_url: '',
  github_url: '',
  linkedin_url: '',
  twitter_url: '',
  website_url: ''
});

const avatarFile = ref<File | null>(null);
const avatarPreview = ref<string | null>(null);
const isUpdatingProfile = ref(false);
const isUploading = ref(false);
const error = ref('');
const success = ref('');

// 处理头像加载错误
const handleAvatarError = (e: Event) => {
  const target = e.target as HTMLImageElement;
  target.src = '/default-avatar.png'; // 设置默认头像
};

// 处理头像选择
const handleAvatarChange = (e: Event) => {
  const target = e.target as HTMLInputElement;
  if (!target.files || target.files.length === 0) {
    return;
  }
  
  const file = target.files[0];
  avatarFile.value = file;
  
  // 创建预览URL
  if (avatarPreview.value) {
    URL.revokeObjectURL(avatarPreview.value);
  }
  avatarPreview.value = URL.createObjectURL(file);
};

// 上传头像
const uploadAvatar = async () => {
  if (!avatarFile.value) return;
  
  isUploading.value = true;
  error.value = '';
  success.value = '';
  
  try {
    const formData = new FormData();
    formData.append('file', avatarFile.value);
    
    console.log('正在上传头像...');
    // 使用API基础URL确保路径正确
    const API_URL = 'http://localhost:8000/api';
    const response = await axios.post(`${API_URL}/uploads/avatar`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });
    
    console.log('头像上传响应:', response);
    
    // 更新头像URL - 确保使用返回的正确路径
    if (response.data && response.data.avatar_url) {
      profile.value.avatar_url = response.data.avatar_url;
      
      // 更新本地存储的用户信息，这样其他地方可以访问到新头像
      const userData = JSON.parse(localStorage.getItem('user') || '{}');
      userData.avatar_url = response.data.avatar_url;
      localStorage.setItem('user', JSON.stringify(userData));
      
      success.value = '头像上传成功';
    } else {
      console.warn('上传成功但未返回头像URL:', response.data);
      success.value = '头像已上传，但获取URL失败';
    }
    
    // 清理
    avatarFile.value = null;
    if (avatarPreview.value) {
      URL.revokeObjectURL(avatarPreview.value);
      avatarPreview.value = null;
    }
    
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('上传头像失败:', err);
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误详情:', err.response.data);
      error.value = err.response.data?.detail || '上传头像失败，请稍后再试';
    } else {
      error.value = err.message || '上传头像失败，请检查网络连接';
    }
  } finally {
    isUploading.value = false;
  }
};

// 加载用户信息
const loadUserProfile = async () => {
  try {
    const response = await usersApi.getCurrentUser();
    const userData = response.data;
    
    // 更新个人信息
    profile.value = {
      username: userData.username || '',
      email: userData.email || '',
      full_name: userData.full_name || '',
      bio: userData.bio || '',
      avatar_url: '/touxiang.png', // 直接使用public目录下的touxiang.png作为头像
      github_url: userData.github_url || '',
      linkedin_url: userData.linkedin_url || '',
      twitter_url: userData.twitter_url || '',
      website_url: userData.website_url || ''
    };
    
    // 更新本地存储的用户信息
    const localUserData = JSON.parse(localStorage.getItem('user') || '{}');
    localUserData.avatar_url = '/touxiang.png';
    localStorage.setItem('user', JSON.stringify(localUserData));
    
  } catch (err: any) {
    console.error('加载用户信息失败:', err);
    error.value = '加载用户信息失败，请稍后再试';
    
    // 使用模拟数据
    profile.value = {
      username: 'admin',
      email: 'admin@example.com',
      full_name: '管理员',
      bio: '全栈开发者，热爱Vue和Python，喜欢分享技术经验。',
      avatar_url: '/touxiang.png', // 同样使用touxiang.png作为默认头像
      github_url: 'https://github.com/yyf-user/nebula-background-forge',
      linkedin_url: '',
      twitter_url: '',
      website_url: ''
    };
  }
};

// 更新个人信息
const updateProfile = async () => {
  isUpdatingProfile.value = true;
  error.value = '';
  success.value = '';
  
  try {
    await usersApi.updateUser(profile.value);
    success.value = '个人信息更新成功';
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('更新个人信息失败:', err);
    error.value = err.response?.data?.detail || '更新个人信息失败，请稍后再试';
  } finally {
    isUpdatingProfile.value = false;
  }
};

// 关闭通知
const closeNotification = () => {
  error.value = '';
  success.value = '';
};

// 初始化
onMounted(() => {
  loadUserProfile();
});
</script>

<style scoped>
.profile-view {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.profile-view h2 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  color: #1e293b;
  font-size: 1.25rem;
}

.profile-view h3 {
  margin: 1.5rem 0 1rem;
  color: #1e293b;
  font-size: 1.125rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.5rem;
}

.profile-container {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.avatar-preview {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #e2e8f0;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.upload-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background-color: #f1f5f9;
  color: #1e293b;
  border: 1px dashed #cbd5e1;
  padding: 0.75rem 1rem;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
  text-align: center;
}

.upload-button:hover {
  background-color: #e2e8f0;
}

.hidden-input {
  display: none;
}

.profile-details {
  flex: 1;
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

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.input-with-icon {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: #64748b;
}

.input-with-icon input {
  padding-left: 2.5rem;
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
  .profile-container {
    grid-template-columns: 1fr;
  }
  
  .avatar-section {
    margin-bottom: 2rem;
  }
}
</style> 