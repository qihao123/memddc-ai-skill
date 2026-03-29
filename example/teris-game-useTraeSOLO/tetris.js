// 游戏配置
const COLS = 10;
const ROWS = 20;
const BLOCK_SIZE = 30;
const NEXT_BLOCK_SIZE = 24;

// 方块形状定义
const SHAPES = {
    I: {
        shape: [
            [0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        color: '#00f0f0'
    },
    O: {
        shape: [
            [1, 1],
            [1, 1]
        ],
        color: '#f0f000'
    },
    T: {
        shape: [
            [0, 1, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        color: '#a000f0'
    },
    S: {
        shape: [
            [0, 1, 1],
            [1, 1, 0],
            [0, 0, 0]
        ],
        color: '#00f000'
    },
    Z: {
        shape: [
            [1, 1, 0],
            [0, 1, 1],
            [0, 0, 0]
        ],
        color: '#f00000'
    },
    J: {
        shape: [
            [1, 0, 0],
            [1, 1, 1],
            [0, 0, 0]
        ],
        color: '#0000f0'
    },
    L: {
        shape: [
            [0, 0, 1],
            [1, 1, 1],
            [0, 0, 0]
        ],
        color: '#f0a000'
    }
};

const SHAPE_KEYS = Object.keys(SHAPES);

// 游戏状态
let board = [];
let currentPiece = null;
let nextPiece = null;
let score = 0;
let level = 1;
let lines = 0;
let gameLoop = null;
let isGameOver = false;
let isPaused = false;
let isGameStarted = false;
let dropCounter = 0;
let dropInterval = 1000;
let lastTime = 0;

// DOM 元素
const canvas = document.getElementById('game-board');
const ctx = canvas.getContext('2d');
const nextCanvas = document.getElementById('next-piece');
const nextCtx = nextCanvas.getContext('2d');
const scoreElement = document.getElementById('score');
const levelElement = document.getElementById('level');
const linesElement = document.getElementById('lines');
const startBtn = document.getElementById('start-btn');
const pauseBtn = document.getElementById('pause-btn');
const restartBtn = document.getElementById('restart-btn');
const modal = document.getElementById('game-over-modal');
const finalScoreElement = document.getElementById('final-score');
const modalRestartBtn = document.getElementById('modal-restart-btn');

// 初始化游戏板
function createBoard() {
    return Array(ROWS).fill(null).map(() => Array(COLS).fill(0));
}

// 创建新方块
function createPiece(type) {
    const piece = SHAPES[type];
    return {
        shape: piece.shape.map(row => [...row]),
        color: piece.color,
        x: Math.floor((COLS - piece.shape[0].length) / 2),
        y: 0
    };
}

// 随机获取方块类型
function getRandomPieceType() {
    return SHAPE_KEYS[Math.floor(Math.random() * SHAPE_KEYS.length)];
}

// 绘制方块
function drawBlock(context, x, y, size, color) {
    context.fillStyle = color;
    context.fillRect(x * size, y * size, size, size);
    
    // 添加高光效果
    context.fillStyle = 'rgba(255, 255, 255, 0.3)';
    context.fillRect(x * size, y * size, size, 3);
    context.fillRect(x * size, y * size, 3, size);
    
    // 添加阴影效果
    context.fillStyle = 'rgba(0, 0, 0, 0.3)';
    context.fillRect(x * size, (y + 1) * size - 3, size, 3);
    context.fillRect((x + 1) * size - 3, y * size, 3, size);
    
    context.strokeStyle = 'rgba(0, 0, 0, 0.5)';
    context.lineWidth = 1;
    context.strokeRect(x * size, y * size, size, size);
}

// 绘制游戏板
function drawBoard() {
    // 清空画布
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // 绘制网格线
    ctx.strokeStyle = '#222';
    ctx.lineWidth = 1;
    for (let i = 0; i <= COLS; i++) {
        ctx.beginPath();
        ctx.moveTo(i * BLOCK_SIZE, 0);
        ctx.lineTo(i * BLOCK_SIZE, canvas.height);
        ctx.stroke();
    }
    for (let i = 0; i <= ROWS; i++) {
        ctx.beginPath();
        ctx.moveTo(0, i * BLOCK_SIZE);
        ctx.lineTo(canvas.width, i * BLOCK_SIZE);
        ctx.stroke();
    }
    
    // 绘制已固定的方块
    for (let y = 0; y < ROWS; y++) {
        for (let x = 0; x < COLS; x++) {
            if (board[y][x]) {
                drawBlock(ctx, x, y, BLOCK_SIZE, board[y][x]);
            }
        }
    }
}

// 绘制当前方块
function drawPiece() {
    if (!currentPiece) return;
    
    currentPiece.shape.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value) {
                drawBlock(
                    ctx,
                    currentPiece.x + x,
                    currentPiece.y + y,
                    BLOCK_SIZE,
                    currentPiece.color
                );
            }
        });
    });
}

