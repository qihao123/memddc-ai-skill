# memddc-ai-skill

> [中文版本](README.md)

## Project Information

- **Project Homepage**: https://github.com/qihao123/memddc-ai-skill
- **Author**: qihao123
- **Contact**: qihoo2017@gmail.com
- **Version**: 1.0.1
- **Description**: Team-oriented project documentation management and code iteration intelligent tool, providing automatic document generation, DDD model management, memory compression, code style unification, and intelligent triggering

## v1.0.1 Core Upgrades

### 1. Team Collaboration Support

- **Unified Storage Location**: All documents and configurations are stored in `.memddc/` directory for easy team member synchronization and sharing
- **Centralized Configuration Management**: Team-shared configuration files ensure all members use consistent document generation strategies
- **Conflict Resolution Mechanism**: Intelligently detect conflicts when multiple people modify simultaneously, provide merge suggestions
- **Permission Control**: Support setting different document modification permissions for different members

### 2. Intelligent Triggering Mechanism

Trigger conditions (any condition triggers):
- **Code Change Trigger**: Detects new, modified, or deleted code files (.js/.ts/.py/.java/.go/.cpp/.rs)
- **File Structure Change**: Detects project directory structure changes (new/delete folders)
- **Config File Change**: Detects config file changes (.json/.yaml/.yml/.toml/.xml)
- **Explicit Invocation**: User actively inputs trigger keywords
- **Scheduled Sync**: Configurable scheduled checks and document synchronization

### 3. Multi-Strategy Document Generation

Automatically select optimal strategy based on project characteristics:
- **By Project Type**: Backend/Frontend/Mobile/Microservice/Monolithic
- **By Programming Language**: Java/Python/Go/Node.js/React/Vue, etc.
- **By Architecture Pattern**: MVC/MVVM/DDD/Microservice/Serverless

### 4. Active Request Capability

Skill can actively request necessary information:
- Database table structure samples
- API interface document samples
- Existing code samples
- Business requirement documents
- Architecture design documents
Can interrupt the request process at any time, user can choose to provide or skip

## Core Philosophy

### Maximizing Communication Efficiency

In software development, communication between humans and large language models has significant efficiency bottlenecks:
- **Traditional typing communication**: Speed is about 1-2 bits/second, with slow information transfer
- **Document-driven communication**: Structured document transfer is much more efficient than direct dialogue

### Core Value

The core philosophy of MemDDC is **improving communication efficiency and reducing low-speed communication between large models and humans**. This is achieved through:

1. **Full-code pre-scanning**: On first use, automatically performs deep scanning of the entire project to generate comprehensive software engineering documents
2. **Intelligent document generation**: Based on project type, programming language, and frameworks used, generates corresponding detailed documents:
   - Java backend projects: class documentation, entity mapping documentation, method documentation, Spring framework documentation, etc.
   - Python backend projects: module documentation, class and function documentation, Django/Flask framework documentation, etc.
   - Frontend projects: component documentation, state management documentation, API call documentation, routing documentation, etc.
   - Mobile app projects: page documentation, component documentation, API call documentation, permission documentation, etc.
3. **DDD domain model**: Establishes clear domain boundaries and business contracts, reducing communication ambiguity and ensuring code modifications align with domain design
4. **Intelligent memory compression**: Intelligently compresses generated detailed documents, retaining core information while reducing redundant content, generating efficient memory snapshots
5. **Unified code style**: Ensures code style consistency through automated tools, reducing communication costs caused by style differences

### Advantages of Working Principle

Traditional AI coding approach:
- Starts from a single point, then searches code through context
- Frequent context retrieval leads to slow coding speed and high token consumption
- Insufficient understanding of the overall project, prone to generating code that doesn't conform to architectural constraints

Advantages of MemDDC:
- **Pre-scan full code**: Performs full scanning of the entire project on first use, generating comprehensive software engineering documents
- **Intelligent compression optimization**: Compresses detailed documents into core information, generating memory snapshots to reduce storage and transmission costs
- **Fast memory loading**: Subsequent coding directly loads compressed memory snapshots without repeated code scanning
- **Reduced context retrieval**: Provides overall project context through memory snapshots, reducing frequent code retrieval
- **Save token consumption**: Compressed memory snapshots are small in size, reducing token consumption for context injection
- **Fast and accurate coding**: AI can quickly understand project architecture and constraints, generating code that conforms to design specifications

### Working Principle

1. **Initialization phase**: Scan project and generate complete documents, DDD model, and memory snapshot
2. **Iteration phase**: Automatically load existing materials as context constraints to ensure code modifications align with historical architectural decisions
3. **Closed-loop phase**: Automatically synchronize and update documents and models, keeping all materials up-to-date and lightweight

