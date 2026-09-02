<template>
  <div class="app-wrapper">
    <header class="app-header">
      <div class="header-inner">
        <div class="logo">
          <span class="logo-icon">◈</span>
          <span class="logo-text">CryptoView</span>
          <span class="logo-badge">模拟演示</span>
        </div>
        <div class="header-right">
          <span class="header-disclaimer">所有数据均为模拟生成</span>
        </div>
      </div>
    </header>
    <main class="app-main">
      <Dashboard />
    </main>
  </div>
</template>

<script setup>
import Dashboard from './views/Dashboard.vue'
</script>

<style scoped>
.app-wrapper {
  min-height: 100vh;
  background: var(--bg-primary);
}

.app-header {
  background: linear-gradient(180deg, #0d1525 0%, var(--bg-primary) 100%);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.header-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 14px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-icon {
  font-size: 24px;
  color: var(--accent-cyan);
  text-shadow: 0 0 10px rgba(0, 212, 255, 0.5);
}

.logo-text {
  font-size: 20px;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.logo-badge {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 4px;
  background: rgba(255, 214, 0, 0.15);
  color: var(--accent-yellow);
  border: 1px solid rgba(255, 214, 0, 0.3);
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-disclaimer {
  font-size: 11px;
  color: var(--text-secondary);
  padding: 4px 10px;
  border: 1px solid rgba(255, 23, 68, 0.2);
  border-radius: 4px;
  background: rgba(255, 23, 68, 0.05);
}

.app-main {
  min-height: calc(100vh - 60px);
}
</style>
