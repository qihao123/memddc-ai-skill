# RuoYi-Vue 前端技术栈文档

## 技术栈

- **框架**: Vue 2.7+
- **路由**: Vue-Router 3.x
- **状态管理**: Vuex 3.x
- **UI库**: Element-UI
- **HTTP**: Axios 0.30.3
- **构建工具**: Vue CLI 5 + Webpack
- **图标**: SVG Sprite

## 项目结构

```
src/
├── api/           # 接口请求封装（按模块组织）
├── assets/        # 静态资源、样式、SVG图标
├── components/    # 全局公共组件
├── directive/     # 自定义指令（permission, clipboard等）
├── layout/        # 布局组件（Sidebar、Navbar、AppMain等）
├── plugins/       # 插件（Element UI、dialog拖拽等）
├── router/        # 路由配置 + 动态路由生成
├── store/         # Vuex（user、permission、settings、tagsView、app）
├── utils/         # 工具函数
│   ├── request.js    # Axios拦截器封装
│   ├── auth.js       # Token操作
│   ├── ruoyi.js      # 通用工具函数
│   └── validate.js   # 表单校验
├── views/         # 页面视图
│   ├── system/    # 系统管理
│   ├── monitor/   # 系统监控
│   ├── tool/      # 系统工具
│   └── dashboard/ # 首页
├── App.vue
├── main.js
├── permission.js  # 路由权限守卫
└── settings.js    # 全局配置项
```

## 核心组件

| 组件 | 路径 | 说明 |
|------|------|------|
| `Pagination` | `components/Pagination` | 分页组件 |
| `DictTag` | `components/DictTag` | 字典值渲染 |
| `FileUpload` | `components/FileUpload` | 文件上传 |
| `ImageUpload` | `components/ImageUpload` | 图片上传 |
| `ImagePreview` | `components/ImagePreview` | 图片预览 |
| `TreePanel` | `components/TreePanel` | 树分割面板 |
| `Editor` | `components/Editor` | 富文本编辑器 |
| `RightToolbar` | `components/RightToolbar` | 表格右工具栏 |
| `Screenfull` | `components/Screenfull` | 全屏切换 |
| `SvgIcon` | `components/SvgIcon` | SVG图标组件 |

## 路由权限控制

1. `permission.js` 中通过 `router.beforeEach` 拦截
2. 检查本地 Token 是否存在
3. 若不存在且非白名单路由，重定向到 `/login`
4. 已登录则根据用户角色动态生成可访问路由列表
5. 路由数据来自后端 `/getRouters` 接口

## Vuex Store 模块

| 模块 | 说明 |
|------|------|
| `user` | 用户信息、Token、登录登出 |
| `permission` | 路由权限、菜单生成 |
| `settings` | 主题、布局、显示设置 |
| `tagsView` | 页签视图、缓存控制 |
| `app` | 侧边栏折叠、设备类型 |

## 常用开发模式

### 表格+搜索+弹窗三件套

几乎所有管理页面都遵循统一模式：
- 顶部搜索表单（`queryParams`）
- 操作按钮行（新增、修改、删除、导出、刷新）
- `el-table` 数据表格
- `pagination` 分页
- `el-dialog` 新增/编辑弹窗

### API请求封装

```js
import request from '@/utils/request'

export function listUser(query) {
  return request({
    url: '/system/user/list',
    method: 'get',
    params: query
  })
}
```

Axios拦截器中统一处理：
- 请求拦截：附加 Token
- 响应拦截：统一错误提示、Blob处理、401跳转
