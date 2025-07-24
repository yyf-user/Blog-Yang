<template>
  <div class="editor-container">
    <div class="editor-header">
      <h2>{{ isEdit ? '编辑项目' : '创建新项目' }}</h2>
      <div class="editor-actions">
        <button 
          class="primary-button" 
          @click="saveProject"
          :disabled="isLoading"
        >
          {{ isEdit ? '更新项目' : '创建项目' }}
        </button>
      </div>
    </div>
    
    <div v-if="error" class="error-alert">{{ error }}</div>
    <div v-if="success" class="success-alert">{{ success }}</div>
    
    <div class="editor-form">
      <div class="form-group">
        <label for="title">项目名称 <span class="required">*</span></label>
        <input 
          type="text" 
          id="title" 
          v-model="project.title" 
          placeholder="项目名称"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="slug">Slug (URL)</label>
        <input 
          type="text" 
          id="slug" 
          v-model="project.slug" 
          placeholder="project-url-slug"
        />
        <small>留空将根据项目名称自动生成</small>
      </div>
      
      <div class="form-group">
        <label for="description">描述 <span class="required">*</span></label>
        <textarea 
          id="description" 
          v-model="project.description" 
          placeholder="项目描述"
          rows="4"
          required
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="image_url">项目图片URL <span class="required">*</span></label>
        <input 
          type="text" 
          id="image_url" 
          v-model="project.image_url" 
          placeholder="https://example.com/image.jpg"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="github_url">GitHub链接</label>
        <input 
          type="text" 
          id="github_url" 
          v-model="project.github_url" 
          placeholder="https://github.com/username/project"
        />
      </div>
      
      <div class="form-group">
        <label for="live_url">在线演示链接</label>
        <input 
          type="text" 
          id="live_url" 
          v-model="project.live_url" 
          placeholder="https://example.com"
        />
      </div>
      
      <div class="form-group">
        <label for="emoji">项目表情符号</label>
        <input 
          type="text" 
          id="emoji" 
          v-model="project.emoji" 
          placeholder="🚀"
          maxlength="2"
        />
        <small>用于项目卡片显示的表情符号</small>
      </div>
      
      <div class="form-group">
        <label for="stars_count">GitHub Stars数量</label>
        <input 
          type="number" 
          id="stars_count" 
          v-model="project.stars_count" 
          placeholder="0"
          min="0"
        />
      </div>
      
      <div class="form-group">
        <label for="forks_count">GitHub Forks数量</label>
        <input 
          type="number" 
          id="forks_count" 
          v-model="project.forks_count" 
          placeholder="0"
          min="0"
        />
      </div>
      
      <div class="form-group">
        <label>标签</label>
        <div class="tags-container">
          <div 
            v-for="tag in availableTags" 
            :key="tag.id" 
            class="tag-item"
            :class="{ 'selected': isTagSelected(tag.id) }"
            @click="toggleTag(tag.id)"
          >
            {{ tag.name }}
          </div>
          <div class="tag-item new-tag" @click="showNewTagModal = true">
            <plus-icon size="14" /> 新标签
          </div>
        </div>
      </div>
      
      <div class="form-group">
        <label class="checkbox-label">
          <input type="checkbox" v-model="project.featured" />
          <span>设为精选项目</span>
        </label>
      </div>
    </div>
    
    <!-- 底部工具栏 -->
    <div class="editor-footer">
      <div></div>
      <div class="editor-actions">
        <button class="text-button" @click="cancel">取消</button>
        <button 
          class="primary-button" 
          @click="saveProject"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          <span v-else>{{ isEdit ? '更新项目' : '创建项目' }}</span>
        </button>
      </div>
    </div>
    
    <!-- 新标签弹窗 -->
    <div class="modal" v-if="showNewTagModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>创建新标签</h3>
          <button class="icon-button" @click="showNewTagModal = false">
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
          <button class="text-button" @click="showNewTagModal = false">取消</button>
          <button 
            class="primary-button" 
            @click="createTag"
            :disabled="!newTag.name || isTagLoading"
          >
            <span v-if="isTagLoading" class="loading-spinner"></span>
            <span v-else>创建标签</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { projectsApi, tagsApi } from '@/api';
import { 
  Plus as PlusIcon,
  X as XIcon
} from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();

// 状态
const isEdit = computed(() => !!route.params.id);
const project = ref({
  title: '',
  slug: '',
  description: '',
  image_url: '',
  github_url: '',
  live_url: '',
  emoji: '🚀',
  stars_count: 0,
  forks_count: 0,
  featured: false,
  tags: [] as number[]
});
const availableTags = ref<any[]>([]);
const isLoading = ref(false);
const isTagLoading = ref(false);
const error = ref('');
const success = ref('');
const showNewTagModal = ref(false);
const newTag = ref({
  name: '',
  slug: ''
});

// 检查标签是否已选择
const isTagSelected = (tagId: number) => {
  return project.value.tags.includes(tagId);
};

// 切换标签选择状态
const toggleTag = (tagId: number) => {
  const index = project.value.tags.indexOf(tagId);
  if (index === -1) {
    project.value.tags.push(tagId);
  } else {
    project.value.tags.splice(index, 1);
  }
};