// 绘制下一个方块预览
function drawNextPiece() {
    nextCtx.fillStyle = '#000';
    nextCtx.fillRect(0, 0, nextCanvas.width, nextCanvas.height);
    
    if (!nextPiece) return;
    
    const offsetX = (nextCanvas.width / NEXT_BLOCK_SIZE - nextPiece.shape[0].length) / 2;
    const offsetY = (nextCanvas.height / NEXT_BLOCK_SIZE - nextPiece.shape.length) / 2;
    
    nextPiece.shape.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value) {
                drawBlock(
                    nextCtx,
                    offsetX + x,
                    offsetY + y,
                    NEXT_BLOCK_SIZE,
                    nextPiece.color
                );
            }
        });
    });
}

// 绘制游戏画面
function draw() {
    drawBoard();
    drawPiece();
    drawNextPiece();
}

// 碰撞检测
function isValidMove(piece, offsetX = 0, offsetY = 0, newShape = null) {
    const shape = newShape || piece.shape;
    
    for (let y = 0; y < shape.length; y++) {
        for (let x = 0; x < shape[y].length; x++) {
            if (shape[y][x]) {
                const newX = piece.x + x + offsetX;
                const newY = piece.y + y + offsetY;
                
                if (newX < 0 || newX >= COLS || newY >= ROWS) {
                    return false;
                }
                
                if (newY >= 0 && board[newY][newX]) {
                    return false;
                }
            }
        }
    }
    return true;
}

// 旋转方块
function rotatePiece() {
    if (!currentPiece) return;
    
    const rotated = currentPiece.shape[0].map((_, i) =>
        currentPiece.shape.map(row => row[i]).reverse()
    );
    
    if (isValidMove(currentPiece, 0, 0, rotated)) {
        currentPiece.shape = rotated;
    } else {
        // 尝试墙踢
        for (const offset of [-1, 1, -2, 2]) {
            if (isValidMove(currentPiece, offset, 0, rotated)) {
                currentPiece.x += offset;
                currentPiece.shape = rotated;
                break;
            }
        }
    }
}

// 固定方块到游戏板
function lockPiece() {
    currentPiece.shape.forEach((row, y) => {
        row.forEach((value, x) => {
            if (value) {
                const boardY = currentPiece.y + y;
                const boardX = currentPiece.x + x;
                if (boardY >= 0) {
                    board[boardY][boardX] = currentPiece.color;
                }
            }
        });
    });
}

// 清除完整的行
function clearLines() {
    let linesCleared = 0;
    
    for (let y = ROWS - 1; y >= 0; y--) {
        if (board[y].every(cell => cell !== 0)) {
            board.splice(y, 1);
            board.unshift(Array(COLS).fill(0));
            linesCleared++;
            y++;
        }
    }
    
    if (linesCleared > 0) {
        lines += linesCleared;
        
        // 计分系统
        const lineScores = [0, 100, 300, 500, 800];
        score += lineScores[linesCleared] * level;
        
        // 升级
        const newLevel = Math.floor(lines / 10) + 1;
        if (newLevel > level) {
            level = newLevel;
            dropInterval = Math.max(100, 1000 - (level - 1) * 100);
        }
        
        updateScore();
    }
}

