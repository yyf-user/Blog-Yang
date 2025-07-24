<template>
  <div class="editor-container">
    <div class="editor-header">
      <h2>{{ isEdit ? '编辑文章' : '创建新文章' }}</h2>
      <div class="editor-actions">
        <button 
          class="secondary-button" 
          @click="saveAsDraft"
          :disabled="isLoading"
        >
          保存为草稿
        </button>
        <button 
          class="primary-button" 
          @click="publishArticle"
          :disabled="isLoading"
        >
          {{ isEdit && article.status === 'published' ? '更新文章' : '发布文章' }}
        </button>
      </div>
    </div>
    
    <div v-if="error" class="error-alert">{{ error }}</div>
    <div v-if="success" class="success-alert">{{ success }}</div>
    
    <div class="editor-form">
      <div class="form-group">
        <label for="title">标题 <span class="required">*</span></label>
        <input 
          type="text" 
          id="title" 
          v-model="article.title" 
          placeholder="文章标题"
          required
        />
      </div>
      
      <div class="form-group">
        <label for="slug">Slug (URL)</label>
        <input 
          type="text" 
          id="slug" 
          v-model="article.slug" 
          placeholder="article-url-slug"
        />
        <small>留空将根据标题自动生成</small>
      </div>
      
      <div class="form-group">
        <label for="excerpt">摘要 <span class="required">*</span></label>
        <textarea 
          id="excerpt" 
          v-model="article.excerpt" 
          placeholder="文章摘要，简短介绍"
          rows="2"
          required
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="content">内容 <span class="required">*</span></label>
        <textarea 
          id="content" 
          v-model="article.content" 
          placeholder="文章内容，支持Markdown格式"
          rows="15"
          required
        ></textarea>
      </div>
      
      <div class="form-group">
        <label for="cover_image">封面图片URL</label>
        <input 
          type="text" 
          id="cover_image" 
          v-model="article.cover_image" 
          placeholder="https://example.com/image.jpg"
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
          <input type="checkbox" v-model="article.featured" />
          <span>设为精选文章</span>
        </label>
      </div>
    </div>
    
    <!-- 预览区域 -->
    <div class="preview-container" v-if="showPreview">
      <div class="preview-header">
        <h3>预览</h3>
        <button class="icon-button" @click="showPreview = false">
          <x-icon size="16" />
        </button>
      </div>
      <div class="preview-content">
        <h1>{{ article.title || '文章标题' }}</h1>
        <div class="preview-excerpt">{{ article.excerpt || '文章摘要' }}</div>
        <div class="preview-body" v-html="formattedContent"></div>
      </div>
    </div>
    
    <!-- 底部工具栏 -->
    <div class="editor-footer">
      <button class="secondary-button" @click="showPreview = !showPreview">
        {{ showPreview ? '关闭预览' : '预览' }}
      </button>
      <div class="editor-actions">
        <button class="text-button" @click="cancel">取消</button>
        <button 
          class="primary-button" 
          @click="publishArticle"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading-spinner"></span>
          <span v-else>{{ isEdit && article.status === 'published' ? '更新文章' : '发布文章' }}</span>
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
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { articlesApi, tagsApi } from '@/api';
import { 
  Plus as PlusIcon,
  X as XIcon
} from 'lucide-vue-next';

// 移除 marked 库的导入
// import { marked } from 'marked';

const router = useRouter();
const route = useRoute();

// 状态
const isEdit = computed(() => !!route.params.id);
const article = ref({
  title: '',
  slug: '',
  excerpt: '',
  content: '',
  cover_image: '',
  featured: false,
  tags: [] as number[],
  status: 'draft'
});
const availableTags = ref<any[]>([]);
const isLoading = ref(false);
const isTagLoading = ref(false);
const error = ref('');
const success = ref('');
const showPreview = ref(false);
const showNewTagModal = ref(false);
const newTag = ref({
  name: '',
  slug: ''
});

