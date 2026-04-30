<template>
  <div class="question-detail">
    <div class="detail-header">
      <button class="back-btn" @click="$router.back()">← 返回</button>
    </div>
    
    <div class="detail-content">
      <div class="detail-title">{{ question.title }}</div>
      <div class="detail-meta">
        <span class="meta-tag type">{{ question.type }}</span>
        <span class="meta-tag category">{{ question.category }}</span>
        <span class="meta-tag importance" :class="'imp-' + question.importance">
          {{ importanceLabel(question.importance) }}
        </span>
        <span class="meta-tag archived" v-if="question.is_archived">已归档</span>
      </div>
      
      <div class="answer-section">
        <h3>答案</h3>
        <div class="markdown-body" v-html="renderedAnswer"></div>
      </div>
      
      <div class="detail-actions" v-if="isAdmin">
        <button class="btn-edit" @click="editQuestion">编辑</button>
        <button class="btn-archive" @click="toggleArchive">
          {{ question.is_archived ? '取消归档' : '归档' }}
        </button>
        <button class="btn-delete" @click="deleteQuestion">删除</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const question = ref({})
const isAdmin = ref(false)

const importanceLabel = (val) => ({ 3: '高', 2: '中', 1: '低' }[val] || '')

const renderedAnswer = computed(() => {
  if (!question.value.answer) return '暂无答案'
  return marked(question.value.answer)
})

const loadQuestion = async () => {
  const res = await axios.get(`/api/questions/${route.params.id}`)
  question.value = res.data
}

const checkLogin = async () => {
  try {
    const res = await axios.get('/api/current-user')
    isAdmin.value = res.data.is_admin
  } catch (e) { isAdmin.value = false }
}

const editQuestion = () => {
  router.push({ path: '/question/edit', query: { id: question.value.id } })
}

const toggleArchive = async () => {
  await axios.post(`/api/questions/${question.value.id}/archive`)
  ElMessage.success('归档状态已更新')
  loadQuestion()
}

const deleteQuestion = async () => {
  await ElMessageBox.confirm('确定删除此题？', '提示', { type: 'warning' })
  await axios.delete(`/api/questions/${question.value.id}`)
  ElMessage.success('删除成功')
  router.push('/')
}

onMounted(() => { loadQuestion(); checkLogin() })
</script>

<style scoped>
.question-detail { max-width: 900px; margin: 0 auto; }

.detail-header { margin-bottom: 24px; }

.back-btn {
  background: none;
  border: none;
  color: var(--accent);
  font-size: 14px;
  cursor: pointer;
  padding: 8px 0;
}

.back-btn:hover { opacity: 0.7; }

.detail-content {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 40px;
}

.detail-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
}

.detail-meta { display: flex; gap: 10px; margin-bottom: 32px; flex-wrap: wrap; }

.meta-tag {
  font-size: 13px;
  padding: 6px 14px;
  border-radius: 8px;
}

.meta-tag.type { background: #e8f5e9; color: #2e7d32; }
.meta-tag.category { background: #e3f2fd; color: #1565c0; }
.meta-tag.importance.imp-3 { background: #c62828; color: #fff; }
.meta-tag.importance.imp-2 { background: #ef6c00; color: #fff; }
.meta-tag.importance.imp-1 { background: #5e35b1; color: #fff; }
.meta-tag.archived { background: #eceff1; color: #546e7a; }

.answer-section { margin-bottom: 32px; }

.answer-section h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--text-secondary);
}

.answer-section pre {
  background: var(--bg-tertiary);
  padding: 24px;
  border-radius: 12px;
  white-space: pre-wrap;
  line-height: 1.8;
  font-size: 15px;
}

.markdown-body {
  background: var(--bg-tertiary);
  padding: 24px;
  border-radius: 12px;
  line-height: 1.8;
  font-size: 15px;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin-top: 20px;
  margin-bottom: 12px;
  font-weight: 600;
}

.markdown-body :deep(p) {
  margin-bottom: 12px;
}

.markdown-body :deep(code) {
  background: #e5e5e5;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
}

.markdown-body :deep(pre) {
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 24px;
  margin-bottom: 12px;
}

.markdown-body :deep(li) {
  margin-bottom: 6px;
}

.markdown-body :deep(blockquote) {
  border-left: 4px solid var(--accent);
  padding-left: 16px;
  color: var(--text-secondary);
  margin: 12px 0;
}

.detail-actions { display: flex; gap: 12px; padding-top: 24px; border-top: 1px solid var(--border); }

.btn-edit, .btn-archive, .btn-delete {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  border: none;
}

.btn-edit { background: var(--bg-tertiary); color: var(--text-primary); }
.btn-archive { background: #e3f2fd; color: #1565c0; }
.btn-delete { background: #ffebee; color: #c62828; }
</style>
