let moveCount = 0;
let timeTaken = 0;
let timer;
let emptyPosition = { row: 3, col: 3 };  // 空のピースの位置
const puzzleSize = 4;

window.onload = function() {
    createPuzzle();
    document.getElementById('shuffle-button').addEventListener('click', shufflePuzzle);
};

function createPuzzle() {
    const board = document.getElementById('puzzle-board');
    board.innerHTML = '';
    const pieces = [];

    for (let row = 0; row < puzzleSize; row++) {
        for (let col = 0; col < puzzleSize; col++) {
            const piece = document.createElement('div');
            piece.classList.add('puzzle-piece');
            piece.dataset.row = row;
            piece.dataset.col = col;
            piece.style.backgroundPosition = `-${col * 100}px -${row * 100}px`;

            // 空のピースを最後に作成
            if (row === puzzleSize - 1 && col === puzzleSize - 1) {
                piece.classList.add('empty');
                emptyPosition = { row: row, col: col };
            } else {
                piece.addEventListener('click', () => movePiece(row, col));
            }

            pieces.push(piece);
            board.appendChild(piece);
        }
    }
}

function shufflePuzzle() {
    moveCount = 0;
    timeTaken = 0;
    document.getElementById('move-count').textContent = `手数: ${moveCount}`;
    document.getElementById('time-taken').textContent = `タイム: ${timeTaken}秒`;

    clearInterval(timer);
    timer = setInterval(() => {
        timeTaken++;
        document.getElementById('time-taken').textContent = `タイム: ${timeTaken}秒`;
    }, 1000);

    // ランダムにタイルを動かす
    for (let i = 0; i < 100; i++) {
        const neighbors = getNeighboringPieces(emptyPosition.row, emptyPosition.col);
        const randomPiece = neighbors[Math.floor(Math.random() * neighbors.length)];
        swapPieces(randomPiece.row, randomPiece.col, emptyPosition.row, emptyPosition.col);
    }
}

function movePiece(row, col) {
    const neighbors = getNeighboringPieces(emptyPosition.row, emptyPosition.col);

    // クリックされたピースが空のピースの隣なら移動
    const clickedPieceIsNeighbor = neighbors.some(piece => piece.row === row && piece.col === col);

    if (clickedPieceIsNeighbor) {
        swapPieces(row, col, emptyPosition.row, emptyPosition.col);
        moveCount++;
        document.getElementById('move-count').textContent = `手数: ${moveCount}`;

        // ゲームクリアのチェック
        if (checkPuzzleCompletion()) {
            clearInterval(timer);
            alert(`完成！ タイム: ${timeTaken}秒、手数: ${moveCount}`);
        }
    }
}

function swapPieces(row1, col1, row2, col2) {
    const piece1 = document.querySelector(`.puzzle-piece[data-row='${row1}'][data-col='${col1}']`);
    const piece2 = document.querySelector(`.puzzle-piece[data-row='${row2}'][data-col='${col2}']`);

    // データ属性の入れ替え
    const tempRow = piece1.dataset.row;
    const tempCol = piece1.dataset.col;

    piece1.dataset.row = piece2.dataset.row;
    piece1.dataset.col = piece2.dataset.col;
    piece2.dataset.row = tempRow;
    piece2.dataset.col = tempCol;

    // 背景画像位置の入れ替え
    const tempBgPosition = piece1.style.backgroundPosition;
    piece1.style.backgroundPosition = piece2.style.backgroundPosition;
    piece2.style.backgroundPosition = tempBgPosition;

    // クラスの入れ替え（空のピースの移動）
    piece1.classList.toggle('empty');
    piece2.classList.toggle('empty');

    // 空のピースの位置を更新
    emptyPosition = { row: row2, col: col2 };  // 常に正確に更新
}

function getNeighboringPieces(row, col) {
    const neighbors = [];

    // 上下左右の隣接ピースを取得
    if (row > 0) neighbors.push({ row: row - 1, col: col });
    if (row < puzzleSize - 1) neighbors.push({ row: row + 1, col: col });
    if (col > 0) neighbors.push({ row: row, col: col - 1 });
    if (col < puzzleSize - 1) neighbors.push({ row: row, col: col + 1 });

    return neighbors;
}

function checkPuzzleCompletion() {
    let isComplete = true;

    // ピースが正しい順序にあるか確認
    document.querySelectorAll('.puzzle-piece').forEach(piece => {
        const row = parseInt(piece.dataset.row);
        const col = parseInt(piece.dataset.col);
        const correctRow = Math.floor(Array.from(piece.parentNode.children).indexOf(piece) / puzzleSize);
        const correctCol = Array.from(piece.parentNode.children).indexOf(piece) % puzzleSize;

        if (row !== correctRow || col !== correctCol) {
            isComplete = false;
        }
    });

    return isComplete;
}
