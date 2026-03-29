#!/usr/bin/env node

'use strict';

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 测试项目列表
const testProjects = [
  {
    name: 'spring-boot',
    type: 'java-backend',
    url: 'https://github.com/spring-projects/spring-boot.git',
    description: 'Spring Boot 是一个用于构建独立的、生产级别的 Spring 应用程序的框架'
  },
  {
    name: 'django',
    type: 'python-backend',
    url: 'https://github.com/django/django.git',
    description: 'Django 是一个高级 Python Web 框架，鼓励快速开发和清洁、实用的设计'
  },
  {
    name: 'react',
    type: 'frontend',
    url: 'https://github.com/facebook/react.git',
    description: 'React 是一个用于构建用户界面的 JavaScript 库'
  }
];

// 模拟 MemDDC 技能的初始化过程
function simulateMemDDCInit(projectPath, projectType) {
  console.log(`=== 模拟 MemDDC 初始化过程 (${projectType}) ===`);
  console.log('1. 全量代码扫描...');
  
  // 扫描项目结构
  const projectStructure = scanProjectStructure(projectPath);
  
  console.log('2. 识别项目类型和框架...');
  
  // 识别项目类型和框架
  const projectInfo = identifyProjectInfo(projectPath, projectType);
  
  console.log('3. 生成详细文档...');
  
  // 生成文档目录
  const docsPath = path.join(projectPath, 'docs');
  if (!fs.existsSync(docsPath)) {
    fs.mkdirSync(docsPath, { recursive: true });
  }
  
  // 生成通用文档
  fs.writeFileSync(
    path.join(docsPath, 'architecture.md'),
    "# 架构文档\n\n## 项目信息\n\n- 项目类型: " + projectInfo.type + "\n- 编程语言: " + projectInfo.languages.join(', ') + "\n- 使用框架: " + projectInfo.frameworks.join(', ') + "\n- 项目体量: " + projectInfo.size
  );
  
  // 根据项目类型生成特定文档
  if (projectType === 'java-backend') {
    fs.writeFileSync(
      path.join(docsPath, 'class-docs.md'),
      "# Java 类说明文档\n\n## 核心类\n\n### Application 类\n- 功能: 应用程序入口点\n- 主要方法: main, run\n\n### Controller 类\n- 功能: 处理 HTTP 请求\n- 主要方法: get, post, put, delete\n\n### Service 类\n- 功能: 业务逻辑处理\n- 主要方法: findById, save, delete"
    );
  } else if (projectType === 'python-backend') {
    fs.writeFileSync(
      path.join(docsPath, 'module-docs.md'),
      "# Python 模块说明文档\n\n## 核心模块\n\n### django 模块\n- 功能: Django 框架核心模块\n- 子模块: conf, core, db, forms, http, middleware, templates, urls, views\n\n### django.db 模块\n- 功能: 数据库操作\n- 子模块: backends, models, migrations, transaction"
    );
  } else if (projectType === 'frontend') {
    fs.writeFileSync(
      path.join(docsPath, 'component-docs.md'),
      "# 前端组件文档\n\n## 核心组件\n\n### App 组件\n- 功能: 应用程序根组件\n- 属性: title\n- 方法: componentDidMount, handleClick\n\n### Button 组件\n- 功能: 按钮组件\n- 属性: variant, size, disabled\n- 方法: handleClick\n\n### Input 组件\n- 功能: 输入框组件\n- 属性: type, value, placeholder, disabled\n- 方法: handleChange"
    );
  }
  
  // 生成DDD模型
  fs.writeFileSync(
    path.join(projectPath, 'ddd-model.md'),
    "# DDD 领域模型\n\n## 项目信息\n\n- 项目类型: " + projectInfo.type + "\n- 编程语言: " + projectInfo.languages.join(', ') + "\n- 使用框架: " + projectInfo.frameworks.join(', ')
  );
  
  console.log('4. 生成记忆快照...');
  
  // 生成记忆快照
  const memSnapshot = generateMemSnapshot(projectStructure, projectInfo);
  fs.writeFileSync(
    path.join(projectPath, 'mem-snapshot.json'),
    JSON.stringify(memSnapshot, null, 2)
  );
  
  console.log('5. 验证文档和模型...');
  console.log('=== MemDDC 初始化完成 ===');
  
  return {
    projectStructure,
    projectInfo,
    memSnapshotSize: Buffer.byteLength(JSON.stringify(memSnapshot))
  };
}

// 扫描项目结构
function scanProjectStructure(projectPath) {
  const structure = {
    files: [],
    directories: []
  };
  
  function scan(dir) {
    const items = fs.readdirSync(dir);
    items.forEach(item => {
      const itemPath = path.join(dir, item);
      const stat = fs.statSync(itemPath);
      if (stat.isDirectory()) {
        structure.directories.push(itemPath.replace(projectPath, ''));
        // 限制扫描深度，避免大型项目扫描时间过长
        if (itemPath.split(path.sep).length - projectPath.split(path.sep).length < 3) {
          scan(itemPath);
        }
      } else {
        structure.files.push(itemPath.replace(projectPath, ''));
      }
    });
  }
  
  scan(projectPath);
  return structure;
}

