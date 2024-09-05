window.onload = function() {
    // =====================================
    // 関数定義
    // =====================================
    var startTime;  // 開始時間を記録する変数
    var timerInterval;  // タイマーのインターバルID

    // 初期化用関数
    function init() {
        var arr = [''];
        for(i = 0; i < 8; i++) {
            arr.push((i + 1).toString());
        }
        shuffle(arr);
        if (!isSolved(arr.slice(0, arr.length))) {
            init();
        } else {
            render(arr);
            startTimer();
        }
    }

    // タイマーをスタートする関数
    function startTimer() {
        startTime = Date.now();
        timerInterval = setInterval(updateTimer, 1000);
    }

    // タイマーを更新する関数
    function updateTimer() {
        var elapsedTime = Math.floor((Date.now() - startTime) / 1000);
        var minutes = Math.floor(elapsedTime / 60);
        var seconds = elapsedTime % 60;
        document.getElementById('timer').textContent = `経過時間: ${minutes}分 ${seconds}秒`;
    }

    // タイマーをストップする関数
    function stopTimer() {
        clearInterval(timerInterval);
    }

    // 完成判定を行う関数
    function checkCompletion(arr) {
        var isComplete = arr.slice(0, arr.length - 1).every((val, index) => val == (index + 1).toString()) && arr[arr.length - 1] === '';
        if (isComplete) {
            stopTimer();
            alert('パズルが完成しました！');
        }
        return isComplete;
    }

    // 配列シャッフル用関数
    function shuffle(arr) {
        var i = arr.length;
        while (i) {
            var j = Math.floor(Math.random() * i--);
            swap(i, j, arr);
        }
    }

    // 配列の値入れ替え用関数
    function swap(i, j, arr) {
        var tmp = arr[i];
        arr[i] = arr[j];
        arr[j] = tmp;
    }

    // 解決可能なパズルかを判定する関数
    function isSolved(arr) {
        var blank_index = arr.indexOf('');
        var dist_vertical = Math.floor(((arr.length - 1) - blank_index) / Math.sqrt(arr.length));
        var dist_horizontal = ((arr.length - 1) - blank_index) % Math.sqrt(arr.length);
        var dist = dist_vertical + dist_horizontal;

        var answer = [];
        for (i = 0; i < 8; i++) {
            answer.push((i + 1).toString());
        }
        answer.push('');

        var count = 0;
        for (var i = 0; i < answer.length; i++) {
            for (var j = i + 1; j < answer.length; j++) {
                if (i + 1 == arr[j]) {
                    swap(i, j, arr);
                    count++;
                }
            }
            if (arr.toString() === answer.toString()) {
                break;
            }
        }

        return count % 2 === dist % 2;
    }

    // パズル描画用関数
    function render(arr) {
        var $jsShowPanel = document.getElementById('js-show-panel');
        while ($jsShowPanel.firstChild) {
            $jsShowPanel.removeChild($jsShowPanel.firstChild);
        }

        var fragment = document.createDocumentFragment();
        arr.forEach(function(element) {
            var tileWrapper = document.createElement('div');
            tileWrapper.className = 'tile-wrapper';

            var tile = document.createElement('div');
            tile.className = element != '' ? 'tile tile-' + element : 'tile tile-none';
            tile.textContent = element;

            tileWrapper.appendChild(tile);
            fragment.appendChild(tileWrapper);
        });
        $jsShowPanel.appendChild(fragment);
        addEventListenerClick(arr);
    }

    // パズルをクリックイベント追加用関数
    function addEventListenerClick(arr) {
        var $tile = document.querySelectorAll('.tile');
        $tile.forEach(function(elem) {
            elem.addEventListener('click', function() {
                var i = arr.indexOf(this.textContent);
                var j;
                if (i <= 5 && arr[i + 3] == '') {
                    j = i + 3;
                } else if (i >= 3 && arr[i - 3] == '') {
                    j = i - 3;
                } else if (i % 3 != 2 && arr[i + 1] == '') {
                    j = i + 1;
                } else if (i % 3 != 0 && arr[i - 1] == '') {
                    j = i - 1;
                } else {
                    return;
                }
                swap(i, j, arr);
                render(arr);
                checkCompletion(arr);  // 完成判定
            });
        });
    }

    // メイン処理
    init();
    document.getElementById('original').addEventListener('click', function() {
        init();
    });
}
