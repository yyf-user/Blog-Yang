<template>
  <div class="chat-widget">
    <!-- 聊天图标 - 可拖动，限制在边缘 -->
    <div 
      class="chat-button" 
      @mousedown="startDrag"
      v-show="!isOpen"
      :class="{ 'animated': isNavigating }"
      :style="{
        left: position.x + 'px',
        top: position.y + 'px',
        right: 'auto',
        bottom: 'auto'
      }"
    >
      <div class="chat-icon">
        <img src="/jiqiren.png" alt="DeepSeek AI助手" class="chat-icon-image" />
      </div>
      <span class="tooltip">与AI助手对话</span>
    </div>
    
    <!-- 聊天窗口 -->
    <div class="chat-window" v-if="isOpen">
      <!-- 标题栏 -->
      <div class="chat-header" @mousedown="startDragWindow">
        <div class="chat-title">
          <div class="chat-avatar">
            <img src="/jiqiren.png" alt="DeepSeek AI助手" />
          </div>
          <span>DeepSeek AI助手</span>
        </div>
        <div class="chat-actions">
          <button class="minimize-button" @click="minimizeChat">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 13H5V11H19V13Z" fill="currentColor"/>
            </svg>
          </button>
          <button class="close-button" @click="closeChat">
            <span class="close-text">关闭</span>
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 6.41L17.59 5L12 10.59L6.41 5L5 6.41L10.59 12L5 17.59L6.41 19L12 13.41L17.59 19L19 17.59L13.41 12L19 6.41Z" fill="currentColor"/>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- 聊天内容 -->
      <div class="chat-messages" ref="messagesContainer">
        <div class="welcome-message">
          <p>你好！我是 DeepSeek AI 助手，请问有什么我可以帮助你的？</p>
        </div>
        
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
          <div v-if="message.role === 'system'" class="message-content system-message">
            <div class="system-badge">系统</div>
            {{ message.content }}
          </div>
          <div class="message-content" v-else-if="message.role === 'user'">
            {{ message.content }}
          </div>
          <div class="message-content markdown-content" v-else v-html="formatMessage(message.content)"></div>
        </div>
        
        <div v-if="isLoading" class="message assistant">
          <div class="message-content">
            <div class="typing-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 输入区域 -->
      <div class="chat-input">
        <textarea 
          ref="inputField"
          v-model="userInput" 
          placeholder="输入您的问题..." 
          @keydown.enter.prevent="sendMessage"
          :disabled="isLoading"
        ></textarea>
        
        <div class="input-actions">
          <!-- 发送按钮 -->
          <button 
            class="send-button" 
            @click="sendMessage" 
            :disabled="!userInput.trim() || isLoading"
          >
            <span class="send-text">发送</span>
            <svg v-if="!isLoading" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M2.01 21L23 12L2.01 3L2 10L17 12L2 14L2.01 21Z" fill="currentColor"/>
            </svg>
            <div v-else class="spinner"></div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, watch, computed } from 'vue';
import { chatApi } from '@/api';
import { marked } from 'marked';
import hljs from 'highlight.js';
import { useRouter } from 'vue-router';

// 初始化路由
const router = useRouter();

// 状态
const isOpen = ref(false);
const isMinimized = ref(false);
const isLoading = ref(false);
const messages = ref<any[]>([]);
const userInput = ref('');
const messagesContainer = ref<HTMLDivElement | null>(null);
const inputField = ref<HTMLTextAreaElement | null>(null);
const chatWidgetRef = ref<HTMLDivElement | null>(null);
const isNavigating = ref(false); // 导航状态，用于动画

// 图标位置
const position = ref({ x: window.innerWidth - 100, y: window.innerHeight - 100 });
const isDragging = ref(false);
const dragOffset = ref({ x: 0, y: 0 });

// 聊天窗口位置
const windowPosition = ref({ x: window.innerWidth - 400, y: window.innerHeight - 600 });
const isWindowDragging = ref(false);
const windowDragOffset = ref({ x: 0, y: 0 });

// 添加打字机效果控制变量
const isTyping = ref(false);
const typingSpeed = ref(10); // 降低打字速度，更明显的打字效果
const typingQueue = ref<string[]>([]); // 打字队列