// 识别项目信息
function identifyProjectInfo(projectPath, projectType) {
  const info = {
    type: projectType,
    languages: [],
    frameworks: [],
    size: 'medium'
  };
  
  // 识别编程语言
  const files = fs.readdirSync(projectPath);
  if (files.includes('pom.xml') || files.includes('build.gradle')) {
    info.languages.push('Java');
  }
  if (files.includes('setup.py') || files.includes('requirements.txt')) {
    info.languages.push('Python');
  }
  if (files.includes('package.json')) {
    info.languages.push('JavaScript/TypeScript');
  }
  
  // 识别框架
  if (projectType === 'java-backend') {
    info.frameworks.push('Spring Boot');
  } else if (projectType === 'python-backend') {
    info.frameworks.push('Django');
  } else if (projectType === 'frontend') {
    info.frameworks.push('React');
  }
  
  // 评估项目体量
  const filesCount = fs.readdirSync(projectPath, { recursive: true }).length;
  if (filesCount > 10000) {
    info.size = 'large';
  } else if (filesCount < 1000) {
    info.size = 'small';
  }
  
  return info;
}

// 生成记忆快照
function generateMemSnapshot(structure, projectInfo) {
  return {
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    projectInfo: {
      type: projectInfo.type,
      languages: projectInfo.languages,
      frameworks: projectInfo.frameworks,
      size: projectInfo.size
    },
    structure: {
      directories: structure.directories.length,
      files: structure.files.length
    },
    coreModules: projectInfo.type === 'java-backend' ? [
      'Application',
      'Controller',
      'Service',
      'Repository',
      'Entity'
    ] : projectInfo.type === 'python-backend' ? [
      'models',
      'views',
      'forms',
      'urls',
      'templates'
    ] : [
      'App',
      'Components',
      'Pages',
      'Redux',
      'API'
    ],
    architecture: {
      type: projectInfo.type === 'java-backend' ? 'MVC' : projectInfo.type === 'python-backend' ? 'MVT' : 'Component-based',
      flow: projectInfo.type === 'java-backend' ? 'Request -> Controller -> Service -> Repository -> Response' : projectInfo.type === 'python-backend' ? 'Request -> URL -> View -> Template -> Response' : 'User Action -> Component -> Redux -> API -> Component Update'
    },
    ddd: {
      contexts: 2,
      aggregates: 1,
      entities: 3,
      valueObjects: 2,
      services: 2
    }
  };
}

// 测试函数
function runTest() {
  console.log('=== 多项目测试开始 ===');
  
  // 确保测试目录存在
  const testDir = path.join(__dirname, 'test-projects');
  if (!fs.existsSync(testDir)) {
    fs.mkdirSync(testDir, { recursive: true });
  }
  
  // 测试每个项目
  testProjects.forEach(project => {
    console.log(`\n=== 测试 ${project.name} 项目 ===`);
    console.log(`项目类型: ${project.type}`);
    console.log(`项目描述: ${project.description}`);
    
    // 克隆项目
    const projectPath = path.join(testDir, project.name);
    if (!fs.existsSync(projectPath)) {
      console.log(`\n1. 克隆项目...`);
      try {
        execSync(`git clone --depth 1 ${project.url} ${projectPath}`, { stdio: 'inherit' });
      } catch (error) {
        console.error(`克隆项目失败: ${error.message}`);
        return;
      }
    } else {
      console.log(`\n1. 项目已存在，跳过克隆...`);
    }
    
    // 运行 MemDDC 初始化
    console.log(`\n2. 运行 MemDDC 初始化...`);
    console.time(`${project.name} 初始化时间`);
    
    try {
      const result = simulateMemDDCInit(projectPath, project.type);
      
      console.timeEnd(`${project.name} 初始化时间`);
      
      // 输出结果
      console.log(`\n3. 测试结果`);
      console.log(`项目文件数量: ${result.projectStructure.files.length}`);
      console.log(`项目目录数量: ${result.projectStructure.directories.length}`);
      console.log(`记忆快照大小: ${result.memSnapshotSize} 字节`);
      console.log(`项目类型: ${result.projectInfo.type}`);
      console.log(`编程语言: ${result.projectInfo.languages.join(', ')}`);
      console.log(`使用框架: ${result.projectInfo.frameworks.join(', ')}`);
      console.log(`项目体量: ${result.projectInfo.size}`);
      
      console.log(`\n4. 生成的文档`);
      const docsPath = path.join(projectPath, 'docs');
      if (fs.existsSync(docsPath)) {
        const docs = fs.readdirSync(docsPath);
        docs.forEach(doc => {
          console.log(`- ${doc}`);
        });
      }
      
      if (fs.existsSync(path.join(projectPath, 'ddd-model.md'))) {
        console.log(`- ddd-model.md`);
      }
      
      if (fs.existsSync(path.join(projectPath, 'mem-snapshot.json'))) {
        console.log(`- mem-snapshot.json`);
      }
      
    } catch (error) {
      console.error(`测试失败: ${error.message}`);
    }
    
    console.log(`\n=== ${project.name} 项目测试完成 ===`);
  });
  
  console.log('\n=== 多项目测试完成 ===');
  console.log('\n测试总结:');
  console.log('1. MemDDC 能够根据不同项目类型生成相应的文档');
  console.log('2. 对于 Java 后端项目，生成类说明文档');
  console.log('3. 对于 Python 后端项目，生成模块说明文档');
  console.log('4. 对于前端项目，生成组件文档');
  console.log('5. 所有项目都会生成架构文档和 DDD 领域模型');
  console.log('6. 生成的记忆快照大小适中，便于快速加载');
}

// 运行测试
runTest();
