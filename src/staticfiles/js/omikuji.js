const elem = document.getElementById('draw');
const element = document.getElementById('start');
const rotateItem = document.getElementById('rotate');
const target = document.getElementById('draw');

elem.addEventListener('click', function() {
    if (element != null) {
        tatefuri();
    }
});

// 画像のサイズを変更する関数
function resizeImages() {
  const fortune = document.getElementById('fortune');
  const rotateItem = document.getElementById('rotate');

  if (fortune) {
      fortune.style.width = '150px'; // 幅を150ピクセルに設定
      fortune.style.height = 'auto'; // 高さは自動調整
  }

  if (rotateItem) {
      rotateItem.style.width = '200px'; // 幅を200ピクセルに設定
      rotateItem.style.height = 'auto'; // 高さは自動調整
  }
}

// ページ読み込み時にサイズを調整
window.onload = resizeImages;


function tatefuri() {
    element.animate(
        [{
            transform: 'translateY(0)'
        }, {
            transform: 'translateY(-30px)'
        }, {
            transform: 'translateY(0)'
        }], {
            duration: 700,
            iterations: 3
        });
    setTimeout(function() {
        kaiten();
    }, 2400);
}

function kaiten() {
    element.animate(
        [{
            transform: 'rotate(0deg)'
        }, {
            transform: 'rotate(180deg)'
        }], {
            duration: 700,
            easing: 'linear',
            fill: 'forwards'
        });
    setTimeout(function() {
        touka();
        btn();
    }, 1000);
}

function btn() {
    target.animate(
        [{
            opacity: 1
        }, {
            opacity: 0
        }], {
            duration: 500,
            fill: 'forwards'
        });
    setTimeout(function() {
        target.remove();
    }, 500);
}

function touka() {
    element.animate(
        [{
            opacity: 1
        }, {
            opacity: 0
        }], {
            duration: 500,
            fill: 'forwards'
        });
    setTimeout(function() {
        element.remove();
        fortuneAnime();
    }, 500);
}

function fortuneAnime() {
    const key = Math.floor(Math.random() * results.length);
    const fortune = document.getElementById("fortune");
    fortune.src = results[key];
    fortune.animate(
        [{
            transform: 'translateY(0) scale(1)'
        }, {
            transform: 'translateY(-30px)'
        }, {
            transform: 'scale(1)'
        }, {
            transform: 'scale(1.1)'
        }, {
            transform: 'translateY(0) scale(1)'
        }], {
            duration: 1000,
            fill: 'forwards'
        });
}
