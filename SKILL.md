# MemDDC

## 技能信息

- **技能名称**: MemDDC
- **版本**: 1.0.2
- **作者**: qihao123
- **描述**: 面向团队协作的项目文档管理与代码迭代智能工具，提供自动文档生成、DDD模型管理、记忆压缩、代码风格统一和智能触发功能
- **触发关键词**: MemDDC, 加载记忆约束修改, 按DDD契约迭代更新, memddc-init, memddc-update, memddc-sync
- **适用场景**: 团队协作开发、复杂架构迭代、遗留系统持续重构、长期多人维护工程AI约束治理

## 实战交互契约

用户说"memddc-sync"或"MemDDC 更新"时：

1. 执行 `git diff --name-only` 获取变更文件列表
2. 将变更文件与 `mem-snapshot.json` 中的模块/实体/API 列表匹配
3. 仅更新受影响的 Markdown 文档段落
4. 更新 snapshot 中标记的字段，其余原样保留

用户提出代码修改需求时：

1. 优先加载 `mem-snapshot.json`
2. 根据 snapshot 中的模块和关键类列表定位相关文件
3. 先输出变更蓝图（影响文件清单），经用户确认后再执行修改

## v1.0.2 核心升级

### 1. 外部信息源整合

#### 1.1 版本控制日志分析

- **Git日志拉取**: 初始化时自动执行 `git log --pretty=format:"%h %s %b" -n 100`
- **SVN日志支持**: 如检测到 `.svn` 目录，执行 `svn log --limit 100`
- **AI整理**: 将原始日志发送给AI分析，提取：
  - 提交频率和规律
  - 关键版本标记（v1.0, release等）
  - 团队协作模式
  - 业务变更周期
- **写入快照**: 分析结果结构化存入 `mem-snapshot.json`

#### 1.2 文件结构智能分析

- **完整文件树扫描**: 递归扫描项目目录结构，生成完整文件树
- **编译器索引利用**: 读取 IDE 生成的索引文件（如 `.idea/`, `.vscode/`, `compile_commands.json`）
- **AI语义分析**: 将文件结构发送给AI，分析：
  - 模块划分合理性
  - 依赖关系复杂度
  - 潜在架构问题
  - 建议的目录重组
- **写入快照**: 分析结论存入快照供后续参考

#### 1.3 用户文档纳入分析

- **docs目录监听**: `.memddc/docs/user-docs/` 目录下的所有文档都会被AI分析
- **支持格式**: `.md`, `.txt`, `.doc`, `.docx`, `.pdf` 等
- **AI业务理解**: 将用户文档内容发送给AI，分析：
  - 业务流程和规则
  - 业务术语定义
  - 需求背景理解
  - 架构决策历史
- **增量更新**: 初始化或更新时，自动检测docs目录变化

## 团队协作（基础版）

- **团队共享目录**: `.memddc/`
- **共享配置**: `config.json` 中的 `team.syncBranch`
- **冲突提示**: 当 `mem-snapshot.json` 与 Git 状态不一致时，提示用户先执行 `memddc-sync`
- **权限控制**: 规划中，当前版本通过 Git 原生权限管理 `.memddc/` 目录

### 3. 智能触发机制

触发条件（满足任一条件即触发）：

- **代码变更触发**: 检测到 `.js/.ts/.py/.java/.go/.cpp/.rs` 等代码文件的新增、修改、删除
- **文件结构变更**: 检测到项目目录结构变化（新建/删除文件夹）
- **配置文件变更**: 检测到 `.json/.yaml/.yml/.toml/.xml` 等配置文件变化
- **显式调用**: 用户主动输入触发关键词
- **定时同步**: 可配置定时检查并同步文档

### 4. 多策略文档生成

根据项目特征自动选择最优策略：

- **按项目类型**: 后端/前端/移动端/微服务/单体
- **按编程语言**: Java/Python/Go/Node.js/React/Vue等
- **按架构模式**: MVC/MVVM/DDD/微服务/Serverless

### 5. 主动申请能力

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

#### 1.2 生成文档清单

根据识别结果自动选择文档生成策略：

**通用**: `architecture.md` / `business.md` / `api.md` / `database.md` / `development.md`

**按语言**: `[java-classes.md / spring.md / vue.md 等]`

**按架构**: `[ddd-model.md / bounded-contexts.md 等]`

**图表**: `diagrams/*.mmd`

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
  - **VCS日志摘要**：Git/SVN日志AI分析结果（提交规律、关键版本、团队协作模式）
  - **文件结构分析**：AI对项目结构的分析结论和建议
  - **业务上下文**：从用户文档中提取的业务术语、规则、流程
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
- **容量检查**: 提交快照前检查文件大小
  - **上下文限制检测**: 快照大小 > 上下文限制的80%时触发压缩
  - **智能压缩**: 优先保留核心信息（VCS摘要、文件结构分析、业务上下文）
  - **逐级压缩**: Level 1 → 精简描述，Level 2 → 只保留关键字段
  - **最小保证**: 压缩后至少保留模块列表、关键API、约束规则

## 目录结构

### v1.0.2 新版目录结构

