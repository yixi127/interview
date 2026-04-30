<template>
  <div id="app">
    <header class="app-header">
      <div class="header-inner">
        <div class="logo" @click="$router.push('/')">
          <span class="logo-icon">✦</span>
          <span class="logo-text">面试题库</span>
        </div>
        <nav class="main-nav">
          <a class="nav-link active" href="/">题库</a>
          <a class="nav-link admin-only" href="/import" v-if="isAdmin">导入</a>
          <a class="nav-link admin-only" href="/categories" v-if="isAdmin">分类</a>
          <a class="nav-link" href="/login" v-if="!isAdmin">登录</a>
          <span class="nav-user" v-else>
            <span class="user-badge">ADMIN</span>
            <a class="nav-link" @click="logout">退出</a>
          </span>
        </nav>
      </div>
    </header>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const isAdmin = ref(false)

const checkLogin = async () => {
  try {
    const res = await axios.get('/api/current-user')
    isAdmin.value = res.data.is_admin
  } catch (e) {
    isAdmin.value = false
  }
}

const logout = async () => {
  await axios.post('/api/logout')
  window.dispatchEvent(new CustomEvent('login-success'))
  router.push('/')
}

const handleLoginSuccess = () => {
  checkLogin()
}

onMounted(() => {
  checkLogin()
  window.addEventListener('login-success', handleLoginSuccess)
})

onUnmounted(() => {
  window.removeEventListener('login-success', handleLoginSuccess)
})
</script>

<style>
:root {
  --bg-primary: #faf9f7;
  --bg-secondary: #fff;
  --bg-tertiary: #f5f3f0;
  --text-primary: #1a1a1a;
  --text-secondary: #5a5a5a;
  --text-tertiary: #8a8a8a;
  --accent: #c9a227;
  --accent-light: #f5efe0;
  --border: #e5e2dd;
  --shadow: rgba(0,0,0,0.04);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Noto Sans SC', sans-serif;
  background: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.6;
}

#app {
  min-height: 100vh;
}

.app-header {
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 32px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.7;
}

.logo-icon {
  font-size: 24px;
  color: var(--accent);
}

.logo-text {
  font-family: 'Noto Serif SC', serif;
  font-size: 22px;
  font-weight: 600;
  letter-spacing: 2px;
}

.main-nav {
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav-link {
  text-decoration: none;
  color: var(--text-secondary);
  font-size: 14px;
  font-weight: 500;
  letter-spacing: 0.5px;
  padding: 8px 0;
  position: relative;
  transition: color 0.2s;
  cursor: pointer;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--accent);
  transition: width 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  color: var(--text-primary);
}

.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}

.admin-only {
  color: var(--accent);
}

.user-badge {
  background: var(--accent-light);
  color: var(--accent);
  font-size: 11px;
  font-weight: 600;
  padding: 4px 10px;
  border-radius: 4px;
  margin-right: 16px;
  letter-spacing: 1px;
}

.nav-user {
  display: flex;
  align-items: center;
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px;
}
</style>
