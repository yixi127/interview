<template>
  <div class="home">
    <div class="home-layout">
      <aside class="sidebar">
        <div class="sidebar-header">
          <span class="sidebar-title">分类</span>
        </div>
        
        <div class="category-list">
          <div class="category-item" :class="{ active: !selectedCategory }" @click="selectCategory('')">
            <span class="cat-icon">◈</span>
            <span class="cat-name">全部题目</span>
            <span class="cat-count">{{ totalCount }}</span>
          </div>
          
          <div class="category-group" v-for="type in categoryGroups" :key="type.name">
            <div class="group-title">{{ type.name }}</div>
            <div v-for="cat in type.categories" :key="cat.id" class="category-item" :class="{ active: selectedCategory === cat.name }" @click="selectCategory(cat.name)">
              <span class="cat-icon">▸</span>
              <span class="cat-name">{{ cat.name }}</span>
              <span class="cat-count">{{ getCount(cat.name) }}</span>
            </div>
          </div>
        </div>
      </aside>
      
      <main class="content">
        <div class="content-header">
          <div class="header-left">
            <h2 class="page-title">{{ selectedCategory || '全部题目' }}</h2>
            <span class="page-subtitle">共 {{ totalItems }} 道题目</span>
          </div>
          
          <div class="header-right">
            <div class="filter-bar">
              <input 
                v-model="filters.search" 
                type="text" 
                placeholder="搜索题目..." 
                class="search-input"
                @keyup.enter="loadQuestions"
              />
              <select v-model="filters.type" @change="loadQuestions" class="filter-select">
                <option value="">全部类型</option>
                <option value="八股">八股</option>
                <option value="算法">算法</option>
                <option value="代码">代码</option>
              </select>
              <select v-model="filters.importance" @change="loadQuestions" class="filter-select">
                <option value="">重要程度</option>
                <option :value="3">高</option>
                <option :value="2">中</option>
                <option :value="1">低</option>
              </select>
            </div>
            
            <div class="action-bar" v-if="isAdmin">
              <button class="btn-secondary" @click="toggleArchived">{{ showArchived ? '未归档' : '已归档' }}</button>
              <button class="btn-secondary" @click="showExport = true">导出</button>
              <button class="btn-primary" @click="$router.push('/question/edit')">+ 添加题目</button>
            </div>
          </div>
        </div>
        
        <div class="questions-list">
          <div v-if="questions.length === 0" class="empty-state">
            <div class="empty-icon">◇</div>
            <p>暂无题目</p>
            <button class="btn-primary" v-if="isAdmin" @click="$router.push('/question/edit')">添加第一道题</button>
          </div>
          
          <div v-else>
            <div v-for="q in questions" :key="q.id" class="question-card">
              <div class="question-main" @click="viewQuestion(q)">
                <div class="question-title">{{ q.title }}</div>
                <div class="question-meta">
                  <span class="meta-tag type">{{ q.type }}</span>
                  <span class="meta-tag category">{{ q.category }}</span>
                  <span class="meta-tag importance" :class="'imp-' + q.importance">{{ importanceLabel(q.importance) }}</span>
                  <span class="meta-tag archived" v-if="q.is_archived">已归档</span>
                </div>
              </div>
              <div class="question-actions" v-if="isAdmin">
                <button class="action-btn" @click="editQuestion(q)">编辑</button>
                <button class="action-btn" @click="toggleArchive(q)">{{ q.is_archived ? '解档' : '归档' }}</button>
                <button class="action-btn danger" @click="deleteQuestion(q)">删除</button>
              </div>
            </div>
            
            <div class="pagination-wrapper">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[10, 20, 50, 100]"
                :total="totalItems"
                layout="total, sizes, prev, pager, next, jumper"
                @size-change="handleSizeChange"
                @current-change="handlePageChange"
              />
            </div>
          </div>
        </div>
      </main>
    </div>

    <el-dialog v-model="showExport" title="导出Markdown" width="500px">
      <el-form :model="exportForm" label-width="80px">
        <el-form-item label="导出范围">
          <el-select v-model="exportForm.scope" placeholder="选择范围">
            <el-option label="当前显示题目" value="current" />
            <el-option label="已归档题目" value="archived" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型" v-if="exportForm.scope === 'archived'">
          <el-select v-model="exportForm.type" placeholder="全部">
            <el-option label="全部" value="all" />
            <el-option label="八股" value="八股" />
            <el-option label="算法" value="算法" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showExport = false">取消</el-button>
        <el-button type="primary" @click="exportMarkdown">下载</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const router = useRouter()
const questions = ref([])
const categories = ref([])
const isAdmin = ref(false)
const showExport = ref(false)
const showArchived = ref(false)
const selectedCategory = ref('')

const filters = reactive({ type: '', importance: '', search: '' })
const exportForm = reactive({ scope: 'current', type: 'all', category: '' })