```
project/
├── .memddc/                          # MemDDC 统一存储目录（团队共享）
│   ├── config.json                   # 团队共享配置
│   ├── mem-snapshot.json             # 全局记忆快照（核心）
│   ├── vcs-log-raw.txt              # 原始VCS日志（最近100条）
│   ├── vcs-log-analysis.md           # AI整理的VCS日志分析
│   ├── file-tree-raw.txt            # 原始文件树
│   ├── file-tree-analysis.md        # AI文件结构分析
│   ├── docs/                        # 项目文档（用户可添加）
│   │   ├── user-docs/              # 用户文档目录（AI会分析其中的业务文档）
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
  "version": "1.0.2",
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
    "autoUpdate": true,
    "analyzeUserDocs": true
  },
  "vcs": {
    "enabled": true,
    "logLimit": 100,
    "types": ["git", "svn"]
  },
  "fileAnalysis": {
    "enabled": true,
    "includeIdeIndexes": true
  },
  "compression": {
    "level": 7,
    "excludePatterns": ["*.log", "*.tmp", "node_modules/**"],
    "contextLimit": 128000,
    "autoCompressThreshold": 0.8
  }
}
```

## 工作流程

### v1.0.2 初始化阶段（核心升级）

1. **VCS日志拉取**
   - 检测版本控制系统类型（Git/SVN）
   - 执行 `git log --pretty=format:"%h %s %b" -n 100` 或 `svn log --limit 100`
   - 保存原始日志到 `.memddc/vcs-log-raw.txt`

2. **AI日志分析**
   - 将原始日志发送给AI分析
   - AI提取：提交规律、关键版本、团队协作模式、业务变更周期
   - 保存分析结果到 `.memddc/vcs-log-analysis.md`

3. **文件树扫描**
   - 递归扫描项目目录结构
   - 收集IDE索引文件（如存在）
   - 保存到 `.memddc/file-tree-raw.txt`

4. **AI结构分析**
   - 将文件结构发送给AI分析
   - AI评估：模块划分、依赖关系、潜在问题
   - 保存分析结果到 `.memddc/file-tree-analysis.md`

5. **用户文档分析**
   - 扫描 `.memddc/docs/user-docs/` 目录
   - 将用户文档发送给AI提取业务上下文
   - 提取：业务流程、业务术语、需求规则

6. **代码扫描与文档生成**
   - 全量代码AST扫描
   - 生成适配项目的结构化文档
   - 构建DDD领域模型

7. **整合写入快照**
   - 将VCS分析、文件结构分析、业务上下文整合
   - 生成包含全部上下文信息的 `mem-snapshot.json`

### 触发检测阶段

1. 监听代码变更事件
2. 分析变更类型和范围
3. 确定需要更新的文档
4. 构建变更上下文

### memddc-sync 增量流程

1. 执行 `git diff --name-only` 获取变更文件
2. 分类：代码文件→更新文档 / 用户文档→更新业务上下文 / 配置文件→更新技术栈说明
3. AI 输出影响面判断：`{"affectedDocs": [...], "snapshotFields": [...]}`
4. 精准读取并更新受影响内容
5. 写入新 snapshot，保留未变更字段

### 迭代修改阶段

1. 加载相关记忆片段（包括VCS历史、文件结构、业务上下文）
2. 注入上下文约束
3. 按DDD边界执行修改
4. 实时验证一致性

### 同步闭环阶段

1. 比对代码变更
2. 更新相关文档
3. 同步DDD模型
4. 重新分析VCS日志和文件结构（如有变化）
5. 更新记忆快照
6. 验证多者一致

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
   - **容量检查**: 快照大小超过上下文限制80%时自动压缩

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

## 技术栈支持

| 技术栈 | 文档生成 | DDD建模 | 记忆压缩 |
|--------|---------|---------|---------|
| Java/Spring Boot | ✅ | ✅ | ✅ |
| Python/Django/Flask | ✅ | ✅ | ✅ |
| Node.js/Express/Nest | ✅ | ✅ | ✅ |
| Go/Gin | ✅ | ✅ | ✅ |
| 前端框架 | ✅ | ⚠️ | ✅ |
| 微服务 | ✅ | ✅ | ✅ |

## 注意事项

1. **首次使用**: 确保项目目录存在且包含源码文件
2. **权限要求**: 需要对项目目录和 `.memddc` 目录有读写权限
3. **版本控制**: 建议将 `.memddc` 目录纳入版本控制
4. **文档维护**: 代码变更后及时运行更新命令

## 故障排除

### 初始化失败

- 检查项目目录权限
- 确保项目中包含足够的源码文件
- 查看 `.memddc/logs/` 下的日志文件

### 文档未同步

- 运行 `MemDDC 更新` 手动同步
- 检查 `config.json` 中的 `autoUpdate` 配置

### Token消耗未降低

- 确认 `.memddc/mem-snapshot.json` 存在
- 尝试开启新对话再触发技能
- 检查文档是否过大（可考虑精简）

## 版本历史

- **v1.0.2** - 当前稳定版 (推荐)
  - VCS日志分析：Git/SVN日志AI整理写入快照
  - 文件结构分析：IDE索引和目录树AI分析
  - 用户文档纳入：docs目录文档自动业务分析
  - 完整的文档生成和DDD建模
  - 智能记忆压缩
  - 团队协作支持
  - 实测降低 23% Token 消耗

- **v1.0.1** - 历史版本
  - 完整的文档生成和DDD建模
  - 智能记忆压缩
  - 团队协作支持

- **v1.0.0** - 初始版本
  - 基础文档生成
  - 简单DDD模型

## 许可协议

MIT License

## 联系方式

- 项目主页: <https://github.com/qihao123/memddc-ai-skill>
- 作者: qihao123
- 邮件: <qihoo2017@gmail.com>
