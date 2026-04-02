# 架构文档

## 1. 技术栈

### 后端
- **框架**: Spring Boot 4.0.3
- **安全**: Spring Security + JWT
- **ORM**: MyBatis 4.0.1
- **数据库连接池**: Druid 1.2.28
- **缓存**: Redis
- **定时任务**: Quartz
- **JSON**: Fastjson 2.0.61
- **API文档**: SpringDoc OpenAPI

### 前端
- **框架**: Vue 2.x
- **UI库**: Element UI
- **路由**: Vue Router
- **状态管理**: Vuex
- **HTTP**: Axios 0.30.3
- **构建**: Webpack

## 2. 模块结构

```
ruoyi/                          # 父项目
├── ruoyi-admin                 # Web服务入口
├── ruoyi-system               # 系统管理业务
├── ruoyi-common               # 公共模块
├── ruoyi-framework            # 框架核心
├── ruoyi-generator            # 代码生成
├── ruoyi-quartz               # 定时任务
└── ruoyi-ui                   # 前端UI
```

## 3. 分层架构

### Controller 层
- 职责: 接收请求、参数校验、调用Service、返回结果
- 注解: `@RestController`, `@RequestMapping`
- 权限: `@PreAuthorize("@ss.hasPermi('module:entity:action')")`
- 日志: `@Log(title="", businessType=BusinessType.xxx)`

### Service 层
- 接口定义契约
- 实现类处理业务逻辑
- 事务控制

### Mapper 层
- 数据访问接口
- XML 定义SQL

### Entity 层
- 数据库表映射
- 验证注解

## 4. 安全设计

### 认证流程
1. 用户登录 -> 生成 JWT Token
2. 请求携带 Token
3. 拦截器验证 Token
4. 权限注解控制访问

### 权限模型
- RBAC (Role-Based Access Control)
- 用户-角色-菜单三级关联
- 数据权限支持五种范围

## 5. 缓存策略

### Redis 用途
- 用户登录信息
- 字典数据缓存
- 配置项缓存
- 验证码

### 缓存注解
- 自定义缓存工具类 `RedisCache`

## 6. 代码生成

### 生成策略
1. 读取数据库表结构
2. Velocity 模板渲染
3. 生成前后端代码
4. 支持自定义模板

### 生成内容
- Controller
- Service + Impl
- Mapper + XML
- Entity
- Vue 页面
- API JS
