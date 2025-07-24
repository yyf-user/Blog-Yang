<template>
  <div class="not-found-container">
    <div class="not-found-content">
      <div class="error-code">404</div>
      <h1 class="error-title">页面未找到</h1>
      <p class="error-message">您访问的页面不存在或已被移除</p>
      <router-link to="/" class="home-button">
        返回首页
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.not-found-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  padding: 2rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
}

.error-code {
  font-size: 8rem;
  font-weight: 800;
  line-height: 1;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
  text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
}

.error-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #f8fafc;
  margin-bottom: 1rem;
}

.error-message {
  font-size: 1.25rem;
  color: #94a3b8;
  margin-bottom: 2rem;
}

.home-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
  color: white;
  text-decoration: none;
  border-radius: 0.5rem;
  font-weight: 600;
  transition: all 0.3s;
}

.home-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.5);
}
</style> 