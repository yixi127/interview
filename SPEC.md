# 面试题管理系统 - interview-bank

## 项目概述
- **技术栈**: Flask (Python后端) + SQLite + 简单HTML/CSS/JS
- **功能**: 存储、分类、归档面试八股题和算法题
- **用户**: 管理员（可添加/编辑/删除）、普通用户（查看）

## 数据库设计

### 表: questions
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| title | TEXT | 题目内容 |
| type | TEXT | 类型: 八股/算法 |
| category | TEXT | 分类 |
| importance | INTEGER | 重要程度: 1-3 |
| answer | TEXT | 答案 |
| is_archived | INTEGER | 是否归档: 0/1 |
| created_at | DATETIME | 创建时间 |

### 表: categories
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| name | TEXT | 分类名称 |
| type | TEXT | 题目类型 |

### 表: users
| 字段 | 类型 | 说明 |
|------|------|------|
| id | INTEGER | 主键 |
| username | TEXT | 用户名 |
| password | TEXT | 密码(哈希) |
| is_admin | INTEGER | 是否管理员 |

## 功能列表

1. **题目管理**
   - 添加/编辑/删除面试题
   - 设置重要程度(1-3级)
   - 标记归档状态

2. **分类管理**
   - 管理员可添加/编辑分类
   - 支持多种分类：Java八股、操作系统、计算机网络、数据库、大模型agent等

3. **查看功能**
   - 按分类筛选
   - 按重要程度筛选
   - 按类型筛选(八股/算法)
   - 查看已归档/未归档

4. **用户认证**
   - 管理员登录
   - 简单的Session认证

## 页面结构

1. **登录页** `/login`
2. **题目列表页** `/` - 首页，显示题目列表，可筛选
3. **添加/编辑题目页** `/question/new`, `/question/edit/<id>`
4. **分类管理页** `/categories` - 管理员可管理分类
5. **归档管理页** `/archived` - 查看已归档题目
