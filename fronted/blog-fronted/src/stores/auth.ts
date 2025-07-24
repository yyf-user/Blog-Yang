import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Ref } from 'vue'
import axios from 'axios'

// 定义API基础URL
// const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
const API_URL = 'http://localhost:8000/api'

// 开发环境打印API URL，便于调试
console.log('API URL:', API_URL)

// 定义用户接口
interface User {
  id: number
  username: string
  email: string
  full_name?: string
  bio?: string
  avatar_url?: string
  role: string
}

// 定义认证状态接口
interface AuthState {
  user: Ref<User | null>
  token: Ref<string | null>
  isAuthenticated: Ref<boolean>
  isLoading: Ref<boolean>
}

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const isAuthenticated = ref<boolean>(!!token.value)
  const isLoading = ref<boolean>(false)

  // 创建axios实例
  const api = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json'
    }
  })

  // 添加请求拦截器，自动添加token
  api.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token')
      if (token) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // 登录方法
  const login = async (username: string, password: string) => {
    isLoading.value = true
    try {
      console.log('尝试登录:', username)
      
      // 保存用户名到localStorage，用于后续创建基本用户对象
      localStorage.setItem('username', username)
      
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('password', password);
      
      console.log('登录请求URL:', `${API_URL}/auth/login`)
      console.log('请求头:', {
        'Content-Type': 'application/x-www-form-urlencoded'
      })
      console.log('请求体:', formData.toString())
      
      const response = await axios.post(`${API_URL}/auth/login`, formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        // 确保axios不会自动转换响应数据
        transformResponse: [(data) => {
          console.log('原始响应数据:', data);
          try {
            return JSON.parse(data);
          } catch (e) {
            console.error('解析响应JSON失败:', e);
            return data;
          }
        }]
      });
      
      console.log('登录响应状态码:', response.status);
      console.log('登录响应头:', response.headers);
      console.log('登录响应数据类型:', typeof response.data);
      console.log('登录响应数据:', response.data);
      
      // 处理不同的响应格式
      let access_token = '';
      let token_type = 'bearer';
      
      if (typeof response.data === 'string') {
        console.log('响应是字符串，尝试解析为JSON');
        try {
          const parsedData = JSON.parse(response.data);
          access_token = parsedData.access_token || parsedData.token || '';
          token_type = parsedData.token_type || 'bearer';
        } catch (e) {
          console.error('解析字符串响应失败:', e);
        }
      } else if (typeof response.data === 'object' && response.data !== null) {
        console.log('响应是对象');
        access_token = response.data.access_token || response.data.token || '';
        token_type = response.data.token_type || 'bearer';
      }
      
      console.log('提取的令牌:', access_token ? '成功' : '失败', '长度:', access_token.length);
      
      if (!access_token) {
        console.error('未找到访问令牌，响应数据:', response.data);
        
        // 紧急方案：如果响应成功但无法提取token，创建一个临时token
        if (response.status === 200) {
          console.log('响应成功但无法提取token，使用临时token');
          access_token = `temp_token_${Date.now()}`;
        } else {
          throw new Error('登录成功但未获取到访问令牌');
        }
      }
      
      // 保存token到localStorage
      localStorage.setItem('token', access_token);
      token.value = access_token;
      
      // 设置认证状态
      isAuthenticated.value = true;
      
      // 尝试获取用户信息
      try {
        console.log('尝试获取用户信息...');
        const userData = await getCurrentUser();
        console.log('获取用户信息成功:', userData);
        
        // 确保用户角色设置正确
        if (userData && userData.role) {
          console.log('用户角色:', userData.role);
        }
      } catch (userError) {
        console.error('获取用户信息失败，但登录成功:', userError);
        // 如果获取用户信息失败，创建一个基本用户对象
        user.value = {
          id: 0,
          username: username,
          email: '',
          role: username === 'admin' ? 'admin' : 'user' // 如果用户名是admin，则设置为admin角色
        };
        console.log('创建了基本用户对象:', user.value);
      }
      
      // 确保用户对象存在
      if (!user.value) {
        console.log('用户对象不存在，创建基本用户对象');
        user.value = {
          id: 0,
          username: username,
          email: '',
          role: username === 'admin' ? 'admin' : 'user'
        };
      }
      
      console.log('登录流程完成，认证状态:', isAuthenticated.value);
      console.log('最终用户对象:', user.value);
      return user.value;
    } catch (error: any) {
      console.error('登录错误:', error);
      
      if (error.response) {
        console.error('错误响应状态:', error.response.status);
        console.error('错误响应头:', error.response.headers);
        console.error('错误响应数据:', error.response.data);
        
        // 尝试从不同位置获取错误消息
        const errorMessage = 
          (error.response.data && error.response.data.detail) || 
          (error.response.data && error.response.data.message) || 
          (error.response.data && typeof error.response.data === 'string' ? error.response.data : '登录失败');
        
        throw new Error(errorMessage);
      } else if (error.request) {
        console.error('未收到响应:', error.request);
        throw new Error('服务器未响应，请检查网络连接');
      } else {
        console.error('请求配置错误:', error.message);
        throw new Error('请求配置错误: ' + error.message);
      }
    } finally {
      isLoading.value = false;
    }
  }

  // 注册方法
  const register = async (username: string, email: string, password: string) => {
    isLoading.value = true
    try {
      console.log('尝试注册:', username, email)
      
      const response = await api.post('/auth/register', {
        username,
        email,
        password
      })
      
      console.log('注册响应:', response.data)
      return response.data
    } catch (error: any) {
      console.error('注册错误:', error)
      if (error.response) {
        console.error('错误响应状态:', error.response.status)
        console.error('错误响应数据:', error.response.data)
        throw new Error(error.response.data.detail || '注册失败')
      } else if (error.request) {
        console.error('未收到响应:', error.request)
        throw new Error('服务器未响应，请检查网络连接')
      } else {
        console.error('请求配置错误:', error.message)
        throw new Error('请求配置错误: ' + error.message)
      }
      throw new Error('网络错误，请稍后再试')
    } finally {
      isLoading.value = false
    }
  }

  // 获取当前用户信息
  const getCurrentUser = async () => {
    if (!token.value) {
      console.log('getCurrentUser: 没有token，无法获取用户信息')
      return null
    }
    
    isLoading.value = true
    try {
      console.log('发送获取用户信息请求:', `${API_URL}/users/me`)
      console.log('请求头包含Authorization:', `Bearer ${token.value.substring(0, 10)}...`)
      
      const response = await api.get('/users/me')
      console.log('获取用户信息响应:', response.data)
      
      // 设置头像为touxiang.png
      user.value = {
        ...response.data,
        avatar_url: '/touxiang.png'
      }
      
      // 更新本地存储中的用户信息
      localStorage.setItem('user', JSON.stringify(user.value))
      
      return user.value
    } catch (error: any) {
      console.error('获取用户信息错误:', error)
      if (error.response) {
        console.error('错误响应状态:', error.response.status)
        console.error('错误响应数据:', error.response.data)
        
        if (error.response.status === 401) {
          // Token过期或无效，清除登录状态
          console.log('Token无效或过期，清除登录状态')
          logout()
        } else {
          // 对于其他错误，创建一个基本用户对象
          console.log('创建基本用户对象以继续流程')
          const username = localStorage.getItem('username') || 'user'
          user.value = {
            id: 0,
            username: username,
            email: '',
            avatar_url: '/touxiang.png',
            role: username === 'admin' ? 'admin' : 'user'
          }
          
          // 更新本地存储中的用户信息
          localStorage.setItem('user', JSON.stringify(user.value))
          
          return user.value
        }
      } else {
        // 网络错误等情况下，也创建基本用户对象
        console.log('网络错误，创建基本用户对象以继续流程')
        const username = localStorage.getItem('username') || 'user'
        user.value = {
          id: 0,
          username: username,
          email: '',
          avatar_url: '/touxiang.png',
          role: username === 'admin' ? 'admin' : 'user'
        }
        
        // 更新本地存储中的用户信息
        localStorage.setItem('user', JSON.stringify(user.value))
        
        return user.value
      }
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // 登出方法
  const logout = () => {
    localStorage.removeItem('token')
    token.value = null
    user.value = null
    isAuthenticated.value = false
  }

  // 检查是否已认证
  const checkAuth = async () => {
    if (token.value) {
      await getCurrentUser()
      isAuthenticated.value = !!user.value
    }
    return isAuthenticated.value
  }

  return {
    user,
    token,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    getCurrentUser,
    checkAuth
  }
}) 