const currentPage = ref(1)
const totalPages = ref(1)
const totalItems = ref(0)
const pageSize = ref(20)

const totalCount = computed(() => totalItems.value)
const importanceLabel = (val) => ({ 3: '高', 2: '中', 1: '低' }[val] || '')

const categoryGroups = computed(() => {
  const groups = {}
  categories.value.forEach(cat => {
    if (!groups[cat.type]) groups[cat.type] = { name: cat.type, categories: [] }
    groups[cat.type].categories.push(cat)
  })
  return Object.values(groups)
})

const categoryCounts = ref({})
const getCount = (catName) => categoryCounts.value[catName] || 0

const loadCategoryCounts = async () => {
  try {
    const res = await axios.get('/api/questions', { params: { archived: '0', per_page: 9999 } })
    const data = res.data
    const items = data.items || data
    const counts = {}
    items.forEach(q => { counts[q.category] = (counts[q.category] || 0) + 1 })
    categoryCounts.value = counts
  } catch (e) {}
}

const selectCategory = (catName) => { selectedCategory.value = catName; currentPage.value = 1; loadQuestions() }

const loadQuestions = async () => {
  const params = { 
    archived: showArchived.value ? '1' : '0',
    page: currentPage.value,
    per_page: pageSize.value
  }
  if (filters.type) params.type = filters.type
  if (filters.importance) params.importance = filters.importance
  if (filters.search) params.search = filters.search
  if (selectedCategory.value) params.category = selectedCategory.value
  
  const res = await axios.get('/api/questions', { params })
  const data = res.data
  if (data.items) {
    questions.value = data.items
    totalPages.value = data.pages
    totalItems.value = data.total
  } else {
    questions.value = data
    totalPages.value = 1
    totalItems.value = data.length
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadQuestions()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  loadQuestions()
}

const loadCategories = async () => { categories.value = (await axios.get('/api/categories')).data }

const checkLogin = async () => { isAdmin.value = (await axios.get('/api/current-user')).data.is_admin }

watch([() => filters.type, () => filters.importance, () => filters.search], () => {
  currentPage.value = 1
  loadQuestions()
})

const viewQuestion = (q) => router.push(`/question/${q.id}`)
const editQuestion = (q) => router.push({ path: '/question/edit', query: { id: q.id } })

const toggleArchive = async (q) => {
  await axios.post(`/api/questions/${q.id}/archive`)
  ElMessage.success('归档状态已更新')
  loadQuestions()
}

const deleteQuestion = async (q) => {
  await ElMessageBox.confirm('确定删除此题？', '提示', { type: 'warning' })
  await axios.delete(`/api/questions/${q.id}`)
  ElMessage.success('删除成功')
  loadQuestions()
}

const toggleArchived = () => { showArchived.value = !showArchived.value; loadQuestions() }

const exportMarkdown = async () => {
  let content = ''
  let filename = ''
  
  if (exportForm.scope === 'current') {
    content = '# 当前题目导出\n\n'
    const importanceLabels = { 3: '[高]', 2: '[中]', 1: '[低]' }
    
    const byCategory = {}
    questions.value.forEach(q => {
      if (!byCategory[q.category]) byCategory[q.category] = []
      byCategory[q.category].push(q)
    })
    
    for (const cat in byCategory) {
      content += `## ${cat}\n\n`
      byCategory[cat].forEach(q => {
        content += `### ${importanceLabels[q.importance]} ${q.title}\n\n`
        if (q.answer) content += `${q.answer}\n\n`
        content += '---\n\n'
      })
    }
    filename = `interview_current_${Date.now()}.md`
  } else {
    const params = { type: exportForm.type }
    const res = await axios.get('/api/export', { params })
    content = res.data.content
    filename = `interview_archived_${Date.now()}.md`
  }
  
  const blob = new Blob([content], { type: 'text/markdown' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = filename
  a.click()
  showExport.value = false
  ElMessage.success('导出成功')
}

onMounted(() => { loadCategories(); loadQuestions(); loadCategoryCounts(); checkLogin() })
</script>

<style scoped>
.home { min-height: calc(100vh - 136px); }
.home-layout { display: grid; grid-template-columns: 260px 1fr; gap: 32px; }

.sidebar { background: var(--bg-secondary); border-radius: 12px; padding: 24px 0; height: fit-content; position: sticky; top: 104px; border: 1px solid var(--border); }
.sidebar-header { padding: 0 24px 20px; border-bottom: 1px solid var(--border); margin-bottom: 16px; }
.sidebar-title { font-family: 'Noto Serif SC', serif; font-size: 14px; font-weight: 600; color: var(--text-tertiary); letter-spacing: 2px; text-transform: uppercase; }
.category-list { padding: 0 12px; }
.category-group { margin-top: 20px; }
.group-title { font-size: 11px; font-weight: 600; color: var(--text-tertiary); letter-spacing: 1.5px; text-transform: uppercase; padding: 0 12px; margin-bottom: 8px; }
.category-item { display: flex; align-items: center; gap: 10px; padding: 12px 16px; border-radius: 8px; cursor: pointer; transition: all 0.2s ease; margin-bottom: 4px; }
.category-item:hover { background: var(--bg-tertiary); }
.category-item.active { background: var(--accent-light); color: var(--accent); }
.cat-icon { font-size: 10px; color: var(--text-tertiary); }
.category-item.active .cat-icon { color: var(--accent); }
.cat-name { flex: 1; font-size: 14px; font-weight: 500; }
.cat-count { font-size: 12px; color: var(--text-tertiary); background: var(--bg-tertiary); padding: 2px 8px; border-radius: 10px; }

.content { min-height: calc(100vh - 136px); }
.content-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
.page-title { font-family: 'Noto Serif SC', serif; font-size: 28px; font-weight: 600; color: var(--text-primary); margin-bottom: 4px; }
.page-subtitle { font-size: 14px; color: var(--text-tertiary); }
.header-right { display: flex; align-items: center; gap: 16px; }
.filter-bar { display: flex; gap: 12px; }
.filter-select { padding: 10px 16px; border: 1px solid var(--border); border-radius: 8px; font-size: 14px; background: var(--bg-secondary); color: var(--text-secondary); cursor: pointer; }
.search-input { padding: 10px 16px; border: 1px solid var(--border); border-radius: 8px; font-size: 14px; background: var(--bg-secondary); width: 180px; }
.search-input:focus { outline: none; border-color: var(--accent); }
.action-bar { display: flex; gap: 12px; }

.btn-primary { padding: 10px 20px; background: var(--accent); color: #fff; border: none; border-radius: 8px; font-size: 14px; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.btn-primary:hover { background: #b89120; transform: translateY(-1px); }
.btn-secondary { padding: 10px 20px; background: var(--bg-secondary); color: var(--text-secondary); border: 1px solid var(--border); border-radius: 8px; font-size: 14px; cursor: pointer; transition: all 0.2s; }
.btn-secondary:hover { border-color: var(--text-tertiary); color: var(--text-primary); }

.questions-list { display: flex; flex-direction: column; gap: 16px; }
.question-card { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 12px; padding: 24px; transition: all 0.2s ease; }
.question-card:hover { border-color: var(--accent); box-shadow: 0 4px 20px var(--shadow); transform: translateY(-2px); }
.question-main { margin-bottom: 16px; cursor: pointer; }
.question-title { font-size: 16px; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; line-height: 1.6; }
.question-meta { display: flex; gap: 8px; flex-wrap: wrap; }

.meta-tag { font-size: 12px; padding: 4px 12px; border-radius: 6px; font-weight: 500; }
.meta-tag.type { background: #e8f5e9; color: #2e7d32; }
.meta-tag.category { background: #e3f2fd; color: #1565c0; }
.meta-tag.importance.imp-3 { background: #c62828; color: #fff; }
.meta-tag.importance.imp-2 { background: #ef6c00; color: #fff; }
.meta-tag.importance.imp-1 { background: #5e35b1; color: #fff; }
.meta-tag.archived { background: #eceff1; color: #546e7a; }

.question-actions { display: flex; gap: 8px; padding-top: 16px; border-top: 1px solid var(--border); }
.action-btn { padding: 8px 16px; background: var(--bg-tertiary); border: none; border-radius: 6px; font-size: 13px; cursor: pointer; transition: all 0.2s; }
.action-btn:hover { background: var(--border); }
.action-btn.danger { color: #c62828; }
.action-btn.danger:hover { background: #ffebee; }

.empty-state { text-align: center; padding: 80px 20px; background: var(--bg-secondary); border: 1px dashed var(--border); border-radius: 12px; }
.empty-icon { font-size: 48px; color: var(--text-tertiary); margin-bottom: 16px; }
.empty-state p { color: var(--text-secondary); margin-bottom: 24px; }

.pagination-wrapper { display: flex; justify-content: center; padding: 24px 0; }
.pagination-wrapper :deep(.el-pagination) { font-weight: 500; }
.pagination-wrapper :deep(.el-pagination__total) { color: var(--text-secondary); }
.pagination-wrapper :deep(.el-pager li.is-active) { background-color: var(--accent); color: #fff; }
.pagination-wrapper :deep(.el-pager li:hover) { color: var(--accent); }
.pagination-wrapper :deep(.el-select .el-input__wrapper) { box-shadow: none; border: 1px solid var(--border); }
.pagination-wrapper :deep(.btn-prev, .btn-next) { background: var(--bg-secondary); border: 1px solid var(--border); border-radius: 6px; }
.pagination-wrapper :deep(.btn-prev:hover, .btn-next:hover) { border-color: var(--accent); color: var(--accent); }
</style>
