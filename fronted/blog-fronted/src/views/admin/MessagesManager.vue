<template>
  <div class="messages-manager">
    <div class="content-header">
      <h2>消息管理</h2>
      <div class="filter-controls">
        <button 
          class="filter-button" 
          :class="{ active: filterStatus === 'all' }"
          @click="filterStatus = 'all'"
        >
          全部
        </button>
        <button 
          class="filter-button" 
          :class="{ active: filterStatus === 'unread' }"
          @click="filterStatus = 'unread'"
        >
          未读
        </button>
        <button 
          class="filter-button" 
          :class="{ active: filterStatus === 'read' }"
          @click="filterStatus = 'read'"
        >
          已读
        </button>
      </div>
    </div>
    
    <div v-if="error" class="error-alert">{{ error }}</div>
    
    <div class="messages-list" v-if="!isLoading && messages.length > 0">
      <div 
        v-for="message in filteredMessages" 
        :key="message.id" 
        class="message-card"
        :class="{ 'unread': !message.is_read }"
      >
        <div class="message-header">
          <div>
            <h3>{{ message.subject || '无主题' }}</h3>
            <div class="message-meta">
              <span class="message-name">{{ message.name }}</span>
              <span class="message-email">{{ message.email }}</span>
            </div>
          </div>
          <span class="message-date">{{ formatDate(message.created_at) }}</span>
        </div>
        
        <p class="message-content">{{ message.message }}</p>
        
        <div class="message-actions">
          <span class="message-id">ID: {{ message.id }}</span>
          <button 
            class="icon-button" 
            :class="{ 'active': message.is_read }" 
            @click="toggleReadStatus(message)"
          >
            <check-icon size="16" />
            <span>{{ message.is_read ? '已读' : '标记为已读' }}</span>
          </button>
          <button class="icon-button" @click="replyToMessage(message)">
            <mail-icon size="16" />
            <span>回复</span>
          </button>
          <button class="icon-button danger" @click="confirmDelete(message)">
            <trash-icon size="16" />
            <span>删除</span>
          </button>
        </div>
      </div>
    </div>
    
    <div class="empty-state" v-else-if="!isLoading && messages.length === 0">
      <inbox-icon size="48" class="empty-icon" />
      <h3>暂无消息</h3>
      <p>当有人通过联系表单发送消息时，将会显示在这里</p>
    </div>
    
    <div class="loading-state" v-if="isLoading">
      <div class="loading-spinner large"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 分页控制 -->
    <div class="pagination" v-if="totalPages > 1">
      <button 
        class="pagination-button" 
        :disabled="currentPage === 1"
        @click="changePage(currentPage - 1)"
      >
        <chevron-left-icon size="16" />
      </button>
      
      <div class="page-info">
        第 {{ currentPage }} 页，共 {{ totalPages }} 页
      </div>
      
      <button 
        class="pagination-button" 
        :disabled="currentPage === totalPages"
        @click="changePage(currentPage + 1)"
      >
        <chevron-right-icon size="16" />
      </button>
    </div>
    
    <!-- 确认删除弹窗 -->
    <div class="modal" v-if="showDeleteModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>确认删除</h3>
          <button class="icon-button" @click="showDeleteModal = false">
            <x-icon size="16" />
          </button>
        </div>
        <div class="modal-body">
          <p>确定要删除来自 <strong>{{ messageToDelete?.name }}</strong> 的消息吗？</p>
          <p class="warning-text">此操作无法撤销。</p>
        </div>
        <div class="modal-footer">
          <button class="text-button" @click="showDeleteModal = false">取消</button>
          <button 
            class="danger-button" 
            @click="deleteMessage"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="loading-spinner"></span>
            <span v-else>删除</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- 回复邮件弹窗 -->
    <div class="modal" v-if="showReplyModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>回复消息</h3>
          <button class="icon-button" @click="showReplyModal = false">
            <x-icon size="16" />
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>收件人</label>
            <div class="recipient">{{ messageToReply?.name }} &lt;{{ messageToReply?.email }}&gt;</div>
          </div>
          <div class="form-group">
            <label for="reply-subject">主题</label>
            <input 
              type="text" 
              id="reply-subject" 
              v-model="replyForm.subject" 
              placeholder="Re: 原始主题"
            />
          </div>
          <div class="form-group">
            <label for="reply-message">内容</label>
            <textarea 
              id="reply-message" 
              v-model="replyForm.message" 
              placeholder="输入回复内容..."
              rows="6"
            ></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="text-button" @click="showReplyModal = false">取消</button>
          <button 
            class="primary-button" 
            @click="sendReply"
            :disabled="!replyForm.message || isSending"
          >
            <span v-if="isSending" class="loading-spinner"></span>
            <span v-else>发送</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { messagesApi } from '@/api';
