/**
 * GameBoard 类 - 游戏板实体
 * 管理游戏区域的状态
 */

class Cell {
  constructor() {
    this.occupied = false;
    this.color = null;
  }

  occupy(color) {
    this.occupied = true;
    this.color = color;
  }

  clear() {
    this.occupied = false;
    this.color = null;
  }
}

class GameBoard {
  constructor(width, height) {
    this.width = width;
    this.height = height;
    this.grid = [];
    this.initGrid();
  }

  /**
   * 初始化游戏板网格
   */
  initGrid() {
    this.grid = [];
    for (let y = 0; y < this.height; y++) {
      const row = [];
      for (let x = 0; x < this.width; x++) {
        row.push(new Cell());
      }
      this.grid.push(row);
    }
  }

  /**
   * 清空游戏板
   */
  clear() {
    this.initGrid();
  }

  /**
   * 检查指定位置是否有效
   * @param {Tetromino} tetromino - 要检查的方块
   * @param {number} offsetX - X 偏移量
   * @param {number} offsetY - Y 偏移量
   * @returns {boolean} 位置是否有效
   */
  isValidPosition(tetromino, offsetX = 0, offsetY = 0) {
    const shape = tetromino.getShape();
    const newX = tetromino.x + offsetX;
    const newY = tetromino.y + offsetY;

    for (let y = 0; y < shape.length; y++) {
      for (let x = 0; x < shape[y].length; x++) {
        if (shape[y][x]) {
          const boardX = newX + x;
          const boardY = newY + y;

          // 检查边界
          if (boardX < 0 || boardX >= this.width || boardY >= this.height) {
            return false;
          }

          // 检查是否与其他方块重叠 (只检查已在游戏板上的)
          if (boardY >= 0 && this.grid[boardY][boardX].occupied) {
            return false;
          }
        }
      }
    }
    return true;
  }

  /**
   * 将方块合并到游戏板
   * @param {Tetromino} tetromino - 要合并的方块
   */
  mergeTetromino(tetromino) {
    const shape = tetromino.getShape();
    for (let y = 0; y < shape.length; y++) {
      for (let x = 0; x < shape[y].length; x++) {
        if (shape[y][x]) {
          const boardX = tetromino.x + x;
          const boardY = tetromino.y + y;
          if (boardY >= 0 && boardY < this.height && boardX >= 0 && boardX < this.width) {
            this.grid[boardY][boardX].occupy(tetromino.color);
          }
        }
      }
    }
  }

  /**
   * 消除满行并返回消除的行数
   * @returns {number} 消除的行数
   */
  clearLines() {
    let linesCleared = 0;
    for (let y = this.height - 1; y >= 0; y--) {
      if (this.isLineFull(y)) {
        this.removeLine(y);
        linesCleared++;
        y++; // 重新检查当前行（因为上面的行下移了）
      }
    }
    return linesCleared;
  }

  /**
   * 检查某一行是否已满
   * @param {number} y - 行索引
   * @returns {boolean}
   */
  isLineFull(y) {
    for (let x = 0; x < this.width; x++) {
      if (!this.grid[y][x].occupied) {
        return false;
      }
    }
    return true;
  }

  /**
   * 移除指定行，并将上面的行下移
   * @param {number} y - 要移除的行索引
   */
  removeLine(y) {
    // 将上面的所有行下移
    for (let row = y; row > 0; row--) {
      for (let x = 0; x < this.width; x++) {
        this.grid[row][x].occupied = this.grid[row - 1][x].occupied;
        this.grid[row][x].color = this.grid[row - 1][x].color;
      }
    }
    // 清空最上面一行
    for (let x = 0; x < this.width; x++) {
      this.grid[0][x].clear();
    }
  }

  /**
   * 获取指定位置的格子
   * @param {number} x - X 坐标
   * @param {number} y - Y 坐标
   * @returns {Cell | null}
   */
  getCell(x, y) {
    if (x >= 0 && x < this.width && y >= 0 && y < this.height) {
      return this.grid[y][x];
    }
    return null;
  }

  /**
   * 检查游戏是否结束
   * @returns {boolean}
   */
  isGameOver() {
    // 检查最上面几行是否有被占用的格子
    for (let y = 0; y < 2; y++) {
      for (let x = 0; x < this.width; x++) {
        if (this.grid[y][x].occupied) {
          return true;
        }
      }
    }
    return false;
  }
}

export { GameBoard, Cell };
