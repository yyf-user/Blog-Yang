import axios from 'axios';

// API基础URL
const API_URL = 'http://localhost:8000/api';

// 创建axios实例
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 添加请求拦截器，自动添加token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器，统一处理错误
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API请求错误:', error);
    
    // 处理特定错误状态码
    if (error.response) {
      switch (error.response.status) {
        case 401:
          // 未授权，可能需要重新登录
          localStorage.removeItem('token');
          break;
        case 403:
          // 禁止访问
          console.error('无权限访问此资源');
          break;
        case 500:
          console.error('服务器内部错误');
          break;
        default:
          console.error(`HTTP错误 ${error.response.status}: ${error.response.data.detail || '未知错误'}`);
      }
    } else if (error.request) {
      console.error('未收到响应，请检查网络连接');
    } else {
      console.error('请求配置错误:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// 文章相关API
export const articlesApi = {
  // 获取文章列表
  getArticles: (params: any = {}) => {
    // 确保使用正确的分页参数名称
    const apiParams = { ...params };
    
    // 将前端的skip参数转换为后端的skip参数(如果存在)
    if (apiParams.skip !== undefined) {
      // 已经是skip，不需要转换
    }
    
    // 确保其他过滤参数正确
    if (apiParams.tag && typeof apiParams.tag === 'number') {
      // 如果tag是ID，需要查找对应的slug
      // 这里暂时保持不变，如果后端API接受ID直接查询，则不需要处理
    }
    
    console.log('获取文章列表，参数:', apiParams);
    return api.get('/articles', { params: apiParams });
  },
  
  // 获取文章详情
  getArticle: (id: number) => api.get(`/articles/${id}`),
  
  // 获取文章详情(通过slug)
  getArticleBySlug: (slug: string) => api.get(`/articles/by-slug/${slug}`),
  
  // 创建文章
  createArticle: (data: any) => api.post('/articles', data),
  
  // 更新文章
  updateArticle: (id: number, data: any) => api.put(`/articles/${id}`, data),
  
  // 发布/取消发布文章
  publishArticle: (id: number, status: string) => api.put(`/articles/${id}/publish`, { status }),
  
  // 删除文章
  deleteArticle: (id: number) => api.delete(`/articles/${id}`)
};

// 项目相关API
export const projectsApi = {
  // 获取项目列表
  getProjects: (params: any = {}) => {
    // 确保使用正确的分页参数名称
    const apiParams = { ...params };
    
    // 将前端的skip参数转换为后端的skip参数(如果存在)
    if (apiParams.skip !== undefined) {
      // 已经是skip，不需要转换
    }
    
    return api.get('/projects', { params: apiParams });
  },
  
  // 按标签获取项目
  getProjectsByTag: (tag: string, limit: number = 10) => {
    return api.get('/projects', { params: { tag, limit } });
  },
  
  // 获取项目详情
  getProject: (id: number) => api.get(`/projects/${id}`),
  
  // 获取项目详情(通过slug)
  getProjectBySlug: (slug: string) => api.get(`/projects/by-slug/${slug}`),
  
  // 创建项目
  createProject: (data: any) => api.post('/projects', data),
  
  // 更新项目
  updateProject: (id: number, data: any) => api.put(`/projects/${id}`, data),
  
  // 更新项目统计信息
  updateProjectStats: (id: number, stats: { stars?: number, forks?: number }) => 
    api.put(`/projects/${id}/stats`, stats),
  
  // 删除项目
  deleteProject: (id: number) => api.delete(`/projects/${id}`)
};

// 标签相关API
export const tagsApi = {
  // 获取标签列表
  getTags: (params: any = {}) => api.get('/tags', { params }),
  
  // 获取标签详情
  getTag: (id: number) => api.get(`/tags/${id}`),
  
  // 创建标签
  createTag: (data: { name: string, slug?: string }) => api.post('/tags', data),
  
  // 删除标签
  deleteTag: (id: number) => api.delete(`/tags/${id}`)
};

// 消息相关API
export const messagesApi = {
  // 获取消息列表
  getMessages: (params: any = {}) => {
    console.log('获取消息列表，参数:', params);
    return api.get('/messages', { params });
  },
  
  // 获取消息详情
  getMessage: (id: number) => api.get(`/messages/${id}`),
  
  // 创建消息(联系表单)
  createMessage: (data: { name: string, email: string, subject: string, message: string }) => {
    console.log('创建消息:', data);
    return api.post('/messages', data);
  },
  
  // 更新消息(标记已读)
  updateMessage: (id: number, data: { is_read: boolean }) => api.put(`/messages/${id}`, data),
  
  // 删除消息
  deleteMessage: (id: number) => api.delete(`/messages/${id}`)
};

// 用户相关API
export const usersApi = {
  // 获取当前用户信息
  getCurrentUser: () => api.get('/users/me'),
  
  // 更新用户信息
  updateUser: (data: any) => api.put('/users/me', data),
  
  // 更新用户密码
  updatePassword: (data: { current_password: string, new_password: string }) => 
    api.put('/users/me/password', data)
};

// 统计相关API
export const statsApi = {
  // 获取统计信息
  getStats: () => api.get('/stats'),
  
  // 获取API调用统计信息
  getApiStats: () => api.get('/stats/api'),
  
  // 获取最近一周的API调用趋势
  getApiTrends: () => api.get('/stats/api/trends'),
  
  // 获取特定API的调用详情
  getApiDetail: (endpoint: string) => api.get(`/stats/api/${endpoint}`)
};

// DeepSeek聊天API
export const chatApi = {
  // 发送消息（非流式）
  sendMessage: (messages: any[]) => {
    return api.post('/chat/message', { messages });
  },
  
  // 获取聊天流URL
  getChatStreamUrl: () => {
    return `${API_URL}/chat/stream`;
  }
};

export default api; 