<template>
  <div class="contact-container">
    <Navigation />
    
    <main class="contact-content">
      <div class="container">
        <div class="contact-header">
          <h1 class="contact-title">联系<span class="text-gradient">我</span></h1>
          <p class="contact-subtitle">有任何问题或合作机会？请随时与我联系</p>
        </div>
        
        <div class="contact-wrapper">
          <!-- 联系信息 -->
          <div class="contact-info">
            <div class="info-card">
              <div class="info-header">
                <h2>联系方式</h2>
                <p>您可以通过以下方式联系我</p>
              </div>
              
              <div class="info-items">
                <div class="info-item">
                  <div class="info-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                      <polyline points="22,6 12,13 2,6"></polyline>
                    </svg>
                  </div>
                  <div class="info-content">
                    <h3>电子邮件</h3>
                    <a href="mailto:contact@example.com">contact@example.com</a>
                  </div>
                </div>
                
                <div class="info-item">
                  <div class="info-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M15.05 5A5 5 0 0 1 19 8.95M15.05 1A9 9 0 0 1 23 8.94m-1 7.98v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                    </svg>
                  </div>
                  <div class="info-content">
                    <h3>电话</h3>
                    <a href="tel:+86123456789">+86 123 456 789</a>
                  </div>
                </div>
                
                <div class="info-item">
                  <div class="info-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                      <circle cx="12" cy="10" r="3"></circle>
                    </svg>
                  </div>
                  <div class="info-content">
                    <h3>地址</h3>
                    <p>中国北京市朝阳区</p>
                  </div>
                </div>
              </div>
              
              <div class="social-links">
                <a href="#" class="social-link" aria-label="GitHub">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path>
                  </svg>
                </a>
                <a href="#" class="social-link" aria-label="Twitter">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path>
                  </svg>
                </a>
                <a href="#" class="social-link" aria-label="LinkedIn">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path>
                    <rect x="2" y="9" width="4" height="12"></rect>
                    <circle cx="4" cy="4" r="2"></circle>
                  </svg>
                </a>
                <a href="#" class="social-link" aria-label="Instagram">
                  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                    <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                    <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
                  </svg>
                </a>
              </div>
            </div>
          </div>
          
          <!-- 联系表单 -->
          <div class="contact-form-container">
            <div class="form-card">
              <div class="form-header">
                <h2>发送消息</h2>
                <p>填写下面的表单，我会尽快回复您</p>
              </div>
              
              <form @submit.prevent="handleSubmit" class="contact-form">
                <div class="form-group">
                  <label for="name">姓名</label>
                  <input 
                    type="text" 
                    id="name" 
                    v-model="formData.name" 
                    placeholder="请输入您的姓名"
                    required
                  />
                </div>
                
                <div class="form-group">
                  <label for="email">电子邮箱</label>
                  <input 
                    type="email" 
                    id="email" 
                    v-model="formData.email" 
                    placeholder="请输入您的电子邮箱"
                    required
                  />
                </div>
                
                <div class="form-group">
                  <label for="subject">主题</label>
                  <input 
                    type="text" 
                    id="subject" 
                    v-model="formData.subject" 
                    placeholder="请输入消息主题"
                    required
                  />
                </div>
                
                <div class="form-group">
                  <label for="message">消息内容</label>
                  <textarea 
                    id="message" 
                    v-model="formData.message" 
                    placeholder="请输入您的消息内容"
                    rows="5"
                    required
                  ></textarea>
                </div>
                
                <div class="form-actions">
                  <button type="submit" class="submit-button" :disabled="isSubmitting ? true : false">
                    <span v-if="isSubmitting" class="loading-spinner"></span>
                    <span v-else>发送消息</span>
                  </button>
                </div>
              </form>
              
              <div v-if="submitStatus.success" class="success-message">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="success-icon">
                  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                  <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <p>消息已成功发送！我会尽快回复您。</p>
              </div>
              
              <div v-if="submitStatus.error" class="error-message">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="error-icon">
                  <circle cx="12" cy="12" r="10"></circle>
                  <line x1="12" y1="8" x2="12" y2="12"></line>
                  <line x1="12" y1="16" x2="12.01" y2="16"></line>
                </svg>
                <p>{{ submitStatus.errorMessage }}</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 订阅区域 -->
        <div class="subscribe-section">
          <div class="subscribe-card">
            <div class="subscribe-content">
              <h2>订阅我的更新</h2>
              <p>获取最新的文章、项目和技术资讯</p>
            </div>
            
            <form @submit.prevent="handleSubscribe" class="subscribe-form">
              <input 
                type="email" 
                v-model="subscribeEmail" 
                placeholder="请输入您的电子邮箱"
                required
              />
              <button type="submit" :disabled="isSubscribing ? true : false">
                <span v-if="isSubscribing" class="loading-spinner"></span>
                <span v-else>订阅</span>
              </button>
            </form>
            
            <div v-if="subscribeStatus.success" class="subscribe-success">
              <p>订阅成功！感谢您的关注。</p>
            </div>
            
            <div v-if="subscribeStatus.error" class="subscribe-error">
              <p>{{ subscribeStatus.errorMessage }}</p>
            </div>
          </div>
        </div>
    </div>
    </main>
    
    <SiteFooter />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import Navigation from '@/components/Navigation.vue';