// 拖动聊天图标
const startDrag = (event: MouseEvent) => {
  // 如果不是鼠标左键，不处理
  if (event.button !== 0) return;
  
  // 记录开始时间和位置，用于判断是点击还是拖动
  const startTime = new Date().getTime();
  const startPos = { x: event.clientX, y: event.clientY };
  
  isDragging.value = true;
  dragOffset.value = {
    x: event.clientX - position.value.x,
    y: event.clientY - position.value.y
  };

  const handleMouseMove = (moveEvent: MouseEvent) => {
    if (!isDragging.value) return;
    
    let x = moveEvent.clientX - dragOffset.value.x;
    let y = moveEvent.clientY - dragOffset.value.y;
    
    // 边缘检测
    const padding = 20; // 图标到边缘的距离
    const iconSize = 80; // 图标尺寸
    const edgeThreshold = 150; // 定义边缘区域宽度
    
    // 计算窗口尺寸
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    
    // 判断是否在边缘区域
    const isLeftEdge = x < edgeThreshold;
    const isRightEdge = x > windowWidth - edgeThreshold - iconSize;
    const isTopEdge = y < edgeThreshold;
    const isBottomEdge = y > windowHeight - edgeThreshold - iconSize;
    
    // 如果不在任何边缘区域，将其移动到最近的边缘
    if (!isLeftEdge && !isRightEdge && !isTopEdge && !isBottomEdge) {
      // 计算到各边缘的距离
      const distToLeft = x;
      const distToRight = windowWidth - x - iconSize;
      const distToTop = y;
      const distToBottom = windowHeight - y - iconSize;
      
      // 找到最小距离的边缘
      const minDist = Math.min(distToLeft, distToRight, distToTop, distToBottom);
      
      // 移动到最近的边缘
      if (minDist === distToLeft) {
        x = padding;
      } else if (minDist === distToRight) {
        x = windowWidth - iconSize - padding;
      } else if (minDist === distToTop) {
        y = padding;
      } else {
        y = windowHeight - iconSize - padding;
      }
    } else {
      // 确保在边缘区域内不会超出视口
      if (x < padding) {
        x = padding;
      } else if (x > windowWidth - iconSize - padding) {
        x = windowWidth - iconSize - padding;
      }
      
      if (y < padding) {
        y = padding;
      } else if (y > windowHeight - iconSize - padding) {
        y = windowHeight - iconSize - padding;
      }
    }
    
    // 更新位置
    position.value = { x, y };
  };
  
  const handleMouseUp = (upEvent: MouseEvent) => {
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
    
    // 如果时间短且移动距离小，认为是点击
    const endTime = new Date().getTime();
    const endPos = { x: upEvent.clientX, y: upEvent.clientY };
    const timeDiff = endTime - startTime;
    const distanceSq = Math.pow(endPos.x - startPos.x, 2) + Math.pow(endPos.y - startPos.y, 2);
    
    if (timeDiff < 200 && distanceSq < 25) { // 小于200ms且移动距离平方小于25px的平方
      toggleChat();
    }
    
    isDragging.value = false;
    
    // 保存位置到localStorage
    saveIconPosition();
  };
  
  document.addEventListener('mousemove', handleMouseMove);
  document.addEventListener('mouseup', handleMouseUp);
  
  // 阻止默认行为和冒泡
  event.preventDefault();
};

// 保存图标位置
const saveIconPosition = () => {
  try {
    localStorage.setItem('chatIconPosition', JSON.stringify(position.value));
  } catch (error) {
    console.error('保存图标位置失败:', error);
  }
};

// 加载图标位置
const loadIconPosition = () => {
  try {
    const savedPosition = localStorage.getItem('chatIconPosition');
    if (savedPosition) {
      position.value = JSON.parse(savedPosition);
    }
  } catch (error) {
    console.error('加载图标位置失败:', error);
  }
};