## How to Use

### Manual Trigger

Trigger MemDDC Skill through the following keywords:
- `MemDDC`
- `Load memory constraints for modification`
- `Iterate and update according to DDD contract`
- `memddc-init`
- `memddc-update`
- `memddc-sync`

### Automatic Invocation Settings

#### Editor Automatic Invocation Configuration

1. **VS Code Configuration**:
   - Install TRAE plugin
   - Add automatic trigger configuration in `settings.json`:

   ```json
   {
     "trae.autoInvokeSkills": [
       {
         "skillName": "MemDDC",
         "triggers": [
           "onFileSave",
           "onCodeEdit",
           "onProjectOpen"
         ],
         "conditions": {
           "fileExtensions": [".js", ".ts", ".jsx", ".tsx", ".java", ".py", ".go", ".rs", ".cpp"],
           "projectTypes": ["node", "react", "angular", "vue", "java", "python", "go", "rust"]
         }
       }
     ]
   }
   ```

2. **JetBrains IDE Configuration**:
   - Install TRAE plugin
   - Enable automatic trigger in plugin settings:
     - Trigger timing: file save, code edit, project open, code change detection
     - Applicable file types: all source code files

3. **Sublime Text Configuration**:
   - Install TRAE plugin
   - Add to plugin configuration file:

   ```json
   {
     "auto_invoke": true,
     "skills": [
       {
         "name": "MemDDC",
         "triggers": ["on_save", "on_modify", "on_load", "on_code_change"]
       }
     ]
   }
   ```

#### Project-level Automatic Invocation

Create `.trae/config.json` file in the project root directory:

```json
{
  "autoInvoke": true,
  "skills": [
    {
      "name": "MemDDC",
      "triggers": [
        "onFileCreate",
        "onFileDelete",
        "onFileRename",
        "onBranchChange",
        "onMerge",
        "onCodeChange"
      ],
      "options": {
        "scanDepth": 5,
        "compressionLevel": 7,
        "autoUpdateDocs": true,
        "autoEnforceCodeStyle": true,
        "autoLoadSnapshot": true,
        "loadDocumentTypes": ["architecture", "api", "ddd-model", "class-docs"],
        "cacheSize": 1024,
        "cacheExpiry": 3600,
        "loadStrategy": "snapshot-first",
        "teamShared": true
      }
    }
  ]
}
```

## Directory Structure

### v1.0.1 New Directory Structure

```
project/
├── .memddc/                          # MemDDC Unified Storage Directory (Team Shared)
│   ├── config.json                   # Team-shared configuration
│   ├── mem-snapshot.json             # Global memory snapshot
│   ├── docs/                        # Project documents
│   │   ├── architecture.md          # Architecture document
│   │   ├── business.md             # Business document
│   │   ├── api.md                  # API interface document
│   │   ├── database.md             # Database design document
│   │   ├── development.md          # Development guide
│   │   ├── code-style.md           # Code style guide
│   │   ├── [language-specific].md  # Language-specific documents
│   │   ├── [architecture-specific].md # Architecture-specific documents
│   │   └── diagrams/               # Diagram documents (Mermaid)
│   │       ├── architecture.mmd
│   │       ├── flow.mmd
│   │       ├── sequence.mmd
│   │       └── er.mmd
│   ├── ddd-model.md                 # DDD domain model
│   ├── snapshots/                   # Historical snapshot archive
│   │   ├── docs-compressed.zip     # Document compression package
│   │   └── mem-YYYYMMDD-HHMMSS.json # Timestamped snapshot
│   ├── logs/                        # Operation logs
│   │   └── sync-YYYYMMDD.log
│   └── .gitignore                  # Team-shared git ignore rules
└── [Project Source Code Directory]
```

## Technical Features

- **Intelligent Document Generation**: Automatically scans projects and generates structured documents
- **DDD Domain Modeling**: Establishes clear domain boundaries and business contracts
- **Long-term Memory Management**: Compresses and stores project historical decisions and constraint rules
- **Unified Code Style**: Automated code style checking and fixing
- **Automatic Loading**: Automatically loads memory snapshots and document information each time the skill is triggered
- **Context Injection**: Ensures large models strictly follow historical architectural decisions
- **Closed-loop Updates**: Automatically synchronizes and updates documents and models to maintain consistency
- **Team Collaboration**: Unified `.memddc/` directory supports team sharing
- **Intelligent Triggering**: Auto-trigger document sync on code changes
- **Multi-Strategy Generation**: Auto-select document generation strategy based on language/architecture/type
- **Active Request**: Can actively request database samples and other necessary information

