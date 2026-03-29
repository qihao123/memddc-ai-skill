/**
 * Game 类 - 游戏控制器
 * 协调整个游戏流程
 */

import { Tetromino, SHAPES, COLORS, createRandomTetromino } from './tetromino.js';
import { GameBoard } from './board.js';
import { Renderer } from './renderer.js';
import { InputHandler } from './input.js';

// 游戏配置
const CONFIG = {
  BOARD_WIDTH: 10,
  BOARD_HEIGHT: 20,
  CELL_SIZE: 30,
  INITIAL_SPEED: 1000,
  SPEED_DECREMENT: 50,
  MIN_SPEED: 100,
  LINES_PER_LEVEL: 10
};

// 分数计算表
const SCORE_TABLE = {
  1: 100,
  2: 300,
  3: 500,
  4: 800
};

class Game {
  constructor(canvas) {
    this.canvas = canvas;
    this.board = new GameBoard(CONFIG.BOARD_WIDTH, CONFIG.BOARD_HEIGHT);
    this.renderer = new Renderer(canvas, CONFIG.CELL_SIZE);
    this.inputHandler = new InputHandler(this);
    
    // 游戏状态
    this.state = 'ready'; // ready, playing, paused, gameover
    this.score = 0;
    this.level = 1;
    this.lines = 0;
    
    // 方块管理
    this.currentTetromino = null;
    this.nextTetrominoType = null;
    
    // 游戏循环
    this.dropInterval = CONFIG.INITIAL_SPEED;
    this.lastDropTime = 0;
    this.animationId = null;
    
    // 将配置暴露到全局（供渲染器使用）
    window.SHAPES = SHAPES;
    window.COLORS = COLORS;
    
    // 初始化画布大小
    this.initCanvas();
    
    // 初始渲染
    this.render();
  }

  /**
   * 初始化画布大小
   */
  initCanvas() {
    // 主游戏区域
    this.canvas.width = CONFIG.BOARD_WIDTH * CONFIG.CELL_SIZE;
    this.canvas.height = CONFIG.BOARD_HEIGHT * CONFIG.CELL_SIZE;
  }

  /**
   * 开始游戏
   */
  start() {
    if (this.state === 'playing') return;
    
    this.state = 'playing';
    this.inputHandler.start();
    this.spawnTetromino();
    this.gameLoop();
  }

  /**
   * 暂停/继续游戏
   */
  pause() {
    if (this.state === 'gameover') return;
    
    if (this.state === 'playing') {
      this.state = 'paused';
      cancelAnimationFrame(this.animationId);
    } else if (this.state === 'paused') {
      this.state = 'playing';
      this.lastDropTime = performance.now();
      this.gameLoop();
    }
    this.render();
  }

  /**
   * 重置游戏
   */
  reset() {
    // 停止游戏循环
    cancelAnimationFrame(this.animationId);
    
    // 重置状态
    this.state = 'ready';
    this.score = 0;
    this.level = 1;
    this.lines = 0;
    this.dropInterval = CONFIG.INITIAL_SPEED;
    
    // 重置游戏板
    this.board.clear();
    this.currentTetromino = null;
    this.nextTetrominoType = null;
    
    // 重新开始
    this.start();
  }

  /**
   * 游戏主循环
   */
  gameLoop() {
    if (this.state !== 'playing') return;
    
    const currentTime = performance.now();
    
    // 自动下落
    if (currentTime - this.lastDropTime > this.dropInterval) {
      this.autoDrop();
      this.lastDropTime = currentTime;
    }
    
    // 渲染
    this.render();
    
    // 继续循环
    this.animationId = requestAnimationFrame(() => this.gameLoop());
  }

  /**
   * 自动生成并放置新方块
   */
  spawnTetromino() {
    // 确定下一个方块类型
    if (!this.nextTetrominoType) {
      this.nextTetrominoType = this.getRandomType();
    }
    
    // 创建当前方块
    const type = this.nextTetrominoType;
    const startX = Math.floor((CONFIG.BOARD_WIDTH - 4) / 2);
    this.currentTetromino = new Tetromino(type, startX, 0);
    
    // 生成下一个方块类型
    this.nextTetrominoType = this.getRandomType();
    
    // 检查是否可以放置
    if (!this.board.isValidPosition(this.currentTetromino)) {
      this.gameOver();
    }
  }

  /**
   * 获取随机方块类型
   * @returns {string}
   */
  getRandomType() {
    const types = Object.keys(SHAPES);
    return types[Math.floor(Math.random() * types.length)];
  }

