// データ取得元
const DATA_URL = '/contents/nosql/feinusers.json';

// DOM要素の取得
const nameInput = document.getElementById('search-name');
const roleSelect = document.getElementById('role-filter');
const sortSelect = document.getElementById('sort-order');
const userList = document.getElementById('fein-user-list');
const roleCount = document.getElementById('role-count');

let users = []; // 外部JSONから読み込んだデータを保持

// JSONを読み込む
fetch(DATA_URL)
 .then(response => {
  if (!response.ok) throw new Error('読み込み失敗: ' + response.status);
  return response.json();
 })
 .then(data => {
  users = data;
  updateView(); // 初期表示
 })
 .catch(error => {
  userList.textContent = 'ユーザーデータの読み込みに失敗しました';
  console.error(error);
 });

// 名前による部分一致検索
function filterByName(keyword) {
 return users.filter(user =>
  user.name.toLowerCase().includes(keyword.toLowerCase())
 );
}

// 役割によるフィルタ
function filterByRole(role, list) {
 if (!role) return list;
 return list.filter(user => user.role === role);
}

// ソート処理
function sortUsers(list, order) {
 const sorted = [...list]; // 元の配列を破壊しないようコピー
 switch (order) {
  case 'id-asc':
   sorted.sort((a, b) => a.id - b.id);
   break;
  case 'id-desc':
   sorted.sort((a, b) => b.id - a.id);
   break;
  case 'name-asc':
   sorted.sort((a, b) => a.name.localeCompare(b.name));
   break;
  case 'name-desc':
   sorted.sort((a, b) => b.name.localeCompare(a.name));
   break;
 }
 return sorted;
}

// 役割ごとの人数集計
function countRoles(filteredUsers) {
 return filteredUsers.reduce((acc, user) => {
  acc[user.role] = (acc[user.role] || 0) + 1;
  return acc;
 }, {});
}

// ユーザー一覧を描画
function renderUserList(filteredUsers) {
 userList.innerHTML = '';
 if (filteredUsers.length === 0) {
  userList.textContent = '該当するユーザーが見つかりません';
  return;
 }

 const ul = document.createElement('ul');
 filteredUsers.forEach(user => {
  const li = document.createElement('li');
  li.textContent = `ID: ${user.id} / 名前: ${user.name} / 役割: ${user.role}`;
  ul.appendChild(li);
 });
 userList.appendChild(ul);
}

// 集計結果を描画
function renderRoleCount(filteredUsers) {
 const counts = countRoles(filteredUsers);
 roleCount.textContent = `Admins: ${counts.admin || 0}, Editors: ${counts.editor || 0}, Users: ${counts.user || 0}`;
}

// 検索・フィルタ・ソートの更新処理
function updateView() {
 const keyword = nameInput.value.trim();
 const role = roleSelect.value;
 const sortOrder = sortSelect.value;

 let result = users;
 if (keyword) result = filterByName(keyword);
 result = filterByRole(role, result);
 result = sortUsers(result, sortOrder);

 renderUserList(result);
 renderRoleCount(result);
}

// イベントリスナーの設定
nameInput.addEventListener('input', updateView);
roleSelect.addEventListener('change', updateView);
sortSelect.addEventListener('change', updateView);
