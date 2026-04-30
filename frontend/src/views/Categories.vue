<template>
  <div class="categories">
    <div class="page-header">
      <h2 class="page-title">分类管理</h2>
      <p class="page-subtitle">管理面试题分类</p>
    </div>

    <div class="categories-content">
      <div class="add-section">
        <input v-model="newCategory.name" type="text" placeholder="分类名称" class="form-input" />
        <select v-model="newCategory.type" class="form-select">
          <option value="八股">八股</option>
          <option value="算法">算法</option>
          <option value="代码">代码</option>
        </select>
        <button class="btn-primary" @click="addCategory">添加分类</button>
      </div>

      <div class="categories-list">
        <div v-for="cat in categories" :key="cat.id" class="category-card">
          <div class="cat-info">
            <template v-if="editingId === cat.id">
              <input v-model="editName" type="text" class="form-input" />
              <select v-model="editType" class="form-select form-select-sm">
                <option value="八股">八股</option>
                <option value="算法">算法</option>
              </select>
              <button class="btn-save" @click="saveEdit(cat)">保存</button>
              <button class="btn-cancel" @click="cancelEdit">取消</button>
            </template>
            <template v-else>
              <span class="cat-name">{{ cat.name }}</span>
              <span class="cat-type" :class="cat.type">{{ cat.type }}</span>
              <button class="btn-edit" @click="startEdit(cat)">编辑</button>
            </template>
          </div>
          <button class="btn-delete" @click="deleteCategory(cat)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'

const categories = ref([])
const newCategory = reactive({ name: '', type: '八股' })
const editingId = ref(null)
const editName = ref('')
const editType = ref('')

const loadCategories = async () => {
  const res = await axios.get('/api/categories')
  categories.value = res.data
}

const addCategory = async () => {
  if (!newCategory.name) return
  try {
    await axios.post('/api/categories', newCategory)
    ElMessage.success('添加成功')
    newCategory.name = ''
    loadCategories()
  } catch (e) {
    console.error('Add category error:', e.response?.data || e.message)
    ElMessage.error(e.response?.data?.error || '添加失败')
  }
}

const startEdit = (cat) => {
  editingId.value = cat.id
  editName.value = cat.name
  editType.value = cat.type
}

const cancelEdit = () => {
  editingId.value = null
}

const saveEdit = async (cat) => {
  if (!editName.value) return
  try {
    await axios.put(`/api/categories/${cat.id}`, { name: editName.value, type: editType.value })
    ElMessage.success('保存成功')
    editingId.value = null
    loadCategories()
  } catch (e) {
    ElMessage.error(e.response?.data?.error || '保存失败')
  }
}

const deleteCategory = async (cat) => {
  await ElMessageBox.confirm('确定删除此分类？', '提示', { type: 'warning' })
  await axios.delete(`/api/categories/${cat.id}`)
  ElMessage.success('删除成功')
  loadCategories()
}

onMounted(loadCategories)
</script>

<style scoped>
.categories { max-width: 800px; margin: 0 auto; }

.page-header {
  margin-bottom: 40px;
  padding-bottom: 24px;
  border-bottom: 1px solid var(--border);
}

.page-title {
  font-family: 'Noto Serif SC', serif;
  font-size: 28px;
  font-weight: 600;
  margin-bottom: 8px;
}

.page-subtitle { color: var(--text-tertiary); font-size: 14px; }

.add-section {
  display: flex;
  gap: 12px;
  margin-bottom: 32px;
}

.form-input, .form-select {
  padding: 12px 16px;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 14px;
  background: var(--bg-secondary);
}

.form-input { flex: 1; }
.form-select { width: 120px; }

.btn-primary {
  padding: 12px 24px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.btn-primary:hover { background: #b89120; }

.categories-list { display: flex; flex-direction: column; gap: 12px; }

.category-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 24px;
}

.cat-info { display: flex; align-items: center; gap: 12px; }
.cat-name { font-size: 15px; font-weight: 500; }

.cat-type {
  font-size: 12px;
  padding: 4px 10px;
  border-radius: 6px;
}

.cat-type.八股 { background: #e8f5e9; color: #2e7d32; }
.cat-type.算法 { background: #fff3e0; color: #ef6c00; }
.cat-type.代码 { background: #e3f2fd; color: #1565c0; }

.btn-delete {
  padding: 8px 16px;
  background: #ffebee;
  color: #c62828;
  border: none;
  border-radius: 6px;
  font-size: 13px;
  cursor: pointer;
}

.btn-delete:hover { background: #ffcdd2; }

.btn-edit {
  padding: 4px 12px;
  background: #e3f2fd;
  color: #1976d2;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  margin-left: 8px;
}

.btn-edit:hover { background: #bbdefb; }

.btn-save {
  padding: 6px 12px;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}

.btn-cancel {
  padding: 6px 12px;
  background: #f5f5f5;
  color: #666;
  border: none;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
  margin-left: 4px;
}

.form-select-sm {
  width: 90px;
  padding: 6px 10px;
  font-size: 13px;
}
</style>
