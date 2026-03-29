# 俄罗斯方块游戏 - API 文档

## 核心类 API

### Tetromino 类

方块实体，表示当前活动的俄罗斯方块。

#### 构造函数
```javascript
new Tetromino(type, x, y)
```
- `type` (string): 方块类型 ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
- `x` (number): 初始 X 坐标
- `y` (number): 初始 Y 坐标

#### 属性
- `type` (string): 方块类型
- `x` (number): 当前 X 坐标
- `y` (number): 当前 Y 坐标
- `rotation` (number): 当前旋转状态 (0-3)
- `color` (string): 方块颜色

#### 方法

##### getShape()
获取当前旋转状态下的形状矩阵。
```javascript
getShape(): boolean[][]
```
返回: 二维布尔数组，true 表示有方块

##### rotate()
顺时针旋转方块。
```javascript
rotate(): void
```

##### moveLeft()
向左移动。
```javascript
moveLeft(): void
```

##### moveRight()
向右移动。
```javascript
moveRight(): void
```

##### moveDown()
向下移动。
```javascript
moveDown(): void
```

---

### GameBoard 类

游戏板实体，管理游戏区域的状态。

#### 构造函数
```javascript
new GameBoard(width, height)
```
- `width` (number): 游戏板宽度（列数）
- `height` (number): 游戏板高度（行数）

#### 属性
- `width` (number): 宽度
- `height` (number): 高度
- `grid` (Cell[][]): 二维格子数组

#### 方法

##### clear()
清空游戏板。
```javascript
clear(): void
```

##### isValidPosition(tetromino, offsetX, offsetY)
检查指定位置是否有效。
```javascript
isValidPosition(tetromino, offsetX, offsetY): boolean
```
- `tetromino` (Tetromino): 要检查的方块
- `offsetX` (number): X 偏移量
- `offsetY` (number): Y 偏移量
返回: 位置是否有效

##### mergeTetromino(tetromino)
将方块合并到游戏板。
```javascript
mergeTetromino(tetromino): void
```

##### clearLines()
消除满行并返回消除的行数。
```javascript
clearLines(): number
```
返回: 消除的行数

##### getCell(x, y)
获取指定位置的格子。
```javascript
getCell(x, y): Cell | null
```

---

### Renderer 类

渲染器，负责 Canvas 绘制。

#### 构造函数
```javascript
new Renderer(canvas, cellSize)
```
- `canvas` (HTMLCanvasElement): Canvas 元素
- `cellSize` (number): 每个格子的大小（像素）

#### 方法

##### clear()
清空画布。
```javascript
clear(): void
```

##### drawBoard(board)
绘制游戏板。
```javascript
drawBoard(board): void
```

##### drawTetromino(tetromino)
绘制当前方块。
```javascript
drawTetromino(tetromino): void
```

##### drawGrid()
绘制网格线。
```javascript
drawGrid(): void
```

---

### InputHandler 类

输入处理器，管理键盘事件。

#### 构造函数
```javascript
new InputHandler(game)
```
- `game` (Game): 游戏实例

#### 方法

##### start()
开始监听键盘事件。
```javascript
start(): void
```

##### stop()
停止监听键盘事件。
```javascript
stop(): void
```

---

### Game 类

游戏控制器，协调整个游戏流程。

#### 构造函数
```javascript
new Game(canvas)
```
- `canvas` (HTMLCanvasElement): Canvas 元素

#### 属性
- `score` (number): 当前分数
- `level` (number): 当前等级
- `lines` (number): 消除的总行数
- `state` (string): 游戏状态 ('playing', 'paused', 'gameover')

#### 方法

##### start()
开始游戏。
```javascript
start(): void
```

##### pause()
暂停/继续游戏。
```javascript
pause(): void
```

##### reset()
重置游戏。
```javascript
reset(): void
```

##### moveLeft()
向左移动当前方块。
```javascript
moveLeft(): void
```

##### moveRight()
向右移动当前方块。
```javascript
moveRight(): void
```

##### rotate()
旋转当前方块。
```javascript
rotate(): void
```

##### moveDown()
加速下落。
```javascript
moveDown(): void
```

##### hardDrop()
直接下落到底部。
```javascript
hardDrop(): void
```

---

## 常量定义

### 方块形状定义

```javascript
const SHAPES = {
  I: [
    [0, 0, 0, 0],
    [1, 1, 1, 1],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
  ],
  O: [
    [1, 1],
    [1, 1]
  ],
  T: [
    [0, 1, 0],
    [1, 1, 1],
    [0, 0, 0]
  ],
  S: [
    [0, 1, 1],
    [1, 1, 0],
    [0, 0, 0]
  ],
  Z: [
    [1, 1, 0],
    [0, 1, 1],
    [0, 0, 0]
  ],
  J: [
    [1, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
  ],
  L: [
    [0, 0, 1],
    [1, 1, 1],
    [0, 0, 0]
  ]
};
```

### 方块颜色定义

```javascript
const COLORS = {
  I: '#00f0f0',
  O: '#f0f000',
  T: '#a000f0',
  S: '#00f000',
  Z: '#f00000',
  J: '#0000f0',
  L: '#f0a000'
};
```

### 游戏配置

```javascript
const CONFIG = {
  BOARD_WIDTH: 10,
  BOARD_HEIGHT: 20,
  CELL_SIZE: 30,
  INITIAL_SPEED: 1000,
  SPEED_INCREMENT: 50,
  LINES_PER_LEVEL: 10
};
```

---

## 分数计算规则

| 消除行数 | 基础分数 | 公式 |
|---------|---------|------|
| 1 行 | 100 | 100 × level |
| 2 行 | 300 | 300 × level |
| 3 行 | 500 | 500 × level |
| 4 行 | 800 | 800 × level |

---

## 键盘控制

| 按键 | 功能 |
|-----|------|
| ← | 左移 |
| → | 右移 |
| ↓ | 加速下落 |
| ↑ | 旋转 |
| 空格 | 直接下落 |
| P | 暂停/继续 |
| R | 重新开始 |
