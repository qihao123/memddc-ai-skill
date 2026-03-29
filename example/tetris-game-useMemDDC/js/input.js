/**
 * InputHandler 类 - 输入处理器
 * 管理键盘事件
 */

class InputHandler {
  constructor(game) {
    this.game = game;
    this.isListening = false;
    this.keyDownHandler = this.handleKeyDown.bind(this);
    this.keyUpHandler = this.handleKeyUp.bind(this);
    
    // 按键重复控制
    this.keyRepeatDelay = 150; // 重复延迟（毫秒）
    this.keyRepeatInterval = 50; // 重复间隔
    this.pressedKeys = new Set();
    this.repeatTimers = {};
  }

  /**
   * 开始监听键盘事件
   */
  start() {
    if (this.isListening) return;
    
    document.addEventListener('keydown', this.keyDownHandler);
    document.addEventListener('keyup', this.keyUpHandler);
    this.isListening = true;
  }

  /**
   * 停止监听键盘事件
   */
  stop() {
    if (!this.isListening) return;
    
    document.removeEventListener('keydown', this.keyDownHandler);
    document.removeEventListener('keyup', this.keyUpHandler);
    this.isListening = false;
    
    // 清除所有定时器
    Object.values(this.repeatTimers).forEach(timer => clearTimeout(timer));
    this.repeatTimers = {};
    this.pressedKeys.clear();
  }

  /**
   * 处理按键按下事件
   * @param {KeyboardEvent} event
   */
  handleKeyDown(event) {
    // 防止默认行为（如页面滚动）
    if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(event.key)) {
      event.preventDefault();
    }

    const key = event.code || event.key;
    
    // 防止重复触发（按住不放时浏览器会重复触发 keydown）
    if (this.pressedKeys.has(key)) {
      return;
    }
    
    this.pressedKeys.add(key);
    this.executeAction(key);

    // 设置重复按键（仅左右下移动）
    if (['ArrowLeft', 'ArrowRight', 'ArrowDown'].includes(event.key)) {
      this.setupKeyRepeat(key, event.key);
    }
  }

  /**
   * 处理按键释放事件
   * @param {KeyboardEvent} event
   */
  handleKeyUp(event) {
    const key = event.code || event.key;
    this.pressedKeys.delete(key);
    
    // 清除重复定时器
    if (this.repeatTimers[key]) {
      clearTimeout(this.repeatTimers[key]);
      delete this.repeatTimers[key];
    }
  }

  /**
   * 设置按键重复
   * @param {string} code - 按键代码
   * @param {string} key - 按键名称
   */
  setupKeyRepeat(code, key) {
    // 延迟后开始重复
    this.repeatTimers[code] = setTimeout(() => {
      const repeat = () => {
        if (this.pressedKeys.has(code)) {
          this.executeActionFromKey(key);
          this.repeatTimers[code] = setTimeout(repeat, this.keyRepeatInterval);
        }
      };
      repeat();
    }, this.keyRepeatDelay);
  }

  /**
   * 根据按键代码执行动作
   * @param {string} code
   */
  executeAction(code) {
    // 使用 event.code (如 'ArrowLeft', 'Space', 'KeyP')
    switch (code) {
      case 'ArrowLeft':
        this.game.moveLeft();
        break;
      case 'ArrowRight':
        this.game.moveRight();
        break;
      case 'ArrowDown':
        this.game.moveDown();
        break;
      case 'ArrowUp':
        this.game.rotate();
        break;
      case 'Space':
        this.game.hardDrop();
        break;
      case 'KeyP':
      case 'Escape':
        this.game.pause();
        break;
      case 'KeyR':
        this.game.reset();
        break;
    }
  }

  /**
   * 根据按键名称执行动作（用于重复）
   * @param {string} key
   */
  executeActionFromKey(key) {
    switch (key) {
      case 'ArrowLeft':
        this.game.moveLeft();
        break;
      case 'ArrowRight':
        this.game.moveRight();
        break;
      case 'ArrowDown':
        this.game.moveDown();
        break;
    }
  }
}

export { InputHandler };