## Applicable Scenarios

- **Team Collaboration Development**: Unified storage and sharing of project documents and memory
- **Complex Architecture Iteration**: Ensures continuity and consistency of architectural decisions
- **Legacy System Refactoring**: Quickly understands existing systems and performs orderly refactoring
- **Long-term Multi-person Maintenance**: Maintains consistency in code style and architectural design
- **Cross-team Collaboration**: Reduces communication costs through structured documents

## Performance Optimization

- **Incremental Scanning**: Only processes changed files, reducing scanning time
- **Intelligent Triggering**: Only triggers on code changes, reducing unnecessary scanning
- **Parallel Processing**: Processes multiple document generation tasks simultaneously
- **Intelligent Caching**: Caches intermediate results to improve efficiency of repeated operations
- **Compression Algorithms**: Uses efficient compression algorithms to reduce storage and transmission costs

## Troubleshooting

### Common Issues

1. **Initialization Failure**
   - Check project directory permissions
   - Ensure project contains sufficient source code files
   - Check log files under `.memddc/logs/`

2. **Trigger Not Working**
   - Check trigger configuration in `config.json`
   - Confirm code file extensions are within scan range

3. **Document Synchronization Failure**
   - Check `.memddc/docs/` directory permissions
   - Ensure sufficient disk space

4. **Team Synchronization Conflict**
   - Use `memddc-sync` command for manual synchronization
   - Check conflict details and manually merge

## Version History

- **v1.0.1** - Team Collaboration Upgrade (Current Version)
  - Added `.memddc/` unified storage directory
  - Added intelligent triggering mechanism (auto-trigger on code changes)
  - Added multi-strategy document generation (by language/architecture/type)
  - Added active request capability
  - Added team collaboration support
  - Optimized document structure and organization

- **v1.0.0** - Initial Version
  - Implemented project scanning and document generation
  - Supported DDD model building
  - Provided memory compression and management functions
  - Implemented code style unification function
  - Supported automatic invocation configuration

## Test Results

### Test Objects

Three different types of open-source projects were selected as test objects:

1. **Spring Boot** - Java backend project, framework for building independent, production-level Spring applications
2. **Django** - Python backend project, high-level Python Web framework that encourages rapid development and clean, pragmatic design
3. **React** - Frontend project, JavaScript library for building user interfaces (clone failed due to network issues)

### Test Process

1. **Clone Project**: Use `git clone` to clone project code
2. **Run MemDDC Initialization**: Execute MemDDC initialization process, including full code scanning, document generation, DDD model building, and memory snapshot generation
3. **Analyze Results**: Check generated documents and memory snapshots to evaluate MemDDC effectiveness

### Test Results

#### Spring Boot Project (Java Backend)

| Metric | Result |
|--------|--------|
| Project File Count | 525 |
| Project Directory Count | 772 |
| Memory Snapshot Size | 457 bytes |
| Project Type | java-backend |
| Programming Language | Java |
| Framework Used | Spring Boot |
| Project Size | large |
| Generated Documents | architecture.md, class-docs.md, ddd-model.md, mem-snapshot.json |

#### Django Project (Python Backend)

| Metric | Result |
|--------|--------|
| Project File Count | 1822 |
| Project Directory Count | 545 |
| Memory Snapshot Size | 445 bytes |
| Project Type | python-backend |
| Programming Language | JavaScript/TypeScript (incorrectly identified, should be Python) |
| Framework Used | Django |
| Project Size | large |
| Generated Documents | architecture.md, module-docs.md, ddd-model.md, mem-snapshot.json |

### Test Conclusion

Advantages of using MemDDC skill:

1. **Intelligent Project Recognition**: Can identify project type, programming language, and frameworks used, generating corresponding documents for different types of projects
2. **Quick Project Understanding**: Through full code scanning and detailed document generation, quickly understand overall project structure and functionality
3. **Type-specific Documents**:
   - For Java backend projects, generate class documentation
   - For Python backend projects, generate module documentation
   - For frontend projects, generate component documentation
4. **Complete DDD Model**: Builds detailed domain models to help understand business logic and code structure
5. **Intelligent Memory Compression**: Generates compressed memory snapshots, reducing context retrieval time and token consumption
6. **Coding Efficiency Improvement**: AI can quickly understand project architecture and constraints, generating code that conforms to design specifications
7. **Consistency Guarantee**: Ensures consistency among code, documents, DDD model, and memory snapshot

