# MemDDC

## 技能信息

- **技能名称**: MemDDC
- **版本**: 1.0.1
- **作者**: qihao123
- **描述**: 面向团队协作的项目文档管理与代码迭代智能工具，提供自动文档生成、DDD模型管理、记忆压缩、代码风格统一和智能触发功能
- **触发关键词**: MemDDC, 加载记忆约束修改, 按DDD契约迭代更新, memddc-init, memddc-update, memddc-sync
- **适用场景**: 团队协作开发、复杂架构迭代、遗留系统持续重构、长期多人维护工程AI约束治理

## v1.0.1 核心升级

### 1. 团队协作支持

- **统一存储位置**: 所有文档和配置统一存放在 `.memddc/` 目录下，便于团队成员同步和共享
- **配置集中管理**: 团队共享配置文件，确保所有成员使用一致的文档生成策略
- **冲突解决机制**: 智能检测多人同时修改的冲突，提供合并建议
- **权限控制**: 支持设置不同成员的文档修改权限

### 2. 智能触发机制

触发条件（满足任一条件即触发）：
- **代码变更触发**: 检测到 `.js/.ts/.py/.java/.go/.cpp/.rs` 等代码文件的新增、修改、删除
- **文件结构变更**: 检测到项目目录结构变化（新建/删除文件夹）
- **配置文件变更**: 检测到 `.json/.yaml/.yml/.toml/.xml` 等配置文件变化
- **显式调用**: 用户主动输入触发关键词
- **定时同步**: 可配置定时检查并同步文档

### 3. 多策略文档生成

根据项目特征自动选择最优策略：
- **按项目类型**: 后端/前端/移动端/微服务/单体
- **按编程语言**: Java/Python/Go/Node.js/React/Vue等
- **按架构模式**: MVC/MVVM/DDD/微服务/Serverless

### 4. 主动申请能力

技能可主动申请必要信息：
- 数据库表结构样本
- API接口文档样本
- 现有代码样本
- 业务需求文档
- 架构设计文档
可随时中断申请流程，用户可选择提供或跳过

## 核心功能

### 1. 初始化流程（首次使用或检测到代码变更时触发）

#### 1.1 智能项目扫描

- **全量代码扫描**: 深度扫描项目目录、源码结构、实体、服务、数据库逻辑、API接口、配置文件等
- **变更检测**: 对比版本历史，精准识别新增、修改、删除的文件
- **项目特征识别**: 自动识别项目类型、编程语言、框架、架构模式
- **影响评估**: 评估代码变更对整体项目的影响范围

#### 1.2 多策略文档生成

根据识别结果自动选择文档生成策略：

**通用文档（所有项目类型）**:
- `.memddc/docs/architecture.md` - 系统架构文档
- `.memddc/docs/business.md` - 业务文档
- `.memddc/docs/api.md` - API接口文档
- `.memddc/docs/database.md` - 数据库设计文档
- `.memddc/docs/development.md` - 开发指南

**按编程语言**:
| 语言 | 专属文档 |
|------|---------|
| Java | `.memddc/docs/java-classes.md`, `.memddc/docs/spring.md`, `.memddc/docs/mybatis.md` |
| Python | `.memddc/docs/python-modules.md`, `.memddc/docs/django.md`, `.memddc/docs/flask.md` |
| Go | `.memddc/docs/go-packages.md`, `.memddc/docs/gin.md` |
| JavaScript/TypeScript | `.memddc/docs/js-modules.md`, `.memddc/docs/react.md`, `.memddc/docs/vue.md`, `.memddc/docs/node-api.md` |
| Rust | `.memddc/docs/rust-crates.md` |

**按架构模式**:
| 架构 | 文档 |
|------|-----|
| DDD | `.memddc/docs/ddd-model.md`, `.memddc/docs/bounded-contexts.md` |
| 微服务 | `.memddc/docs/services.md`, `.memddc/docs/service_mesh.md` |
| MVC | `.memddc/docs/mvc-structure.md` |
| MVVM | `.memddc/docs/mvvm-structure.md` |

**图表文档（使用Mermaid语法）**:
- `.memddc/docs/diagrams/architecture.mmd` - 架构图
- `.memddc/docs/diagrams/flow.mmd` - 流程图
- `.memddc/docs/diagrams/sequence.mmd` - 时序图
- `.memddc/docs/diagrams/er.mmd` - ER图

#### 1.3 DDD领域模型

- **限界上下文**: 边界定义、上下文映射、上下文关系
- **聚合**: 聚合根、实体、值对象、领域事件
- **领域服务**: 服务定义、职责边界、协作关系
- **领域规则**: 业务规则、不变量、约束条件
- **战术设计**: 实体设计、值对象设计、领域服务设计

#### 1.4 智能记忆压缩

