document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('container');
    const imageUrl = "/static/img/fall_ebi.png";

    function createObject(x, y) {
        const newObject = document.createElement('img'); // img要素を作成
        newObject.className = 'object';
        newObject.src = imageUrl; // ここに画像のパスを指定
        newObject.style.position = 'absolute'; // 画像を絶対配置
        newObject.style.left = `${x - 10}px`;  // 中心がクリック位置になるように調整
        newObject.style.top = `${y - 10}px`;   // 中心がクリック位置になるように調整
        container.appendChild(newObject);

        // 落下アニメーションの開始
        setTimeout(() => {
            newObject.style.transform = `translateY(${window.innerHeight - y - 60}px)`;
            newObject.style.transition = 'transform 2s ease';
        }, 10);
    }

    // タッチイベント（モバイル対応）
    container.addEventListener('touchend', (event) => {
        // タッチの座標を取得
        const touch = event.changedTouches[0];
        createObject(touch.clientX, touch.clientY);
    });

    // マウスクリックイベント
    container.addEventListener('click', (event) => {
        createObject(event.clientX, event.clientY);
    });
});
