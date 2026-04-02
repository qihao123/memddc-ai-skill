# RuoYi-Vue 代码风格指南

## Java 代码风格

- 包名: 全小写 `com.ruoyi.xxx`
- 类名: 大驼峰 `SysUserController`
- 接口: Service接口以 `I` 开头 `ISysUserService`
- 方法名: 小驼峰 `getUserList()`
- 常量: 全大写下划线 `CACHE_CONSTANT`
- 注释: 类/公共方法需要 Javadoc
- 缩进: 4个空格（或Tab）
- 行长: 建议不超过120字符

## Vue 代码风格

- 组件名: 大驼峰 `UserManage.vue`
- 变量名: 小驼峰 `userList`
- 常量: 全大写 `const STATUS_NORMAL = '0'`
- API函数名: `listXxx`, `getXxx`, `addXxx`, `updateXxx`, `delXxx`
- 引用组件: `import Pagination from '@/components/Pagination'`
- 模板中属性绑定: 统一使用 `:` 和 `@`

## 接口命名规范

后端URL遵循 RESTful 风格结合 RuoYi 约定:
- 列表: `GET /module/list`
- 详情: `GET /module/{id}`
- 新增: `POST /module`
- 修改: `PUT /module`
- 删除: `DELETE /module/{ids}`
- 导出: `POST /module/export`
- 字典/下拉: `GET /module/dict`

## 权限标识规范

格式: `模块:功能:操作`
- `system:user:list`
- `system:user:add`
- `system:user:edit`
- `system:user:remove`
- `system:user:export`