- **文档压缩包**: `.memddc/snapshots/docs-compressed.zip` - 保留完整详细文档
- **记忆快照**: `.memddc/snapshots/mem-snapshot.json` - 智能压缩核心信息
  - 程序结构信息：目录结构、模块划分、依赖关系
  - 文件描述信息：文件功能、核心逻辑、关键API
  - 代码风格规范：项目代码风格规则
  - 领域模型摘要：DDD边界、聚合、实体

### 2. 自动加载流程（每次技能被触发时执行）

- **变更检测**: 首先检查自上次同步后有哪些文件发生了变化
- **智能加载**: 仅加载与变更相关的文档片段，而非全部文档
- **上下文构建**: 将压缩记忆与变更信息结合，生成精准上下文
- **影响分析**: 分析变更影响范围，识别需要同步更新的关联文档

### 3. 迭代修改流程

- **快速记忆加载**: 触发后自动加载最新压缩记忆快照
- **变更感知**: 了解本次需要修改的范围和内容
- **DDD约束**: 确保修改符合领域模型和业务契约
- **一致性保证**: 修改完成后自动同步更新相关文档

### 4. 同步压缩闭环

- **变更比对**: 记录本次所有代码变更
- **文档同步**: 更新受影响的Markdown文档
- **模型更新**: 同步DDD模型定义
- **记忆归档**: 合并决策，更新记忆快照
- **一致性验证**: 确保代码、文档、模型、记忆四者一致

## 目录结构

### v1.0.1 新版目录结构

```
project/
├── .memddc/                          # MemDDC 统一存储目录（团队共享）
│   ├── config.json                   # 团队共享配置
│   ├── mem-snapshot.json             # 全局记忆快照
│   ├── docs/                        # 项目文档
│   │   ├── architecture.md          # 架构文档
│   │   ├── business.md             # 业务文档
│   │   ├── api.md                  # API接口文档
│   │   ├── database.md             # 数据库设计文档
│   │   ├── development.md          # 开发指南
│   │   ├── code-style.md           # 代码风格指南
│   │   ├── [language-specific].md # 语言专属文档
│   │   ├── [architecture-specific].md # 架构专属文档
│   │   └── diagrams/               # 图表文档（Mermaid）
│   │       ├── architecture.mmd
│   │       ├── flow.mmd
│   │       ├── sequence.mmd
│   │       └── er.mmd
│   ├── ddd-model.md                 # DDD领域模型
│   ├── snapshots/                   # 历史快照存档
│   │   ├── docs-compressed.zip     # 文档压缩包
│   │   └── mem-YYYYMMDD-HHMMSS.json # 时间戳快照
│   ├── logs/                        # 操作日志
│   │   └── sync-YYYYMMDD.log
│   └── .gitignore                  # 团队共享的git忽略规则
└── [项目源代码目录]
```

### 配置文件 (config.json)

```json
{
  "version": "1.0.1",
  "project": {
    "name": "项目名称",
    "type": "backend|frontend|mobile|microservice",
    "language": "java|python|go|javascript|typescript|rust",
    "framework": "spring|django|gin|react|vue|flask",
    "architecture": "mvc|mvvm|ddd|microservice|serverless|monolithic"
  },
  "team": {
    "shared": true,
    "members": ["member1@example.com", "member2@example.com"],
    "syncBranch": "main"
  },
  "triggers": {
    "codeChange": true,
    "structureChange": true,
    "configChange": true,
    "manual": true,
    "scheduled": false,
    "scheduleCron": "0 2 * * *"
  },
  "document": {
    "types": ["architecture", "business", "api", "database"],
    "includeDiagrams": true,
    "autoUpdate": true
  },
  "compression": {
    "level": 7,
    "excludePatterns": ["*.log", "*.tmp", "node_modules/**"]
  }
}
```

## 工作流程

### 初始化阶段

1. 检测项目特征（类型、语言、框架、架构）
2. 选择匹配的文档生成策略
3. 全量代码扫描
4. 生成所有适用文档
5. 构建DDD领域模型
6. 创建初始记忆快照
7. 创建 `.memddc` 目录结构

### 触发检测阶段

1. 监听代码变更事件
2. 分析变更类型和范围
3. 确定需要更新的文档
4. 构建变更上下文

### 迭代修改阶段

1. 加载相关记忆片段
2. 注入上下文约束
3. 按DDD边界执行修改
4. 实时验证一致性

### 同步闭环阶段

1. 比对代码变更
2. 更新相关文档
3. 同步DDD模型
4. 重新压缩记忆
5. 验证四者一致

## 技术实现

### 核心模块

1. **项目扫描器**
   - 深度目录结构分析
   - 多语言源码解析
   - 依赖关系分析
   - API接口分析
   - 数据库逻辑分析
   - 配置文件分析
   - 变更检测器

2. **策略选择器**
   - 项目类型识别
   - 编程语言识别
   - 框架识别
   - 架构模式识别
   - 最优策略匹配

3. **文档生成器**
   - 架构文档生成
   - 业务文档生成
   - API文档生成
   - 数据库文档生成
   - 语言专属文档生成
   - 架构专属文档生成
   - Mermaid图表生成

