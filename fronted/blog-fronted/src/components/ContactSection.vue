<template>
  <section id="contact" class="contact-section">
    <div class="container">
      <div class="section-header">
        <h2 class="section-title">联系<span class="highlight">我</span></h2>
        <p class="section-subtitle">有问题或想合作？请填写下面的表单</p>
      </div>
      
      <div class="contact-container">
        <div class="contact-info">
          <div class="info-header">
            <message-square-icon />
            <h3>让我们交流</h3>
          </div>
          <p>无论您有问题、建议还是合作意向，都可以通过以下方式或填写表单与我联系。</p>
          
          <div class="info-list">
            <div class="info-item">
              <mail-icon />
              <span>example@example.com</span>
            </div>
            <div class="info-item">
              <map-pin-icon />
              <span>北京市, 中国</span>
            </div>
            <div class="info-item">
              <clock-icon />
              <span>工作时间: 周一至周五 9:00 - 18:00</span>
            </div>
          </div>
          
          <div class="social-links">
            <a href="https://github.com/yyf-user/nebula-background-forge" target="_blank" rel="noopener noreferrer" class="social-link">
              <github-icon class="social-icon" />
            </a>
            <a href="https://linkedin.com/" target="_blank" rel="noopener noreferrer" class="social-link">
              <linkedin-icon />
            </a>
            <a href="https://twitter.com/" target="_blank" rel="noopener noreferrer" class="social-link">
              <twitter-icon />
            </a>
          </div>
          
          <div class="newsletter">
            <h4>订阅我的通讯</h4>
            <p>获取最新的技术文章和项目更新</p>
            <form @submit.prevent="handleSubscribe" class="subscribe-form">
              <div class="subscribe-input-group">
                <mail-icon />
                <input 
                  type="email" 
                  v-model="emailSubscribe" 
                  placeholder="您的邮箱地址"
                  required
                />
              </div>
              <button type="submit" :disabled="isSubscribing" class="subscribe-button">
                <span v-if="!isSubscribing">订阅</span>
                <span v-else class="loading-spinner"></span>
              </button>
            </form>
          </div>
        </div>
        
        <div class="contact-form-container">
          <form @submit.prevent="handleSubmit" class="contact-form">
            <div class="form-group">
              <label for="name">您的姓名</label>
              <div class="input-container">
                <user-icon />
                <input 
                  type="text" 
                  id="name" 
                  v-model="form.name" 
                  placeholder="请输入您的姓名"
                  required
                />
              </div>
            </div>
            
            <div class="form-group">
              <label for="email">电子邮箱</label>
              <div class="input-container">
                <mail-icon />
                <input 
                  type="email" 
                  id="email" 
                  v-model="form.email" 
                  placeholder="请输入您的邮箱"
                  required
                />
              </div>
            </div>
            
            <div class="form-group">
              <label for="subject">主题</label>
              <div class="input-container">
                <tag-icon />
                <input 
                  type="text" 
                  id="subject" 
                  v-model="form.subject" 
                  placeholder="消息主题"
                  required
                />
              </div>
            </div>
            
            <div class="form-group">
              <label for="message">消息内容</label>
              <div class="textarea-container">
                <message-square-icon />
                <textarea 
                  id="message" 
                  v-model="form.message" 
                  placeholder="请输入您的消息"
                  rows="5"
                  required
                ></textarea>
              </div>
            </div>
            
            <button type="submit" class="submit-button" :disabled="isSubmitting">
              <span v-if="!isSubmitting">发送消息</span>
              <span v-else class="loading-spinner"></span>
            </button>
            
            <div v-if="submitMessage" :class="['form-message', { 'success': submitSuccess, 'error': !submitSuccess }]">
              {{ submitMessage }}
            </div>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { 
  MessageSquare as MessageSquareIcon,
  Mail as MailIcon, 
  MapPin as MapPinIcon,
  Clock as ClockIcon,
  Github as GithubIcon,
  Linkedin as LinkedinIcon,
  Twitter as TwitterIcon,
  User as UserIcon,
  Tag as TagIcon
} from 'lucide-vue-next';
import { messagesApi } from '@/api';

// 表单数据
const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
});

// 订阅邮箱
const emailSubscribe = ref('');

// 状态
const isSubmitting = ref(false);
const isSubscribing = ref(false);
const submitMessage = ref('');
const submitSuccess = ref(false);

// 发送消息
const handleSubmit = async () => {
  isSubmitting.value = true;
  submitMessage.value = '';
  
  try {
    // 调用实际API发送消息
    await messagesApi.createMessage(form.value);
    
    // 成功提示
    submitSuccess.value = true;
    submitMessage.value = '消息发送成功！我会尽快回复您。';
    
    // 重置表单
    form.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    };
  } catch (error) {
    // 失败提示
    submitSuccess.value = false;
    submitMessage.value = '发送失败，请稍后再试。';
    console.error('Error sending message:', error);
  } finally {
    isSubmitting.value = false;
  }
};