// 格式化内容为HTML
const formattedContent = computed(() => {
  if (!article.value.content) return '';
  try {
    // 简单的Markdown格式化方法
    return article.value.content
      .replace(/\n\n/g, '</p><p>')
      .replace(/\n/g, '<br>')
      .replace(/#{4,6}\s+(.+?)(?:\n|$)/g, '<h4>$1</h4>')
      .replace(/###\s+(.+?)(?:\n|$)/g, '<h3>$1</h3>')
      .replace(/##\s+(.+?)(?:\n|$)/g, '<h2>$1</h2>')
      .replace(/^(.+?)(?:\n|$)/g, '<p>$1</p>');
  } catch (e) {
    console.error('格式化内容错误:', e);
    return `<p>${article.value.content}</p>`;
  }
});

// 检查标签是否已选择
const isTagSelected = (tagId: number) => {
  return article.value.tags.includes(tagId);
};

// 切换标签选择状态
const toggleTag = (tagId: number) => {
  const index = article.value.tags.indexOf(tagId);
  if (index === -1) {
    article.value.tags.push(tagId);
  } else {
    article.value.tags.splice(index, 1);
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
    article.value.tags.push(response.data.id);
    
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

// 加载文章详情
const loadArticle = async (id: number) => {
  isLoading.value = true;
  try {
    const response = await articlesApi.getArticle(id);
    const articleData = response.data;
    
    // 设置文章数据
    article.value = {
      title: articleData.title,
      slug: articleData.slug,
      excerpt: articleData.excerpt,
      content: articleData.content,
      cover_image: articleData.cover_image || '',
      featured: articleData.featured || false,
      tags: articleData.tags.map((tag: any) => tag.id),
      status: articleData.status
    };
  } catch (err: any) {
    console.error('加载文章失败:', err);
    error.value = '加载文章失败，请稍后再试';
  } finally {
    isLoading.value = false;
  }
};

// 保存为草稿
const saveAsDraft = async () => {
  article.value.status = 'draft';
  await saveArticle();
};

// 发布文章
const publishArticle = async () => {
  article.value.status = 'published';
  await saveArticle();
};

// 保存文章
const saveArticle = async () => {
  // 验证必填字段
  if (!article.value.title || !article.value.excerpt || !article.value.content) {
    error.value = '请填写标题、摘要和内容';
    return;
  }
  
  isLoading.value = true;
  error.value = '';
  success.value = '';
  
  try {
    let response;
    
    if (isEdit.value) {
      // 更新文章
      response = await articlesApi.updateArticle(Number(route.params.id), article.value);
    } else {
      // 创建文章
      response = await articlesApi.createArticle(article.value);
    }
    
    success.value = isEdit.value ? '文章更新成功' : '文章创建成功';
    
    // 如果是新创建的文章，跳转到编辑页面
    if (!isEdit.value) {
      setTimeout(() => {
        router.push(`/admin/articles/edit/${response.data.id}`);
      }, 1000);
    }
  } catch (err: any) {
    console.error('保存文章失败:', err);
    error.value = err.response?.data?.detail || '保存失败，请稍后再试';
  } finally {
    isLoading.value = false;
  }
};

// 取消编辑
const cancel = () => {
  router.push('/admin/articles');
};

// 初始化
onMounted(async () => {
  await loadTags();
  
  if (isEdit.value && route.params.id) {
    await loadArticle(Number(route.params.id));
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

.secondary-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background-color: white;
  color: #1e293b;
  border: 1px solid #e2e8f0;
  padding: 0.5rem 1rem;
  border-radius: 0.375rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.secondary-button:hover {
  background-color: #f8fafc;
}

.secondary-button:disabled {
  color: #94a3b8;
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

/* 预览区域 */
.preview-container {
  margin: 0 1.5rem 1.5rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  overflow: hidden;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: #f8fafc;
  border-bottom: 1px solid #e2e8f0;
}

.preview-header h3 {
  margin: 0;
  font-size: 0.875rem;
  color: #64748b;
}

.preview-content {
  padding: 1.5rem;
  max-height: 500px;
  overflow-y: auto;
}

.preview-content h1 {
  margin-top: 0;
  color: #1e293b;
}

.preview-excerpt {
  color: #64748b;
  font-size: 1.125rem;
  margin-bottom: 1.5rem;
}

.preview-body {
  color: #334155;
  line-height: 1.6;
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