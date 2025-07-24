<template>
  <div class="tech-background">
    <div class="grid"></div>
    <div class="gradient-overlay"></div>
  </div>
</template>

<style scoped>
.tech-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  background-color: #0f172a;
  overflow: hidden;
}

.grid {
  position: absolute;
  width: 200%;
  height: 200%;
  top: -50%;
  left: -50%;
  background-image: 
    linear-gradient(rgba(59, 130, 246, 0.1) 1px, transparent 1px),
    linear-gradient(90deg, rgba(59, 130, 246, 0.1) 1px, transparent 1px);
  background-size: 40px 40px;
  transform: perspective(500px) rotateX(30deg);
  animation: grid-move 60s linear infinite;
}

.gradient-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 30%, rgba(59, 130, 246, 0.1), transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(99, 102, 241, 0.1), transparent 40%);
}

@keyframes grid-move {
  0% {
    transform: perspective(500px) rotateX(30deg) translateY(0);
  }
  100% {
    transform: perspective(500px) rotateX(30deg) translateY(40px);
  }
}
</style> 