import SiteFooter from '@/components/SiteFooter.vue';
import { messagesApi } from '@/api';

// 联系表单数据
const formData = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
});

// 表单提交状态
const isSubmitting = ref(false);
const submitStatus = ref({
  success: false,
  error: false,
  errorMessage: ''
});

// 提交表单
const handleSubmit = async () => {
  isSubmitting.value = true;
  submitStatus.value = {
    success: false,
    error: false,
    errorMessage: ''
  };
  
  try {
    // 调用真实API发送消息
    console.log('发送消息:', formData.value);
    const response = await messagesApi.createMessage(formData.value);
    console.log('发送消息响应:', response);
    
    // 处理成功响应
    submitStatus.value.success = true;
    
    // 重置表单
    formData.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    };
  } catch (err: any) {
    console.error('发送消息失败:', err);
    submitStatus.value.error = true;
    
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误详情:', err.response.data);
      submitStatus.value.errorMessage = err.response.data.detail || '发送消息失败，请稍后再试';
    } else {
      submitStatus.value.errorMessage = err.message || '发送消息失败，请稍后再试';
    }
  } finally {
    isSubmitting.value = false;
  }
};

// 订阅表单数据
const subscribeEmail = ref('');
const isSubscribing = ref(false);
const subscribeStatus = ref({
  success: false,
  error: false,
  errorMessage: ''
});

// 提交订阅
const handleSubscribe = async () => {
  isSubscribing.value = true;
  subscribeStatus.value = {
    success: false,
    error: false,
    errorMessage: ''
  };
  
  try {
    // 实际项目中应该调用API
    // const response = await axios.post('/api/subscribers', { email: subscribeEmail.value });
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 模拟成功响应
    subscribeStatus.value.success = true;
    
    // 重置表单
    subscribeEmail.value = '';
  } catch (err: any) {
    subscribeStatus.value.error = true;
    subscribeStatus.value.errorMessage = err.message || '订阅失败，请稍后再试';
    console.error('Failed to subscribe:', err);
  } finally {
    isSubscribing.value = false;
  }
};
</script>

<style scoped>
.contact-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.contact-content {
  flex: 1;
  padding: 6rem 0;
}

.contact-header {
  text-align: center;
  margin-bottom: 3rem;
}

.contact-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  color: var(--color-text);
}

.contact-subtitle {
  font-size: 1.25rem;
  color: var(--color-text-muted);
  max-width: 600px;
  margin: 0 auto;
}

.contact-wrapper {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 2rem;
  margin-bottom: 4rem;
}

