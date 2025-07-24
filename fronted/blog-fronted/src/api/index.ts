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

// 增强API请求日志记录

// 添加更详细的请求拦截器
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    // 添加详细的请求日志
    console.log(`🚀 API请求: ${config.method?.toUpperCase()} ${config.url}`, {
      params: config.params,
      data: config.data,
      headers: config.headers
    });
    
    return config;
  },
  (error) => {
    console.error('❌ API请求错误:', error);
    return Promise.reject(error);
  }
);

// 添加更详细的响应拦截器
api.interceptors.response.use(
  (response) => {
    // 记录成功的响应
    console.log(`✅ API响应: ${response.config.method?.toUpperCase()} ${response.config.url}`, {
      status: response.status,
      data: response.data,
      headers: response.headers
    });
    
    return response;
  },
  (error) => {
    console.error('❌ API响应错误:', error);
    
    // 记录详细的错误信息
    if (error.response) {
      console.error(`API错误响应 [${error.response.status}]:`, {
        url: error.config.url,
        method: error.config.method?.toUpperCase(),
        params: error.config.params,
        data: error.config.data,
        responseData: error.response.data,
        headers: error.response.headers
      });
      
      switch (error.response.status) {
        case 401:
          // 未授权，可能需要重新登录
          console.error('认证失效，需要重新登录');
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
      console.error('未收到响应，请检查网络连接', {
        url: error.config.url,
        method: error.config.method?.toUpperCase(),
        params: error.config.params,
        data: error.config.data
      });
    } else {
      console.error('请求配置错误:', error.message);
    }
    
    return Promise.reject(error);
  }
);

// 修改文章API中获取文章的逻辑，增加更多日志和兼容性处理
export const articlesApi = {
  // 获取文章列表
  getArticles: (params: any = {}) => {
    // 确保使用正确的分页参数名称
    const apiParams = { ...params };
    
    // 将前端的skip参数转换为后端的skip参数(如果存在)
    if (apiParams.skip !== undefined) {
      // 已经是skip，不需要转换
      console.log(`使用分页参数: skip=${apiParams.skip}, limit=${apiParams.limit}`);
    }
    
    // 确保标签参数名称正确 - 尝试多种可能的参数名
    if (apiParams.tag_id !== undefined) {
      // 设置多种可能的标签参数以增加兼容性
      apiParams.tag = apiParams.tag_id;
      apiParams.tag_id = apiParams.tag_id;
      apiParams.tags = apiParams.tag_id;
      console.log(`设置标签筛选参数: tag=${apiParams.tag}, tag_id=${apiParams.tag_id}, tags=${apiParams.tags}`);
    }
    
    console.log('📊 获取文章列表，完整参数:', apiParams);
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

// 为项目API添加更强的数字类型保障，确保Stars和Forks参数正确传递

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
  getProject: (id: number) => {
    return api.get(`/projects/${id}`).then(response => {
      // 在返回响应前确保数字字段被正确处理
      if (response.data) {
        // 确保数值字段为数字
        response.data.stars_count = Number(response.data.stars_count || 0);
        response.data.forks_count = Number(response.data.forks_count || 0);
        
        console.log('处理后的项目数据:', {
          id: response.data.id,
          title: response.data.title,
          stars: response.data.stars_count,
          stars_type: typeof response.data.stars_count,
          forks: response.data.forks_count,
          forks_type: typeof response.data.forks_count
        });
      }
      
      return response;
    });
  },
  
  // 获取项目详情(通过slug)
  getProjectBySlug: (slug: string) => {
    return api.get(`/projects/by-slug/${slug}`).then(response => {
      // 在返回响应前确保数字字段被正确处理
      if (response.data) {
        // 确保数值字段为数字
        response.data.stars_count = Number(response.data.stars_count || 0);
        response.data.forks_count = Number(response.data.forks_count || 0);
        
        console.log('处理后的项目数据 (slug):', {
          id: response.data.id,
          title: response.data.title,
          stars: response.data.stars_count,
          stars_type: typeof response.data.stars_count,
          forks: response.data.forks_count,
          forks_type: typeof response.data.forks_count
        });
      }
      
      return response;
    });
  },
  
  // 创建项目
  createProject: (data: any) => {
    // 确保数字字段是数字类型
    const projectData = { ...data };
    projectData.stars_count = Number(projectData.stars_count || 0);
    projectData.forks_count = Number(projectData.forks_count || 0);
    
    console.log('创建项目，数据:', projectData);
    return api.post('/projects', projectData);
  },
  
  // 更新项目
  updateProject: (id: number, data: any) => {
    // 创建一个新对象，避免修改原始数据
    const projectData = { ...data };
    
    // 确保数字字段为数字类型（使用显式的Number转换）
    projectData.stars_count = Number(projectData.stars_count || 0);
    projectData.forks_count = Number(projectData.forks_count || 0);
    
    // 打印完整调试信息
    console.log(`📊 更新项目数据 [ID: ${id}]:`, {
      title: projectData.title,
      stars_count: {
        value: projectData.stars_count,
        type: typeof projectData.stars_count
      },
      forks_count: {
        value: projectData.forks_count,
        type: typeof projectData.forks_count
      }
    });
    
    // 直接向API发送原始值以及显示转换后的值（作为调试参考）
    console.log('更新项目API调用参数对照:');
    console.log('1. 原始参数:', JSON.stringify({
      stars_count: data.stars_count,
      forks_count: data.forks_count
    }));
    console.log('2. 转换后参数:', JSON.stringify({
      stars_count: projectData.stars_count,
      forks_count: projectData.forks_count
    }));
    
    // 增加双重保障，确保数字参数作为数字发送
    const queryParams = new URLSearchParams();
    queryParams.append('ensure_numbers', 'true');
    
    return api.put(`/projects/${id}?${queryParams.toString()}`, projectData);
  },
  
  // 更新项目统计信息 - 单独接口
  updateProjectStats: (id: number, stats: { stars?: number, forks?: number }) => {
    // 确保传入的是数字
    const statsData = { 
      stars: Number(stats.stars || 0),
      forks: Number(stats.forks || 0)
    };
    
    console.log(`📈 更新项目统计 [ID: ${id}]:`, {
      stars: {
        value: statsData.stars,
        type: typeof statsData.stars
      },
      forks: {
        value: statsData.forks,
        type: typeof statsData.forks
      }
    });
    
    // 创建特定的请求参数
    const requestData = {
      ...statsData,
      _numeric: true // 给后端一个提示，表示这些值应该作为数字处理
    };
    
    // 以多种格式发送，增加与后端兼容性
    const payload = {
      ...requestData,
      stars_count: statsData.stars, // 尝试不同的字段名
      forks_count: statsData.forks,
      starCount: statsData.stars,
      forkCount: statsData.forks
    };
    
    // 直接将整数作为字符串路径参数传递
    const queryParams = new URLSearchParams();
    queryParams.append('stars', String(statsData.stars));
    queryParams.append('forks', String(statsData.forks));
    
    // 使用查询参数，确保数字值正确传递
    return api.put(`/projects/${id}/stats?${queryParams.toString()}`, payload);
  },
  
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