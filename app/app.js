/* Инструкция AI Arena · защищённый просмотр.
   Страницы приходят с сервера только после проверки пароля и учёта просмотра:
   сервер отдаёт ключ контента, завёрнутый в ключ, выведенный из пароля
   пользователя (PBKDF2-SHA256, 600000 итераций), и клиент расшифровывает
   content/content.bin (AES-256-GCM) прямо в браузере. */
"use strict";

(function () {
  var CFG = window.ARENA_CONFIG || {};
  var AAD_CK = "arena-ck-v1";
  var AAD_BUNDLE = "arena-bundle-v1";
  var MAGIC = "ARENAPG1";

  var $ = function (id) { return document.getElementById(id); };
  var loginEl = $("login"), appEl = $("app"), limitEl = $("limit"),
      wmEl = $("wm"), coverEl = $("cover");

  var curUser = "", curLeft = 0, curMax = 0, isOwner = false;
  var pages = [], cur = 0;

  /* ---------------- кодировки и WebCrypto ---------------- */
  function b64d(s) {
    var bin = atob(s), out = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
    return out;
  }
  function hasCrypto() {
    return !!(window.crypto && window.crypto.subtle && window.isSecureContext);
  }
  function pbkdf2(password, salt, iter) {
    var enc = new TextEncoder();
    return crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveBits"])
      .then(function (key) {
        return crypto.subtle.deriveBits(
          { name: "PBKDF2", hash: "SHA-256", salt: salt, iterations: iter }, key, 256);
      }).then(function (bits) { return new Uint8Array(bits); });
  }
  function unwrapCK(password, saltK, wrappedB64, iter) {
    var blob = b64d(wrappedB64);
    return pbkdf2(password, b64d(saltK), iter)
      .then(function (kek) {
        return crypto.subtle.importKey("raw", kek, "AES-GCM", false, ["decrypt"]);
      })
      .then(function (key) {
        return crypto.subtle.decrypt(
          { name: "AES-GCM", iv: blob.slice(0, 12), additionalData: new TextEncoder().encode(AAD_CK) },
          key, blob.slice(12));
      })
      .then(function (raw) {
        return crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
      });
  }
  function getBundle() {
    if (window.ARENA_BUNDLE_B64) return Promise.resolve(b64d(window.ARENA_BUNDLE_B64));
    return fetch(CFG.bundle || "content/content.bin").then(function (r) {
      if (!r.ok) throw new Error("bundle " + r.status);
      return r.arrayBuffer();
    }).then(function (b) { return new Uint8Array(b); });
  }
  function decryptBundle(ck, data) {
    var ct = data.slice(12);
    return crypto.subtle.decrypt(
      { name: "AES-GCM", iv: data.slice(0, 12), additionalData: new TextEncoder().encode(AAD_BUNDLE) },
      ck, ct).then(function (pt) {
      var buf = new Uint8Array(pt);
      var head = String.fromCharCode.apply(null, buf.slice(0, 8));
      if (head !== MAGIC) throw new Error("формат контента не распознан");
      var view = new DataView(buf.buffer, buf.byteOffset);
      var n = view.getUint32(8);
      var sizes = [], off = 12 + 4 * n, i;
      for (i = 0; i < n; i++) sizes.push(view.getUint32(12 + 4 * i));
      var out = [];
      for (i = 0; i < n; i++) {
        out.push(URL.createObjectURL(new Blob([buf.slice(off, off + sizes[i])], { type: "image/jpeg" })));
        off += sizes[i];
      }
      return out;
    });
  }

  /* ---------------- вход ---------------- */
  function setErr(text, wait) {
    var el = $("loginErr");
    el.textContent = text || "";
    el.className = wait ? "wait" : "";
  }
  function setBusy(busy) {
    $("btnLogin").disabled = busy;
    $("btnLogin").textContent = busy ? "Проверка…" : "Открыть инструкцию";
  }
  function apiUrl(path) { return (CFG.api || "") + path; }

  function tryLogin() {
    var u = $("inpUser").value.trim(), p = $("inpPass").value;
    if (!u || !p) { setErr("Введите логин и пароль."); return; }
    if (!hasCrypto()) {
      setErr("Браузер запретил шифрование для этого способа открытия (файл с телефона " +
             "или адрес без HTTPS). " +
             (CFG.link ? "Откройте инструкцию по ссылке: " + CFG.link
                       : "Откройте инструкцию по HTTPS-ссылке в современном браузере."));
      return;
    }
    setBusy(true);
    setErr("Проверка доступа на сервере защиты…", true);

    fetch(apiUrl("/api/check"), {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: u, pass: p, v: 1 })
    }).then(function (r) {
      return r.json().then(function (j) { return { status: r.status, body: j }; },
                          function () { return { status: r.status, body: null }; });
    }).then(function (res) {
      var j = res.body || {};
      if (res.status === 404 || res.status === 405 || res.status === 501) {
        throw new Error("NOSERVER");
      }
      if (j.wait) { setBusy(false); setErr("Слишком много неверных попыток. Повторите через " +
        Math.ceil((j.wait || 60000) / 60000) + " мин."); return; }
      if (j.limit) { setBusy(false); showLimit(); return; }
      if (!j.ok) { setBusy(false); setErr("Неверный логин или пароль."); return; }

      curUser = u; isOwner = !!j.unlimited;
      curMax = j.max == null ? 0 : j.max;
      curLeft = j.left == null ? 0 : j.left;
      setErr("Доступ разрешён. Расшифровка страниц…", true);

      var ckP = unwrapCK(p, j.salt_k, j.wrapped_ck, j.iter);
      var bufP = getBundle();
      return Promise.all([ckP, bufP]).then(function (both) {
        return decryptBundle(both[0], both[1]);
      }).then(function (list) {
        pages = list;
        $("inpPass").value = "";
        setBusy(false); setErr("");
        openViewer();
      });
    }).catch(function (e) {
      setBusy(false);
      if (e && e.message === "NOSERVER") {
        setErr("Сервер защиты не подключён. Укажите его адрес в файле app/config.js " +
               "(инструкция: docs/ЗАЩИТА.md).");
      } else if (e && String(e.message || "").indexOf("bundle") === 0) {
        setErr("Не удалось загрузить зашифрованные страницы (content/content.bin).");
      } else {
        setErr("Пароль верный, но расшифровка не удалась. Сообщите разработчику. " +
               "Если ошибка повторяется — проверьте, что страница обновлена (Ctrl+F5).");
      }
    });
  }
  $("btnLogin").onclick = tryLogin;
  $("inpPass").addEventListener("keydown", function (e) { if (e.key === "Enter") tryLogin(); });
  $("inpUser").addEventListener("keydown", function (e) { if (e.key === "Enter") $("inpPass").focus(); });

  /* ---------------- просмотр ---------------- */
  function openViewer() {
    loginEl.classList.add("hidden"); limitEl.classList.add("hidden");
    appEl.classList.remove("hidden"); wmEl.classList.remove("hidden");
    $("chipUser").textContent = isOwner ? "владелец · без лимита" : "пользователь: " + curUser;
    if (isOwner) { $("chipLeft").textContent = "просмотры: без лимита"; }
    else { $("chipLeft").textContent = "осталось просмотров: " + curLeft; }
    buildWM();
    show(0);
  }
  function showLimit() {
    loginEl.classList.add("hidden"); appEl.classList.add("hidden");
    wmEl.classList.add("hidden");
    limitEl.classList.remove("hidden");
  }
  function show(i) {
    if (!pages.length) return;
    cur = Math.max(0, Math.min(pages.length - 1, i));
    $("pageImg").src = pages[cur];
    $("pglbl").textContent = "стр. " + (cur + 1) + " / " + pages.length;
  }
  $("bPrev").onclick = function () { show(cur - 1); };
  $("bNext").onclick = function () { show(cur + 1); };
  document.addEventListener("keydown", function (e) {
    if (appEl.classList.contains("hidden")) return;
    if (e.key === "ArrowLeft" || e.key === "PageUp") show(cur - 1);
    if (e.key === "ArrowRight" || e.key === "PageDown" || e.key === " ") show(cur + 1);
    if (e.key === "Home") show(0);
    if (e.key === "End") show(pages.length - 1);
  });
  var tx = null;
  $("stage").addEventListener("touchstart", function (e) { tx = e.touches[0].clientX; }, { passive: true });
  $("stage").addEventListener("touchend", function (e) {
    if (tx === null) return;
    var dx = e.changedTouches[0].clientX - tx; tx = null;
    if (dx < -40) show(cur + 1); else if (dx > 40) show(cur - 1);
  }, { passive: true });

  /* ---------------- водяной знак ---------------- */
  function buildWM() {
    var now = new Date();
    var txt = curUser + " · " + now.toLocaleDateString("ru-RU") + " " +
              now.toLocaleTimeString("ru-RU").slice(0, 5);
    var html = "", x, y, n = 0;
    for (y = 6; y < 100; y += 16) {
      for (x = -10; x < 100; x += 34) {
        html += '<span style="left:' + (x + (n % 2) * 9) + '%;top:' + y + '%">' + txt + '</span>';
        n++;
      }
    }
    wmEl.innerHTML = html;
  }

  /* ---------------- защита ---------------- */
  ["copy", "cut", "selectstart", "dragstart", "contextmenu"].forEach(function (ev) {
    document.addEventListener(ev, function (e) { e.preventDefault(); });
  });
  document.addEventListener("keydown", function (e) {
    var k = e.key, c = e.ctrlKey || e.metaKey;
    if (c && ["p", "s", "c", "x", "a", "u"].indexOf(k.toLowerCase()) >= 0) { e.preventDefault(); flash(); }
    if (k === "F12" || (c && e.shiftKey && ["i", "j", "c", "k"].indexOf(k.toLowerCase()) >= 0)) {
      e.preventDefault(); flash();
    }
    if (k === "PrintScreen") {
      e.preventDefault(); flash();
      try { navigator.clipboard && navigator.clipboard.writeText(" "); } catch (err) { }
    }
  });
  var flashT = null;
  function flash() {
    if (appEl.classList.contains("hidden")) return;
    coverEl.classList.remove("hidden");
    clearTimeout(flashT);
    flashT = setTimeout(function () {
      if (document.hasFocus()) coverEl.classList.add("hidden");
    }, 900);
  }
  window.addEventListener("beforeprint", function (e) { if (e && e.preventDefault) e.preventDefault(); });
  window.addEventListener("blur", function () {
    if (!appEl.classList.contains("hidden")) coverEl.classList.remove("hidden");
  });
  window.addEventListener("focus", function () { coverEl.classList.add("hidden"); });
  document.addEventListener("visibilitychange", function () {
    if (document.hidden && !appEl.classList.contains("hidden")) coverEl.classList.remove("hidden");
  });

  /* ---------------- подсказка про сервер ---------------- */
  (function () {
    var host = CFG.api ? CFG.api.replace(/^https?:\/\//, "") : location.host;
    $("srvInfo").textContent = "сервер защиты: " + host;
  })();
})();
