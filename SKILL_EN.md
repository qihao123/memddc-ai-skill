# MemDDC

## Skill Information

- **Skill Name**: MemDDC
- **Version**: 1.0.1
- **Author**: qihao123
- **Description**: Team-oriented project documentation management and code iteration intelligent tool, providing automatic document generation, DDD model management, memory compression, code style unification, and intelligent triggering
- **Trigger Keywords**: MemDDC, Load memory constraints for modification, Iterate and update according to DDD contract, memddc-init, memddc-update, memddc-sync
- **Applicable Scenarios**: Team collaboration development, Complex architecture iteration, Legacy system refactoring, Long-term multi-person maintenance with AI governance

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

## Core Functions

### 1. Initialization Process (Triggered on First Use or Code Changes)

#### 1.1 Intelligent Project Scanning

- **Full Code Scanning**: Deep scanning of project directories, source code structure, entities, services, database logic, API interfaces, configuration files, etc.
- **Change Detection**: Compare version history, precisely identify new, modified, deleted files
- **Project Feature Recognition**: Automatically identify project type, programming language, framework, architecture pattern
- **Impact Assessment**: Assess the impact scope of code changes on the overall project

#### 1.2 Multi-Strategy Document Generation

Automatically select document generation strategy based on recognition results:

**General Documents (All Project Types)**:
- `.memddc/docs/architecture.md` - System architecture document
- `.memddc/docs/business.md` - Business document
- `.memddc/docs/api.md` - API interface document
- `.memddc/docs/database.md` - Database design document
- `.memddc/docs/development.md` - Development guide

**By Programming Language**:
| Language | Specific Documents |
|----------|-------------------|
| Java | `.memddc/docs/java-classes.md`, `.memddc/docs/spring.md`, `.memddc/docs/mybatis.md` |
| Python | `.memddc/docs/python-modules.md`, `.memddc/docs/django.md`, `.memddc/docs/flask.md` |
| Go | `.memddc/docs/go-packages.md`, `.memddc/docs/gin.md` |
| JavaScript/TypeScript | `.memddc/docs/js-modules.md`, `.memddc/docs/react.md`, `.memddc/docs/vue.md`, `.memddc/docs/node-api.md` |
| Rust | `.memddc/docs/rust-crates.md` |

**By Architecture Pattern**:
| Architecture | Documents |
|-------------|-----------|
| DDD | `.memddc/docs/ddd-model.md`, `.memddc/docs/bounded-contexts.md` |
| Microservices | `.memddc/docs/services.md`, `.memddc/docs/service_mesh.md` |
| MVC | `.memddc/docs/mvc-structure.md` |
| MVVM | `.memddc/docs/mvvm-structure.md` |

**Diagram Documents (Using Mermaid Syntax)**:
- `.memddc/docs/diagrams/architecture.mmd` - Architecture diagram
- `.memddc/docs/diagrams/flow.mmd` - Flowchart
- `.memddc/docs/diagrams/sequence.mmd` - Sequence diagram
- `.memddc/docs/diagrams/er.mmd` - ER diagram

#### 1.3 DDD Domain Model

- **Bounded Contexts**: Boundary definitions, context mapping, context relationships
- **Aggregates**: Aggregate roots, entities, value objects, domain events
- **Domain Services**: Service definitions, responsibility boundaries, collaboration relationships
- **Domain Rules**: Business rules, invariants, constraint conditions
- **Tactical Design**: Entity design, value object design, domain service design

#### 1.4 Intelligent Memory Compression

- **Document Compression Package**: `.memddc/snapshots/docs-compressed.zip` - Retain complete detailed documents
- **Memory Snapshot**: `.memddc/snapshots/mem-snapshot.json` - Intelligently compress core information
  - Program structure information: Directory structure, module division, dependency relationships
  - File description information: File functions, core logic, key APIs
  - Code style standards: Project code style rules
  - Domain model summary: DDD boundaries, aggregates, entities

### 2. Auto-loading Process (Executed Each Time Skill is Triggered)

- **Change Detection**: First check which files have changed since last synchronization
- **Smart Loading**: Only load document fragments related to changes, not all documents
- **Context Construction**: Combine compressed memory with change information to generate precise context
- **Impact Analysis**: Analyze change impact scope, identify related documents that need synchronization

### 3. Iterative Modification Process

- **Fast Memory Loading**: Automatically load latest compressed memory snapshot after triggering
- **Change Awareness**: Understand the scope and content of this modification
- **DDD Constraints**: Ensure modifications conform to domain models and business contracts
- **Consistency Guarantee**: Automatically synchronize and update related documents after modification

### 4. Synchronization Compression Closed Loop

- **Change Comparison**: Record all code changes for this session
- **Document Synchronization**: Update affected Markdown documents
- **Model Update**: Synchronize DDD model definitions
- **Memory Archiving**: Merge decisions, update memory snapshots
- **Consistency Verification**: Ensure code, documents, models, memory are consistent

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

### Configuration File (config.json)

