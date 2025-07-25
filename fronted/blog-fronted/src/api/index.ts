import axios from 'axios';
import type { AxiosResponse } from 'axios';

// 修改API基础URL，使其能够适配Docker环境和开发环境
const baseURL = import.meta.env.PROD 
  ? '/api' // 生产环境通过Nginx代理
  : 'http://localhost:8001/api'; // 开发环境更新端口为8001

// 创建一个axios实例
const api = axios.create({
  baseURL,
  timeout: 15000, // 15秒超时
  headers: {
    'Content-Type': 'application/json',
  },
});

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 从localStorage获取token
    const token = localStorage.getItem('token');
    // 如果有token则添加到请求头
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      const { status } = error.response;

      // 身份验证错误
      if (status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        // 如果在登录页面则不跳转
        if (window.location.pathname !== '/login') {
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// 文件上传基础URL
export const uploadBaseURL = import.meta.env.PROD 
  ? '/uploads' // 生产环境通过Nginx代理
  : 'http://localhost:8000/uploads'; // 开发环境

// 以下是API服务

// 用户相关API
export const usersApi = {
  // 登录
  login: (data: { username: string; password: string }): Promise<AxiosResponse> =>
    api.post('/auth/login', data),

  // 注册
  register: (data: any): Promise<AxiosResponse> =>
    api.post('/users', data),

  // 获取当前用户信息
  getCurrentUser: (): Promise<AxiosResponse> =>
    api.get('/users/me'),

  // 更新用户信息
  updateUser: (data: any): Promise<AxiosResponse> =>
    api.put(`/users/me`, data),

  // 更新用户头像
  updateAvatar: (formData: FormData): Promise<AxiosResponse> =>
    api.post('/users/avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }),
};

// 文章相关API
export const articlesApi = {
  // 获取文章列表
  getArticles: (params?: any): Promise<AxiosResponse> =>
    api.get('/articles', { params }),

  // 获取文章详情
  getArticle: (id: number): Promise<AxiosResponse> =>
    api.get(`/articles/${id}`),

  // 获取文章详情（通过slug）
  getArticleBySlug: (slug: string): Promise<AxiosResponse> =>
    api.get(`/articles/slug/${slug}`),

  // 创建文章
  createArticle: (data: any): Promise<AxiosResponse> =>
    api.post('/articles', data),

  // 更新文章
  updateArticle: (id: number, data: any): Promise<AxiosResponse> =>
    api.put(`/articles/${id}`, data),

  // 删除文章
  deleteArticle: (id: number): Promise<AxiosResponse> =>
    api.delete(`/articles/${id}`),

  // 上传文章图片
  uploadImage: (formData: FormData): Promise<AxiosResponse> =>
    api.post('/articles/upload-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }),
};

// 标签相关API
export const tagsApi = {
  // 获取所有标签
  getTags: (): Promise<AxiosResponse> =>
    api.get('/tags'),

  // 创建标签
  createTag: (data: { name: string }): Promise<AxiosResponse> =>
    api.post('/tags', data),

  // 更新标签
  updateTag: (id: number, data: { name: string }): Promise<AxiosResponse> =>
    api.put(`/tags/${id}`, data),

  // 删除标签
  deleteTag: (id: number): Promise<AxiosResponse> =>
    api.delete(`/tags/${id}`),

  // 获取指定标签下的文章
  getArticlesByTag: (slug: string): Promise<AxiosResponse> =>
    api.get(`/tags/slug/${slug}/articles`),
};

// 项目相关API
export const projectsApi = {
  // 获取项目列表
  getProjects: (params?: any): Promise<AxiosResponse> =>
    api.get('/projects', { params }),

  // 获取项目详情
  getProject: (id: number): Promise<AxiosResponse> =>
    api.get(`/projects/${id}`),

  // 获取项目详情（通过slug）
  getProjectBySlug: (slug: string): Promise<AxiosResponse> =>
    api.get(`/projects/slug/${slug}`),

  // 创建项目
  createProject: (data: any): Promise<AxiosResponse> => {
    // 确保数字字段是数字类型
    if (data.stars_count !== undefined) {
      data.stars_count = Number(data.stars_count);
    }
    if (data.forks_count !== undefined) {
      data.forks_count = Number(data.forks_count);
    }
    return api.post('/projects', data);
  },

  // 更新项目
  updateProject: (id: number, data: any): Promise<AxiosResponse> => {
    // 确保数字字段是数字类型
    if (data.stars_count !== undefined) {
      data.stars_count = Number(data.stars_count);
    }
    if (data.forks_count !== undefined) {
      data.forks_count = Number(data.forks_count);
    }
    return api.put(`/projects/${id}`, data);
  },

  // 更新项目统计数据
  updateProjectStats: (id: number, stats: { stars: number; forks: number }): Promise<AxiosResponse> => {
    const data = {
      stars: Number(stats.stars),
      forks: Number(stats.forks)
    };
    return api.put(`/projects/${id}/stats`, data);
  },

  // 删除项目
  deleteProject: (id: number): Promise<AxiosResponse> =>
    api.delete(`/projects/${id}`),

  // 获取指定标签下的项目
  getProjectsByTag: (slug: string, limit?: number): Promise<AxiosResponse> => {
    const params = limit ? { limit } : {};
    return api.get(`/tags/slug/${slug}/projects`, { params });
  },
};

// 消息相关API
export const messagesApi = {
  // 获取消息列表
  getMessages: (params?: any): Promise<AxiosResponse> =>
    api.get('/messages', { params }),

  // 获取消息详情
  getMessage: (id: number): Promise<AxiosResponse> =>
    api.get(`/messages/${id}`),

  // 创建消息
  createMessage: (data: any): Promise<AxiosResponse> =>
    api.post('/messages', data),

  // 更新消息状态
  updateMessageStatus: (id: number, status: string): Promise<AxiosResponse> =>
    api.put(`/messages/${id}/status`, { status }),

  // 删除消息
  deleteMessage: (id: number): Promise<AxiosResponse> =>
    api.delete(`/messages/${id}`),
};

// 聊天相关API
export const chatApi = {
  // 发送消息
  sendMessage: (message: string): Promise<AxiosResponse> =>
    api.post('/chat/message', { message }),

  // 获取会话历史
  getChatHistory: (): Promise<AxiosResponse> =>
    api.get('/chat/history'),
    
  // 获取聊天流URL
  getChatStreamUrl: (): string => {
    return `${baseURL}/chat/stream`;
  }
};

// 统计相关API
export const statsApi = {
  // 获取网站统计信息
  getStats: (): Promise<AxiosResponse> =>
    api.get('/stats'),
  
  // 获取API路径统计
  getApiStats: (params?: any): Promise<AxiosResponse> =>
    api.get('/stats/api-paths', { params }),
};

// 订阅相关API
export const subscribersApi = {
  // 创建订阅
  createSubscriber: (data: { email: string }): Promise<AxiosResponse> =>
    api.post('/subscribers', data),

  // 获取所有订阅者
  getSubscribers: (): Promise<AxiosResponse> =>
    api.get('/subscribers'),

  // 删除订阅者
  deleteSubscriber: (id: number): Promise<AxiosResponse> =>
    api.delete(`/subscribers/${id}`),
};

// 技能相关API
export const skillsApi = {
  // 获取所有技能
  getSkills: (): Promise<AxiosResponse> =>
    api.get('/skills'),

  // 创建技能
  createSkill: (data: any): Promise<AxiosResponse> =>
    api.post('/skills', data),

  // 更新技能
  updateSkill: (id: number, data: any): Promise<AxiosResponse> =>
    api.put(`/skills/${id}`, data),

  // 删除技能
  deleteSkill: (id: number): Promise<AxiosResponse> =>
    api.delete(`/skills/${id}`),
};

export default api; 