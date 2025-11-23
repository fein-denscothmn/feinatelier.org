// ★スクロールを追いかけるボタンを実装する
window.onscroll = function () {
 var scrollToTopBtn = document.getElementById("scrollToTopBtn");
 if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
  scrollToTopBtn.style.display = "block";
 } else {
  scrollToTopBtn.style.display = "none";
 }
};

function scrollToTop() {
 const scrollDuration = 800;
 const scrollStep = -window.scrollY / (scrollDuration / 15);
 const scrollInterval = setInterval(() => {
  if (window.scrollY !== 0) {
   window.scrollBy(0, scrollStep);
  } else {
   clearInterval(scrollInterval);
  }
 }, 15);
}

// ★ヘッダーのロゴ画像をスクロールする
document.addEventListener("DOMContentLoaded", function () {
 const headerImage = document.querySelector('.header-image');

 headerImage.style.opacity = 0;
 headerImage.style.transform = 'translateX(100%)';

 setTimeout(() => {
  headerImage.style.opacity = 1;
  headerImage.style.transform = 'translateX(0)';
  console.log("Header image is visible");
 }, 100);
});

// ★タイピングエフェクト
document.addEventListener("DOMContentLoaded", function () {
 const codeBlocks = document.querySelectorAll("code.feintyping");

 const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
   if (entry.isIntersecting) {
    const codeEl = entry.target;
    if (codeEl.dataset.typed) return; // 二重実行防止
    codeEl.dataset.typed = "true";

    const text = codeEl.textContent.trim();
    codeEl.textContent = ""; // 一旦空にしてからタイプ開始

    // カーソル用の span を追加
    const cursor = document.createElement("span");
    cursor.className = "cursor";
    codeEl.appendChild(cursor);

    // 1秒遅延してからタイプ開始
    setTimeout(() => {
     let i = 0;
     function typeChar() {
      if (i < text.length) {
       // カーソルの前に文字を挿入
       cursor.insertAdjacentText("beforebegin", text[i]);
       i++;

       // 基本のランダム打鍵速度を倍速に
       let delay = 15 + Math.random() * 60;

       // 改行後は少し長めに待つ
       if (text[i - 1] === "\n") {
        delay += 200;
       }

       // 時々「考えている間」のように止まる
       if (Math.random() < 0.02) {
        delay += 400;
       }

       setTimeout(typeChar, delay);
      } else {
       cursor.remove(); // タイピング終了後カーソル削除
       Prism.highlightElement(codeEl); // ハイライト適用
      }
     }
     typeChar();
    }, 1000); // 1秒待ってから開始
   }
  });
 }, { threshold: 0.3 }); // 30%見えたら発火

 codeBlocks.forEach((block) => observer.observe(block));
});