// 加载标签
const loadTags = async () => {
  try {
    const response = await tagsApi.getTags();
    availableTags.value = response.data;
  } catch (err: any) {
    console.error('加载标签失败:', err);
    error.value = '加载标签失败';
  }
};

// 创建新标签
const createTag = async () => {
  if (!newTag.value.name) return;
  
  isTagLoading.value = true;
  try {
    const response = await tagsApi.createTag({
      name: newTag.value.name,
      slug: newTag.value.slug || undefined
    });
    
    // 添加新标签到列表
    availableTags.value.push(response.data);
    
    // 选择新创建的标签
    project.value.tags.push(response.data.id);
    
    // 重置表单
    newTag.value = { name: '', slug: '' };
    showNewTagModal.value = false;
    
    success.value = '标签创建成功';
    setTimeout(() => {
      success.value = '';
    }, 3000);
  } catch (err: any) {
    console.error('创建标签失败:', err);
    error.value = err.response?.data?.detail || '创建标签失败';
  } finally {
    isTagLoading.value = false;
  }
};

// 加载项目详情
const loadProject = async (id: number) => {
  isLoading.value = true;
  try {
    const response = await projectsApi.getProject(id);
    const projectData = response.data;
    
    // 设置项目数据
    project.value = {
      title: projectData.title,
      slug: projectData.slug,
      description: projectData.description,
      image_url: projectData.image_url || '',
      github_url: projectData.github_url || '',
      live_url: projectData.live_url || '',
      emoji: projectData.emoji || '🚀',
      stars_count: projectData.stars_count || 0,
      forks_count: projectData.forks_count || 0,
      featured: projectData.featured || false,
      tags: projectData.tags.map((tag: any) => tag.id)
    };
  } catch (err: any) {
    console.error('加载项目失败:', err);
    error.value = '加载项目失败，请稍后再试';
  } finally {
    isLoading.value = false;
  }
};

// 保存项目
const saveProject = async () => {
  // 验证必填字段
  if (!project.value.title || !project.value.description || !project.value.image_url) {
    error.value = '请填写项目名称、描述和图片URL';
    return;
  }
  
  isLoading.value = true;
  error.value = '';
  success.value = '';
  
  try {
    let response;
    
    if (isEdit.value) {
      // 更新项目
      response = await projectsApi.updateProject(Number(route.params.id), project.value);
    } else {
      // 创建项目
      response = await projectsApi.createProject(project.value);
    }
    
    success.value = isEdit.value ? '项目更新成功' : '项目创建成功';
    
    // 如果是新创建的项目，跳转到编辑页面
    if (!isEdit.value) {
      setTimeout(() => {
        router.push(`/admin/projects/edit/${response.data.id}`);
      }, 1000);
    }
  } catch (err: any) {
    console.error('保存项目失败:', err);
    error.value = err.response?.data?.detail || '保存失败，请稍后再试';
  } finally {
    isLoading.value = false;
  }
};

// 取消编辑
const cancel = () => {
  router.push('/admin/projects');
};

// 初始化
onMounted(async () => {
  await loadTags();
  
  if (isEdit.value && route.params.id) {
    await loadProject(Number(route.params.id));
  }
});
</script>

<style scoped>
.editor-container {
  background-color: white;
  border-radius: 0.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e2e8f0;
}

.editor-header h2 {
  margin: 0;
  color: #1e293b;
  font-size: 1.25rem;
}

.editor-actions {
  display: flex;
  gap: 1rem;
}

.editor-form {
  padding: 1.5rem;
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

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.3);
}

.form-group small {
  display: block;
  margin-top: 0.25rem;
  color: #64748b;
  font-size: 0.75rem;
}

.required {
  color: #ef4444;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.checkbox-label input {
  width: auto;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.25rem 0.75rem;
  background-color: #f1f5f9;
  border-radius: 9999px;
  font-size: 0.875rem;
  color: #64748b;
  cursor: pointer;
  transition: all 0.2s;
}

.tag-item:hover {
  background-color: #e2e8f0;
}

.tag-item.selected {
  background-color: #3b82f6;
  color: white;
}

.tag-item.new-tag {
  background-color: #f8fafc;
  border: 1px dashed #cbd5e1;
}

.editor-footer {
  display: flex;
  justify-content: space-between;
  padding: 1.5rem;
  border-top: 1px solid #e2e8f0;
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

.icon-button {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: transparent;
  border: none;
  color: #64748b;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: all 0.2s;
}

.icon-button:hover {
  background-color: #f1f5f9;
  color: #1e293b;
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
  margin: 1rem 1.5rem 0;
  padding: 0.75rem 1rem;
  background-color: rgba(239, 68, 68, 0.1);
  border-left: 3px solid #ef4444;
  color: #b91c1c;
  border-radius: 0.25rem;
}

.success-alert {
  margin: 1rem 1.5rem 0;
  padding: 0.75rem 1rem;
  background-color: rgba(34, 197, 94, 0.1);
  border-left: 3px solid #22c55e;
  color: #166534;
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
</style> 