// 订阅通讯
const handleSubscribe = async () => {
  if (!emailSubscribe.value) return;
  
  isSubscribing.value = true;
  
  try {
    // 实际项目中应该调用API
    // await axios.post('/api/subscribers', { email: emailSubscribe.value });
    
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 成功提示
    alert('订阅成功！感谢您的关注。');
    
    // 重置表单
    emailSubscribe.value = '';
  } catch (error) {
    // 失败提示
    alert('订阅失败，请稍后再试。');
    console.error('Error subscribing:', error);
  } finally {
    isSubscribing.value = false;
  }
};
</script>

<style scoped>
.contact-section {
  padding: 6rem 2rem;
  position: relative;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  color: #f8fafc;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #94a3b8;
  max-width: 600px;
  margin: 0 auto;
}

.highlight {
  color: #3b82f6;
}

.contact-container {
  display: grid;
  grid-template-columns: 1fr 1.5fr;
  gap: 2.5rem;
  animation: fadeIn 1s ease-out;
}

/* 联系信息部分 */
.contact-info {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 2.5rem;
  border: 1px solid rgba(99, 102, 241, 0.1);
  display: flex;
  flex-direction: column;
}

.info-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.info-header svg {
  width: 1.5rem;
  height: 1.5rem;
  color: #3b82f6;
}

.info-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #f8fafc;
  margin: 0;
}

.contact-info p {
  color: #94a3b8;
  margin-bottom: 2rem;
  line-height: 1.7;
}

.info-list {
  margin-bottom: 2rem;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.info-item svg {
  width: 1.25rem;
  height: 1.25rem;
  color: #3b82f6;
}

.info-item span {
  color: #e2e8f0;
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  background: rgba(15, 23, 42, 0.5);
  color: #e2e8f0;
  transition: all 0.3s ease;
}

.social-link:hover {
  background: #3b82f6;
  transform: translateY(-3px);
}

/* 订阅部分 */
.newsletter {
  margin-top: auto;
  padding-top: 2rem;
  border-top: 1px solid rgba(99, 102, 241, 0.1);
}

.newsletter h4 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #f8fafc;
  margin-bottom: 0.5rem;
}

.newsletter p {
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

.subscribe-form {
  display: flex;
  gap: 0.5rem;
}

.subscribe-input-group {
  flex: 1;
  position: relative;
}

.subscribe-input-group svg {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1rem;
  height: 1rem;
  color: #64748b;
}

.subscribe-input-group input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(99, 102, 241, 0.2);
  background: rgba(15, 23, 42, 0.5);
  color: #e2e8f0;
  font-size: 0.875rem;
}

.subscribe-input-group input:focus {
  outline: none;
  border-color: #3b82f6;
}

.subscribe-button {
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  color: white;
  border: none;
  padding: 0 1.5rem;
  border-radius: 0.5rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.subscribe-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.subscribe-button:disabled {
  background: #475569;
  cursor: not-allowed;
}

/* 联系表单部分 */
.contact-form-container {
  background: rgba(30, 41, 59, 0.5);
  border-radius: 1rem;
  padding: 2.5rem;
  border: 1px solid rgba(99, 102, 241, 0.1);
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

.input-container,
.textarea-container {
  position: relative;
}

.input-container svg,
.textarea-container svg {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1rem;
  height: 1rem;
  color: #64748b;
}

.textarea-container svg {
  top: 1.25rem;
  transform: none;
}

.input-container input,
.textarea-container textarea {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border-radius: 0.5rem;
  border: 1px solid rgba(99, 102, 241, 0.2);
  background: rgba(15, 23, 42, 0.5);
  color: #e2e8f0;
  font-size: 0.875rem;
}

.textarea-container textarea {
  resize: vertical;
  min-height: 120px;
}

.input-container input:focus,
.textarea-container textarea:focus {
  outline: none;
  border-color: #3b82f6;
}

.submit-button {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
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

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
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

.form-message {
  margin-top: 1rem;
  padding: 0.75rem;
  border-radius: 0.5rem;
  text-align: center;
  font-weight: 500;
}

.form-message.success {
  background: rgba(16, 185, 129, 0.1);
  color: #10b981;
  border: 1px solid rgba(16, 185, 129, 0.2);
}

.form-message.error {
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border: 1px solid rgba(239, 68, 68, 0.2);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 992px) {
  .contact-container {
    grid-template-columns: 1fr;
  }
  
  .contact-info {
    order: 2;
  }
  
  .contact-form-container {
    order: 1;
  }
}

@media (max-width: 576px) {
  .subscribe-form {
    flex-direction: column;
  }
  
  .subscribe-button {
    width: 100%;
    padding: 0.75rem;
  }
}
</style> 