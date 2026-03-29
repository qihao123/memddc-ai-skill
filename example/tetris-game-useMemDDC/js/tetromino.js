/**
 * Tetromino 类 - 俄罗斯方块实体
 * 表示当前活动的方块
 */

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

const COLORS = {
  I: '#00f0f0',
  O: '#f0f000',
  T: '#a000f0',
  S: '#00f000',
  Z: '#f00000',
  J: '#0000f0',
  L: '#f0a000'
};

class Tetromino {
  constructor(type, x, y) {
    this.type = type;
    this.x = x;
    this.y = y;
    this.rotation = 0;
    this.color = COLORS[type];
    this.shape = SHAPES[type];
  }

  /**
   * 获取当前旋转状态下的形状矩阵
   * @returns {boolean[][]} 二维布尔数组
   */
  getShape() {
    return this.rotateMatrix(this.shape, this.rotation);
  }

  /**
   * 顺时针旋转方块
   */
  rotate() {
    this.rotation = (this.rotation + 1) % 4;
  }

  /**
   * 向左移动
   */
  moveLeft() {
    this.x--;
  }

  /**
   * 向右移动
   */
  moveRight() {
    this.x++;
  }

  /**
   * 向下移动
   */
  moveDown() {
    this.y++;
  }

  /**
   * 旋转矩阵
   * @param {number[][]} matrix - 原始矩阵
   * @param {number} rotation - 旋转次数 (0-3)
   * @returns {number[][]} 旋转后的矩阵
   */
  rotateMatrix(matrix, rotation) {
    let result = matrix;
    for (let i = 0; i < rotation; i++) {
      result = this.rotate90(result);
    }
    return result;
  }

  /**
   * 顺时针旋转90度
   * @param {number[][]} matrix - 原始矩阵
   * @returns {number[][]} 旋转后的矩阵
   */
  rotate90(matrix) {
    const N = matrix.length;
    const result = Array(N).fill(null).map(() => Array(N).fill(0));
    for (let i = 0; i < N; i++) {
      for (let j = 0; j < N; j++) {
        result[j][N - 1 - i] = matrix[i][j];
      }
    }
    return result;
  }

  /**
   * 获取方块的宽度
   * @returns {number}
   */
  getWidth() {
    return this.getShape()[0].length;
  }

  /**
   * 获取方块的高度
   * @returns {number}
   */
  getHeight() {
    return this.getShape().length;
  }

  /**
   * 克隆当前方块
   * @returns {Tetromino}
   */
  clone() {
    const clone = new Tetromino(this.type, this.x, this.y);
    clone.rotation = this.rotation;
    return clone;
  }
}

/**
 * 随机生成一个方块
 * @param {number} x - 初始 X 坐标
 * @param {number} y - 初始 Y 坐标
 * @returns {Tetromino}
 */
function createRandomTetromino(x, y) {
  const types = Object.keys(SHAPES);
  const randomType = types[Math.floor(Math.random() * types.length)];
  return new Tetromino(randomType, x, y);
}

export { Tetromino, SHAPES, COLORS, createRandomTetromino };
