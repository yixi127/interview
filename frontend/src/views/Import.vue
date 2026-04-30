<template>
  <div class="import">
    <div class="page-header">
      <h2 class="page-title">批量导入</h2>
      <p class="page-subtitle">支持文本输入和文件上传</p>
    </div>

    <div class="import-content">
      <div class="import-tabs">
        <button class="tab-btn" :class="{ active: activeTab === 'text' }" @click="activeTab = 'text'">
          <span class="tab-icon">📝</span>
          文本输入
        </button>
        <button class="tab-btn" :class="{ active: activeTab === 'file' }" @click="activeTab = 'file'">
          <span class="tab-icon">📁</span>
          文件上传
        </button>
      </div>

      <div class="format-tip" v-if="activeTab === 'text'">
        <span class="tip-title">格式说明</span>
        <p>1.题目内容。答案内容 2.题目内容。答案内容</p>
        <p class="tip-example">例如：1.HashMap的底层实现原理。HashMap基于哈希表实现... 2.ArrayList和LinkedList的区别...</p>
      </div>

      <div class="format-tip" v-else>
        <span class="tip-title">支持格式</span>
        <div class="format-list">
          <span class="format-item">.txt 文本文件</span>
          <span class="format-item">.md Markdown文件</span>
          <span class="format-item">.docx Word文档</span>
        </div>
      </div>

      <div v-if="activeTab === 'text'" class="input-section">
        <textarea v-model="content" class="textarea-input" placeholder="请输入题目，以数字序号开头..."></textarea>
        <button class="btn-primary" @click="parseContent" :disabled="!content.trim()">解析</button>
      </div>

      <div v-else class="file-section">
        <div class="drop-zone" @dragover.prevent @drop.prevent="handleDrop" @click="triggerFile">
          <input type="file" ref="fileInput" @change="handleFileSelect" accept=".txt,.md,.doc,.docx" hidden />
          <div class="drop-icon">📄</div>
          <p>点击或拖拽文件到此处</p>
          <span class="drop-hint">支持 TXT、MD、DOC、DOCX 格式</span>
        </div>
        <div v-if="selectedFile" class="file-info">
          <span class="file-name">{{ selectedFile.name }}</span>
          <button class="btn-primary" @click="uploadFile" :disabled="uploading">
            {{ uploading ? '解析中...' : '解析' }}
          </button>
        </div>
      </div>

      <div v-if="parsedQuestions.length > 0" class="parse-section">
        <div class="form-row">
          <div class="form-group">
            <label>类型</label>
            <select v-model="importForm.type" class="form-select">
              <option value="八股">八股</option>
              <option value="算法">算法</option>
              <option value="代码">代码</option>
            </select>
          </div>
          <div class="form-group">
            <label>分类</label>
            <select v-model="importForm.category" class="form-select">
              <option v-for="cat in filteredCategories" :key="cat.id" :label="cat.name" :value="cat.name" />
            </select>
          </div>
          <div class="form-group">
            <label>统一重要程度</label>
            <select v-model="globalImportance" @change="applyGlobalImportance" class="form-select">
              <option :value="0">不统一设置</option>
              <option :value="3">高</option>
              <option :value="2">中</option>
              <option :value="1">低</option>
            </select>
          </div>
        </div>

        <div class="parsed-header">
          <span class="parsed-count">解析结果 ({{ parsedQuestions.length }} 道)</span>
          <label class="select-all">
            <input type="checkbox" v-model="selectAll" @change="toggleSelectAll" />
            全选
          </label>
        </div>

        <div class="parsed-list">
          <div v-for="(q, i) in parsedQuestions" :key="i" class="parsed-item" :class="{ excluded: !q.selected }">
            <div class="item-header">
              <label class="item-check">
                <input type="checkbox" v-model="q.selected" />
                <span class="item-num">{{ i + 1 }}</span>
              </label>
            </div>
            <div class="item-content">
              <input v-model="q.title" type="text" class="form-input" placeholder="题目" />
              <textarea v-model="q.answer" class="textarea-small" placeholder="答案（支持Markdown）"></textarea>
              <div class="item-importance">
                <label>重要程度：</label>
                <select v-model="q.importance" class="form-select-small">
                  <option :value="3">高</option>
                  <option :value="2">中</option>
                  <option :value="1">低</option>
                </select>
              </div>
            </div>
            <button class="btn-remove" @click="removeItem(i)">×</button>
          </div>
        </div>

        <div class="actions">
          <button class="btn-secondary" @click="clearParse">重新解析</button>
          <button class="btn-primary" @click="saveQuestions">
            确认导入 ({{ selectedCount }} 道)
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const activeTab = ref('text')
const content = ref('')
const selectedFile = ref(null)
const fileInput = ref(null)
const uploading = ref(false)
const categories = ref([])
const parsedQuestions = ref([])

