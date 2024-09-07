const ebi = document.getElementById('ebi');
const enemiesContainer = document.getElementById('enemies');
const bulletsContainer = document.getElementById('bullets');
const scoreElement = document.getElementById('score');
const restartBtn = document.getElementById('restart-btn');
let score = 0;
let gameOver = false;
let lives = 1;
let powerUpActive = false;
let powerUpTimer = null;
let enemyInterval = 1000;
let enemySpeed = 2;

function moveEbi(e) {
  if (!gameOver) {
    ebi.style.left = `${e.clientX - 25}px`;
  }
}

function createEnemy() {
  if (!gameOver) {
    const enemyType = Math.random() < 0.3 ? 'straight' : Math.random() < 0.6 ? 'zigzag' : Math.random() < 0.8 ? 'random' : 'chasing';
    const enemy = document.createElement('div');
    enemy.className = `enemy-${enemyType}`;
    enemy.style.left = `${Math.random() * (window.innerWidth - 30)}px`;
    enemiesContainer.appendChild(enemy);
    let position = -30;
    let direction = 1;
    const interval = setInterval(() => {
      if (enemyType === 'straight') {
        position += enemySpeed;
        enemy.style.top = `${position}px`;
      } else if (enemyType === 'zigzag') {
        position += enemySpeed;
        enemy.style.top = `${position}px`;
        enemy.style.left = `${parseFloat(enemy.style.left) + direction * enemySpeed}px`;
        if (parseFloat(enemy.style.left) <= 0 || parseFloat(enemy.style.left) >= window.innerWidth - 30) {
          direction *= -1;
        }
      } else if (enemyType === 'random') {
        position += enemySpeed;
        enemy.style.top = `${position}px`;
        enemy.style.left = `${parseFloat(enemy.style.left) + (Math.random() - 0.5) * enemySpeed * 2}px`;
      } else if (enemyType === 'chasing') {
        position += enemySpeed / 2;
        enemy.style.top = `${position}px`;
        const enemyX = parseFloat(enemy.style.left);
        const ebiX = parseFloat(ebi.style.left);
        enemy.style.left = `${enemyX + (ebiX - enemyX) * 0.02}px`;
      }
      if (isColliding(ebi, enemy)) {
        enemiesContainer.removeChild(enemy);
        clearInterval(interval);
        lives--;
        if (lives <= 0) {
          gameOver = true;
          const rank = score >= 100 ? 'S' : score >= 50 ? 'A' : score >= 20 ? 'B' : 'C';
          alert(`ゲームオーバー！スコア: ${score} (ランク: ${rank})`);
          enemiesContainer.innerHTML = '';
          bulletsContainer.innerHTML = '';
          restartBtn.style.display = 'block';
        }
      }
      if (position >= 600) {
        enemiesContainer.removeChild(enemy);
        clearInterval(interval);
      }
    }, 20);

    createEnemyBullet(enemy);
  }
}

function createEnemyBullet(enemy) {
  if (!gameOver) {
    const enemyBullet = document.createElement('div');
    enemyBullet.className = 'enemy-bullet';
    enemyBullet.style.left = `${enemy.offsetLeft + 12.5}px`;
    enemyBullet.style.top = `${enemy.offsetTop + 30}px`;
    bulletsContainer.appendChild(enemyBullet);
    let position = enemyBullet.offsetTop;
    const interval = setInterval(() => {
      position += 5;
      enemyBullet.style.top = `${position}px`;
      if (isCollidingWithEbiAndBullet(ebi, enemyBullet)) {
        bulletsContainer.removeChild(enemyBullet);
        clearInterval(interval);
        lives--;
        if (lives <= 0) {
          gameOver = true;
          const rank = score >= 100 ? 'S' : score >= 50 ? 'A' : score >= 20 ? 'B' : 'C';
          alert(`ゲームオーバー！スコア: ${score} (ランク: ${rank})`);
          enemiesContainer.innerHTML = '';
          bulletsContainer.innerHTML = '';
          restartBtn.style.display = 'block';
        }
      }
      if (position >= 600) {
        bulletsContainer.removeChild(enemyBullet);
        clearInterval(interval);
      }
    }, 20);
  }
}

function createPowerUp() {
  if (!gameOver) {
    const powerUp = document.createElement('div');
    powerUp.className = 'power-up';
    powerUp.style.left = `${Math.random() * (window.innerWidth - 30)}px`;
    enemiesContainer.appendChild(powerUp);
    let position = -30;
    const interval = setInterval(() => {
      position += 2;
      powerUp.style.top = `${position}px`;
      if (isColliding(ebi, powerUp)) {
        enemiesContainer.removeChild(powerUp);
        clearInterval(interval);
        activatePowerUp();
      }
      if (position >= 600) {
        enemiesContainer.removeChild(powerUp);
        clearInterval(interval);
      }
    }, 20);
  }
}

function activatePowerUp() {
  powerUpActive = true;
  if (powerUpTimer) {
    clearTimeout(powerUpTimer);
  }
  powerUpTimer = setTimeout(() => {
    powerUpActive = false;
  }, 5000);
}

function createBullet() {
  if (!gameOver) {
    const bullet = document.createElement('div');
    bullet.className = 'bullet';
    bullet.style.left = `${ebi.offsetLeft + 22.5}px`;
    bullet.style.top = `${ebi.offsetTop}px`;
    bulletsContainer.appendChild(bullet);
    let position = bullet.offsetTop;
    const speed = powerUpActive ? 10 : 5;
    const interval = setInterval(() => {
      position -= speed;
      bullet.style.top = `${position}px`;
      const enemies = document.querySelectorAll('.enemy-straight, .enemy-zigzag, .enemy-random, .enemy-chasing');
      enemies.forEach(enemy => {
        if (isColliding(bullet, enemy)) {
          enemiesContainer.removeChild(enemy);
          bulletsContainer.removeChild(bullet);
          clearInterval(interval);
          score++;
          scoreElement.textContent = `スコア: ${score}`;
        }
      });
      if (position <= 0) {
        bulletsContainer.removeChild(bullet);
        clearInterval(interval);
      }
    }, 20);
  }
}

function isColliding(obj1, obj2) {
  const rect1 = obj1.getBoundingClientRect();
  const rect2 = obj2.getBoundingClientRect();
  return !(
    rect1.bottom < rect2.top ||
    rect1.top > rect2.bottom ||
    rect1.right < rect2.left ||
    rect1.left > rect2.right
  );
}

function isCollidingWithEbiAndBullet(obj1, obj2) {
  const rect1 = obj1.getBoundingClientRect();
  const rect2 = obj2.getBoundingClientRect();
  return !(
    rect1.bottom < rect2.top ||
    rect1.top > rect2.bottom ||
    rect1.right < rect2.left ||
    rect1.left > rect2.right
  );
}

function restartGame() {
  gameOver = false;
  score = 0;
  lives = 1;
  scoreElement.textContent = `スコア: ${score}`;
  restartBtn.style.display = 'none';
  enemyInterval = 1000;
  enemySpeed = 2;
}

document.addEventListener('mousemove', moveEbi);
document.addEventListener('click', createBullet);
restartBtn.addEventListener('click', restartGame);

setInterval(() => {
  createEnemy();
  if (enemyInterval > 500) {
    enemyInterval -= 10;
  }
  if (enemySpeed < 5) {
    enemySpeed += 0.01;
  }
}, enemyInterval);

setInterval(createPowerUp, 10000);