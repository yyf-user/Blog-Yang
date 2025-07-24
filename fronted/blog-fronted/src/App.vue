<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import ChatWidget from './components/chat/ChatWidget.vue'
import { onMounted, ref, nextTick } from 'vue'

const appMounted = ref(false);
const chatWidgetRef = ref<InstanceType<typeof ChatWidget> | null>(null);

// 确保组件在挂载后可见
onMounted(() => {
  console.log('应用已挂载，ChatWidget组件应该可见')
  appMounted.value = true;

  // 确保组件渲染
  nextTick(() => {
    console.log('应用挂载后的nextTick执行')
    
    // 强制重新检查DOM
    setTimeout(() => {
      const chatButton = document.querySelector('.chat-button');
      console.log('聊天按钮元素:', chatButton);
    }, 100);
  });
})
</script>

<template>
  <div class="app-container">
    <div class="fixed-background"></div>
    <router-view />
    
    <!-- 渲染聊天组件 -->
    <div class="chat-container">
      <ChatWidget ref="chatWidgetRef" />
    </div>
  </div>
</template>

<style>
/* 全局样式已在main.css中定义 */
.app-container {
  position: relative;
  min-height: 100vh;
}

.fixed-background {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('@/assets/images/background.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  z-index: -1;
}

.chat-container {
  position: fixed;
  bottom: 0;
  right: 0;
  z-index: 10000;
  pointer-events: none;
  width: 100%;
  height: 100%;
}
</style>