const importForm = reactive({ type: '八股', category: '' })
const globalImportance = ref(0)

const selectAll = ref(true)

const selectedCount = computed(() => parsedQuestions.value.filter(q => q.selected).length)

const applyGlobalImportance = () => {
  if (globalImportance.value > 0) {
    parsedQuestions.value.forEach(q => {
      q.importance = globalImportance.value
    })
  }
}

const loadCategories = async () => {
  const res = await axios.get('/api/categories')
  categories.value = res.data
  updateCategoryOptions()
}

const filteredCategories = computed(() => {
  return categories.value.filter(cat => cat.type === importForm.type)
})

const updateCategoryOptions = () => {
  const filtered = filteredCategories.value
  if (filtered.length && !filtered.find(c => c.name === importForm.category)) {
    importForm.category = filtered[0]?.name || ''
  }
}

watch(() => importForm.type, updateCategoryOptions)

const parseContent = async () => {
  if (!content.value.trim()) return
  try {
    const res = await axios.post('/api/import/parse', { content: content.value })
    parsedQuestions.value = res.data.map(q => ({ ...q, selected: true, importance: 2 }))
  } catch (e) {
    console.error('Parse error:', e.response?.data || e.message)
    ElMessage.error(e.response?.data?.error || '解析失败')
  }
}

const triggerFile = () => fileInput.value?.click()

const handleFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    selectedFile.value = file
    uploadFile()
  }
}

const handleDrop = (e) => {
  const file = e.dataTransfer.files[0]
  if (file && ['.txt', '.md', '.doc', '.docx'].some(ext => file.name.toLowerCase().endsWith(ext))) {
    selectedFile.value = file
    uploadFile()
  }
}

const uploadFile = async () => {
  if (!selectedFile.value) return
  uploading.value = true
  
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  
  try {
    const res = await axios.post('/api/import/parse', formData)
    parsedQuestions.value = res.data.map(q => ({ ...q, selected: true, importance: 2 }))
  } catch (e) {
    console.error('Upload error:', e.response?.data || e.message)
    ElMessage.error(e.response?.data?.error || '文件解析失败')
  } finally {
    uploading.value = false
  }
}

const removeItem = (i) => parsedQuestions.value.splice(i, 1)

const clearParse = () => {
  parsedQuestions.value = []
  content.value = ''
  selectedFile.value = null
}

const toggleSelectAll = () => {
  parsedQuestions.value.forEach(q => q.selected = selectAll.value)
}

const saveQuestions = async () => {
  const selected = parsedQuestions.value.filter(q => q.selected && q.title)
  if (selected.length === 0) {
    ElMessage.warning('请至少选择一道题目')
    return
  }
  
  const questions = selected.map(q => ({
    title: q.title,
    answer: q.answer,
    importance: q.importance || 2
  }))
  
  const res = await axios.post('/api/import/save', {
    questions: questions,
    type: importForm.type,
    category: importForm.category
  })
  ElMessage.success(res.data.message)
  clearParse()
}

onMounted(loadCategories)
</script>

<style scoped>
.import { max-width: 1000px; margin: 0 auto; }

