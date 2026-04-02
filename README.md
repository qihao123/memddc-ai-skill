# memddc-ai-skill

> [English Version](README_EN.md)

## 一句话理解

**MemDDC = 给代码做体检，拿着病历去看 AI 医生**

代码出问题了？不用东奔西跑问 AI "这项目用的啥框架"、"这个接口在哪个文件"，MemDDC 先给代码做个全面体检，生成病历（项目架构、文件索引、变更历史），AI 医生一眼就能定位问题，给出解决方案。

## 核心能力

| 能力 | 说明 |
|------|------|
| **项目体检** | 首次使用自动扫描全量代码，生成项目病历 |
| **三级索引** | metadata/index/context 结构，快速定位文件 |
| **关联映射** | entity→mapper→service→controller→view，按 ID 查表 |
| **DDD约束** | 修改必须符合领域模型和业务契约 |
| **VCS分析** | 自动分析 Git 提交规律，了解团队协作模式 |
| **Token节省** | 实测复杂业务修改节省 53% Token 消耗 |

## 快速开始

### 触发关键词

```
MemDDC, 加载记忆约束修改, 按DDD契约迭代更新, memddc-init, memddc-update, memddc-sync
```

### 初始化项目

```
用户: memddc-init
AI:   正在扫描项目...
      检测到: Java + Spring Boot + MyBatis-Plus
      生成项目病历: architecture.md, ddd-model.md, mem-snapshot.json
      体检完成，已建立三级索引
```

### 修改代码

```
用户: 修改 SysDept 部门的状态字段

AI:   正在加载病历...
      定位到: SysDept → {entity, mapper, service, controller, views[]}
      文件定位: ruoyi-admin/src/main/java/.../domain/SysDept.java
               ruoyi-admin/src/main/resources/mapper/system/SysDeptMapper.xml
      符合 DDD 约束，开始修改...
      修改完成，已同步更新相关文档
```

## 病历结构 (mem-snapshot.json)

```json
{
  "metadata": { "name": "RuoYi-Vue", "version": "1.0", "tech": "Java+Spring Boot" },
  "index": {
    "entities": { "SysDept": { "path": ".../SysDept.java", "module": "system" } },
    "services": { "SysDeptServiceImpl": { "path": "...", "interface": "ISysDeptService" } },
    "relations": {
      "SysDept": {
        "entity": ".../SysDept.java",
        "mapper": ".../SysDeptMapper.xml",
        "service": ".../SysDeptServiceImpl.java",
        "controller": ".../SysDeptController.java",
        "views": [".../dept/index.vue"]
      }
    }
  },
  "context": {
    "patterns": ["treeBuild", "pagination", "crudApi"],
    "codeStyle": { "returnType": "AjaxResult", "annotation": "@RestController" }
  }
}
```

## 工作流程

1. **体检阶段** (memddc-init): 扫描代码 → 生成病历 → 建立索引
2. **就诊阶段** (修改代码): 加载病历 → 定位文件 → 按约束修改
3. **复诊阶段** (memddc-sync): 比对变更 → 同步文档 → 更新病历

## 实战效果

RuoYi-Vue 前后端分离项目实测：

| 场景 | 使用MemDDC | 不使用 | 节省 |
|------|-----------|--------|------|
| 项目说明生成 | ~49,000 token | ~77,000 token | **36%** |
| 业务功能修改 | ~18,000 token | ~38,000 token | **53%** |
| 对话轮数 | 4轮 | 6-10轮 | **60%** |

## 目录结构

```
project/
├── .memddc/                    # 病历本目录
│   ├── mem-snapshot.json       # 病历主文件（三级索引）
│   ├── vcs-log-analysis.md    # 病史（Git提交记录）
│   ├── file-tree-analysis.md   # 体检报告（结构分析）
│   └── docs/                   # 详细检查报告
│       ├── architecture.md      # 系统架构
│       ├── ddd-model.md         # 领域模型
│       └── api.md              # 接口文档
└── [项目源码]
```

## 适用场景

- **团队协作**: 统一病历，新成员快速上手
- **复杂架构**: DDD 约束，避免野蛮修改
- **遗留系统**: 拿着体检报告再做重构
- **长期维护**: 记录决策历史，理解设计意图

## 技术栈支持

| 语言/框架 | 文档生成 | DDD建模 | 记忆压缩 |
|-----------|---------|---------|----------|
| Java/Spring | ✅ | ✅ | ✅ |
| Python/Django | ✅ | ✅ | ✅ |
| Go/Gin | ✅ | ✅ | ✅ |
| Vue/React | ✅ | ⚠️ | ✅ |

## 版本

- **v1.0.2** (当前): 三级索引 + 关联映射 + VCS分析
- **v1.0.1**: 团队协作 + 智能触发

## 链接

- GitHub: <https://github.com/qihao123/memddc-ai-skill>
- Email: <qihoo2017@gmail.com>
