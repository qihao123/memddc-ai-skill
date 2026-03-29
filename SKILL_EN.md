# MemDDC

## Skill Information

- **Skill Name**: MemDDC
- **Version**: 1.0.0
- **Author**: qihao123
- **Description**: Intelligent tool for project documentation management and code iteration, providing automatic document generation, DDD model management, memory compression, and code style unification
- **Trigger Keywords**: MemDDC, Load memory constraints for modification, Iterate and update according to DDD contract
- **Applicable Scenarios**: Complex architecture iteration, Legacy system refactoring, Long-term multi-person maintenance with AI governance

## Core Functions

### 1. Initialization Process (Auto-triggered on First Use)

- **Full Code Scanning**: Deep scanning of project directories, source code structure, entities, services, database logic, API interfaces, configuration files, etc.
- **Intelligent Document Generation**: Based on project type, programming language, and frameworks used, automatically reverse-generate complete docs/ software engineering documents:
  - **General Documents**:
    - Architecture Document: System architecture, module division, dependency relationships, deployment architecture, including detailed module descriptions and dependency diagrams
    - Business Document: Business processes, use case analysis, requirement specifications, user stories, including detailed business process descriptions and use case diagrams
    - Technical Document: API interface documentation, database design, algorithm descriptions, technology selection, including detailed API interface descriptions and database table structures
    - Development Document: Coding standards, development environment, testing strategies, deployment processes, including detailed development environment configuration and deployment steps
    - Diagram Documents: ER diagrams, flowcharts, sequence diagrams, architecture diagrams, using Mermaid syntax to generate detailed charts
  - **Java Backend Projects**:
    - Class Documentation: Detailed descriptions of all classes, inheritance relationships, implemented interfaces, including detailed functional descriptions and code examples for each class
    - Entity Mapping Documentation: Mapping relationships between entity classes and database tables, including detailed entity class definitions and table structures
    - Method Documentation: Parameters, return values, and functional descriptions of all methods, including detailed method signatures and examples
    - Spring Framework Documentation: Configuration files, Bean definitions, dependency injection, including detailed configuration descriptions and examples
    - MyBatis/Hibernate Documentation: ORM mappings, SQL statements, including detailed mapping configurations and SQL examples
  - **Python Backend Projects**:
    - Module Documentation: Functions and dependencies of all modules, including detailed module functional descriptions and dependency relationships
    - Class and Function Documentation: Detailed class and function descriptions, including detailed functional descriptions and code examples for each class and function
    - Django/Flask Framework Documentation: Route configuration, view functions, templates, including detailed route configurations and view function examples
    - Database Documentation: ORM models, migration scripts, including detailed model definitions and migration examples
  - **Frontend Projects**:
    - Component Documentation: Properties, methods, and events of all components, including detailed component definitions and usage examples
    - State Management Documentation: Redux/Vuex state management, including detailed state definitions and operation examples
    - API Call Documentation: Interaction interfaces between frontend and backend, including detailed API call examples
    - Routing Documentation: Frontend route configuration, including detailed route definitions and navigation examples
  - **Mobile App Projects**:
    - Page Documentation: Functions and navigation of all pages, including detailed page functional descriptions and navigation flowcharts
    - Component Documentation: Usage methods of custom components, including detailed component definitions and usage examples
    - API Call Documentation: Interaction interfaces with backend, including detailed API call examples
    - Permission Documentation: App permission configuration, including detailed permission configurations and usage examples
- **Detailed DDD Domain Model**: Automatically generate complete ddd-model.md domain model, including:
  - Bounded Contexts: Boundary definitions, context mapping, context relationships
  - Aggregates: Aggregate roots, entities, value objects, domain events
  - Domain Services: Service definitions, responsibility boundaries, collaboration relationships
  - Domain Rules: Business rules, invariants, constraint conditions
  - Tactical Design: Entity design, value object design, domain service design
- **Intelligent Memory Compression**: Generate original memory files and perform first-level dual compression:
  - Document Compression Package: Retain complete detailed documents
  - mem-snapshot.json Memory Snapshot: Intelligently compress core information to ensure AI can quickly understand
    - Program Structure Information: Includes project directory structure, module division, dependency relationships, etc. (code-related files only)
    - File Description Information: AI-generated file functional descriptions, core logic explanations, key APIs, etc. (code-related files only)
    - Code Style Standards: Project code style rules and best practices
    - File Filtering Mechanism: Automatically filter out unnecessary files, such as configuration files, log files, temporary files, etc.