// 窗口大小变化时调整图标位置
const handleResize = () => {
  const iconSize = 80;
  const padding = 20;
  
  // 确保图标始终在可视区域内
  if (position.value.x < padding) {
    position.value.x = padding;
  } else if (position.value.x > window.innerWidth - iconSize - padding) {
    position.value.x = window.innerWidth - iconSize - padding;
  }
  
  if (position.value.y < padding) {
    position.value.y = padding;
  } else if (position.value.y > window.innerHeight - iconSize - padding) {
    position.value.y = window.innerHeight - iconSize - padding;
  }
  
  // 确保图标在边缘区域
  const edgeThreshold = 150;
  const x = position.value.x;
  const y = position.value.y;
  const windowWidth = window.innerWidth;
  const windowHeight = window.innerHeight;
  
  const isLeftEdge = x < edgeThreshold;
  const isRightEdge = x > windowWidth - edgeThreshold - iconSize;
  const isTopEdge = y < edgeThreshold;
  const isBottomEdge = y > windowHeight - edgeThreshold - iconSize;
  
  if (!isLeftEdge && !isRightEdge && !isTopEdge && !isBottomEdge) {
    // 如果不在任何边缘，默认放在右下角
    position.value.x = windowWidth - iconSize - padding;
    position.value.y = windowHeight - iconSize - padding;
  }
};

// 拖动聊天窗口
const startDragWindow = (event: MouseEvent) => {
  // 只有点击标题栏时才能拖动
  const target = event.target as HTMLElement;
  if (target.closest('.minimize-button') || target.closest('.close-button')) {
    return;
  }

  isWindowDragging.value = true;
  const chatWindow = document.querySelector('.chat-window') as HTMLElement;
  if (!chatWindow) return;

  windowDragOffset.value = {
    x: event.clientX - chatWindow.getBoundingClientRect().left,
    y: event.clientY - chatWindow.getBoundingClientRect().top
  };

  document.addEventListener('mousemove', handleWindowDrag);
  document.addEventListener('mouseup', stopWindowDrag);
};

const handleWindowDrag = (event: MouseEvent) => {
  if (!isWindowDragging.value) return;

  const chatWindow = document.querySelector('.chat-window') as HTMLElement;
  if (!chatWindow) return;

  let x = event.clientX - windowDragOffset.value.x;
  let y = event.clientY - windowDragOffset.value.y;

  // 限制在窗口内
  const padding = 10;
  if (x < padding) {
    x = padding;
  } else if (x > window.innerWidth - chatWindow.offsetWidth - padding) {
    x = window.innerWidth - chatWindow.offsetWidth - padding;
  }

  if (y < padding) {
    y = padding;
  } else if (y > window.innerHeight - chatWindow.offsetHeight - padding) {
    y = window.innerHeight - chatWindow.offsetHeight - padding;
  }

  chatWindow.style.left = `${x}px`;
  chatWindow.style.top = `${y}px`;
  chatWindow.style.right = 'auto';
  chatWindow.style.bottom = 'auto';
};

const stopWindowDrag = () => {
  isWindowDragging.value = false;
  document.removeEventListener('mousemove', handleWindowDrag);
  document.removeEventListener('mouseup', stopWindowDrag);
};

// 切换聊天窗口
const toggleChat = () => {
  console.log('切换聊天窗口, 当前状态:', isOpen.value);
  isOpen.value = !isOpen.value;
  isMinimized.value = false;
  
  if (isOpen.value) {
    // 加载聊天历史
    loadChatHistory();
    
    nextTick(() => {
      if (inputField.value) {
        inputField.value.focus();
      }
      scrollToBottom();
    });
  }
};

// 最小化聊天窗口
const minimizeChat = () => {
  isMinimized.value = true;
  isOpen.value = false;
};

// 关闭聊天窗口
const closeChat = () => {
  isOpen.value = false;
  
  // 保存聊天历史
  saveChatHistory();
};

// 打开聊天窗口
const openChat = () => {
  isOpen.value = true;
  isMinimized.value = false;
  
  // 聊天窗口打开后，将焦点放到输入框
  setTimeout(() => {
    if (inputField.value) {
      inputField.value.focus();
    }
  }, 100);
  
  // 添加调试消息
  console.log('聊天窗口已打开');
  
  // 调试: 测试直接访问/api/chat端点
  console.log('测试直接访问/api/chat端点');
  fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      messages: [{ role: 'user', content: '你好' }] 
    })
  })
  .then(r => r.json())
  .then(d => console.log('测试结果:', d))
  .catch(e => console.error('测试错误:', e));
};