  /**
   * 自动下落
   */
  autoDrop() {
    if (!this.currentTetromino) return;
    
    if (this.board.isValidPosition(this.currentTetromino, 0, 1)) {
      this.currentTetromino.moveDown();
    } else {
      this.lockTetromino();
    }
  }

  /**
   * 固定当前方块到游戏板
   */
  lockTetromino() {
    if (!this.currentTetromino) return;
    
    // 合并到游戏板
    this.board.mergeTetromino(this.currentTetromino);
    
    // 消除满行
    const linesCleared = this.board.clearLines();
    if (linesCleared > 0) {
      this.updateScore(linesCleared);
    }
    
    // 生成新方块
    this.spawnTetromino();
  }

  /**
   * 更新分数
   * @param {number} linesCleared - 消除的行数
   */
  updateScore(linesCleared) {
    // 计算分数
    const baseScore = SCORE_TABLE[linesCleared] || 0;
    this.score += baseScore * this.level;
    this.lines += linesCleared;
    
    // 更新等级
    const newLevel = Math.floor(this.lines / CONFIG.LINES_PER_LEVEL) + 1;
    if (newLevel > this.level) {
      this.level = newLevel;
      // 加快下落速度
      this.dropInterval = Math.max(
        CONFIG.MIN_SPEED,
        CONFIG.INITIAL_SPEED - (this.level - 1) * CONFIG.SPEED_DECREMENT
      );
    }
  }

  /**
   * 游戏结束
   */
  gameOver() {
    this.state = 'gameover';
    cancelAnimationFrame(this.animationId);
    this.render();
  }

  /**
   * 向左移动
   */
  moveLeft() {
    if (this.state !== 'playing' || !this.currentTetromino) return;
    
    if (this.board.isValidPosition(this.currentTetromino, -1, 0)) {
      this.currentTetromino.moveLeft();
    }
  }

  /**
   * 向右移动
   */
  moveRight() {
    if (this.state !== 'playing' || !this.currentTetromino) return;
    
    if (this.board.isValidPosition(this.currentTetromino, 1, 0)) {
      this.currentTetromino.moveRight();
    }
  }

  /**
   * 向下移动（软降）
   */
  moveDown() {
    if (this.state !== 'playing' || !this.currentTetromino) return;
    
    if (this.board.isValidPosition(this.currentTetromino, 0, 1)) {
      this.currentTetromino.moveDown();
      this.score += 1; // 软降加分
    } else {
      this.lockTetromino();
    }
  }

  /**
   * 旋转方块
   */
  rotate() {
    if (this.state !== 'playing' || !this.currentTetromino) return;
    
    // 克隆当前方块进行测试旋转
    const testTetromino = this.currentTetromino.clone();
    testTetromino.rotate();
    
    // 检查旋转后是否有效
    if (this.board.isValidPosition(testTetromino)) {
      this.currentTetromino.rotate();
    } else {
      // 尝试墙踢（Wall Kick）
      const kicks = [-1, 1, -2, 2];
      for (const kick of kicks) {
        if (this.board.isValidPosition(testTetromino, kick, 0)) {
          this.currentTetromino.rotate();
          this.currentTetromino.x += kick;
          break;
        }
      }
    }
  }

  /**
   * 硬降（直接落到底部）
   */
  hardDrop() {
    if (this.state !== 'playing' || !this.currentTetromino) return;
    
    let dropDistance = 0;
    while (this.board.isValidPosition(this.currentTetromino, 0, dropDistance + 1)) {
      dropDistance++;
    }
    
    if (dropDistance > 0) {
      this.currentTetromino.y += dropDistance;
      this.score += dropDistance * 2; // 硬降加分
    }
    
    this.lockTetromino();
  }

  /**
   * 渲染游戏画面
   */
  render() {
    // 清空画布
    this.renderer.clear();
    
    // 绘制游戏板
    this.renderer.drawBoard(this.board);
    
    // 绘制当前方块
    if (this.currentTetromino) {
      this.renderer.drawTetromino(this.currentTetromino);
    }
    
    // 绘制游戏信息
    this.renderer.drawInfo({
      score: this.score,
      level: this.level,
      lines: this.lines,
      nextType: this.nextTetrominoType
    });
    
    // 绘制下一个方块预览
    this.renderer.drawNextPiece(this.nextTetrominoType);
    
    // 绘制暂停/游戏结束画面
    if (this.state === 'paused') {
      this.renderer.drawPaused();
    } else if (this.state === 'gameover') {
      this.renderer.drawGameOver();
    }
  }
}

export { Game, CONFIG };
