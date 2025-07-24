<template>
  <div class="tags-manager">
    <div class="content-header">
      <h2>标签管理</h2>
      <button class="primary-button" @click="showCreateModal = true">
        <plus-icon size="16" />
        创建标签
      </button>
    </div>
    
    <div v-if="error" class="error-alert">{{ error }}</div>
    <div v-if="success" class="success-alert">{{ success }}</div>
    
    <div class="tags-grid" v-if="!isLoading && tags.length > 0">
      <div 
        v-for="tag in tags" 
        :key="tag.id" 
        class="tag-card"
      >
        <div class="tag-id">ID: {{ tag.id }}</div>
        <div class="tag-name">{{ tag.name }}</div>
        <div class="tag-slug">{{ tag.slug }}</div>
        <div class="tag-actions">
          <button class="icon-button danger" @click="confirmDelete(tag)">
            <trash-icon size="16" />
          </button>
        </div>
      </div>
    </div>
    
    <div class="empty-state" v-else-if="!isLoading && tags.length === 0">
      <tag-icon size="48" class="empty-icon" />
      <h3>暂无标签</h3>
      <p>创建标签来分类你的文章和项目</p>
      <button class="primary-button" @click="showCreateModal = true">
        <plus-icon size="16" />
        创建标签
      </button>
    </div>
    
    <div class="loading-state" v-if="isLoading">
      <div class="loading-spinner large"></div>
      <p>加载中...</p>
    </div>
    
    <!-- 创建标签弹窗 -->
    <div class="modal" v-if="showCreateModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>创建新标签</h3>
          <button class="icon-button" @click="showCreateModal = false">
            <x-icon size="16" />
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="tag-name">标签名称 <span class="required">*</span></label>
            <input 
              type="text" 
              id="tag-name" 
              v-model="newTag.name" 
              placeholder="输入标签名称"
              required
            />
          </div>
          <div class="form-group">
            <label for="tag-slug">标签Slug</label>
            <input 
              type="text" 
              id="tag-slug" 
              v-model="newTag.slug" 
              placeholder="tag-slug"
            />
            <small>留空将根据标签名自动生成</small>
          </div>
        </div>
        <div class="modal-footer">
          <button class="text-button" @click="showCreateModal = false">取消</button>
          <button 
            class="primary-button" 
            @click="createTag"
            :disabled="!newTag.name || isCreating"
          >
            <span v-if="isCreating" class="loading-spinner"></span>
            <span v-else>创建标签</span>
          </button>
        </div>
      </div>
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
          <p>确定要删除标签 <strong>{{ tagToDelete?.name }}</strong> 吗？</p>
          <p class="warning-text">此操作无法撤销。删除标签不会删除使用该标签的文章或项目，但会从它们中移除此标签。</p>
        </div>
        <div class="modal-footer">
          <button class="text-button" @click="showDeleteModal = false">取消</button>
          <button 
            class="danger-button" 
            @click="deleteTag"
            :disabled="isDeleting"
          >
            <span v-if="isDeleting" class="loading-spinner"></span>
            <span v-else>删除</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { tagsApi } from '@/api';
import { 
  Plus as PlusIcon,
  Trash as TrashIcon,
  Tag as TagIcon,
  X as XIcon
} from 'lucide-vue-next';

// 状态
const tags = ref<any[]>([]);
const isLoading = ref(false);
const error = ref('');
const success = ref('');

// 创建标签
const showCreateModal = ref(false);
const isCreating = ref(false);
const newTag = ref({
  name: '',
  slug: ''
});

// 删除标签
const showDeleteModal = ref(false);
const isDeleting = ref(false);
const tagToDelete = ref<any>(null);

// 加载标签
const loadTags = async () => {
  isLoading.value = true;
  error.value = '';
  
  try {
    const response = await tagsApi.getTags();
    tags.value = response.data;
  } catch (err: any) {
    console.error('加载标签失败:', err);
    error.value = '加载标签失败，请稍后再试';
  } finally {
    isLoading.value = false;
  }
};

// 创建标签
const createTag = async () => {
  if (!newTag.value.name) return;
  
  isCreating.value = true;
  error.value = '';
  success.value = '';
  
  try {
    const response = await tagsApi.createTag({
      name: newTag.value.name,
      slug: newTag.value.slug || undefined
    });
    
    // 添加新标签到列表
    tags.value.push(response.data);
    
    // 重置表单和关闭弹窗
    newTag.value = { name: '', slug: '' };
    showCreateModal.value = false;
    
    success.value = '标签创建成功';
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('创建标签失败:', err);
    error.value = err.response?.data?.detail || '创建标签失败';
  } finally {
    isCreating.value = false;
  }
};

// 确认删除
const confirmDelete = (tag: any) => {
  tagToDelete.value = tag;
  showDeleteModal.value = true;
};

// 删除标签
const deleteTag = async () => {
  if (!tagToDelete.value) return;
  
  isDeleting.value = true;
  error.value = '';
  success.value = '';
  
  try {
    await tagsApi.deleteTag(tagToDelete.value.id);
    
    // 从列表中移除
    tags.value = tags.value.filter(tag => tag.id !== tagToDelete.value.id);
    
    // 关闭弹窗
    showDeleteModal.value = false;
    tagToDelete.value = null;
    
    success.value = '标签删除成功';
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('删除标签失败:', err);
    error.value = err.response?.data?.detail || '删除标签失败';
  } finally {
    isDeleting.value = false;
  }
};

// 初始化
onMounted(() => {
  loadTags();
});
</script>

<style scoped>
.tags-manager {
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

.tags-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.tag-card {
  background-color: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: all 0.2s;
}

.tag-card:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.tag-id {
  color: #3b82f6;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.tag-name {
  font-weight: 600;
  color: #1e293b;
}

.tag-slug {
  color: #64748b;
  font-size: 0.875rem;
}

.tag-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
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
  margin-bottom: 1.5rem;
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
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

.loading-spinner.large {
  width: 2rem;
  height: 2rem;
  border: 3px solid rgba(59, 130, 246, 0.3);
  border-top-color: #3b82f6;
  margin-bottom: 1rem;
}

.loading-state p {
  color: #64748b;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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

.icon-button {
  display: flex;
  align-items: center;
  justify-content: center;
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

.icon-button.danger:hover {
  background-color: rgba(239, 68, 68, 0.1);
  color: #ef4444;
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

.required {
  color: #ef4444;
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

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #1e293b;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: #64748b;
  font-size: 0.75rem;
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

.warning-text {
  color: #f59e0b;
  font-size: 0.875rem;
}
</style> 