import { 
  Check as CheckIcon,
  Mail as MailIcon,
  Trash as TrashIcon,
  ChevronLeft as ChevronLeftIcon,
  ChevronRight as ChevronRightIcon,
  Inbox as InboxIcon,
  X as XIcon
} from 'lucide-vue-next';

// 状态
const messages = ref<any[]>([]);
const isLoading = ref(false);
const error = ref('');
const filterStatus = ref('all'); // all, read, unread
const currentPage = ref(1);
const totalMessages = ref(0);
const pageSize = 10;

// 删除相关
const showDeleteModal = ref(false);
const messageToDelete = ref<any>(null);
const isDeleting = ref(false);

// 回复相关
const showReplyModal = ref(false);
const messageToReply = ref<any>(null);
const isSending = ref(false);
const replyForm = ref({
  subject: '',
  message: ''
});

// 计算属性
const totalPages = computed(() => Math.ceil(totalMessages.value / pageSize));

const filteredMessages = computed(() => {
  if (filterStatus.value === 'all') {
    return messages.value;
  } else if (filterStatus.value === 'read') {
    return messages.value.filter(msg => msg.is_read);
  } else {
    return messages.value.filter(msg => !msg.is_read);
  }
});

// 格式化日期
const formatDate = (dateString: string) => {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 加载消息
const loadMessages = async () => {
  isLoading.value = true;
  error.value = '';
  
  try {
    console.log('正在加载消息列表...');
    
    // 构建查询参数
    const params: any = {
      skip: (currentPage.value - 1) * pageSize,
      limit: pageSize
    };
    
    // 如果有过滤条件，添加到参数
    if (filterStatus.value === 'read') {
      params.is_read = true;
    } else if (filterStatus.value === 'unread') {
      params.is_read = false;
    }
    
    const response = await messagesApi.getMessages(params);
    console.log('消息列表响应:', response);
    
    if (Array.isArray(response.data)) {
      messages.value = response.data;
      console.log(`成功加载 ${messages.value.length} 条消息`);
    } else {
      console.warn('消息数据格式不符合预期:', response.data);
      messages.value = [];
    }
    
    // 假设总数从响应头中获取，如果后端没有提供，则使用当前页面消息数
    // 在实际应用中，可能需要单独的API调用来获取总数
    totalMessages.value = parseInt(response.headers['x-total-count'] || '0');
    if (isNaN(totalMessages.value) || totalMessages.value === 0) {
      // 如果无法从头部获取，则假设至少有当前页数据量的消息
      totalMessages.value = Math.max(messages.value.length, totalMessages.value);
    }
    
    // 如果当前页没有数据但总消息数大于0，可能是页码超出范围，尝试回到第一页
    if (messages.value.length === 0 && totalMessages.value > 0 && currentPage.value > 1) {
      currentPage.value = 1;
      await loadMessages();
      return;
    }
  } catch (err: any) {
    console.error('加载消息失败:', err);
    if (err.response) {
      console.error('错误状态码:', err.response.status);
      console.error('错误详情:', err.response.data);
    }
    error.value = '加载消息失败，请稍后再试';
    messages.value = [];
  } finally {
    isLoading.value = false;
  }
};

// 切换已读状态
const toggleReadStatus = async (message: any) => {
  try {
    const updatedStatus = !message.is_read;
    await messagesApi.updateMessage(message.id, { is_read: updatedStatus });
    message.is_read = updatedStatus;
  } catch (err: any) {
    console.error('更新消息状态失败:', err);
    error.value = '更新消息状态失败，请稍后再试';
  }
};

// 确认删除
const confirmDelete = (message: any) => {
  messageToDelete.value = message;
  showDeleteModal.value = true;
};

// 删除消息
const deleteMessage = async () => {
  if (!messageToDelete.value) return;
  
  isDeleting.value = true;
  try {
    await messagesApi.deleteMessage(messageToDelete.value.id);
    
    // 从列表中移除
    messages.value = messages.value.filter(msg => msg.id !== messageToDelete.value.id);
    
    // 关闭弹窗
    showDeleteModal.value = false;
    messageToDelete.value = null;
  } catch (err: any) {
    console.error('删除消息失败:', err);
    error.value = '删除消息失败，请稍后再试';
  } finally {
    isDeleting.value = false;
  }
};

// 回复消息
const replyToMessage = (message: any) => {
  messageToReply.value = message;
  replyForm.value.subject = `Re: ${message.subject || '无主题'}`;
  replyForm.value.message = '';
  showReplyModal.value = true;
};

// 发送回复
const sendReply = async () => {
  if (!messageToReply.value || !replyForm.value.message) return;
  
  isSending.value = true;
  try {
    // 在实际应用中，这里应该调用发送邮件的API
    // 这里我们只是模拟发送
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 标记消息为已读
    if (!messageToReply.value.is_read) {
      await messagesApi.updateMessage(messageToReply.value.id, { is_read: true });
      messageToReply.value.is_read = true;
    }
    
    // 关闭弹窗
    showReplyModal.value = false;
    messageToReply.value = null;
    replyForm.value = { subject: '', message: '' };
    
    // 显示成功消息
    alert('回复已发送');
  } catch (err: any) {
    console.error('发送回复失败:', err);
    error.value = '发送回复失败，请稍后再试';
  } finally {
    isSending.value = false;
  }
};

// 切换页面
const changePage = (page: number) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
};

