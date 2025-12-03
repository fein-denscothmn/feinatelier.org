// ★見出しに下線を引く
document.addEventListener("DOMContentLoaded", function () {
 const headings = document.querySelectorAll("h2, h3, h4");

 window.addEventListener("scroll", function () {
  headings.forEach(function (heading) {
   const rect = heading.getBoundingClientRect();
   if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
    heading.classList.add("visible");
   } else {
    heading.classList.remove("visible");
   }
  });
 });
});


// ★アトリエページのチェックボタン
document.addEventListener('DOMContentLoaded', () => {
 const buttons = document.querySelectorAll('.inline-button');

 buttons.forEach(button => {
  button.addEventListener('click', () => {
   if (button.textContent === '□') {
    button.textContent = '✅';
   } else {
    button.textContent = '□';
   }
  });
 });
});