// 更新分数显示
function updateScore() {
    scoreElement.textContent = score;
    levelElement.textContent = level;
    linesElement.textContent = lines;
}

// 生成新方块
function spawnPiece() {
    currentPiece = nextPiece || createPiece(getRandomPieceType());
    nextPiece = createPiece(getRandomPieceType());
    
    // 检查游戏结束
    if (!isValidMove(currentPiece)) {
        gameOver();
        return false;
    }
    
    return true;
}

// 移动方块
function movePiece(dx, dy) {
    if (!currentPiece || isPaused || isGameOver) return false;
    
    if (isValidMove(currentPiece, dx, dy)) {
        currentPiece.x += dx;
        currentPiece.y += dy;
        return true;
    }
    return false;
}

// 硬降落（直接落下）
function hardDrop() {
    if (!currentPiece || isPaused || isGameOver) return;
    
    while (isValidMove(currentPiece, 0, 1)) {
        currentPiece.y++;
        score += 2;
    }
    
    updateScore();
    lockPiece();
    clearLines();
    
    if (!spawnPiece()) {
        return;
    }
}

// 游戏主循环
function update(time = 0) {
    if (isGameOver || isPaused || !isGameStarted) return;
    
    const deltaTime = time - lastTime;
    lastTime = time;
    
    dropCounter += deltaTime;
    
    if (dropCounter > dropInterval) {
        if (!movePiece(0, 1)) {
            lockPiece();
            clearLines();
            
            if (!spawnPiece()) {
                return;
            }
        }
        dropCounter = 0;
    }
    
    draw();
    gameLoop = requestAnimationFrame(update);
}

// 游戏结束
function gameOver() {
    isGameOver = true;
    isGameStarted = false;
    cancelAnimationFrame(gameLoop);
    
    finalScoreElement.textContent = score;
    modal.classList.remove('hidden');
    
    startBtn.disabled = false;
    pauseBtn.disabled = true;
}

// 开始游戏
function startGame() {
    if (isGameStarted) return;
    
    board = createBoard();
    score = 0;
    level = 1;
    lines = 0;
    dropInterval = 1000;
    isGameOver = false;
    isPaused = false;
    isGameStarted = true;
    currentPiece = null;
    nextPiece = null;
    
    updateScore();
    
    startBtn.disabled = true;
    pauseBtn.disabled = false;
    pauseBtn.textContent = '暂停';
    modal.classList.add('hidden');
    
    spawnPiece();
    lastTime = performance.now();
    update();
}

// 暂停/继续游戏
function togglePause() {
    if (!isGameStarted || isGameOver) return;
    
    isPaused = !isPaused;
    
    if (isPaused) {
        pauseBtn.textContent = '继续';
        cancelAnimationFrame(gameLoop);
    } else {
        pauseBtn.textContent = '暂停';
        lastTime = performance.now();
        update();
    }
}

// 重新开始游戏
function restartGame() {
    cancelAnimationFrame(gameLoop);
    modal.classList.add('hidden');
    startGame();
}

// 键盘控制
function handleKeyDown(e) {
    if (!isGameStarted || isGameOver) {
        if (e.key === 'Enter' && !isGameStarted) {
            startGame();
        }
        return;
    }
    
    switch(e.key) {
        case 'ArrowLeft':
            e.preventDefault();
            movePiece(-1, 0);
            break;
        case 'ArrowRight':
            e.preventDefault();
            movePiece(1, 0);
            break;
        case 'ArrowDown':
            e.preventDefault();
            if (movePiece(0, 1)) {
                score += 1;
                updateScore();
            }
            break;
        case 'ArrowUp':
            e.preventDefault();
            rotatePiece();
            break;
        case ' ':
            e.preventDefault();
            hardDrop();
            break;
        case 'p':
        case 'P':
            togglePause();
            break;
    }
    
    draw();
}

// 事件监听
startBtn.addEventListener('click', startGame);
pauseBtn.addEventListener('click', togglePause);
restartBtn.addEventListener('click', restartGame);
modalRestartBtn.addEventListener('click', restartGame);
document.addEventListener('keydown', handleKeyDown);

// 初始化显示
drawBoard();
drawNextPiece();
