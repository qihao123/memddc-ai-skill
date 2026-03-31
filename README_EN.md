# MemDDC Skill

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.1-blue.svg" alt="version">
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="license">
  <img src="https://img.shields.io/badge/AI-Kimi%202.5-purple.svg" alt="ai">
</p>

<p align="center">
  <b>Documentation-Driven Development Assistant</b><br>
  Reduce Token consumption by 23%, improve code readability and business alignment
</p>

---

## 📋 Table of Contents

- [Core Benefits](#-core-benefits)
- [Quick Start](#-quick-start)
- [Detailed Usage Guide](#-detailed-usage-guide)
- [Performance Comparison](#-performance-comparison)
- [Version Info](#-version-info)
- [Examples](#-examples)
- [Best Practices](#-best-practices)

---

## 🎯 Core Benefits

### 💰 Significantly Reduce Token Consumption

Tested with Kimi 2.5 (same codebase analysis task):

| Metric | Without Skill | With MemDDC | Improvement |
|--------|--------------|-------------|-------------|
| **Token Usage** | ~170,000 | ~130,000 | **↓ 23.5%** |
| **Output Quality** | Generic tech description | Business-context aware | **↑ Readability** |
| **Interaction Steps** | Multiple clarification rounds | Direct & precise | **↓ Steps** |
| **Processing Time** | Baseline | Est. -10% | **↑ Efficiency** |

### 🚀 Why It Works

```
Traditional Approach:            MemDDC Approach:
───────────────────              ───────────────
User asks                        User asks
   ↓                                ↓
AI: Show me the code        AI: [Load .memddc/ docs]
   ↑                                ↓
User pastes code            AI: Answer based on context
   ↓                                ↓
AI analyzes...              Precise output
   ↓
Multiple rounds...
```

**Core Principles**:
1. **Pre-scan & Persist**: Full project scan during initialization
2. **Context Reuse**: Reference documents instead of re-analyzing code
3. **Precise Constraints**: DDD models guide code generation

---

## 🚀 Quick Start

### Step 1: Trigger Initialization

In your project root directory, say to AI:

```
MemDDC initialize
```

Or:

```
Documentation-driven initialize
```

### Step 2: Confirm Generation

AI will scan your project and prompt:

```
📁 Will create .memddc/ directory:
   ├── architecture.md      # Project architecture
   ├── ddd-model.md         # DDD domain model
   ├── api.md              # API documentation
   ├── database.md         # Database design
   └── development.md      # Development guide
```

Reply **"Confirm"** to generate.

### Step 3: Start Using

After initialization, simply describe your needs:

```
User: Modify order module to add cancellation feature

AI (auto-loaded .memddc/ddd-model.md):
   Based on domain model, Order aggregate has methods:
   - create()
   - pay()
   - ship()
   
   Suggest adding cancel() method and trigger OrderCancelled event.
   This will affect:
   1. ddd-model.md - Update Order aggregate
   2. api.md - Add cancellation endpoint
   
   Confirm to proceed?
```

---

## 📖 Detailed Usage Guide

### 📝 Trigger Keywords

| Keyword | Purpose |
|---------|---------|
| `MemDDC` | Interactive mode, list available actions |
| `MemDDC initialize` | First time use, generate full documentation |
| `MemDDC update` | Sync docs after code changes |
| `Load memory constraints` | Manually load docs as context |
| `Modify per DDD contract` | Code changes based on domain model |
| `Documentation-driven` | Quick trigger |

### 🔄 Complete Workflow

#### Scenario A: New Project

```
1. Open project root directory
   ↓
2. Say: "MemDDC initialize"
   ↓
3. AI scans project, generates .memddc/ directory
   ↓
4. Review and refine generated docs
   ↓
5. Start coding with AI referencing docs
```

#### Scenario B: Feature Iteration

```
1. Describe requirement: "Add user points feature"
   ↓
2. AI auto-loads ddd-model.md
   ↓
3. AI suggests:
   - Add points field to User aggregate
   - Create PointsRecord entity
   - Add domain event: PointsEarned
   ↓
4. AI generates code after confirmation
   ↓
5. Say: "MemDDC update" to sync docs
```

#### Scenario C: Legacy Project Takeover

```
1. Say: "MemDDC initialize"
   ↓
2. AI scans legacy code, generates:
   - Directory structure analysis
   - Identified domain concepts
   - API endpoint inventory
   - Database table relationships
   ↓
3. Read generated docs to understand project
   ↓
4. Reference docs when modifying code
```

---

## 📊 Performance Comparison

### Test Environment

- **AI Model**: Kimi 2.5
- **Test Project**: Medium-scale Java Spring Boot project
- **Test Task**: Analyze order module and add refund feature

### Detailed Data

#### Token Consumption

| Phase | Without Skill | With MemDDC |
|-------|--------------|-------------|
| Understand code structure | 45,000 tokens | 5,000 tokens* |
| Analyze business logic | 60,000 tokens | 40,000 tokens |
| Solution discussion | 35,000 tokens | 15,000 tokens |
| Code generation | 30,000 tokens | 25,000 tokens |
| **Total** | **~170,000** | **~130,000** |

*With Skill: directly load pre-generated docs, no re-analysis needed

#### Key Improvements

| Dimension | Improvement |
|-----------|-------------|
| **Understanding Speed** | AI reads docs instead of line-by-line code analysis |
| **Business Alignment** | Business terms and rules persisted in docs |
| **Consistency** | Follow established architecture and coding standards |
| **Iteration Efficiency** | Say "update docs" after changes |

---

## 🏷️ Version Info

### Current: v1.0.1 (Stable) ⭐

**Status**: Production ready, recommended for use

**Features**:
- ✅ Intelligent documentation generation
- ✅ DDD domain modeling
- ✅ Smart memory compression
- ✅ Code change detection
- ✅ Team collaboration support

### History: v1.0.0

**Status**: Initial proof of concept

### Future: v1.0.2 (In Planning)

**Status**: Roadmap, expected Q2 2025

**Planned Features**:
- 🔨 More pragmatic feature positioning
- 🔨 Standardized document templates
- 🔨 Clearer boundary definitions
- 🔨 Large project performance optimization

**Design Philosophy Shift**:
- From "automation tool" to "development assistant"
- Honest feature boundary descriptions
- Focus on documentation-driven core value

---

## 💡 Examples

### Comparison: Tetris Game

See `example/` directory for two development approaches:

#### Approach 1: Direct AI (Quick Prototype)

```
Path: example/teris-game-useTraeSOLO/

Characteristics:
- Single file implementation (tetris.js)
- Quick idea validation
- No documentation

For: Personal prototypes, temporary scripts
```

#### Approach 2: MemDDC Documentation-Driven (Recommended)

```
Path: example/tetris-game-useMemDDC/

Characteristics:
- Complete DDD domain model
- Layered architecture
- Architecture documentation

For: Production projects, team collaboration, long-term maintenance
```

**Summary**:

| Dimension | Direct AI | MemDDC |
|-----------|-----------|--------|
| Token Usage | Higher (multiple clarification) | **↓ 23%** |
| Code Structure | Simple | **Layered** |
| Business Understanding | Technical view | **Business-aligned** |
| Knowledge Persistence | None | **Complete docs** |

---

## 🛠️ Tech Stack Support

| Tech Stack | Doc Generation | DDD Modeling | Memory Compression |
|------------|---------------|--------------|-------------------|
| Java / Spring Boot | ✅ | ✅ | ✅ |
| Python / Django / Flask | ✅ | ✅ | ✅ |
| Node.js / Express / Nest | ✅ | ✅ | ✅ |
| Go / Gin | ✅ | ✅ | ✅ |
| Frontend (React/Vue/Angular) | ✅ | ⚠️ | ✅ |
| Microservices | ✅ | ✅ | ✅ |

---

## 📚 Best Practices

### ✅ Recommended

1. **Initialize at project start**
   ```
   git init
   MemDDC initialize
   git add .memddc/
   ```

2. **Include .memddc/ in version control**
   ```
   # .gitignore
   # DO NOT ignore .memddc/
   # It's shared team knowledge
   ```

3. **Update docs after code changes**
   ```
   Modify code → Test → MemDDC update → Commit
   ```

### ❌ Avoid

- Adding .memddc/ to .gitignore
- Not updating docs after code changes
- Letting docs diverge from code

---

## 📄 License

MIT License

## 📧 Contact

- Project: https://github.com/qihao123/memddc-ai-skill
- Author: qihao123
- Email: qihoo2017@gmail.com

---

<p align="center">
  Made with ❤️ for better AI-assisted development
</p>
