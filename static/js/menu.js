function toggleMenu() {
 var menu = document.getElementById('fden-menu');
 var button = document.getElementById('fden-hamburger-button');
 if (menu.classList.contains('show')) {
  menu.classList.remove('show');
  button.innerHTML = '☰ メニューを開く ▼';
  setTimeout(function () {
   menu.style.display = 'none';
  }, 300);
 } else {
  menu.style.display = 'block';
  button.innerHTML = '× メニューを閉じる ▲';
  setTimeout(function () {
   menu.classList.add('show');
  }, 10);
 }
}

function toggleSubMenu(id, buttonId, event) {
 event.preventDefault(); // デフォルト動作を防止
 var submenu = document.getElementById(id);
 var button = document.getElementById(buttonId);
 if (submenu.classList.contains('show')) {
  submenu.classList.remove('show');
  button.innerHTML = button.innerHTML.replace('▲', '▼');
  setTimeout(function () {
   submenu.style.display = 'none';
  }, 300);
 } else {
  submenu.style.display = 'block';
  button.innerHTML = button.innerHTML.replace('▼', '▲');
  setTimeout(function () {
   submenu.classList.add('show');
  }, 10);
 }
}

document.addEventListener('DOMContentLoaded', function () {
 fetch('/static/menu/menu.html')
  .then(response => response.text())
  .then(data => {
   document.getElementById('fden-menu-content').innerHTML = data;
  });

 document.addEventListener('click', function (event) {
  var menu = document.getElementById('fden-menu');
  var button = document.getElementById('fden-hamburger-button');
  var isClickInside = menu.contains(event.target) || button.contains(event.target);
  if (!isClickInside && menu.classList.contains('show')) {
   menu.classList.remove('show');
   button.innerHTML = '☰ メニューを開く ▼';
   setTimeout(function () {
    menu.style.display = 'none';
   }, 300);
  }
 });
});

document.addEventListener("DOMContentLoaded", function () {
 const links = document.querySelectorAll(".animated-link");
 links.forEach(link => {
  link.classList.add("loaded");
 });
});