// 发送消息
const sendMessage = async () => {
  const content = userInput.value.trim();
  if (!content || isLoading.value) return;
  
  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: content
  });
  
  // 清空输入框并滚动到底部
  userInput.value = '';
  await nextTick();
  scrollToBottom();
  
  // 显示加载状态
  isLoading.value = true;
  
  try {
    // 准备请求消息
    const requestMessages = messages.value
      .filter(msg => msg.role !== 'system') // 过滤掉系统消息
      .map(msg => ({ 
        role: msg.role, 
        content: msg.content 
    }));
    
    // 使用流式传输获取响应
    await streamChatResponse(requestMessages);
  } catch (error) {
    console.error('聊天请求失败:', error);
    messages.value.push({
      role: 'assistant',
      content: '抱歉，发生了错误，请稍后再试。'
    });
  } finally {
    // 确保即使在错误情况下也会重置加载状态
    isLoading.value = false;
    // 无论成功或失败，确保保存聊天历史
    saveChatHistory();
    scrollToBottom();
  }
};

// 流式获取聊天响应 - 完全重写此函数以修复流式输出
const streamChatResponse = async (requestMessages: any[]) => {
  try {
    console.log('开始请求流式响应');
    isLoading.value = true;
    
    // 创建请求选项
    const options: any = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'text/event-stream',
      },
      body: JSON.stringify({ messages: requestMessages }),
    };
    
    // 添加认证令牌(如果有)
    const token = localStorage.getItem('token');
    if (token) {
      options.headers['Authorization'] = `Bearer ${token}`;
    }
    
    // 发送请求
    console.log('发送请求到:', chatApi.getChatStreamUrl());
    const response = await fetch(chatApi.getChatStreamUrl(), options);
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`HTTP错误! 状态: ${response.status}`, errorText);
      throw new Error(`请求失败 (${response.status}): ${errorText || '未知错误'}`);
    }
    
    console.log('收到响应，开始处理流式数据');
    
    // 添加助手消息
    const assistantMessage = {
      role: 'assistant',
      content: ''
    };
    messages.value.push(assistantMessage);
    
    // 清空之前的队列
    typingQueue.value = [];
    isTyping.value = false;
    
    // 处理SSE流
    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('无法读取响应流');
    }
    
    // 解码器
    const decoder = new TextDecoder();
    
    // 处理打字效果
    const processTyping = () => {
      if (typingQueue.value.length === 0) {
        if (!isTyping.value) {
          // 如果队列为空且不在打字中，检查是否已完成
          if (assistantMessage.content.length > 0) {
            // 流处理完成
            isLoading.value = false;
          }
        }
        return;
      }
      
      if (!isTyping.value) {
        typeNextChunk();
      }
    };
    
    // 打字效果函数
    const typeNextChunk = async () => {
      if (typingQueue.value.length === 0) {
        isTyping.value = false;
        return;
      }
      
      isTyping.value = true;
      const char = typingQueue.value.shift() || '';
      
      // 添加字符到消息内容
      assistantMessage.content += char;
      
      // 滚动到底部
      await nextTick();
      scrollToBottom();
      
      // 设置延迟以实现打字效果
      setTimeout(() => {
        isTyping.value = false;
        typeNextChunk();
      }, typingSpeed.value);
    };
    
    // 开始流处理
    let buffer = '';
    const pump = async () => {
      try {
        const { done, value } = await reader.read();
        
        if (done) {
          console.log('流式读取完成');
          // 确保队列中的内容都已处理
          if (typingQueue.value.length === 0 && !isTyping.value) {
            isLoading.value = false;
          }
          return;
        }
        
        // 解码数据并处理
        const text = decoder.decode(value, { stream: true });
        buffer += text;
        
        // 解析所有完整的SSE消息行
        const lines = buffer.split('\n');
        buffer = lines.pop() || ''; // 保留最后一个不完整的行
        
        for (const line of lines) {
          if (line.trim() === '') continue;
          
          // 处理错误
          if (line.includes('event: error')) {
            const errorMessage = line.replace(/^event: error\s*data: /, '');
            console.error('SSE错误:', errorMessage);
            continue;
          }
          
          // 处理结束信号
          if (line.includes('data: [DONE]')) {
            console.log('收到结束标记');
            continue;
          }
          
          // 处理普通数据行
          if (line.startsWith('data:')) {
            const content = line.substring(5).trim(); // 跳过 "data: "
            if (content) {
              console.log('收到内容片段:', content);
              // 将每个字符添加到打字队列
              for (const char of content) {
                typingQueue.value.push(char);
              }
            }
          }
        }
        
        // 如果还没有开始打字，开始处理打字队列
        if (!isTyping.value) {
          processTyping();
        }
        
        // 继续泵取数据
        return pump();
      } catch (error) {
        console.error('处理流时出错:', error);
        isLoading.value = false;
        throw error;
      }
    };
    
    // 启动数据泵
    await pump();
    
  } catch (error) {
    console.error('流式响应处理错误:', error);
    isLoading.value = false;
    throw error;
  }
};

