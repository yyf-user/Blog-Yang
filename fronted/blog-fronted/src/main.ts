import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 动态设置favicon
import logoSvg from './assets/logo.svg'
const link = document.querySelector("link[rel~='icon']") as HTMLLinkElement
if (link) {
  link.href = logoSvg
} else {
  const newLink = document.createElement('link')
  newLink.rel = 'icon'
  newLink.href = logoSvg
  document.head.appendChild(newLink)
}

// 创建Vue应用实例
const app = createApp(App)
app.use(createPinia())
app.use(router)

// 确保DOM完全加载后立即挂载应用
console.log('准备挂载Vue应用')

// 即使DOMContentLoaded事件已经触发，这个函数也会被调用
function mountApp() {
  console.log('DOM已加载，立即挂载Vue应用')
  app.mount('#app')
  console.log('Vue应用挂载完成')
}

// 如果DOM已经加载完成，立即挂载
if (document.readyState === 'loading') {
  // 如果DOM仍在加载中，等待DOMContentLoaded事件
  document.addEventListener('DOMContentLoaded', mountApp)
} else {
  // 如果DOM已加载完成，立即挂载
  mountApp()
}