### 2. Auto-loading Process (Executed Each Time Skill is Triggered)

- **Memory Snapshot Check**: When skill is triggered, first check if mem-snapshot.json file exists in project root directory
- **Auto-loading**: If memory snapshot exists, automatically read and parse its content, injecting core information into context
- **Document Integration**: Simultaneously check docs/ directory, loading key documents (such as architecture, class documents, etc.) as supplementary context
- **Caching Mechanism**: Cache loaded information to avoid repeated reading and improve efficiency of subsequent operations
- **Intelligent Context Injection**: Inject loaded information as context into conversation to ensure subsequent operations are based on same project understanding

### 3. Iterative Modification General Process (Executed Each Time Code is Modified/Features are Added)

- **Fast Memory Loading**: After triggering Skill, automatically load latest compressed memory snapshot without reading original code and complete documents
- **Intelligent Context Injection**: Inject compressed core information as context into large model to ensure strict adherence to historical architecture constraints
- **Precise Code Modification**: Complete new/modified/refactored code according to DDD boundaries and original business contracts, reducing context retrieval time
- **Real-time Validation**: Real-time validation during modification whether code conforms to domain model and architecture constraints

### 4. Configuration Options

- **Default Enabled**: Set `auto_load_snapshot` configuration item to `true`, automatically load memory snapshot by default
- **Configurable Scope**: Allow users to specify document types to load (such as architecture, API, DDD model, etc.) through configuration
- **Cache Settings**: Configurable cache size and expiration time to optimize memory usage
- **Loading Strategy**: Can choose to prioritize loading memory snapshots or detailed documents, adjusted according to specific scenarios

### 5. Post-modification Synchronization Compression Closed Loop (Enforced After Modification Ends)

- **Intelligent Change Detection**: Compare code changes, identify impact scope and change types
- **Document Synchronization Update**: Synchronously update corresponding detailed Markdown documents and DDD model definitions to ensure documents and code remain consistent
- **Intelligent Compression Optimization**: Re-execute lightweight compression updates on latest complete set of documents, retaining core information and reducing redundant content
- **Memory Snapshot Update**: Merge this modification decision, update memory snapshot and secondary compression archiving to ensure memory snapshot always reflects latest state
- **Consistency Verification**: Ensure strong consistency among code, documents, DDD, and memory compression to avoid information deviation

## File Directory Standards

- `/docs` - Full engineering original documents & AI lightweight compressed documents
- `/ddd-model.md` - Complete DDD domain model definition for the project
- `/mem-snapshot.json` - Global compressed long-term memory snapshot file

## Workflow

### Initialization Phase

1. Scan project structure, analyze source code files
2. Generate complete engineering documents (architecture, business, ER diagrams, flowcharts)
3. Build DDD domain model, define bounded contexts, aggregates, and entity boundaries
4. Create initial memory snapshot and compress archive

### Iterative Modification Phase

1. Load existing documents, DDD model, and memory snapshot
2. Inject context constraints to ensure code modifications conform to historical architecture decisions
3. Execute code modifications according to DDD boundaries and business contracts

### Closed-loop Update Phase

1. Compare code changes, update related documents and DDD model
2. Re-compress documents and memory snapshot
3. Ensure all materials remain up-to-date and lightweight

## Technical Implementation

### Core Modules

1. **Project Scanner**
   - Deep directory structure analysis
   - Multi-language source code file parsing
   - Dependency relationship identification and analysis
   - API interface analysis
   - Database logic analysis
   - Configuration file analysis
   - File filtering mechanism: Automatically filter out unnecessary files, such as configuration files, log files, temporary files, etc., keeping only code-related files
2. **Document Generator**
   - Detailed architecture document generation
   - Comprehensive business process document generation
   - Detailed API interface document generation
   - Database design document generation
   - Coding standards document generation
   - Multi-type chart automatic drawing (ER diagrams, flowcharts, sequence diagrams, architecture diagrams)