/* 联系信息样式 */
.info-card {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 2rem;
  height: 100%;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.info-header {
  margin-bottom: 2rem;
}

.info-header h2 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.info-header p {
  color: var(--color-text-muted);
}

.info-items {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  gap: 1rem;
}

.info-icon {
  width: 3rem;
  height: 3rem;
  background: rgba(59, 130, 246, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.info-icon svg {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-primary);
}

.info-content h3 {
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
  color: var(--color-text);
}

.info-content a {
  color: var(--color-primary);
  text-decoration: none;
  transition: color 0.3s;
}

.info-content a:hover {
  color: var(--color-secondary);
  text-decoration: underline;
}

.info-content p {
  color: var(--color-text-muted);
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: auto;
}

.social-link {
  width: 2.5rem;
  height: 2.5rem;
  background: rgba(30, 41, 59, 0.8);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
}

.social-link svg {
  width: 1.25rem;
  height: 1.25rem;
  color: var(--color-text-muted);
  transition: color 0.3s;
}

.social-link:hover {
  background: rgba(59, 130, 246, 0.2);
}

.social-link:hover svg {
  color: var(--color-primary);
}

/* 表单样式 */
.form-card {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-header {
  margin-bottom: 2rem;
}

.form-header h2 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.form-header p {
  color: var(--color-text-muted);
}

.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: var(--color-text-light);
}

.form-group input,
.form-group textarea {
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 0.5rem;
  color: var(--color-text);
  font-size: 1rem;
  transition: all 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.form-actions {
  margin-top: 1rem;
}

.submit-button {
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
}

.submit-button:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
}

.submit-button:active {
  transform: translateY(0);
  box-shadow: none;
}

.submit-button:disabled {
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

.success-message,
.error-message {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-top: 1.5rem;
  padding: 1rem;
  border-radius: 0.5rem;
}

.success-message {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.error-message {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.success-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-success);
  flex-shrink: 0;
}

.error-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: var(--color-error);
  flex-shrink: 0;
}

.success-message p {
  color: var(--color-success);
}

.error-message p {
  color: var(--color-error);
}

/* 订阅区域样式 */
.subscribe-section {
  margin-top: 4rem;
}

.subscribe-card {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 2rem;
  border: 1px solid rgba(99, 102, 241, 0.2);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.subscribe-content {
  margin-bottom: 1.5rem;
}

.subscribe-content h2 {
  font-size: 1.75rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.subscribe-content p {
  color: var(--color-text-muted);
  max-width: 500px;
  margin: 0 auto;
}

.subscribe-form {
  display: flex;
  max-width: 500px;
  margin: 0 auto;
  gap: 1rem;
}

.subscribe-form input {
  flex: 1;
  padding: 0.75rem 1rem;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(71, 85, 105, 0.5);
  border-radius: 0.5rem;
  color: var(--color-text);
  font-size: 1rem;
  transition: all 0.3s;
}

.subscribe-form input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

.subscribe-form button {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
}

.subscribe-form button:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
}

.subscribe-form button:active {
  transform: translateY(0);
  box-shadow: none;
}

.subscribe-form button:disabled {
  background: #475569;
  cursor: not-allowed;
}

.subscribe-success,
.subscribe-error {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
}

.subscribe-success {
  background: rgba(16, 185, 129, 0.1);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.subscribe-error {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.subscribe-success p {
  color: var(--color-success);
}

.subscribe-error p {
  color: var(--color-error);
}

/* 响应式调整 */
@media (max-width: 992px) {
  .contact-wrapper {
    grid-template-columns: 1fr;
  }
  
  .subscribe-form {
    flex-direction: column;
  }
}

@media (max-width: 768px) {
  .contact-content {
    padding: 5rem 0;
  }
  
  .contact-title {
    font-size: 2.5rem;
  }
  
  .info-card,
  .form-card,
  .subscribe-card {
    padding: 1.5rem;
  }
}
</style> 