// 格式化消息内容（支持Markdown和代码高亮）
const formatMessage = (content: string) => {
  if (!content) return '';
  
  try {
    // 设置marked选项
    marked.setOptions({
      highlight: function(code, lang) {
        if (lang && hljs.getLanguage(lang)) {
          return hljs.highlight(code, { language: lang }).value;
        }
        return hljs.highlightAuto(code).value;
      },
      breaks: true
    });
    
    // 使用marked解析Markdown
    return marked(content);
  } catch (error) {
    console.error('Markdown解析错误:', error);
    return content;
  }
};

// 滚动到对话底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
  }
};

// 加载聊天历史
const loadChatHistory = () => {
  try {
    const history = localStorage.getItem('chatHistory');
    if (history) {
      messages.value = JSON.parse(history);
    }
  } catch (error) {
    console.error('加载聊天历史失败:', error);
  }
};

// 保存聊天历史
const saveChatHistory = () => {
  try {
    localStorage.setItem('chatHistory', JSON.stringify(messages.value));
  } catch (error) {
    console.error('保存聊天历史失败:', error);
  }
};

// 生命周期钩子
onMounted(() => {
  console.log("聊天组件已加载");
  
  // 设置默认位置在右下角，确保聊天窗口默认是关闭的
  const defaultPosition = { 
    x: window.innerWidth - 100, 
    y: window.innerHeight - 100 
  };
  
  // 尝试从localStorage加载上次保存的位置
  loadIconPosition();
  
  // 强制设置为关闭状态
  isOpen.value = false;
  isMinimized.value = false;
  
  // 确保加载历史记录
  loadChatHistory();
  
  // 确保位置合理
  handleResize();

  // 监听窗口大小变化
  window.addEventListener('resize', handleResize);
  
  // 添加调试消息
  console.log('ChatWidget组件已挂载', position.value);
});

onUnmounted(() => {
  // 保存窗口状态
  localStorage.setItem('chatWidgetState', JSON.stringify({
    isOpen: isOpen.value,
    isMinimized: isMinimized.value
  }));
  
  // 保存图标位置
  saveIconPosition();

  // 移除窗口大小变化监听
  window.removeEventListener('resize', handleResize);
});

// 监听消息变化，自动滚动
watch(
  () => messages.value.length,
  () => {
    nextTick(() => {
      scrollToBottom();
    });
  }
);
</script>

<style>
.chat-widget {
  position: fixed;
  z-index: 9999;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  pointer-events: none;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
}

.chat-button {
  position: absolute;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #ff3366;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  z-index: 10000;
  cursor: pointer;
  border: 4px solid #ffffff;
  animation: pulse 2s infinite;
  pointer-events: auto;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 4px 30px rgba(255, 51, 102, 0.8);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
  }
}

.chat-button:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.4);
}

.chat-button:hover .tooltip {
  opacity: 1;
  transform: translateY(0);
}

.chat-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-icon img.chat-icon-image {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;
  filter: brightness(1.2) contrast(1.1) drop-shadow(0 0 3px rgba(0, 0, 0, 0.5));
}

.tooltip {
  position: absolute;
  top: -40px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 14px;
  opacity: 0;
  transform: translateY(5px);
  transition: all 0.2s ease;
  white-space: nowrap;
}

