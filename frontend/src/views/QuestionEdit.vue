<template>
  <div class="question-edit">
    <div class="edit-header">
      <button class="back-btn" @click="$router.back()">← 返回</button>
      <h2 class="page-title">{{ isEdit ? '编辑题目' : '添加题目' }}</h2>
    </div>

    <div class="edit-form">
      <div class="form-group">
        <label>题目内容 *</label>
        <textarea v-model="form.title" class="form-textarea" rows="3" placeholder="请输入题目"></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>类型 *</label>
          <select v-model="form.type" class="form-select">
            <option value="八股">八股</option>
            <option value="算法">算法</option>
          </select>
        </div>

        <div class="form-group">
          <label>分类 *</label>
          <select v-model="form.category" class="form-select">
            <option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.name" />
          </select>
        </div>

        <div class="form-group">
          <label>重要程度 *</label>
          <select v-model="form.importance" class="form-select">
            <option :value="3">高</option>
            <option :value="2">中</option>
            <option :value="1">低</option>
          </select>
        </div>
      </div>

      <div class="form-group">
        <label>答案</label>
        <textarea v-model="form.answer" class="form-textarea" rows="8" placeholder="请输入答案"></textarea>
      </div>

      <div class="form-actions">
        <button class="btn-secondary" @click="$router.back()">取消</button>
        <button class="btn-primary" @click="saveQuestion">保存</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.query.id)

const categories = ref([])
const form = reactive({
  title: '',
  type: '八股',
  category: '',
  importance: 2,
  answer: ''
})

const loadCategories = async () => {
  const res = await axios.get('/api/categories')
  categories.value = res.data
  if (categories.value.length) form.category = categories.value[0].name
}

const loadQuestion = async () => {
  if (route.query.id) {
    const res = await axios.get(`/api/questions/${route.query.id}`)
    Object.assign(form, res.data)
  }
}

const saveQuestion = async () => {
  if (!form.title) { ElMessage.warning('请输入题目'); return }
  if (isEdit.value) {
    await axios.put(`/api/questions/${route.query.id}`, form)
    ElMessage.success('更新成功')
    router.push(`/question/${route.query.id}`)
  } else {
    await axios.post('/api/questions', form)
    ElMessage.success('添加成功')
    router.push('/')
  }
}

onMounted(() => { loadCategories(); loadQuestion() })
</script>

<style scoped>
.question-edit { max-width: 800px; margin: 0 auto; }

.edit-header { margin-bottom: 32px; }

.back-btn {
  background: none;
  border: none;
  color: var(--accent);
  font-size: 14px;
  cursor: pointer;
  padding: 8px 0;
  margin-bottom: 16px;
}

.page-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 28px;
  font-weight: 600;
}

.edit-form {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 32px;
}

.form-group { margin-bottom: 24px; }
.form-group label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 8px; }

.form-textarea {
  width: 100%;
  padding: 14px 16px;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 15px;
  background: var(--bg-primary);
  resize: vertical;
}

.form-textarea:focus { outline: none; border-color: var(--accent); }

.form-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }

.form-select {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  background: var(--bg-primary);
}

.form-actions { display: flex; gap: 12px; justify-content: flex-end; margin-top: 32px; }

.btn-primary, .btn-secondary {
  padding: 12px 32px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  border: none;
}

.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: #b89120; }
.btn-secondary { background: var(--bg-tertiary); color: var(--text-secondary); }
</style>