4. **DDD模型构建器**
   - 限界上下文识别
   - 聚合根分析
   - 实体边界定义
   - 值对象设计
   - 领域服务提取
   - 领域事件识别

5. **记忆管理系统**
   - 智能文档压缩
   - 记忆快照生成
   - 历史决策记录
   - 上下文注入
   - 增量更新
   - 冲突检测

6. **变更追踪器**
   - 代码变更检测
   - 文档同步更新
   - 模型一致性验证
   - 影响分析

7. **团队协作器**
   - 配置同步
   - 冲突检测
   - 权限管理
   - 版本控制集成

### 主动申请能力

技能可主动请求必要信息：

```
[MemDDC] 检测到项目使用了数据库，但未找到数据库设计文档。
请提供以下信息之一：
1. 数据库表结构（CREATE TABLE 语句或 ER 图）
2. 现有数据库的连接信息（我将从现有库逆向生成）
3. 业务需求文档（我将根据需求推断数据库设计）

输入 "skip" 可跳过此步骤。
输入 "pause" 可暂停文档生成，稍后继续。
```

支持主动申请的内容类型：
- 数据库表结构样本
- API接口文档样本
- 现有代码样本
- 业务需求文档
- 架构设计文档
- 第三方服务集成文档
- 安全需求文档

## 配置选项

### 基本配置

- `projectRoot`: 项目根目录路径
- `memddcPath`: MemDDC存储目录，默认为 `./.memddc`
- `docOutputPath`: 文档输出路径，默认为 `./.memddc/docs`
- `dddModelPath`: DDD模型文件路径，默认为 `./.memddc/ddd-model.md`
- `memSnapshotPath`: 记忆快照路径，默认为 `./.memddc/mem-snapshot.json`

### 触发配置

- `triggers.codeChange`: 代码变更触发，默认为 `true`
- `triggers.structureChange`: 目录结构变更触发，默认为 `true`
- `triggers.configChange`: 配置文件变更触发，默认为 `true`
- `triggers.manual`: 手动触发，默认为 `true`
- `triggers.scheduled`: 定时触发，默认为 `false`

### 文档配置

- `document.types`: 文档类型列表
- `document.includeDiagrams`: 是否包含图表，默认为 `true`
- `document.autoUpdate`: 变更时自动更新，默认为 `true`

### 团队配置

- `team.shared`: 是否团队共享模式
- `team.members`: 团队成员列表
- `team.syncBranch`: 同步分支

### 高级配置

- `scanDepth`: 目录扫描深度，默认为 5
- `compressionLevel`: 压缩级别，默认为 7（0-9）
- `contextInjectionThreshold`: 上下文注入阈值，默认为 80%

## 使用示例

### 初始化项目

```
用户: MemDDC 初始化项目
技能: 开始扫描项目结构...
      检测到: Java + Spring Boot + DDD 架构
      选择策略: Java后端 + DDD 文档集
      开始生成文档...
```

### 触发代码修改

```
用户: 修改了 UserService.java 添加了新的查询方法
技能: 检测到代码变更
      加载相关记忆...
      更新 API 文档
      更新 DDD 模型
      同步完成
```

### 团队协作

```
用户A: MemDDC 更新了业务文档
技能: 检测到文档更新
      同步到团队配置...
      通知其他成员...
      冲突检测: 无
      同步完成
```

## 注意事项

1. **首次使用**: 确保项目目录存在且包含源码文件
2. **权限要求**: 需要对项目目录和 `.memddc` 目录有读写权限
3. **团队协作**: 建议将 `.memddc` 目录纳入版本控制
4. **性能考虑**: 大型项目初始化可能需要较长时间
5. **备份建议**: 在执行重大修改前，建议备份 `.memddc` 目录

## 故障排除

### 常见问题

1. **初始化失败**
   - 检查项目目录权限
   - 确保项目中包含源码文件
   - 查看 `.memddc/logs/` 下的日志文件

2. **触发未生效**
   - 检查 `config.json` 中的触发配置
   - 确认代码文件扩展名在扫描范围内

3. **文档同步失败**
   - 检查 `.memddc/docs/` 目录权限
   - 确保磁盘空间充足

4. **团队同步冲突**
   - 使用 `memddc-sync` 命令手动同步
   - 查看冲突详情并手动合并

## 版本历史

- **v1.0.1** - 团队协作升级版 (当前版本)
  - 新增 `.memddc/` 统一存储目录
  - 新增智能触发机制（代码变更自动触发）
  - 新增多策略文档生成（按语言/架构/类型）
  - 新增主动申请能力
  - 新增团队协作支持
  - 优化文档结构和组织方式

- **v1.0.0** - 初始版本
  - 实现项目扫描和文档生成
  - 支持DDD模型构建
  - 提供记忆压缩和管理功能

## 许可协议

MIT License

## 联系方式

- 项目主页: <https://github.com/qihao123/memddc-ai-skill>
- 作者: qihao123
- 邮件支持: <qihoo2017@gmail.com>