// 监听过滤器变化，重新加载消息
watch(filterStatus, () => {
  currentPage.value = 1; // 重置页码
  loadMessages();
});

// 监听页码变化，重新加载消息
watch(currentPage, () => {
  loadMessages();
});

// 初始化
onMounted(() => {
  loadMessages();
});
</script>

<style scoped>
.messages-manager {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.content-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.content-header h2 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
}

.filter-controls {
  display: flex;
  gap: 0.5rem;
}

.filter-button {
  background-color: white;
  border: 1px solid #e2e8f0;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-button:hover {
  background-color: #f8fafc;
}

.filter-button.active {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.messages-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message-card {
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1.5rem;
  transition: all 0.2s;
}

.message-card.unread {
  border-left: 3px solid #3b82f6;
  background-color: #f8fafc;
}

.message-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.message-header h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.125rem;
  color: #1e293b;
}

.message-meta {
  display: flex;
  gap: 1rem;
  color: #64748b;
  font-size: 0.875rem;
}

.message-name {
  font-weight: 500;
}

.message-email {
  color: #94a3b8;
}

.message-date {
  color: #94a3b8;
  font-size: 0.875rem;
}

.message-content {
  color: #334155;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  white-space: pre-line;
}

.message-actions {
  display: flex;
  gap: 1rem;
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.message-id {
  color: #3b82f6;
  font-size: 0.875rem;
  margin-right: 1rem;
  font-weight: 600;
}

.icon-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.icon-button:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

.icon-button.active {
  color: #22c55e;
}

.icon-button.danger:hover {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
  text-align: center;
}

.empty-icon {
  color: #cbd5e1;
  margin-bottom: 1rem;
}

.empty-state h3 {
  margin: 0 0 0.5rem 0;
  color: #1e293b;
  font-size: 1.25rem;
}

.empty-state p {
  color: #64748b;
  max-width: 400px;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 0;
}

.loading-spinner {
  display: inline-block;
  width: 1rem;
  height: 1rem;
  border: 2px solid rgba(59, 130, 246, 0.3);
  border-radius: 50%;
  border-top-color: #3b82f6;
  animation: spin 1s ease-in-out infinite;
}

.loading-spinner.large {
  width: 2rem;
  height: 2rem;
  border-width: 3px;
  margin-bottom: 1rem;
}

.loading-state p {
  color: #64748b;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 2rem;
  gap: 1rem;
}

.pagination-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.pagination-button:hover:not(:disabled) {
  background-color: #f8fafc;
  color: #1e293b;
}

.pagination-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: #64748b;
  font-size: 0.875rem;
}

.error-alert {
  margin-bottom: 1.5rem;
  padding: 0.75rem 1rem;
  background-color: rgba(239, 68, 68, 0.1);
  border-left: 3px solid #ef4444;
  color: #b91c1c;
  border-radius: 0.25rem;
}

/* 弹窗 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 0.5rem;
  width: 100%;
  max-width: 500px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.modal-header h3 {
  margin: 0;
  color: #1e293b;
  font-size: 1.125rem;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1rem 1.5rem;
  border-top: 1px solid #e2e8f0;
}

.warning-text {
  color: #ef4444;
  font-size: 0.875rem;
}

.danger-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.danger-button:hover {
  background-color: #dc2626;
}

.danger-button:disabled {
  background-color: #94a3b8;
  cursor: not-allowed;
}

.primary-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
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

.text-button {
  background-color: transparent;
  color: #64748b;
  border: none;
  padding: 0.5rem 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: color 0.2s;
}

.text-button:hover {
  color: #1e293b;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #1e293b;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.recipient {
  padding: 0.75rem 1rem;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  color: #1e293b;
}
</style> 