<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-header">
        <span class="logo-icon">✦</span>
        <h2>管理员登录</h2>
      </div>
      <form @submit.prevent="login">
        <div class="form-group">
          <input v-model="form.username" type="text" placeholder="用户名" class="form-input" />
        </div>
        <div class="form-group">
          <input v-model="form.password" type="password" placeholder="密码" class="form-input" />
        </div>
        <button type="submit" class="btn-login">登录</button>
      </form>
      <div class="tip">默认账号: admin / admin123</div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const form = reactive({ username: '', password: '' })

const login = async () => {
  try {
    await axios.post('/api/login', form)
    ElMessage.success('登录成功')
    window.dispatchEvent(new CustomEvent('login-success'))
    router.push('/')
  } catch (e) {
    ElMessage.error('用户名或密码错误')
  }
}

const logout = async () => {
  await axios.post('/api/logout')
  window.dispatchEvent(new CustomEvent('login-success'))
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 136px);
}

.login-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 48px;
  width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  font-size: 32px;
  color: var(--accent);
  display: block;
  margin-bottom: 12px;
}

.login-header h2 {
  font-family: 'Noto Serif SC', serif;
  font-size: 24px;
  font-weight: 600;
}

.form-group { margin-bottom: 20px; }

.form-input {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  background: var(--bg-primary);
  transition: all 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--accent);
}

.btn-login {
  width: 100%;
  padding: 14px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-login:hover { background: #b89120; }

.tip {
  text-align: center;
  color: var(--text-tertiary);
  font-size: 13px;
  margin-top: 24px;
}
</style>
