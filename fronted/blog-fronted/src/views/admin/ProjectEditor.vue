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
          class="form-input"
        />
      </div>
      
      <div class="form-group">
        <label for="slug">Slug (URL)</label>
        <input 
          type="text" 
          id="slug" 
          v-model="project.slug" 
          placeholder="project-url-slug"
          class="form-input"
        />
        <small>留空将根据项目名称自动生成</small>
      </div>
      
      <div class="form-group markdown-editor-container">
        <label for="description">描述 <span class="required">*</span></label>
        <div class="markdown-toolbar">
          <button type="button" class="toolbar-button" @click="insertMarkdown('bold')">
            <b>B</b>
          </button>
          <button type="button" class="toolbar-button" @click="insertMarkdown('italic')">
            <i>I</i>
          </button>
          <button type="button" class="toolbar-button" @click="insertMarkdown('heading')">
            H
          </button>
          <button type="button" class="toolbar-button" @click="insertMarkdown('link')">
            Link
          </button>
          <button type="button" class="toolbar-button" @click="insertMarkdown('list')">
            List
          </button>
          <button type="button" class="toolbar-button" @click="insertMarkdown('code')">
            Code
          </button>
          <div class="toolbar-divider"></div>
          <button 
            type="button" 
            class="toolbar-button preview-toggle" 
            :class="{ 'active': showPreview }"
            @click="togglePreview"
          >
            预览
          </button>
        </div>
        <div class="markdown-editor-area">
          <textarea 
            id="description" 
            v-model="project.description" 
            placeholder="项目描述，支持Markdown格式"
            rows="15"
            required
            class="form-textarea"
            v-show="!showPreview"
            ref="descriptionTextarea"
          ></textarea>
          <div 
            v-show="showPreview" 
            class="markdown-preview" 
            v-html="formattedDescription"
          ></div>
        </div>
        <small>支持Markdown格式 - 
          <a href="#" @click.prevent="showHelpModal = true">查看Markdown帮助</a>
        </small>
      </div>
      
      <div class="form-group">
        <label for="image_url">项目图片URL <span class="required">*</span></label>
        <input 
          type="text" 
          id="image_url" 
          v-model="project.image_url" 
          placeholder="https://example.com/image.jpg"
          required
          class="form-input"
        />
      </div>
      
      <div class="form-group">
        <label for="github_url">GitHub链接</label>
        <input 
          type="text" 
          id="github_url" 
          v-model="project.github_url" 
          placeholder="https://github.com/username/project"
          class="form-input"
        />
      </div>
      
      <div class="form-group">
        <label for="live_url">在线演示链接</label>
        <input 
          type="text" 
          id="live_url" 
          v-model="project.live_url" 
          placeholder="https://example.com"
          class="form-input"
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
          class="form-input"
        />
        <small>用于项目卡片显示的表情符号</small>
      </div>
      
      <div class="form-group">
        <label for="stars-count">GitHub Stars数量</label>
        <input 
          type="number" 
          id="stars-count" 
          :value="project.stars_count" 
          @input="e => project.stars_count = Number(e.target.value) || 0" 
          min="0" 
          class="form-input"
          placeholder="GitHub Stars数量"
        />
        <small>当前值: {{ project.stars_count }}（数字类型: {{ typeof project.stars_count }}）</small>
      </div>
      
      <div class="form-group">
        <label for="forks-count">GitHub Forks数量</label>
        <input 
          type="number" 
          id="forks-count" 
          :value="project.forks_count" 
          @input="e => project.forks_count = Number(e.target.value) || 0" 
          min="0" 
          class="form-input"
          placeholder="GitHub Forks数量"
        />
        <small>当前值: {{ project.forks_count }}（数字类型: {{ typeof project.forks_count }}）</small>
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
              class="form-input"
            />
          </div>
          <div class="form-group">
            <label for="tag-slug">标签Slug</label>
            <input 
              type="text" 
              id="tag-slug" 
              v-model="newTag.slug" 
              placeholder="tag-slug"
              class="form-input"
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

    <!-- Markdown帮助弹窗 -->
    <div class="modal" v-if="showHelpModal">
      <div class="modal-content modal-lg">
        <div class="modal-header">
          <h3>Markdown 语法帮助</h3>
          <button class="icon-button" @click="showHelpModal = false">
            <x-icon size="16" />
          </button>
        </div>
        <div class="modal-body markdown-help">
          <div class="help-section">
            <h4>标题</h4>
            <div class="help-item">
              <code># 一级标题</code>
              <code>## 二级标题</code>
              <code>### 三级标题</code>
            </div>
          </div>
          
          <div class="help-section">
            <h4>格式</h4>
            <div class="help-item">
              <code>**粗体文本**</code>
              <code>*斜体文本*</code>
              <code>~~删除线~~</code>
              <code>`行内代码`</code>
            </div>
          </div>
          
          <div class="help-section">
            <h4>列表</h4>
            <div class="help-item">
              <code>- 项目1</code>
              <code>- 项目2</code>
              <code>&nbsp;&nbsp;- 嵌套项目</code>
              <code>1. 有序项目1</code>
              <code>2. 有序项目2</code>
            </div>
          </div>
          
          <div class="help-section">
            <h4>链接与图片</h4>
            <div class="help-item">
              <code>[链接文字](https://example.com)</code>
              <code>![图片描述](https://example.com/image.jpg)</code>
            </div>
          </div>
          
          <div class="help-section">
            <h4>代码块</h4>
            <div class="help-item">
              <pre><code>```javascript
function hello() {
  console.log('Hello');
}
```</code></pre>
            </div>
          </div>
          
          <div class="help-section">
            <h4>引用</h4>
            <div class="help-item">
              <code>> 这是一段引用文本</code>
              <code>> 这是引用的第二行</code>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="primary-button" @click="showHelpModal = false">关闭</button>
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
import { marked } from 'marked';

const router = useRouter();
const route = useRoute();

// 状态
const isEdit = computed(() => !!route.params.id);
// 修改用于存储项目数据的响应式对象，强制指定数字类型
const project = ref<{
  title: string,
  slug: string,
  description: string,
  image_url: string,
  github_url: string,
  live_url: string,
  emoji: string,
  stars_count: number,
  forks_count: number,
  featured: boolean,
  tags: number[]
}>({
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
  tags: []
});
const availableTags = ref<any[]>([]);
const isLoading = ref(false);
const isTagLoading = ref(false);
const error = ref('');
const success = ref('');
const showNewTagModal = ref(false);
const showPreview = ref(false);
const showHelpModal = ref(false);
const newTag = ref({
  name: '',
  slug: ''
});
const descriptionTextarea = ref<HTMLTextAreaElement | null>(null);

// 格式化描述为HTML
const formattedDescription = computed(() => {
  if (!project.value.description) return '<p class="empty-preview">预览区域为空。开始输入内容以查看预览效果。</p>';
  try {
    return marked(project.value.description);
  } catch (e) {
    console.error('格式化内容错误:', e);
    return `<p>${project.value.description}</p>`;
  }
});

// 切换预览
const togglePreview = () => {
  showPreview.value = !showPreview.value;
};

// 插入Markdown语法
const insertMarkdown = (type: string) => {
  if (!descriptionTextarea.value) return;
  
  const textarea = descriptionTextarea.value;
  const start = textarea.selectionStart;
  const end = textarea.selectionEnd;
  const text = textarea.value;
  const selectedText = text.substring(start, end);
  
  let insertion = '';
  let cursorOffset = 0;
  
  switch(type) {
    case 'bold':
      insertion = `**${selectedText || '粗体文本'}**`;
      cursorOffset = selectedText ? 0 : -2;
      break;
    case 'italic':
      insertion = `*${selectedText || '斜体文本'}*`;
      cursorOffset = selectedText ? 0 : -1;
      break;
    case 'heading':
      insertion = `## ${selectedText || '标题'}`;
      cursorOffset = selectedText ? 0 : -0;
      break;
    case 'link':
      insertion = `[${selectedText || '链接文本'}](https://example.com)`;
      cursorOffset = -1;
      break;
    case 'list':
      insertion = `\n- ${selectedText || '列表项'}\n- `;
      cursorOffset = -2;
      break;
    case 'code':
      insertion = selectedText ? `\`\`\`\n${selectedText}\n\`\`\`` : "```\n代码块\n```";
      cursorOffset = selectedText ? 0 : -4;
      break;
    default:
      return;
  }
  
  // 插入文本
  project.value.description = 
    text.substring(0, start) + 
    insertion + 
    text.substring(end);
  
  // 设置光标位置
  setTimeout(() => {
    if (descriptionTextarea.value) {
      descriptionTextarea.value.focus();
      if (cursorOffset < 0) {
        descriptionTextarea.value.selectionStart = 
          descriptionTextarea.value.selectionEnd = 
            start + insertion.length + cursorOffset;
      } else {
        descriptionTextarea.value.selectionStart = 
          descriptionTextarea.value.selectionEnd = 
            start + insertion.length;
      }
    }
  }, 0);
};

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
    
    // 设置项目数据，确保数值正确转换
    project.value = {
      title: projectData.title,
      slug: projectData.slug,
      description: projectData.description,
      image_url: projectData.image_url || '',
      github_url: projectData.github_url || '',
      live_url: projectData.live_url || '',
      emoji: projectData.emoji || '🚀',
      stars_count: Number(projectData.stars_count || 0),
      forks_count: Number(projectData.forks_count || 0),
      featured: projectData.featured || false,
      tags: projectData.tags.map((tag: any) => tag.id)
    };
    
    console.log('加载的项目数据:', project.value);
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
    // 创建一个新对象而非使用JSON序列化，以避免可能的类型转换问题
    const projectToSave = {
      ...project.value,
      // 强制转换为数字
      stars_count: Number(project.value.stars_count || 0),
      forks_count: Number(project.value.forks_count || 0)
    };
    
    console.log('项目数据类型:', {
      stars_count_type: typeof projectToSave.stars_count,
      forks_count_type: typeof projectToSave.forks_count
    });
    
    console.log('保存项目数据:', projectToSave);
    
    let response;
    
    if (isEdit.value) {
      const projectId = Number(route.params.id);
      
      // 首先单独更新项目统计数据
      console.log('先更新项目统计数据...');
      await projectsApi.updateProjectStats(projectId, {
        stars: projectToSave.stars_count,
        forks: projectToSave.forks_count
      });
      
      // 然后更新整个项目
      console.log('再更新整个项目...');
      response = await projectsApi.updateProject(projectId, projectToSave);
    } else {
      // 创建项目
      response = await projectsApi.createProject(projectToSave);
      
      // 如果是新项目，立即更新统计数据
      if (response.data && response.data.id) {
        await projectsApi.updateProjectStats(response.data.id, {
          stars: projectToSave.stars_count,
          forks: projectToSave.forks_count
        });
      }
    }
    
    success.value = isEdit.value ? '项目更新成功' : '项目创建成功';
    
    // 如果是新创建的项目，跳转到编辑页面
    if (!isEdit.value && response.data && response.data.id) {
      setTimeout(() => {
        router.push(`/admin/projects/edit/${response.data.id}`);
      }, 1000);
    } else if (isEdit.value) {
      // 重新加载项目数据以确认更新成功
      await loadProject(Number(route.params.id));
      
      // 验证加载的数据是否正确
      console.log('验证已更新的数据:', {
        stars_count: project.value.stars_count,
        forks_count: project.value.forks_count
      });
    }
  } catch (err: any) {
    console.error('保存项目失败:', err);
    error.value = err.response?.data?.detail || '保存失败，请稍后再试';
    
    // 输出更详细的错误信息以便调试
    if (err.response) {
      console.error('API响应状态码:', err.response.status);
      console.error('API响应数据:', err.response.data);
    }
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

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  font-size: 0.875rem;
}

.form-input:focus,
.form-textarea:focus {
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

.form-group small a {
  color: #3b82f6;
  text-decoration: none;
}

.form-group small a:hover {
  text-decoration: underline;
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

/* Markdown编辑器 */
.markdown-editor-container {
  border: 1px solid #e2e8f0;
  border-radius: 0.375rem;
  overflow: hidden;
}

.markdown-toolbar {
  display: flex;
  padding: 0.5rem;
  border-bottom: 1px solid #e2e8f0;
  background-color: #f8fafc;
  flex-wrap: wrap;
}

.toolbar-button {
  padding: 0.25rem 0.5rem;
  background-color: transparent;
  border: 1px solid #e2e8f0;
  border-radius: 0.25rem;
  color: #64748b;
  cursor: pointer;
  margin-right: 0.25rem;
  font-size: 0.875rem;
}

.toolbar-button:hover {
  background-color: #f1f5f9;
  color: #1e293b;
}

.toolbar-button.active {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.toolbar-divider {
  width: 1px;
  background-color: #e2e8f0;
  margin: 0 0.5rem;
}

.preview-toggle {
  margin-left: auto;
}

.markdown-editor-area {
  position: relative;
  min-height: 300px;
}

.form-textarea {
  width: 100%;
  min-height: 300px;
  padding: 1rem;
  border: none;
  font-family: monospace;
  resize: vertical;
}

.markdown-preview {
  padding: 1rem;
  min-height: 300px;
  max-height: 600px;
  overflow-y: auto;
  color: #1e293b;
  line-height: 1.6;
}

.markdown-preview h1,
.markdown-preview h2,
.markdown-preview h3,
.markdown-preview h4 {
  margin-top: 1.5rem;
  margin-bottom: 1rem;
  color: #1e293b;
}

.markdown-preview h1 {
  font-size: 1.875rem;
}

.markdown-preview h2 {
  font-size: 1.5rem;
}

.markdown-preview h3 {
  font-size: 1.25rem;
}

.markdown-preview p {
  margin-bottom: 1rem;
}

.markdown-preview ul,
.markdown-preview ol {
  margin-bottom: 1rem;
  padding-left: 2rem;
}

.markdown-preview li {
  margin-bottom: 0.25rem;
}

.markdown-preview code {
  background-color: #f1f5f9;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: monospace;
}

.markdown-preview pre code {
  display: block;
  padding: 1rem;
  overflow-x: auto;
  border-radius: 0.375rem;
}

.markdown-preview blockquote {
  border-left: 3px solid #94a3b8;
  padding-left: 1rem;
  color: #64748b;
  margin-left: 0;
  margin-right: 0;
}

.empty-preview {
  color: #94a3b8;
  font-style: italic;
}

/* Markdown帮助 */
.modal-lg {
  max-width: 800px;
}

.markdown-help {
  max-height: 70vh;
  overflow-y: auto;
}

.help-section {
  margin-bottom: 1.5rem;
}

.help-section h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #1e293b;
}

.help-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.help-item code {
  background-color: #f1f5f9;
  padding: 0.5rem;
  border-radius: 0.25rem;
  font-family: monospace;
  white-space: pre-wrap;
}

.help-item pre {
  margin: 0;
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