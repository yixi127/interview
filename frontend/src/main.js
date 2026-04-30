import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import Home from './views/Home.vue'
import Login from './views/Login.vue'
import Categories from './views/Categories.vue'
import Import from './views/Import.vue'
import QuestionDetail from './views/QuestionDetail.vue'
import QuestionEdit from './views/QuestionEdit.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/login', component: Login },
  { path: '/categories', component: Categories },
  { path: '/import', component: Import },
  { path: '/question/:id', component: QuestionDetail },
  { path: '/question/edit', component: QuestionEdit },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.use(ElementPlus)
app.mount('#app')
