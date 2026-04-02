# memddc-ai-skill

> [中文版本](README.md)

## One-Line Summary

**MemDDC = Get a health checkup for your code, then visit the AI doctor with the medical record**

Code has problems? No more running around asking AI "what framework does this project use" or "which file has this interface". MemDDC gives your code a full health checkup first, generates medical records (project architecture, file index, change history), so the AI doctor can pinpoint the issue at a glance and provide solutions.

## Core Capabilities

| Capability | Description |
|------------|-------------|
| **Project Checkup** | Auto-scan full codebase on first use, generate medical record |
| **Three-Tier Index** | metadata/index/context structure, fast file positioning |
| **Relation Mapping** | entity→mapper→service→controller→view, lookup by ID |
| **DDD Constraints** | Modifications must conform to domain model and contracts |
| **VCS Analysis** | Auto-analyze Git commit patterns, understand team collaboration |
| **Token Savings** | 53% Token reduction measured in complex business modifications |

## Quick Start

### Trigger Keywords

```
MemDDC, Load memory constraints for modification, Iterate according to DDD contract, memddc-init, memddc-update, memddc-sync
```

### Initialize Project

```
User: memddc-init
AI:   Scanning project...
      Detected: Java + Spring Boot + MyBatis-Plus
      Generated medical record: architecture.md, ddd-model.md, mem-snapshot.json
      Checkup complete, three-tier index established
```

### Modify Code

```
User: Modify SysDept department status field

AI:   Loading medical record...
      Located: SysDept → {entity, mapper, service, controller, views[]}
      File path: ruoyi-admin/src/main/java/.../domain/SysDept.java
               ruoyi-admin/src/main/resources/mapper/system/SysDeptMapper.xml
      Conforms to DDD constraints, starting modification...
      Modification complete, related documents synced
```

## Medical Record Structure (mem-snapshot.json)

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

## Workflow

1. **Checkup Phase** (memddc-init): Scan code → Generate record → Build index
2. **Consultation Phase** (modify code): Load record → Locate files → Modify with constraints
3. **Follow-up Phase** (memddc-sync): Compare changes → Sync docs → Update record

## Measured Results

Tested on RuoYi-Vue full-stack project:

| Scenario | With MemDDC | Without | Savings |
|----------|-------------|---------|---------|
| Project description | ~49,000 token | ~77,000 token | **36%** |
| Business modification | ~18,000 token | ~38,000 token | **53%** |
| Conversation rounds | 4 rounds | 6-10 rounds | **60%** |

## Directory Structure

```
project/
├── .memddc/                    # Medical record directory
│   ├── mem-snapshot.json       # Main medical record (three-tier index)
│   ├── vcs-log-analysis.md    # Medical history (Git commits)
│   ├── file-tree-analysis.md   # Checkup report (structure analysis)
│   └── docs/                   # Detailed inspection reports
│       ├── architecture.md      # System architecture
│       ├── ddd-model.md         # Domain model
│       └── api.md              # API documentation
└── [Project Source]
```

## Use Cases

- **Team Collaboration**: Unified records, new members get up to speed quickly
- **Complex Architecture**: DDD constraints, prevent reckless modifications
- **Legacy Systems**: Checkup report before refactoring
- **Long-term Maintenance**: Record decision history, understand design intent

## Tech Stack Support

| Language/Framework | Doc Generation | DDD Modeling | Memory Compression |
|--------------------|----------------|--------------|-------------------|
| Java/Spring | ✅ | ✅ | ✅ |
| Python/Django | ✅ | ✅ | ✅ |
| Go/Gin | ✅ | ✅ | ✅ |
| Vue/React | ✅ | ⚠️ | ✅ |

## Versions

- **v1.0.2** (current): Three-tier index + Relation mapping + VCS analysis
- **v1.0.1**: Team collaboration + Smart triggers

## Links

- GitHub: <https://github.com/qihao123/memddc-ai-skill>
- Email: <qihoo2017@gmail.com>
