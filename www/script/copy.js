document.getElementById('copyText').addEventListener('click', function () {
 const text = this.textContent;
 navigator.clipboard.writeText(text).then(() => {
  alert('招待コードをコピーしました。『アナザーエデン 時空を超える猫』×『FINAL FANTASY IX』コラボを楽しんでくださいね♪');
 }).catch(err => {
  alert('招待コードのコピーに失敗しました。申し訳ございませんが、お使いのモバイルデバイスの機能を使ってコピー願います。');
  console.error(err);
 });
});
