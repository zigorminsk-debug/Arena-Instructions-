# -*- coding: utf-8 -*-
"""Сборка защищённого HTML-приложения русской инструкции.
python3 build_html_app.py -> /home/user/Arena_Instruction_App.html"""
import base64
import glob
import json

OUT = "/home/user/Arena_Instruction_App.html"

pages = []
for f in sorted(glob.glob("/tmp/pgs/*.jpg")):
    b = open(f, "rb").read()
    pages.append("data:image/jpeg;base64," + base64.b64encode(b).decode())

TEMPLATE = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Инструкция по работе с AI Arena · Agent Mode</title>
<style>
  :root{
    --bg:#0b1526; --card:#101d33; --line:#233654; --acc:#2563eb; --acc2:#38bdf8;
    --txt:#e8eefb; --mut:#8fa3c4; --bad:#ef4444; --ok:#22c55e;
  }
  *{margin:0;padding:0;box-sizing:border-box;
    -webkit-user-select:none;user-select:none;
    -webkit-touch-callout:none;-webkit-tap-highlight-color:transparent;}
  html,body{height:100%;}
  body{background:var(--bg);color:var(--txt);
    font-family:"Segoe UI",Roboto,Arial,sans-serif;overflow:hidden;}
  img{-webkit-user-drag:none;pointer-events:none;}
  a{color:var(--acc2);}
  .hidden{display:none !important;}
  /* ---------- логин ---------- */
  #login{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;
    background:radial-gradient(1200px 600px at 70% -10%,#16305c 0%,var(--bg) 60%);}
  .lcard{width:min(430px,92vw);background:var(--card);border:1px solid var(--line);
    border-radius:16px;padding:34px 34px 26px;box-shadow:0 24px 70px #0009;}
  .logo{display:flex;gap:12px;align-items:center;margin-bottom:8px;}
  .logo svg{flex:0 0 auto;}
  .logo b{font-size:19px;letter-spacing:.3px;}
  .logo small{display:block;color:var(--mut);font-size:12px;margin-top:2px;}
  .lcard h1{font-size:16px;margin:14px 0 4px;color:var(--acc2);}
  .lcard p.sub{color:var(--mut);font-size:13px;margin-bottom:20px;line-height:1.45;}
  label{display:block;font-size:12px;color:var(--mut);margin:12px 0 5px;letter-spacing:.4px;}
  input{width:100%;background:#0a1424;border:1px solid var(--line);border-radius:9px;
    color:var(--txt);padding:11px 12px;font-size:15px;outline:none;}
  input:focus{border-color:var(--acc);}
  #btnLogin{width:100%;margin-top:20px;background:var(--acc);border:0;border-radius:9px;
    color:#fff;font-size:15px;font-weight:600;padding:12px;cursor:pointer;}
  #btnLogin:hover{background:#1d4fd7;}
  #loginErr{color:var(--bad);font-size:13px;margin-top:12px;min-height:18px;}
  .devline{margin-top:18px;padding-top:14px;border-top:1px solid var(--line);
    color:var(--mut);font-size:12px;line-height:1.7;}
  /* ---------- просмотр ---------- */
  #top{position:fixed;top:0;left:0;right:0;height:52px;background:var(--card);
    border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;
    padding:0 14px;z-index:5;}
  #top .t{font-size:14px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
  .chip{background:#0a1424;border:1px solid var(--line);border-radius:999px;
    padding:4px 11px;font-size:12px;color:var(--acc2);white-space:nowrap;}
  .chip.warn{color:#fbbf24;border-color:#6b5b1e;}
  #top .sp{flex:1;}
  #nav{position:fixed;bottom:0;left:0;right:0;height:56px;background:var(--card);
    border-top:1px solid var(--line);display:flex;align-items:center;justify-content:center;
    gap:12px;z-index:5;}
  #nav button{background:#0a1424;border:1px solid var(--line);color:var(--txt);
    border-radius:9px;padding:9px 16px;font-size:14px;cursor:pointer;}
  #nav button:hover{border-color:var(--acc);}
  #pglbl{font-size:13px;color:var(--mut);min-width:90px;text-align:center;}
  #stage{position:fixed;top:52px;bottom:56px;left:0;right:0;overflow:auto;
    display:flex;justify-content:center;background:#060d1a;}
  #pageImg{max-width:100%;box-shadow:0 0 40px #000a;background:#fff;}
  /* водяной знак */
  #wm{position:fixed;inset:0;z-index:6;pointer-events:none;overflow:hidden;opacity:.08;}
  #wm span{position:absolute;color:#fff;font-size:15px;white-space:nowrap;
    transform:rotate(-28deg);font-weight:600;}
  /* защита от скриншота при потере фокуса */
  #cover{position:fixed;inset:0;z-index:9;background:var(--bg);display:flex;
    align-items:center;justify-content:center;flex-direction:column;gap:14px;text-align:center;}
  #cover .big{font-size:20px;font-weight:700;}
  #cover p{color:var(--mut);font-size:14px;max-width:420px;line-height:1.5;}
  /* печать запрещена */
  #printBlock{display:none;}
  @media print{
    #top,#nav,#stage,#wm,#login,#limit{display:none !important;}
    #printBlock{display:block !important;padding:40px;font-size:16px;color:#000;}
  }
  /* ---------- лимит исчерпан ---------- */
  #limit{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;
    background:radial-gradient(1000px 500px at 50% -10%,#3b1620 0%,var(--bg) 60%);}
  .dcard{width:min(470px,92vw);background:var(--card);border:1px solid #5b2330;
    border-radius:16px;padding:34px;box-shadow:0 24px 70px #0009;text-align:center;}
  .dcard h1{font-size:20px;margin:14px 0 8px;}
  .dcard p{color:var(--mut);font-size:14px;line-height:1.55;margin-bottom:20px;}
  .drow{background:#0a1424;border:1px solid var(--line);border-radius:10px;
    padding:10px 14px;margin:8px 0;font-size:14px;display:flex;justify-content:space-between;}
  .drow b{color:var(--mut);font-weight:500;}
</style>
</head>
<body>

<!-- ================= ЛОГИН ================= -->
<div id="login">
  <div class="lcard">
    <div class="logo">
      <svg width="40" height="40" viewBox="0 0 40 40"><rect x="1" y="1" width="38" height="38" rx="9" fill="#2563eb"/><path d="M12 26 L20 10 L28 26 M15.2 20 h9.6" stroke="#fff" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>
      <div><b>AI Arena · Agent Mode</b><small>защищённое издание инструкции</small></div>
    </div>
    <h1>Вход по личному паролю</h1>
    <p class="sub">Каждому пользователю выдаётся личный логин и пароль. Доступно <b>5 просмотров</b>;
      счётчик хранится на сервере защиты и не сбрасывается ни очисткой кеша, ни открытием
      на другом устройстве. Печать, копирование, скриншоты и изменение запрещены.</p>
    <label>ПОЛЬЗОВАТЕЛЬ</label>
    <input id="inpUser" autocomplete="off" spellcheck="false">
    <label>ПАРОЛЬ</label>
    <input id="inpPass" type="password" autocomplete="off">
    <button id="btnLogin">Открыть инструкцию</button>
    <div id="loginErr"></div>
    <div class="devline">разработчик: Zakharevich Igor ·
      <a href="mailto:&#122;&#105;&#118;&#64;&#99;&#115;&#108;&#46;&#98;&#121;">&#122;&#105;&#118;&#64;&#99;&#115;&#108;&#46;&#98;&#121;</a> ·
      <a href="http://csl.by">csl.by</a> ·
      <a href="tel:+375293371412">+375 29 337-14-12</a></div>
  </div>
</div>

<!-- ================= ПРОСМОТР ================= -->
<div id="app" class="hidden">
  <div id="top">
    <div class="t">Инструкция по работе с AI Arena · Agent Mode</div>
    <div class="sp"></div>
    <div class="chip" id="chipUser"></div>
    <div class="chip warn" id="chipLeft"></div>
  </div>
  <div id="stage"><img id="pageImg" alt=""></div>
  <div id="nav">
    <button id="bPrev">← Назад</button>
    <div id="pglbl"></div>
    <button id="bNext">Вперёд →</button>
  </div>
</div>
<div id="wm" class="hidden"></div>
<div id="cover" class="hidden">
  <svg width="54" height="54" viewBox="0 0 54 54"><rect x="10" y="22" width="34" height="26" rx="5" fill="#2563eb"/><path d="M17 22 v-7 a10 10 0 0 1 20 0 v7" stroke="#2563eb" stroke-width="5" fill="none"/></svg>
  <div class="big">Просмотр приостановлен</div>
  <p>Вернитесь в окно приложения: содержимое скрывается, пока окно не активно, —
     это защита от скриншотов и записи экрана.</p>
</div>

<!-- ================= ЛИМИТ ================= -->
<div id="limit" class="hidden">
  <div class="dcard">
    <svg width="52" height="52" viewBox="0 0 52 52"><circle cx="26" cy="26" r="24" fill="none" stroke="#ef4444" stroke-width="3"/><path d="M26 14 v15 M26 35.5 v3" stroke="#ef4444" stroke-width="4" stroke-linecap="round"/></svg>
    <h1>Доступ завершён</h1>
    <p>Вы использовали все 5 просмотров инструкции.
       Для продления доступа свяжитесь с разработчиком:</p>
    <div class="drow"><b>Разработчик</b><span>Zakharevich Igor</span></div>
    <div class="drow"><b>E-mail</b><a href="mailto:&#122;&#105;&#118;&#64;&#99;&#115;&#108;&#46;&#98;&#121;">&#122;&#105;&#118;&#64;&#99;&#115;&#108;&#46;&#98;&#121;</a></div>
    <div class="drow"><b>Сайт</b><a href="http://csl.by">csl.by</a></div>
    <div class="drow"><b>Телефон</b><a href="tel:+375293371412">+375 29 337-14-12</a></div>
  </div>
</div>

<div id="printBlock">Печать этого документа запрещена. По вопросам доступа:
  разработчик Zakharevich Igor, &#122;&#105;&#118;&#64;&#99;&#115;&#108;&#46;&#98;&#121;, csl.by, +375 29 337-14-12.</div>

<script>
"use strict";
/* ================= КОНФИГУРАЦИЯ =================
   users  — обычные пользователи: личный пароль и лимит просмотров.
   owner  — владелец: без лимита, полные права.
   Добавить пользователя: дописать строку в users.                */
/* api: "" — если приложение открывается с этого же сервера защиты;
   укажите "https://ваш-домен" — если раздаёте html-файл отдельно от сервера. */
var CONFIG = {
  api: "",
  owner: { name: "developer", pass: "turbo2*(+" },
  dev: { name: "Zakharevich Igor", email: "ziv" + "@" + "csl.by",
         site: "csl.by", phone: "+375 29 337-14-12" }
};
var PAGES = __PAGES_JSON__;

/* ---------- счётчик ведёт сервер защиты: в файле и в браузере ничего не хранится,
   поэтому сброс кеша, другое устройство или пересохранение файла не обнуляют лимит ---------- */
var leftNow = 0;

/* ---------- элементы ---------- */
var $ = function(id){ return document.getElementById(id); };
var loginEl=$("login"), appEl=$("app"), limitEl=$("limit"), wmEl=$("wm"), coverEl=$("cover");
var cur = 0, curUser = "", curMax = 0, isOwner = false;

/* ---------- вход ---------- */
function tryLogin(){
  var u = $("inpUser").value.trim(), p = $("inpPass").value, err = $("loginErr");
  /* владелец проверяется локально и работает даже без интернета */
  if (u === CONFIG.owner.name && p === CONFIG.owner.pass){
    isOwner = true; curUser = u; curMax = -1; openViewer(); return;
  }
  err.textContent = "Проверка доступа на сервере защиты…";
  fetch(CONFIG.api + "/api/check", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({user: u, pass: p})
  }).then(function(r){ return r.json(); }).then(function(res){
    if (res.limit){ showLimit(); return; }
    if (res.ok){
      isOwner = false; curUser = u; curMax = res.max; leftNow = res.left;
      openViewer();
    } else { err.textContent = "Неверный логин или пароль."; }
  }).catch(function(){
    err.textContent = "Нет связи с сервером защиты: нужно подключение к интернету.";
  });
}
$("btnLogin").onclick = tryLogin;
$("inpPass").addEventListener("keydown", function(e){ if (e.key === "Enter") tryLogin(); });
$("inpUser").addEventListener("keydown", function(e){ if (e.key === "Enter") $("inpPass").focus(); });

/* ---------- просмотр ---------- */
function openViewer(){
  loginEl.classList.add("hidden"); limitEl.classList.add("hidden");
  appEl.classList.remove("hidden"); wmEl.classList.remove("hidden");
  $("chipUser").textContent = isOwner ? "владелец · без лимита" : "пользователь: " + curUser;
  if (isOwner){ $("chipLeft").textContent = "просмотры: без лимита"; }
  else { $("chipLeft").textContent = "осталось просмотров: " + leftNow; }
  buildWM();
  show(0);
}
function showLimit(){
  loginEl.classList.add("hidden"); appEl.classList.add("hidden");
  wmEl.classList.add("hidden");
  limitEl.classList.remove("hidden");
}
function show(i){
  cur = Math.max(0, Math.min(PAGES.length - 1, i));
  $("pageImg").src = PAGES[cur];
  $("pglbl").textContent = "стр. " + (cur+1) + " / " + PAGES.length;
  if (cur+1 < PAGES.length){ var im = new Image(); im.src = PAGES[cur+1]; }
}
$("bPrev").onclick = function(){ show(cur-1); };
$("bNext").onclick = function(){ show(cur+1); };
document.addEventListener("keydown", function(e){
  if (appEl.classList.contains("hidden")) return;
  if (e.key === "ArrowLeft" || e.key === "PageUp") show(cur-1);
  if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") show(cur+1);
  if (e.key === "Home") show(0);
  if (e.key === "End") show(PAGES.length-1);
});
/* свайпы на телефоне */
var tx = null;
$("stage").addEventListener("touchstart", function(e){ tx = e.touches[0].clientX; }, {passive:true});
$("stage").addEventListener("touchend", function(e){
  if (tx === null) return;
  var dx = e.changedTouches[0].clientX - tx; tx = null;
  if (dx < -40) show(cur+1); else if (dx > 40) show(cur-1);
}, {passive:true});

/* ---------- водяной знак ---------- */
function buildWM(){
  var now = new Date();
  var txt = curUser + " · " + now.toLocaleDateString("ru-RU") + " " +
            now.toLocaleTimeString("ru-RU").slice(0,5);
  var html = "", x, y, n = 0;
  for (y = 6; y < 100; y += 16){
    for (x = -10; x < 100; x += 34){
      html += '<span style="left:' + (x + (n%2)*9) + '%;top:' + y + '%">' + txt + '</span>';
      n++;
    }
  }
  wmEl.innerHTML = html;
}

/* ================= ЗАЩИТА ================= */
/* копирование / выделение / контекстное меню / перетаскивание */
["copy","cut","selectstart","dragstart","contextmenu"].forEach(function(ev){
  document.addEventListener(ev, function(e){ e.preventDefault(); });
});
/* клавиши: печать, сохранение, копирование, исходники, devtools, скриншот */
document.addEventListener("keydown", function(e){
  var k = e.key, c = e.ctrlKey || e.metaKey;
  if (c && ["p","s","c","x","a","u"].indexOf(k.toLowerCase()) >= 0){ e.preventDefault(); flash(); }
  if (k === "F12" || (c && e.shiftKey && ["i","j","c","k"].indexOf(k.toLowerCase()) >= 0)){
    e.preventDefault(); flash();
  }
  if (k === "PrintScreen"){
    e.preventDefault(); flash();
    try { navigator.clipboard && navigator.clipboard.writeText(" "); } catch(err){}
  }
});
var flashT = null;
function flash(){
  coverEl.classList.remove("hidden");
  clearTimeout(flashT);
  flashT = setTimeout(function(){
    if (document.hasFocus()) coverEl.classList.add("hidden");
  }, 900);
}
/* печать: экран-заглушка + отмена */
window.addEventListener("beforeprint", function(e){ if (e && e.preventDefault) e.preventDefault(); });
/* скриншоты: при потере фокуса контент скрывается */
window.addEventListener("blur", function(){ if (!appEl.classList.contains("hidden")) coverEl.classList.remove("hidden"); });
window.addEventListener("focus", function(){ coverEl.classList.add("hidden"); });
document.addEventListener("visibilitychange", function(){
  if (document.hidden && !appEl.classList.contains("hidden")) coverEl.classList.remove("hidden");
});
</script>
</body>
</html>
"""

html = TEMPLATE.replace("__PAGES_JSON__", json.dumps(pages))
import os
os.makedirs("/home/user/arena_web", exist_ok=True)
open("/home/user/arena_web/index.html", "w", encoding="utf-8").write(html)
open(OUT, "w", encoding="utf-8").write(html)
print("OK:", OUT, len(html) // 1024, "KB | pages:", len(pages))