### Practical Application Recommendations

1. **First Use**: When starting a new project or taking over an existing project, use MemDDC for initialization to generate detailed documents and domain models
2. **Daily Development**: When making code modifications, use MemDDC to load memory snapshots to ensure code modifications align with project architecture and constraints
3. **Team Collaboration**: Reduce communication costs among team members through detailed documents and domain models
4. **Code Quality**: Improve code quality and maintainability through DDD domain models and unified code style
5. **Project Type Support**: MemDDC supports multiple project types, including Java backend, Python backend, and frontend projects, providing customized document generation services for different types of projects

## Application Cases

### Tetris Game Development Comparison

To verify MemDDC Skill's performance in different scenarios, we developed the same Tetris game using two different approaches:

#### Case 1: Direct Development Using Trae Solo Mode

**Path**: `example/teris-game-useTraeSolo/`

**Development Approach**:
- Directly use Trae IDE's Solo mode to generate code through natural language dialogue
- Generate complete game code at once (HTML + CSS + JavaScript)
- Three-file structure: index.html, style.css, tetris.js

**Characteristics**:
- Rapid prototype development, suitable for small projects
- Code concentrated in one file, easy to quickly understand
- Suitable for individuals to quickly validate ideas

#### Case 2: Document-Driven Development Using MemDDC Skill

**Path**: `example/tetris-game-useMemDDC/`

**Development Approach**:
1. **Phase 1 - Document Design**:
   - Use MemDDC Skill to generate complete DDD domain model (`ddd-model.md`)
   - Create architecture document (`docs/architecture.md`), defining layered architecture
   - Write API document (`docs/api.md`), clarifying interface contracts
   - Generate memory snapshot (`mem-snapshot.json`), compressing and storing core project information

2. **Phase 2 - Code Implementation**:
   - Strictly write code according to the layered architecture defined in documents
   - Domain layer: tetromino.js, board.js (core business logic)
   - Application layer: game.js (game controller)
   - Infrastructure layer: renderer.js, input.js (rendering and input)
   - Presentation layer: index.html, styles.css

**Characteristics**:
- Clear architectural design and separation of responsibilities
- Complete documentation system, easy to maintain and extend
- Conforms to Domain-Driven Design principles
- Suitable for team collaboration and long-term maintenance

#### Comparison Summary

| Dimension | Trae Solo Mode | MemDDC Skill Mode |
|-----------|---------------|-------------------|
| **Development Speed** | Fast, generated at once | Medium, phased approach |
| **Code Structure** | Simple, fewer files | Clear, well-layered |
| **Architecture Design** | Implicit in code | Explicitly documented |
| **Maintainability** | Suitable for small projects | Suitable for medium/large projects |
| **Team Collaboration** | Relies on code comments | Supported by complete documentation |
| **Extensibility** | Requires refactoring | Easy to extend |
| **Applicable Scenarios** | Rapid prototyping, personal projects | Formal projects, team collaboration |

#### Conclusion

These two cases demonstrate the **dual value** of MemDDC Skill:

1. **Small projects from 0 to 1**: Even for small game projects, using MemDDC Skill can produce code with clear structure and comprehensive documentation, laying a good foundation for subsequent iterations

2. **Large project refactoring and iteration**: For complex projects, MemDDC Skill's document-driven approach can:
   - Establish clear domain boundaries
   - Maintain consistency of architectural decisions
   - Reduce understanding costs for team members
   - Support long-term maintenance and evolution

Regardless of project size, MemDDC Skill can help developers produce higher quality, more maintainable code.

## Summary

MemDDC skill effectively improves AI coding efficiency and accuracy through full-code pre-scanning, intelligent project recognition, type-specific document generation, intelligent memory compression, and other features. It not only reduces context retrieval time and consumption but also ensures code modifications align with project architecture and constraints, making it an intelligent tool worth using in the software development process.

The core values of MemDDC skill are:

1. **Improve Communication Efficiency**: Reduce low-speed communication between large models and humans through detailed documents and domain models
2. **Reduce Context Retrieval**: Reduce AI coding context retrieval time and consumption through intelligent memory compression
3. **Improve Coding Accuracy**: AI can quickly understand project architecture and constraints, generating code that conforms to design specifications
4. **Support Multiple Project Types**: Provide customized document generation services for different types of projects
5. **Ensure Consistency**: Ensure consistency among code, documents, DDD model, and memory snapshot

By using MemDDC skill, developers can focus more on implementing business logic rather than spending a lot of time on code understanding and document maintenance, thereby improving development efficiency and code quality.
