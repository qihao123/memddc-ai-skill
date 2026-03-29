# 俄罗斯方块游戏 - DDD 领域模型

## 项目概述

一个基于 Web 的俄罗斯方块游戏，使用原生 JavaScript 和 HTML5 Canvas 实现。

## 限界上下文 (Bounded Context)

### 1. 游戏核心上下文 (Game Core Context)
负责游戏的核心逻辑，包括方块移动、旋转、消除等。

### 2. 渲染上下文 (Rendering Context)
负责游戏的视觉呈现，包括绘制方块、游戏板、UI 等。

### 3. 输入控制上下文 (Input Control Context)
负责处理用户输入，包括键盘事件监听和处理。

## 聚合 (Aggregates)

### 游戏板聚合 (GameBoard Aggregate)
- **聚合根**: GameBoard
- **实体**: Cell (格子)
- **值对象**: Position (位置), Color (颜色)

### 方块聚合 (Tetromino Aggregate)
- **聚合根**: Tetromino
- **实体**: Block (方块单元)
- **值对象**: Shape (形状), Rotation (旋转状态)

### 游戏状态聚合 (GameState Aggregate)
- **聚合根**: GameState
- **值对象**: Score (分数), Level (等级), Speed (速度)

## 领域实体 (Domain Entities)

### GameBoard
- 属性: width, height, cells (二维数组)
- 方法: clear(), isValidPosition(), mergeTetromino(), clearLines()

### Tetromino
- 属性: type, shape, position, rotation
- 方法: rotate(), moveLeft(), moveRight(), moveDown(), getShape()

### Cell
- 属性: occupied, color
- 方法: occupy(color), clear()

## 值对象 (Value Objects)

### Position
- x: number
- y: number

### Color
- r: number
- g: number
- b: number
- toString(): string

### Shape
- matrix: boolean[][]
- rotate(): Shape

## 领域服务 (Domain Services)

### CollisionDetectionService
- checkCollision(board, tetromino, position): boolean

### LineClearService
- detectFullLines(board): number[]
- clearLines(board, lines): number (返回消除行数)

### ScoreCalculationService
- calculateScore(linesCleared, level): number
- calculateLevel(totalLines): number

## 领域事件 (Domain Events)

- TetrominoPlaced
- LineCleared
- GameOver
- ScoreUpdated
- LevelUp

## 战术设计

### 实体设计

#### Tetromino 类型枚举
```
I: 长条
O: 方块
T: T形
S: S形
Z: Z形
J: J形
L: L形
```

#### 游戏板设计
- 标准尺寸: 10列 x 20行
- 使用二维数组存储格子状态

### 领域规则

1. 方块不能移出游戏板边界
2. 方块不能与其他已固定的方块重叠
3. 当方块无法继续下落时，固定到游戏板
4. 填满一行时，消除该行并计分
5. 游戏结束条件：新方块无法放置

## 架构分层

### 表现层 (Presentation Layer)
- index.html
- 游戏界面布局

### 应用层 (Application Layer)
- game.js - 游戏主控制器
- 协调各领域服务

### 领域层 (Domain Layer)
- tetromino.js - 方块实体
- board.js - 游戏板实体
- collision.js - 碰撞检测服务

### 基础设施层 (Infrastructure Layer)
- renderer.js - Canvas 渲染
- input.js - 键盘输入处理
