// document.addEventListener('DOMContentLoaded', () => {
//     let score = 0;
//     const scoreDisplay = document.getElementById('score');
//     const ebis = document.querySelectorAll('.ebi');

//     // ランダムな時間で状態を変更するための関数
//     function getRandomTime(min, max) {
//         return Math.random() * (max - min) + min;
//     }

//     // エビの状態を管理する関数
//     function changeEbiState(ebi) {
//         let state = parseInt(ebi.getAttribute('data-state'));  // HTMLのdata-stateから状態を取得

//         const changeState = () => {
//             state = parseInt(ebi.getAttribute('data-state'));  // 状態を毎回取得
//             switch (state) {
//                 case 0:
//                     ebi.setAttribute('data-state', '1');  // 次の状態に変更
//                     setTimeout(changeState, getRandomTime(3000, 7000));
//                     break;
//                 case 1:
//                     ebi.setAttribute('data-state', '2');
//                     setTimeout(changeState, getRandomTime(3000, 7000));
//                     break;
//                 case 2:
//                     ebi.setAttribute('data-state', '3');
//                     setTimeout(resetEbi, getRandomTime(3000, 5000));
//                     break;
//             }
//         };

//         const resetEbi = () => {
//             ebi.setAttribute('data-state', '0');  // 状態をリセット
//             setTimeout(changeState, getRandomTime(3000, 7000));
//         };

//         ebi.addEventListener('click', () => {
//             let currentState = parseInt(ebi.getAttribute('data-state'));  // クリック時に状態を取得

//             if (currentState !== 0) {
//                 ebi.style.visibility = 'hidden';  // 一旦非表示に
//                 setTimeout(() => {
//                     ebi.style.visibility = 'visible';  // 再表示してリセット
//                     resetEbi();
//                 }, 500);
//             }

//             if (currentState === 2) {
//                 score++;
//                 scoreDisplay.textContent = score;
//             }
//         });

//         setTimeout(changeState, getRandomTime(3000, 7000));
//     }

//     // すべてのエビをセット
//     ebis.forEach(changeEbiState);
// });

document.addEventListener('DOMContentLoaded', () => {
    let score = 0;
    const scoreDisplay = document.getElementById('score');
    const ebis = document.querySelectorAll('.ebi');

    // ランダムな時間で状態を変更するための関数
    function getRandomTime(min, max) {
        return Math.random() * (max - min) + min;
    }

    // 画像を状態に応じて変更する関数
    function updateEbiImage(ebi) {
        const state = parseInt(ebi.getAttribute('data-state'));
        switch (state) {
            case 0:
                ebi.src = "/static/img/yaki0.png";
                break;
            case 1:
                ebi.src = "/static/img/yaki1.png";
                break;
            case 2:
                ebi.src = "/static/img/yaki2.png";
                break;
            case 3:
                ebi.src = "/static/img/yaki3.png";
                break;
        }
    }

    // エビの状態を管理する関数
    function changeEbiState(ebi) {
        let state = parseInt(ebi.getAttribute('data-state'));  // HTMLのdata-stateから状態を取得

        const changeState = () => {
            state = parseInt(ebi.getAttribute('data-state'));  // 状態を毎回取得
            switch (state) {
                case 0:
                    ebi.setAttribute('data-state', '1');  // 次の状態に変更
                    updateEbiImage(ebi);  // 画像を更新
                    setTimeout(changeState, getRandomTime(3000, 7000));
                    break;
                case 1:
                    ebi.setAttribute('data-state', '2');
                    updateEbiImage(ebi);  // 画像を更新
                    setTimeout(changeState, getRandomTime(3000, 7000));
                    break;
                case 2:
                    ebi.setAttribute('data-state', '3');
                    updateEbiImage(ebi);  // 画像を更新
                    setTimeout(resetEbi, getRandomTime(3000, 5000));
                    break;
            }
        };

        const resetEbi = () => {
            ebi.setAttribute('data-state', '0');  // 状態をリセット
            updateEbiImage(ebi);  // 画像をリセット
            setTimeout(changeState, getRandomTime(3000, 7000));
        };

        ebi.addEventListener('click', () => {
            let currentState = parseInt(ebi.getAttribute('data-state'));  // クリック時に状態を取得

            if (currentState !== 0) {
                ebi.style.visibility = 'hidden';  // 一旦非表示に
                setTimeout(() => {
                    ebi.style.visibility = 'visible';  // 再表示してリセット
                    resetEbi();
                }, 500);
            }

            if (currentState === 2) {
                score++;
                scoreDisplay.textContent = score;
            }
        });

        setTimeout(changeState, getRandomTime(3000, 7000));
    }

    // すべてのエビをセット
    ebis.forEach(changeEbiState);
});
