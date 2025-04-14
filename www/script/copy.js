document.getElementById('copyText').addEventListener('click', function () {
 const text = this.textContent;
 navigator.clipboard.writeText(text).then(() => {
  alert('招待コードをコピーしました！');
 }).catch(err => {
  alert('招待コードのコピーに失敗しました。申し訳ございませんが、スマホのデフォルト機能を使ってコピー願います。');
  console.error(err);
 });
});