.page-header { margin-bottom: 32px; padding-bottom: 24px; border-bottom: 1px solid var(--border); }
.page-title { font-family: 'Noto Serif SC', serif; font-size: 28px; font-weight: 600; margin-bottom: 8px; }
.page-subtitle { color: var(--text-tertiary); font-size: 14px; }

.import-tabs { display: flex; gap: 12px; margin-bottom: 24px; }
.tab-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  font-size: 15px;
  cursor: pointer;
  transition: all 0.2s;
}
.tab-btn:hover { border-color: var(--accent); }
.tab-btn.active { background: var(--accent-light); border-color: var(--accent); color: var(--accent); }
.tab-icon { font-size: 18px; }

.format-tip {
  background: var(--accent-light);
  border: 1px solid var(--accent);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 24px;
}
.tip-title { font-weight: 600; color: var(--accent); display: block; margin-bottom: 8px; }
.format-tip p { font-size: 14px; color: var(--text-secondary); }
.tip-example { margin-top: 8px; font-size: 13px; }
.format-list { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px; }
.format-item { background: #fff; padding: 6px 12px; border-radius: 6px; font-size: 13px; }

.input-section { display: flex; flex-direction: column; gap: 16px; }
.textarea-input { width: 100%; min-height: 280px; padding: 16px; border: 1px solid var(--border); border-radius: 12px; font-size: 14px; background: var(--bg-secondary); resize: vertical; }

.file-section { margin-bottom: 24px; }
.drop-zone {
  border: 2px dashed var(--border);
  border-radius: 16px;
  padding: 48px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}
.drop-zone:hover { border-color: var(--accent); background: var(--accent-light); }
.drop-icon { font-size: 48px; margin-bottom: 12px; }
.drop-hint { display: block; color: var(--text-tertiary); font-size: 13px; margin-top: 8px; }

.file-info { display: flex; align-items: center; justify-content: center; gap: 16px; margin-top: 16px; }
.file-name { background: var(--bg-tertiary); padding: 8px 16px; border-radius: 8px; }

.btn-primary {
  padding: 12px 32px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 10px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-primary:hover { background: #b89120; }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.parse-section { margin-top: 32px; }
.form-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px; }
.form-group label { display: block; font-size: 13px; font-weight: 500; margin-bottom: 8px; }
.form-select { width: 100%; padding: 12px 16px; border: 1px solid var(--border); border-radius: 10px; background: var(--bg-secondary); }

.parsed-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
.parsed-count { font-size: 16px; font-weight: 600; }
.select-all { display: flex; align-items: center; gap: 8px; font-size: 14px; cursor: pointer; }

.parsed-list { max-height: 500px; overflow-y: auto; }
.parsed-item {
  display: flex;
  gap: 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  transition: opacity 0.2s;
}
.parsed-item.excluded { opacity: 0.5; }

.item-header { display: flex; align-items: flex-start; }
.item-check { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.item-num { background: var(--bg-tertiary); padding: 4px 10px; border-radius: 6px; font-size: 12px; }

.item-content { flex: 1; }
.form-input { width: 100%; padding: 10px 14px; border: 1px solid var(--border); border-radius: 8px; font-size: 14px; margin-bottom: 10px; }
.textarea-small { width: 100%; padding: 10px 14px; border: 1px solid var(--border); border-radius: 8px; font-size: 14px; min-height: 60px; resize: vertical; }

.item-importance { display: flex; align-items: center; gap: 8px; margin-top: 8px; }
.item-importance label { font-size: 13px; color: var(--text-secondary); }
.form-select-small { padding: 6px 10px; border: 1px solid var(--border); border-radius: 6px; font-size: 13px; }

.btn-remove {
  width: 28px;
  height: 28px;
  background: #ffebee;
  color: #c62828;
  border: none;
  border-radius: 6px;
  font-size: 18px;
  cursor: pointer;
}
.btn-remove:hover { background: #ffcdd2; }

.actions { display: flex; gap: 12px; justify-content: center; margin-top: 24px; }
.btn-secondary {
  padding: 12px 24px;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  border: 1px solid var(--border);
  border-radius: 10px;
  font-size: 14px;
  cursor: pointer;
}
</style>
