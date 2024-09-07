const gameArea = document.getElementById('gameArea');
const scoreElement = document.getElementById('score');
const timerElement = document.getElementById('timer');
const startButton = document.getElementById('startButton');
const shrimp = document.getElementById('shrimp'); // 海老画像の要素を取得

let score = 0;
let timer;
let isGameActive = false;

// ゲームを開始する関数
function startGame() {
    if (isGameActive) return;
    isGameActive = true;
    score = 0;
    scoreElement.textContent = score;
    timerElement.textContent = 30;

    const endTime = Date.now() + 30000; // 30秒後の時間

    // タイマーのセット
    timer = setInterval(() => {
        const timeLeft = Math.max(0, Math.floor((endTime - Date.now()) / 1000));
        timerElement.textContent = timeLeft;
        if (timeLeft === 0) {
            clearInterval(timer);
            isGameActive = false;
            shrimp.style.display = 'none'; // ゲーム終了時に海老を非表示にする
            alert(`ゲーム終了! あなたのスコアは ${score} です。`);
        }
    }, 1000);

    // クリックイベントリスナーのリセット
    shrimp.removeEventListener('click', handleClick);
    
    // 海老を表示する関数を呼び出す
    displayShrimp();
}

// クリックイベントハンドラー
function handleClick() {
    if (isGameActive) {
        score++;
        scoreElement.textContent = score;
        displayShrimp(); // 新しい海老を表示
    }
}

// 海老をランダムに表示する関数
function displayShrimp() {
    if (!isGameActive) return;
    
    // 海老の画像を表示
    shrimp.style.display = 'block';

    // ランダムな位置に海老を配置
    const maxX = gameArea.clientWidth - shrimp.width;
    const maxY = gameArea.clientHeight - shrimp.height;
    const randomX = Math.floor(Math.random() * maxX);
    const randomY = Math.floor(Math.random() * maxY);

    shrimp.style.left = `${randomX}px`;
    shrimp.style.top = `${randomY}px`;

    // クリックイベントの設定
    shrimp.addEventListener('click', handleClick);
}

// ゲーム開始ボタンにイベントリスナーを追加
startButton.addEventListener('click', startGame);
