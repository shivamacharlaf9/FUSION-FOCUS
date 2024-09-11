let grid, score, timer, time, gameStarted;

document.getElementById('new-game').addEventListener('click', initGame);
document.getElementById('tryagain').addEventListener('click', initGame);

document.addEventListener('keydown', handleInput);

function initGame() {
    grid = createEmptyGrid();
    score = 0;
    time = 0;
    timer = 0;
    gameStarted = false;
    updateScore();
    addRandomTile();
    addRandomTile();
    drawGrid();
    hideGameOverMessage();
}

let pauseButton = document.getElementById('pause-resume');
let isPaused = false;

pauseButton.addEventListener('click', function () {
    if (isPaused) {
        resumeGame();
    } else {
        pauseGame();
    }
});

function pauseGame() {
    isPaused = true;
    clearInterval(timer);
    pauseButton.textContent = 'Resume';
}

function resumeGame() {
    isPaused = false;
    startTime();
    pauseButton.textContent = 'Pause';
}

// Modified the setInterval function to check if the game is paused
function startTime() {
    clearInterval(timer);
    timer = setInterval(() => {
        if (!isPaused) {
            time++;
            document.getElementById('game-time').textContent = 'Time: ' + formatTime(time);
        }
    }, 1000);
}

function createEmptyGrid() {
    return [...Array(4)].map(() => Array(4).fill(0));
}

function addRandomTile() {
    let emptyTiles = [];
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            if (grid[i][j] === 0) {
                emptyTiles.push({ i, j });
            }
        }
    }
    if (emptyTiles.length) {
        let { i, j } = emptyTiles[Math.floor(Math.random() * emptyTiles.length)];
        grid[i][j] = Math.random() > 0.9 ? 4 : 2;
    }
}

// Define a mapping of values to colors
const colorMap = {
    2: '#ffc0cb',   // light pink
    4: '#add8e6',   // light blue
    8: '#98fb98',   // pale green
    16: '#ffd700',  // gold
    32: '#ffa07a',  // light salmon
    64: '#87ceeb',  // sky blue
    128: '#ffff00', // yellow
    256: '#40e0d0', // turquoise
    512: '#ff69b4', // hot pink
    1024: '#7b68ee',// medium slate blue
    2048: '#ff6347',// tomato
    4096: '#a9a9a9' // dark gray
};

function drawGrid() {
    const gridContainer = document.getElementById('grid-container');
    gridContainer.innerHTML = '';
    grid.forEach((row, i) => {
        row.forEach((value, j) => {
            let tile = document.createElement('div');
            tile.className = 'tile';
            if (value) {
                tile.style.backgroundColor = colorMap[value] || '#f4f4f4'; // Apply color based on value
            } else {
                tile.style.backgroundColor = '#f4f4f4'; // Default color for empty cells
            }
            tile.textContent = ''; // Hide the number, display color only
            gridContainer.appendChild(tile);
        });
    });

    if (isGameOver()) {
        showGameOverMessage();
        clearInterval(timer);
    }
}

function handleInput(e) {
    if (isGameOver()) {
        return;
    }

    let key = e.key;
    if (key === 'ArrowUp' || key === 'ArrowDown' || key === 'ArrowLeft' || key === 'ArrowRight') {
        if (!gameStarted) {
            startTime();
            gameStarted = true;
        }

        let oldGrid = JSON.stringify(grid);
        moveTiles(key);
        mergeTiles(key);
        moveTiles(key); // To fill in the gaps after merging
        if (oldGrid !== JSON.stringify(grid)) {
            addRandomTile();
        }
        drawGrid();
        updateScore();
    }
}

function moveTiles(direction) {
    let isVertical = direction === 'ArrowUp' || direction === 'ArrowDown';
    let isForward = direction === 'ArrowRight' || direction === 'ArrowDown';

    for (let i = 0; i < 4; i++) {
        let row = [];
        for (let j = 0; j < 4; j++) {
            let cell = isVertical ? grid[j][i] : grid[i][j];
            if (cell) row.push(cell);
        }

        let missing = 4 - row.length;
        let zeros = Array(missing).fill(0);
        row = isForward ? zeros.concat(row) : row.concat(zeros);

        for (let j = 0; j < 4; j++) {
            if (isVertical) {
                grid[j][i] = row[j];
            } else {
                grid[i][j] = row[j];
            }
        }
    }
}

function mergeTiles(direction) {
    let isVertical = direction === 'ArrowUp' || direction === 'ArrowDown';
    let isForward = direction === 'ArrowRight' || direction === 'ArrowDown';

    for (let i = 0; i < 4; i++) {
        for (let j = isForward ? 3 : 0; isForward ? j > 0 : j < 3; isForward ? j-- : j++) {
            let current = isVertical ? grid[j][i] : grid[i][j];
            let next = isVertical ? grid[isForward ? j - 1 : j + 1][i] : grid[i][isForward ? j - 1 : j + 1];
            if (current !== 0 && current === next) {
                let mergedTile = current * 2;
                isVertical ? grid[j][i] = mergedTile : grid[i][j] = mergedTile;
                isVertical ? grid[isForward ? j - 1 : j + 1][i] = 0 : grid[i][isForward ? j - 1 : j + 1] = 0;
                score += mergedTile;
                break; // Prevent double merge in one swipe
            }
        }
    }
}

function updateScore() {
    document.getElementById('game-score').textContent = 'Score: ' + score;
}

function formatTime(timeInSeconds) {
    let minutes = Math.floor(timeInSeconds / 60);
    let seconds = timeInSeconds % 60;
    return minutes.toString().padStart(2, '0') + ':' + seconds.toString().padStart(2, '0');
}

function isGameOver() {
    return isGridFull() && !canMakeMove();
}

function isGridFull() {
    return grid.every(row => row.every(cell => cell !== 0));
}

function canMakeMove() {
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            let value = grid[i][j];
            if (value !== 0) {
                if (i < 3 && value === grid[i + 1][j]) return true;
                if (j < 3 && value === grid[i][j + 1]) return true;
            }
        }
    }
    return false;
}

function showGameOverMessage() {
    const gameOverMessage = document.getElementById('game-over');
    gameOverMessage.style.cssText = 'display: block; ';
}

function hideGameOverMessage() {
    const gameOverMessage = document.getElementById('game-over');
    gameOverMessage.style.cssText = 'display: none; ';
    initGame();
}

initGame();