.chat-window {
  position: fixed;
  width: 380px;
  height: 550px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  animation: slideUp 0.3s ease forwards;
  z-index: 10000;
  right: 20px;
  bottom: 20px;
  pointer-events: auto;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.chat-header {
  background: linear-gradient(135deg, #0066FF, #0099FF);
  color: white;
  padding: 12px 15px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: move; /* 指示可拖动 */
}

.chat-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 500;
}

.chat-avatar {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.chat-avatar img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.chat-actions {
  display: flex;
  gap: 10px;
}

.minimize-button {
  background: transparent;
  border: none;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0.8;
  transition: opacity 0.2s;
  cursor: pointer;
}

.minimize-button:hover {
  opacity: 1;
}

.close-button {
  background: #ff3366;
  border: 2px solid white;
  padding: 0 10px;
  height: 28px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 1;
  transition: all 0.2s;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  gap: 4px;
}

.close-text {
  font-size: 12px;
  font-weight: bold;
}

.close-button svg {
  width: 16px;
  height: 16px;
}

.close-button:hover {
  opacity: 1;
  background: #ff1a4d;
  transform: scale(1.05);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
  background-color: #f8fafc;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.welcome-message {
  background-color: rgba(0, 102, 255, 0.1);
  padding: 12px;
  border-radius: 10px;
  border-top-left-radius: 0;
  align-self: flex-start;
  max-width: 80%;
}

.welcome-message p {
  margin: 0;
  color: #374151;
  font-size: 14px;
  line-height: 1.5;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 80%;
}

.message.user {
  align-self: flex-end;
}

.message.assistant {
  align-self: flex-start;
}

.message-content {
  padding: 12px;
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.5;
  overflow-wrap: break-word;
}

.user .message-content {
  background: #0066FF;
  color: white;
  border-top-right-radius: 0;
}

.assistant .message-content {
  background: white;
  color: #374151;
  border: 1px solid #e5e7eb;
  border-top-left-radius: 0;
}

/* 代码块样式 */
.assistant .message-content :deep(pre) {
  background: #1e293b;
  color: #e2e8f0;
  border-radius: 6px;
  padding: 12px;
  overflow-x: auto;
  margin: 10px 0;
}

.assistant .message-content :deep(code) {
  font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}

.assistant .message-content :deep(p) {
  margin: 0.5em 0;
}

.assistant .message-content :deep(ul), 
.assistant .message-content :deep(ol) {
  padding-left: 20px;
}

.typing-indicator {
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #0066FF;
  border-radius: 50%;
  display: block;
  opacity: 0.6;
  animation: typing 1s infinite;
}

.typing-indicator span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-indicator span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes typing {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-5px);
  }
}

.chat-input {
  padding: 10px;
  display: flex;
  gap: 10px;
  background: white;
  border-top: 1px solid #e5e7eb;
}

textarea {
  flex: 1;
  resize: none;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 10px;
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
  height: 40px;
  max-height: 100px;
}

textarea:focus {
  border-color: #0066FF;
}

.input-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.send-button {
  min-width: 80px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0066FF;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  transition: background 0.2s;
  gap: 5px;
  padding: 0 15px;
}

.send-text {
  font-size: 14px;
  font-weight: 500;
}

.send-button svg {
  width: 18px;
  height: 18px;
}

.send-button:hover:not(:disabled) {
  background: #0052cc;
}

.send-button:disabled {
  background: #94a3b8;
  cursor: not-allowed;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.system-message {
  background-color: rgba(0, 102, 255, 0.05) !important;
  color: #666 !important;
  font-style: italic;
  padding: 8px !important;
  border-radius: 8px !important;
  border: none !important;
  position: relative;
}

.system-badge {
  position: absolute;
  top: -8px;
  left: 8px;
  background-color: #0066ff;
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 10px;
  font-weight: bold;
}

/* 响应式样式 */
@media (max-width: 480px) {
  .chat-window {
    width: 90%;
    height: 80%;
    max-width: none;
    max-height: none;
    left: 5% !important;
    right: 5% !important;
    top: 10% !important;
    bottom: 10% !important;
    border-radius: 10px;
  }
}

/* 导航动画 */
.chat-button.animated {
  animation: bounce 1s infinite alternate, spin 2s infinite linear;
}

@keyframes bounce {
  0% {
    transform: translateY(0);
  }
  100% {
    transform: translateY(-20px);
  }
}
</style> 