3. **DDD Model Builder**
   - Bounded context identification and mapping
   - Aggregate root analysis and design
   - Entity boundary definition and relationships
   - Value object identification and design
   - Domain service extraction and definition
   - Domain event identification and design
   - Domain rule extraction and organization
4. **Memory Management System**
   - Intelligent document compression algorithm
   - Efficient memory snapshot generation
   - Historical decision recording and management
   - Intelligent context injection mechanism
   - Incremental memory updates
   - Memory retrieval optimization
5. **Change Tracker**
   - Precise code change detection
   - Intelligent document synchronization updates
   - Model consistency verification
   - Change impact analysis
   - Automatic document updates

### Execution Logic

1. **Initialization Execution**
   - Check project structure and environment
   - Full code scanning and analysis
   - Identify project type, programming language, and frameworks used
   - Evaluate project size and complexity
   - Generate corresponding detailed software engineering documents according to project type
   - Build complete DDD domain model
   - Intelligently compress and generate memory snapshot
   - Verify integrity of documents and models
2. **Iterative Execution**
   - Fast loading of compressed memory snapshot
   - Intelligent context injection to reduce token consumption
   - Execute code modifications according to DDD boundaries and business contracts
   - Real-time validation of modification legitimacy
   - Provide modification suggestions and best practices
3. **Closed-loop Execution**
   - Precise detection of code changes
   - Intelligent analysis of change impact scope
   - Update detailed documents and DDD model
   - Re-compress and generate memory snapshot
   - Verify consistency among the four elements (code, documents, DDD, memory)

## Configuration Options

### Basic Configuration

- `projectRoot`: Project root directory path
- `docOutputPath`: Document output path, default is `./docs`
- `dddModelPath`: DDD model file path, default is `./ddd-model.md`
- `memSnapshotPath`: Memory snapshot path, default is `./mem-snapshot.json`

### Advanced Configuration

- `scanDepth`: Directory scan depth, default is 5
- `compressionLevel`: Compression level, default is 7 (0-9)
- `contextInjectionThreshold`: Context injection threshold, default is 80%
- `modelUpdateStrategy`: Model update strategy, default is `incremental`

## Usage Examples

### Initialize Project

To trigger MemDDC initialization process in Trae IDE:

1. Open a project file in the editor
2. Type `MemDDC` in the chat box and send
3. The skill will automatically scan the project and generate documents and memory snapshots

### Execute Code Modification

To load memory constraints and execute modifications in Trae IDE:

1. Open a project file in the editor
2. Type `MemDDC Load memory constraints for modification` in the chat box and send
3. The skill will automatically load memory snapshots and inject context constraints
4. Execute code modifications according to DDD boundaries and business contracts

### Iterate According to DDD Contract

1. Open a project file in the editor
2. Type `MemDDC Iterate and update according to DDD contract` in the chat box and send
3. The skill will automatically load memory snapshots and DDD models
4. Ensure code modifications conform to DDD domain models and architectural constraints

## Notes

1. **First Use**: Ensure project directory exists and contains source code files
2. **Permission Requirements**: Need read and write permissions for project directory
3. **Performance Considerations**: Large project initialization may take longer
4. **Version Control**: Recommend including generated documents and model files in version control
5. **Backup Recommendations**: Before executing major modifications, recommend backing up existing documents and model files

## Troubleshooting

### Common Issues

1. **Initialization Failure**
   - Check project directory permissions
   - Ensure project contains sufficient source code files
   - Check log files for specific errors
2. **Memory Loading Failure**
   - Check if memory snapshot file exists
   - Verify file format is correct
   - Try reinitializing the project
3. **Document Update Failure**
   - Check document directory permissions
   - Ensure sufficient disk space
   - Check log files for specific errors
4. **Model Consistency Issues**
   - Manually check consistency between DDD model and code
   - Try regenerating model files
   - Verify code modifications conform to domain model definitions

## Version History

- **v1.0.0** - Initial Version
  - Implemented project scanning and document generation
  - Supported DDD model building
  - Provided memory compression and management functions
  - Implemented complete workflow

## License

MIT License

## Contact

- Project Homepage: <https://github.com/qihao123/memddc-ai-skill>
- Author: qihao123
- Email Support: <qihoo2017@gmail.com>
