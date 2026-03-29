/**
 * Renderer 类 - 渲染器
 * 负责 Canvas 绘制
 */

class Renderer {
  constructor(canvas, cellSize) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d');
    this.cellSize = cellSize;
    this.gridColor = '#333';
    this.backgroundColor = '#111';
  }

  /**
   * 清空画布
   */
  clear() {
    this.ctx.fillStyle = this.backgroundColor;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
  }

  /**
   * 绘制游戏板
   * @param {GameBoard} board - 游戏板实例
   */
  drawBoard(board) {
    for (let y = 0; y < board.height; y++) {
      for (let x = 0; x < board.width; x++) {
        const cell = board.getCell(x, y);
        if (cell && cell.occupied) {
          this.drawCell(x, y, cell.color);
        } else {
          this.drawEmptyCell(x, y);
        }
      }
    }
  }

  /**
   * 绘制当前方块
   * @param {Tetromino} tetromino - 当前方块
   */
  drawTetromino(tetromino) {
    const shape = tetromino.getShape();
    for (let y = 0; y < shape.length; y++) {
      for (let x = 0; x < shape[y].length; x++) {
        if (shape[y][x]) {
          const boardX = tetromino.x + x;
          const boardY = tetromino.y + y;
          if (boardY >= 0) {
            this.drawCell(boardX, boardY, tetromino.color);
          }
        }
      }
    }
  }

  /**
   * 绘制单个格子
   * @param {number} x - X 坐标
   * @param {number} y - Y 坐标
   * @param {string} color - 颜色
   */
  drawCell(x, y, color) {
    const px = x * this.cellSize;
    const py = y * this.cellSize;
    const size = this.cellSize - 1;

    // 绘制主体
    this.ctx.fillStyle = color;
    this.ctx.fillRect(px + 1, py + 1, size, size);

    // 绘制高光（3D效果）
    this.ctx.fillStyle = this.lightenColor(color, 30);
    this.ctx.fillRect(px + 1, py + 1, size, 3);
    this.ctx.fillRect(px + 1, py + 1, 3, size);

    // 绘制阴影
    this.ctx.fillStyle = this.darkenColor(color, 30);
    this.ctx.fillRect(px + 1, py + size - 2, size, 3);
    this.ctx.fillRect(px + size - 2, py + 1, 3, size);
  }

  /**
   * 绘制空格子（网格效果）
   * @param {number} x - X 坐标
   * @param {number} y - Y 坐标
   */
  drawEmptyCell(x, y) {
    const px = x * this.cellSize;
    const py = y * this.cellSize;
    const size = this.cellSize - 1;

    this.ctx.fillStyle = '#1a1a1a';
    this.ctx.fillRect(px + 1, py + 1, size, size);

    // 绘制网格线
    this.ctx.strokeStyle = '#2a2a2a';
    this.ctx.lineWidth = 1;
    this.ctx.strokeRect(px + 0.5, py + 0.5, this.cellSize, this.cellSize);
  }

  /**
   * 绘制网格线
   */
  drawGrid() {
    this.ctx.strokeStyle = this.gridColor;
    this.ctx.lineWidth = 1;

    // 垂直线
    for (let x = 0; x <= this.canvas.width; x += this.cellSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(x, 0);
      this.ctx.lineTo(x, this.canvas.height);
      this.ctx.stroke();
    }

    // 水平线
    for (let y = 0; y <= this.canvas.height; y += this.cellSize) {
      this.ctx.beginPath();
      this.ctx.moveTo(0, y);
      this.ctx.lineTo(this.canvas.width, y);
      this.ctx.stroke();
    }
  }

  /**
   * 绘制游戏信息
   * @param {Object} info - 游戏信息对象
   */
  drawInfo(info) {
    const { score, level, lines, nextType } = info;
    
    // 绘制信息背景
    this.ctx.fillStyle = '#222';
    this.ctx.fillRect(this.canvas.width + 10, 10, 150, 200);
    this.ctx.strokeStyle = '#444';
    this.ctx.strokeRect(this.canvas.width + 10, 10, 150, 200);

    // 绘制分数
    this.ctx.fillStyle = '#fff';
    this.ctx.font = 'bold 16px Arial';
    this.ctx.textAlign = 'left';
    this.ctx.fillText('分数', this.canvas.width + 20, 40);
    this.ctx.font = '20px Arial';
    this.ctx.fillText(score.toString(), this.canvas.width + 20, 65);

    // 绘制等级
    this.ctx.font = 'bold 16px Arial';
    this.ctx.fillText('等级', this.canvas.width + 20, 100);
    this.ctx.font = '20px Arial';
    this.ctx.fillText(level.toString(), this.canvas.width + 20, 125);

    // 绘制消除行数
    this.ctx.font = 'bold 16px Arial';
    this.ctx.fillText('行数', this.canvas.width + 20, 160);
    this.ctx.font = '20px Arial';
    this.ctx.fillText(lines.toString(), this.canvas.width + 20, 185);
  }

  /**
   * 绘制下一个方块预览
   * @param {string} nextType - 下一个方块类型
   */
  drawNextPiece(nextType) {
    const previewX = this.canvas.width + 20;
    const previewY = 230;
    const previewSize = 20;

    // 绘制预览区域背景
    this.ctx.fillStyle = '#222';
    this.ctx.fillRect(previewX - 10, previewY - 20, 130, 130);
    this.ctx.strokeStyle = '#444';
    this.ctx.strokeRect(previewX - 10, previewY - 20, 130, 130);

    this.ctx.fillStyle = '#fff';
    this.ctx.font = 'bold 16px Arial';
    this.ctx.fillText('下一个', previewX, previewY);

    if (!nextType) return;

    const { SHAPES, COLORS } = window;
    const shape = SHAPES[nextType];
    const color = COLORS[nextType];

    // 计算居中位置
    const offsetX = previewX + 30 - (shape[0].length * previewSize) / 2;
    const offsetY = previewY + 40 - (shape.length * previewSize) / 2;

    for (let y = 0; y < shape.length; y++) {
      for (let x = 0; x < shape[y].length; x++) {
        if (shape[y][x]) {
          const px = offsetX + x * previewSize;
          const py = offsetY + y * previewSize;
          
          this.ctx.fillStyle = color;
          this.ctx.fillRect(px, py, previewSize - 1, previewSize - 1);
        }
      }
    }
  }

  /**
   * 绘制游戏结束画面
   */
  drawGameOver() {
    // 半透明遮罩
    this.ctx.fillStyle = 'rgba(0, 0, 0, 0.75)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 游戏结束文字
    this.ctx.fillStyle = '#f00';
    this.ctx.font = 'bold 40px Arial';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('游戏结束', this.canvas.width / 2, this.canvas.height / 2 - 20);

    this.ctx.fillStyle = '#fff';
    this.ctx.font = '20px Arial';
    this.ctx.fillText('按 R 重新开始', this.canvas.width / 2, this.canvas.height / 2 + 30);
  }

  /**
   * 绘制暂停画面
   */
  drawPaused() {
    // 半透明遮罩
    this.ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    // 暂停文字
    this.ctx.fillStyle = '#ff0';
    this.ctx.font = 'bold 40px Arial';
    this.ctx.textAlign = 'center';
    this.ctx.fillText('暂停', this.canvas.width / 2, this.canvas.height / 2);
  }

  /**
   * 颜色变亮
   * @param {string} color - 十六进制颜色
   * @param {number} percent - 百分比
   * @returns {string}
   */
  lightenColor(color, percent) {
    const num = parseInt(color.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = Math.min(255, (num >> 16) + amt);
    const G = Math.min(255, ((num >> 8) & 0x00FF) + amt);
    const B = Math.min(255, (num & 0x0000FF) + amt);
    return '#' + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
  }

  /**
   * 颜色变暗
   * @param {string} color - 十六进制颜色
   * @param {number} percent - 百分比
   * @returns {string}
   */
  darkenColor(color, percent) {
    const num = parseInt(color.replace('#', ''), 16);
    const amt = Math.round(2.55 * percent);
    const R = Math.max(0, (num >> 16) - amt);
    const G = Math.max(0, ((num >> 8) & 0x00FF) - amt);
    const B = Math.max(0, (num & 0x0000FF) - amt);
    return '#' + (0x1000000 + R * 0x10000 + G * 0x100 + B).toString(16).slice(1);
  }
}

export { Renderer };
