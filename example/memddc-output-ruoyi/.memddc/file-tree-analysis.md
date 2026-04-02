# 项目结构分析

## 整体架构
RuoYi-Vue 采用经典的后端分层架构 + 前端 Vue 单页应用架构。

## 后端模块划分

### ruoyi-admin (Web 层)
- **职责**: 控制器层、应用启动、全局配置
- **关键类**: 
  - `Sys*Controller`: 系统管理相关接口
  - `RuoYiApplication`: 应用入口
- **特点**: 依赖其他所有模块，不包含业务逻辑

### ruoyi-system (业务层)
- **职责**: 核心业务逻辑、数据访问
- **关键包**:
  - `service/impl`: 业务实现
  - `mapper`: 数据访问层
  - `domain`: 领域对象
- **特点**: 核心业务模块，实体最多

### ruoyi-common (公共模块)
- **职责**: 实体定义、工具类、常量
- **关键包**:
  - `core/domain/entity`: 核心实体类
  - `utils`: 工具类
  - `annotation`: 自定义注解
- **特点**: 被所有模块依赖，无外部依赖

### ruoyi-framework (框架层)
- **职责**: 安全、拦截器、全局异常处理
- **关键包**:
  - `security`: Spring Security 配置
  - `interceptor`: 拦截器
  - `web/exception`: 全局异常处理
- **特点**: 技术基础设施

### ruoyi-generator (代码生成)
- **职责**: 根据数据库表生成前后端代码
- **关键类**:
  - `GenController`: 生成接口
  - `VelocityUtils`: 模板处理
- **特点**: 独立模块，不依赖业务

### ruoyi-quartz (定时任务)
- **职责**: 定时任务调度
- **关键类**:
  - `SysJobController`: 任务管理
  - `ScheduleUtils`: 调度工具
- **特点**: 基于 Quartz 框架

## 前端结构 (ruoyi-ui)

### 目录组织
```
src/
├── api/          # API 接口封装
├── components/   # 公共组件
├── layout/       # 布局组件
├── router/       # 路由配置
├── store/        # Vuex 状态管理
├── utils/        # 工具函数
└── views/        # 页面视图
```

### API 组织
按模块划分，与后端 Controller 对应：
- `system/`: 系统管理 API
- `monitor/`: 监控 API
- `tool/`: 工具 API

### Views 组织
按功能模块组织：
- `system/`: 用户、角色、菜单、部门等
- `monitor/`: 服务器、在线用户、操作日志等
- `tool/`: 代码生成

## 架构评估

### 优点
1. **模块职责清晰**: 按层和职责划分
2. **依赖关系合理**: 上层依赖下层，无循环依赖
3. **代码复用性好**: common 模块被多处复用
4. **扩展性强**: 新增模块方便

### 潜在改进
1. **领域边界**: 可考虑按领域进一步拆分
2. **依赖注入**: 部分地方可直接使用构造器注入
3. **API 版本**: 缺少 API 版本控制机制