```json
{
  "version": "1.0.1",
  "project": {
    "name": "Project Name",
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

## Workflow

### Initialization Phase

1. Detect project features (type, language, framework, architecture)
2. Select matching document generation strategy
3. Full code scanning
4. Generate all applicable documents
5. Build DDD domain model
6. Create initial memory snapshot
7. Create `.memddc` directory structure

### Trigger Detection Phase

1. Listen for code change events
2. Analyze change type and scope
3. Determine documents that need updating
4. Construct change context

### Iterative Modification Phase

1. Load relevant memory fragments
2. Inject context constraints
3. Execute modifications according to DDD boundaries
4. Real-time consistency verification

### Synchronization Closed Loop Phase

1. Compare code changes
2. Update related documents
3. Synchronize DDD model
4. Re-compress memory
5. Verify four-party consistency

## Technical Implementation

### Core Modules

1. **Project Scanner**
   - Deep directory structure analysis
   - Multi-language source code parsing
   - Dependency relationship analysis
   - API interface analysis
   - Database logic analysis
   - Configuration file analysis
   - Change Detector

2. **Strategy Selector**
   - Project type recognition
   - Programming language recognition
   - Framework recognition
   - Architecture pattern recognition
   - Optimal strategy matching

3. **Document Generator**
   - Architecture document generation
   - Business document generation
   - API document generation
   - Database document generation
   - Language-specific document generation
   - Architecture-specific document generation
   - Mermaid diagram generation

4. **DDD Model Builder**
   - Bounded context identification
   - Aggregate root analysis
   - Entity boundary definition
   - Value object design
   - Domain service extraction
   - Domain event identification

5. **Memory Management System**
   - Intelligent document compression
   - Memory snapshot generation
   - Historical decision recording
   - Context injection
   - Incremental updates
   - Conflict detection

6. **Change Tracker**
   - Code change detection
   - Document synchronization updates
   - Model consistency verification
   - Impact analysis

7. **Team Collaboration Manager**
   - Configuration synchronization
   - Conflict detection
   - Permission management
   - Version control integration

### Active Request Capability

Skill can actively request necessary information:

```
[MemDDC] Detected that project uses database, but no database design document found.
Please provide one of the following:
1. Database table structure (CREATE TABLE statements or ER diagram)
2. Existing database connection info (I will reverse-engineer from existing database)
3. Business requirement document (I will infer database design from requirements)

Input "skip" to skip this step.
Input "pause" to pause document generation, continue later.
```

Supported active request content types:
- Database table structure samples
- API interface document samples
- Existing code samples
- Business requirement documents
- Architecture design documents
- Third-party service integration documents
- Security requirement documents

## Configuration Options

### Basic Configuration

- `projectRoot`: Project root directory path
- `memddcPath`: MemDDC storage directory, default is `./.memddc`
- `docOutputPath`: Document output path, default is `./.memddc/docs`
- `dddModelPath`: DDD model file path, default is `./.memddc/ddd-model.md`
- `memSnapshotPath`: Memory snapshot path, default is `./.memddc/mem-snapshot.json`

### Trigger Configuration

- `triggers.codeChange`: Code change trigger, default is `true`
- `triggers.structureChange`: Directory structure change trigger, default is `true`
- `triggers.configChange`: Config file change trigger, default is `true`
- `triggers.manual`: Manual trigger, default is `true`
- `triggers.scheduled`: Scheduled trigger, default is `false`

### Document Configuration

- `document.types`: Document type list
- `document.includeDiagrams`: Whether to include diagrams, default is `true`
- `document.autoUpdate`: Auto-update on changes, default is `true`

### Team Configuration

- `team.shared`: Team sharing mode
- `team.members`: Team member list
- `team.syncBranch`: Synchronization branch

### Advanced Configuration

- `scanDepth`: Directory scan depth, default is 5
- `compressionLevel`: Compression level, default is 7 (0-9)
- `contextInjectionThreshold`: Context injection threshold, default is 80%

## Usage Examples

### Initialize Project

```
User: MemDDC Initialize Project
Skill: Starting to scan project structure...
      Detected: Java + Spring Boot + DDD Architecture
      Selected Strategy: Java Backend + DDD Document Set
      Starting document generation...
```

### Trigger Code Modification

```
User: Modified UserService.java, added new query method
Skill: Detected code change
      Loading relevant memory...
      Updating API document
      Updating DDD model
      Synchronization complete
```

### Team Collaboration

```
UserA: MemDDC Updated business document
Skill: Detected document update
      Synchronizing to team configuration...
      Notifying other members...
      Conflict detection: None
      Synchronization complete
```

## Notes

1. **First Use**: Ensure project directory exists and contains source code files
2. **Permission Requirements**: Need read/write permissions for project and `.memddc` directories
3. **Team Collaboration**: Recommend including `.memddc` directory in version control
4. **Performance Considerations**: Large project initialization may take longer
5. **Backup Recommendations**: Recommend backing up `.memddc` directory before major modifications

## Troubleshooting

### Common Issues

1. **Initialization Failure**
   - Check project directory permissions
   - Ensure project contains source code files
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

## License

MIT License

## Contact

- Project Homepage: <https://github.com/qihao123/memddc-ai-skill>
- Author: qihao123
- Email Support: <qihoo2017@gmail.com>
