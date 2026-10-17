(function () {
  "use strict";
  var D = window.D || {}, page = document.body.dataset.page;
  var ROT = ["-2.4deg", "1.8deg", "-1.2deg", "2.6deg", "-1.8deg", "1deg"];
  var OY = ["yanvar", "fevral", "mart", "aprel", "may", "iyun", "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"];
  var WD = ["Ya", "Du", "Se", "Ch", "Pa", "Ju", "Sh"], WDL = ["yakshanba", "dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba"];
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var pin = '<svg class="pin" aria-hidden="true"><use href="#pinS"/></svg>';
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  function go(href, el, cls) {
    if (reduce || !el) { location.href = href; return; }
    el.classList.add(cls || "tear"); setTimeout(function () { location.href = href; }, 520);
  }

  /* ================= HOME: cover parallax ================= */
  (function () {
    var img = document.querySelector(".cv-img img"); if (!img || reduce) return;
    var cover = img.closest(".hero-cv"), tick = false;
    addEventListener("scroll", function () {
      if (tick) return; tick = true;
      requestAnimationFrame(function () { var y = scrollY, h = cover.offsetHeight; if (y < h) img.style.setProperty("--py", (y * 0.28).toFixed(1) + "px"); tick = false; });
    }, { passive: true });
  })();
  /* ================= HOME: folders ================= */
  if (page === "home") {
    var stack = document.getElementById("stack"), P = D.projects || [], els = [], order = P.map(function (_, i) { return i; });
    var PAPERS = [["#DCE3E3", "#CFD8D8"], ["#E2E8E8", "#D6DEDE"], ["#E8EDED", "#DDE4E4"], ["#EEF2F2", "#E4EAEA"], ["#F3F6F4", "#EAEFEF"], ["#FAFBF9", "#F1F4F2"]];
    P.forEach(function (p, i) {
      var f = document.createElement("div"); f.className = "folder " + (i % 2 ? "R" : "L");
      var href = D.r + "loyiha/" + p.slug + ".html";
      f.innerHTML = '<div class="shape"><div class="sheet-peek">' + p.c + ' ta hujjat</div><div class="f-body"></div><button type="button" class="f-tab" aria-label="' + esc(p.n) + ' papkasi, ' + p.c + ' ta muammo hal qilindi"><span class="f-name"><span class="fn-l">' + esc(p.n.length <= 18 ? p.n : p.q) + '</span><span class="fn-s">' + esc(p.q) + '</span></span><span class="badge">' + p.c + "</span></button></div>" +
        '<svg class="clip" aria-hidden="true"><use href="#clipS"/></svg>' +
        '<div class="f-content"><div><div class="f-meta"><span class="live">' + (p.holat === "faol" ? "Faol" : "Yakunlangan") + "</span><span>" + esc(p.s) + "</span><span>· " + esc(p.x) + '</span></div><p class="f-desc">' + esc(p.t) + '</p><a class="f-btn" href="' + href + '">Papkani ochish <span aria-hidden="true">→</span></a></div>' +
        (p.last ? '<div class="f-last"><small>oxirgi yechim</small><b>' + esc(p.last.t) + '</b><div class="sk">' + p.last.sk + "</div></div>" : '<div class="f-last"><small>hali hujjat yo\'q</small></div>') + "</div>";
      f.querySelector(".f-tab").addEventListener("click", function () { pick(i); });
      f.querySelector(".f-body").addEventListener("click", function () { pick(i); });
      f.querySelector(".f-btn").addEventListener("click", function (e) { e.preventDefault(); openInside(p.slug); });
      f.addEventListener("mouseenter", function () { f.classList.add("peek"); });
      f.addEventListener("mouseleave", function () { f.classList.remove("peek"); });
      f.querySelector(".f-tab").addEventListener("focus", function () { f.classList.add("peek"); });
      f.querySelector(".f-tab").addEventListener("blur", function () { f.classList.remove("peek"); });
      stack.appendChild(f); els.push(f);
    });
    var lay = function () {
      var cs = getComputedStyle(stack), step = parseFloat(cs.getPropertyValue("--step")), fh = parseFloat(cs.getPropertyValue("--fh"));
      if (!order.length) { stack.style.height = "auto"; return; }
      stack.style.height = ((order.length - 1) * step + fh + 60) + "px";
      order.forEach(function (idx, pos) {
        var e = els[idx], pp = PAPERS[Math.max(0, PAPERS.length - order.length + pos)];
        e.style.top = (pos * step + 56) + "px"; e.style.zIndex = pos + 1;
        e.style.setProperty("--pp", pp[0]); e.style.setProperty("--pp2", pp[1]);
        e.classList.toggle("front", pos === order.length - 1);
      });
    };
    var busy = false;
    var pick = function (i) {
      if (busy || order[order.length - 1] === i) return; busy = true;
      var e = els[i]; e.classList.add("lift"); e.style.zIndex = 60;
      setTimeout(function () {
        order.splice(order.indexOf(i), 1); order.push(i); lay(); e.style.zIndex = 60;
        setTimeout(function () { e.classList.remove("lift"); lay(); busy = false; }, 460);
      }, reduce ? 0 : 240);
    };
    lay(); addEventListener("resize", lay);

    // touch: press-and-hold, slide to flip through folders
    (function () {
      var tip = document.createElement("div"); tip.className = "scrub-tip"; tip.textContent = "barmoqni yuring, qo'yib yuboring"; stack.appendChild(tip);
      var timer = null, on = false, sx = 0, sy = 0, cur = null;
      var at = function (x, y) { var el = document.elementFromPoint(x, y); return el && el.closest ? el.closest(".folder") : null; };
      var peek = function (f) { if (f === cur) return; if (cur) cur.classList.remove("peek"); cur = f; if (f) { try { navigator.vibrate && navigator.vibrate(8); } catch (e) {} f.classList.add("peek"); } };
      stack.addEventListener("touchstart", function (e) {
        if (busy || e.touches.length > 1 || e.target.closest(".f-content a")) return;
        var t = e.touches[0]; sx = t.clientX; sy = t.clientY;
        timer = setTimeout(function () { on = true; stack.classList.add("scrub"); peek(at(sx, sy)); }, 260);
      }, { passive: true });
      stack.addEventListener("touchmove", function (e) {
        var t = e.touches[0];
        if (!on) { if (Math.abs(t.clientY - sy) > 10 || Math.abs(t.clientX - sx) > 10) clearTimeout(timer); return; }
        e.preventDefault(); peek(at(t.clientX, t.clientY));
      }, { passive: false });
      stack.addEventListener("touchend", function (e) {
        clearTimeout(timer); if (!on) return; on = false; stack.classList.remove("scrub");
        var f = cur; peek(null); if (e.cancelable) e.preventDefault();
        if (f) { var i = els.indexOf(f); if (i > -1) pick(i); }
      }, { passive: false });
      stack.addEventListener("touchcancel", function () { clearTimeout(timer); on = false; stack.classList.remove("scrub"); peek(null); });
    })();

    if (!P.length) { stack.innerHTML = '<p class="stack-empty">Birinchi papka tez orada shu yerda ochiladi.</p>'; var dn = document.querySelector(".desk-note"); if (dn) dn.hidden = true; }

    /* ================= HOME: calendar ================= */
    var posts = D.posts || [], byDay = {}, months = [];
    posts.forEach(function (p) { (byDay[p.d] = byDay[p.d] || []).push(p); var m = p.d.slice(0, 7); if (months.indexOf(m) < 0) months.push(m); });
    months.sort();
    if (!months.length) { var td = new Date(); months.push(td.getFullYear() + "-" + ("0" + (td.getMonth() + 1)).slice(-2)); }
    var mi = months.length - 1;
    var grid = document.getElementById("grid"), tray = document.getElementById("tray"), strip = document.getElementById("strip"), pages = document.getElementById("pages");
    var pad = function (n) { return (n < 10 ? "0" : "") + n; };
    var card = function (p, i, open) {
      var a = document.createElement("a"); a.className = "card"; a.href = D.r + "post/" + p.id + ".html"; a.style.setProperty("--r", ROT[i % 6]);
      a.innerHTML = pin + '<span class="sway"><span class="paper"><span class="chip">' + esc(p.pn) + '</span><span class="sk">' + p.sk + "</span><h4>" + esc(p.t) + (p.demo ? '<span class="demo">namuna</span>' : "") + "</h4><p>" + esc(p.m) + "</p></span></span>";
      a.addEventListener("click", function (e) { e.preventDefault(); if (!open) { go(a.href, a); return; } a.classList.add("tear"); setTimeout(function () { open(p, a); }, reduce ? 0 : 520); });
      return a;
    };
    var renderMonth = function () {
      if (!months.length) { grid.innerHTML = ""; tray.innerHTML = '<p class="hint">Birinchi pin shu oyda qadaladi.</p>'; return; }
      var ym = months[mi], y = +ym.slice(0, 4), m = +ym.slice(5), title = OY[m - 1][0].toUpperCase() + OY[m - 1].slice(1) + ", " + y;
      document.getElementById("moT").textContent = title; document.getElementById("moT2").textContent = title;
      [["moP", -1], ["moN", 1], ["moP2", -1], ["moN2", 1]].forEach(function (b) { var el = document.getElementById(b[0]); el.disabled = !months[mi + b[1]]; el.style.opacity = months[mi + b[1]] ? 1 : .35; });
      var n = 0, dcount = 0; posts.forEach(function (p) { if (p.d.slice(0, 7) === ym) n++; });
      Object.keys(byDay).forEach(function (k) { if (k.slice(0, 7) === ym) dcount++; });
      document.getElementById("total").textContent = n + " ta yechim · " + dcount + " kun";
      var first = new Date(y, m - 1, 1).getDay(), lead = (first + 6) % 7, dim = new Date(y, m, 0).getDate(), prevDim = new Date(y, m - 1, 0).getDate();
      var cells = Math.ceil((lead + dim) / 7) * 7, html = "", now = new Date(), today = now.getFullYear() === y && now.getMonth() === m - 1 ? now.getDate() : -1;
      grid.innerHTML = "";
      for (var c = 0; c < cells; c++) {
        var d = c - lead + 1, inM = d >= 1 && d <= dim, lbl = inM ? d : (d < 1 ? prevDim + d : d - dim);
        var cell = document.createElement("div"); cell.className = "cell" + (inM ? "" : " out") + (d === today ? " today" : "");
        cell.innerHTML = (d === today ? '<svg class="ring" viewBox="0 0 58 44" aria-hidden="true"><path d="M40 6 C24 0, 4 6, 5 22 C6 38, 34 42, 50 32 C60 24, 52 6, 30 5" fill="none" stroke="#17211F" stroke-width="1.6" stroke-linecap="round"/></svg>' : "") + '<span class="n">' + lbl + "</span>";
        var L = inM && byDay[ym + "-" + pad(d)];
        if (L) {
          var b = document.createElement("button"); b.type = "button"; b.className = "note"; b.style.setProperty("--r", ROT[d % 6]);
          b.setAttribute("aria-label", d + "-" + OY[m - 1] + ": " + L.length + " ta yechim");
          b.innerHTML = pin + '<span class="sway">' + (L.length > 1 ? '<span class="under u1"></span>' + (L.length > 2 ? '<span class="under u2"></span>' : "") + '<span class="badge">' + L.length + "</span>" : "") + '<span class="paper"><span>' + esc(L[0].t) + "</span></span></span>";
          (function (dd, ce) { b.addEventListener("click", function () { openDay(ym, dd, ce); }); })(d, cell);
          cell.appendChild(b);
        }
        grid.appendChild(cell);
      }
      tray.innerHTML = '<p class="hint">pinlangan kunni bosing ↑</p>';
      // mobile pages
      strip.innerHTML = ""; pages.innerHTML = "";
      var days = [], sb = {}, lastDay = 0;
      Object.keys(byDay).forEach(function (k) { if (k.slice(0, 7) === ym) lastDay = Math.max(lastDay, +k.slice(8)); });
      for (var dd = 1; dd <= lastDay; dd++) {
        var key = ym + "-" + pad(dd), wd = new Date(y, m - 1, dd).getDay(), s = document.createElement("button"); s.type = "button";
        s.className = "sd" + (byDay[key] ? " has" : ""); s.innerHTML = WD[wd] + "<b>" + dd + "</b>";
        if (byDay[key]) { days.push(dd); (function (x) { s.addEventListener("click", function () { pages.scrollTo({ left: days.indexOf(x) * pages.clientWidth, behavior: "smooth" }); }); })(dd); }
        else { s.disabled = true; s.setAttribute("aria-label", dd + "-" + OY[m - 1] + ", yozuv yo'q"); }
        sb[dd] = s; strip.appendChild(s);
      }
      days.forEach(function (dd) {
        var L = byDay[ym + "-" + pad(dd)], wd = new Date(y, m - 1, dd).getDay(), pg = document.createElement("section"); pg.className = "pg";
        pg.innerHTML = '<div class="dh"><b>' + dd + "</b><span>" + WDL[wd] + "<br>" + L.length + " ta yechim</span></div>";
        L.forEach(function (p, i) { pg.appendChild(card(p, dd + i, function (pp, el) { pages.hidden = true; strip.hidden = true; showPost(mhost, pp, "kunlarga qaytish", function () { mhost.innerHTML = ""; pages.hidden = false; strip.hidden = false; el.classList.remove("tear"); }); })); });
        pages.appendChild(pg);
      });
      var mark = function () { var d = days[Math.round(pages.scrollLeft / Math.max(1, pages.clientWidth))]; Object.keys(sb).forEach(function (k) { sb[k].classList.toggle("on", +k === d); }); if (sb[d]) strip.scrollTo({ left: sb[d].offsetLeft - strip.clientWidth / 2 + sb[d].offsetWidth / 2, behavior: "smooth" }); };
      pages.onscroll = function () { clearTimeout(pages._t); pages._t = setTimeout(mark, 90); };
      requestAnimationFrame(function () { pages.scrollLeft = pages.scrollWidth; mark(); });
    };
    var sel = null;
    /* ---- post sheet in place ---- */
    var showPost = function (host, p, backLabel, back) {
      var dd = +p.d.slice(8), mm = +p.d.slice(5, 7);
      host.innerHTML = '<article class="post"><div class="sheet"><button type="button" class="back">← ' + esc(backLabel) + '</button><div class="f-meta"><span>' + dd + "-" + OY[mm - 1] + ", " + p.d.slice(0, 4) + "</span><span>· " + esc(p.pn) + "</span><span>· " + esc(p.g) + "</span>" + (p.demo ? '<span class="demo">namuna</span>' : "") + "</div><h3>" + esc(p.t) + '</h3><div class="sk">' + p.sk + '</div><div class="blocks"><div><b>' + esc((p.labels || [])[0] || "Muammo") + '</b><p>' + esc(p.m) + "</p></div><div><b>" + esc((p.labels || [])[1] || "Yechim") + "</b><p>" + esc(p.y) + "</p></div><div><b>" + esc((p.labels || [])[2] || "Natija") + "</b><p>" + esc(p.n) + '</p></div></div><div class="tags">' + p.tags.map(function (t) { return "<span>#" + esc(t) + "</span>"; }).join("") + (D.single ? "" : '<a href="post/' + p.id + '.html">havola ↗</a>') + "</div></div></article>";
      host.querySelector(".back").onclick = back;
      host.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" });
    };
    /* ---- folder interior in place ---- */
    var openInside = function (slug) {
      var p = P.filter(function (x) { return x.slug === slug; })[0]; if (!p) return;
      var docs = (D.posts || []).filter(function (x) { return x.ps === slug; });
      var types = {}; docs.forEach(function (d) { types[d.g] = (types[d.g] || 0) + 1; });
      var mx = Math.max.apply(null, [1].concat(Object.keys(types).map(function (k) { return types[k]; })));
      var groups = [], n = 0;
      docs.forEach(function (d) { var k = d.d.slice(0, 7), g = groups.filter(function (x) { return x.k === k; })[0]; if (!g) { g = { k: k, items: [] }; groups.push(g); } g.items.push(d); });
      var flat = [];
      var docsHtml = groups.map(function (g) {
        var m = +g.k.slice(5);
        return '<div class="mon">' + OY[m - 1][0].toUpperCase() + OY[m - 1].slice(1) + " " + g.k.slice(0, 4) + '</div><div class="dlist">' + g.items.map(function (d) {
          var k = n++; flat.push(d);
          return '<button type="button" class="doc" data-k="' + k + '" style="--r:' + ROT[k % 6] + ";--i:" + k + '"><svg class="clip" aria-hidden="true"><use href="#clipS"/></svg><span class="stamp">' + (+d.d.slice(8)) + " " + OY[m - 1].slice(0, 3) + '</span><span class="chip">' + esc(d.g) + '</span><span class="sk">' + d.sk + "</span><h4>" + esc(d.t) + (d.demo ? '<span class="demo">namuna</span>' : "") + "</h4><p>" + esc(d.m) + '</p><span class="read">O\'qish →</span></button>';
        }).join("") + "</div>";
      }).join("") || '<p class="empty">Bu papkaga hali hujjat tushmagan.</p>';
      var last = docs[0];
      var of = document.getElementById("of"), sec = document.getElementById("inside");
      of.innerHTML = '<div class="of-tab">' + esc(p.n) + '<span class="badge">' + docs.length + '</span></div><div class="of-body"><aside class="info"><svg class="clip" aria-hidden="true"><use href="#clipS"/></svg><button type="button" class="close" id="cls">← Papkani yopish</button>' +
        '<div class="f-meta"><span class="live">' + (p.holat === "faol" ? "Faol" : "Yakunlangan") + "</span><span>" + esc(p.since) + "</span></div><h2>" + esc(p.n) + "</h2><p>" + esc(p.t) + '</p><div class="chips">' + p.xs.map(function (c) { return "<span>" + esc(c) + "</span>"; }).join("") + "</div>" +
        '<div class="bignum"><b>' + docs.length + "</b><span>ta muammo hal qilindi" + (last ? "<br>oxirgisi: " + (+last.d.slice(8)) + "-" + OY[+last.d.slice(5, 7) - 1] : "") + "</span></div>" +
        (docs.length ? '<div class="types"><h5>Qaysi muammolar</h5>' + Object.keys(types).sort(function (a, b) { return types[b] - types[a]; }).map(function (k) { return '<div class="trow"><span>' + esc(k) + '</span><i style="width:' + Math.round(types[k] / mx * 100) + '%"></i><em>' + types[k] + "</em></div>"; }).join("") + "</div>" : "") +
        '<a class="f-btn ask" href="https://t.me/' + esc(D.tg) + '" target="_blank" rel="noopener">Menda ham shunday muammo bor →</a></aside><div class="docs" id="docs">' + docsHtml + "</div></div>";
      var docsEl = document.getElementById("docs"), saved = docsEl.innerHTML;
      var bind = function () {
        docsEl.querySelectorAll(".doc").forEach(function (b) {
          b.addEventListener("click", function () {
            var d = flat[+b.dataset.k]; b.classList.add("tear");
            setTimeout(function () { showPost(docsEl, d, "Papkaga qaytish", function () { docsEl.innerHTML = saved; bind(); docsEl.scrollIntoView({ behavior: "smooth", block: "start" }); }); }, reduce ? 0 : 420);
          });
        });
      };
      bind();
      document.getElementById("cls").onclick = function () { sec.hidden = true; try { history.replaceState(null, "", location.pathname); } catch (e) {} document.getElementById("loyihalar").scrollIntoView({ behavior: "smooth" }); };
      sec.hidden = false; try { history.replaceState(null, "", "#loyiha-" + slug); } catch (e) {}
      sec.scrollIntoView({ behavior: reduce ? "auto" : "smooth" });
    };
    var openDay = function (ym, d, cell) {
      if (sel) sel.classList.remove("sel"); sel = cell; cell.classList.add("sel"); selKey = ym + "-" + pad(d);
      var L = byDay[ym + "-" + pad(d)], m = +ym.slice(5), wd = new Date(+ym.slice(0, 4), m - 1, d).getDay();
      tray.innerHTML = '<div class="tray-h"><b>' + d + "-" + OY[m - 1] + "<span>" + WDL[wd] + " · " + L.length + ' ta yechim</span></b><div class="arrows"><button type="button" aria-label="Oldingi kartochka">←</button><button type="button" aria-label="Keyingi kartochka">→</button></div></div><div class="rail"></div>';
      var rail = tray.querySelector(".rail"), ab = tray.querySelectorAll(".arrows button");
      L.forEach(function (p, i) { rail.appendChild(card(p, d + i, function (pp) { showPost(tray, pp, d + "-" + OY[m - 1] + "ga qaytish", function () { openDay(ym, d, cell); }); })); });
      ab[0].onclick = function () { rail.scrollBy({ left: -330, behavior: "smooth" }); };
      ab[1].onclick = function () { rail.scrollBy({ left: 330, behavior: "smooth" }); };
      tray.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest" });
    };
    /* ---- Kun / Hafta / Oy ---- */
    var view = "oy", selKey = null, allDays = Object.keys(byDay).sort(), anchor = allDays[allDays.length - 1] || null;
    var weekv = document.getElementById("weekv"), dayv = document.getElementById("dayv"), wkh = document.querySelector(".win .wk"), segBtns = [].slice.call(document.querySelectorAll(".seg button"));
    var toD = function (s) { return new Date(+s.slice(0, 4), +s.slice(5, 7) - 1, +s.slice(8)); };
    var toS = function (d) { return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); };
    var addD = function (s, n) { var d = toD(s); d.setDate(d.getDate() + n); return toS(d); };
    var monday = function (s) { var d = toD(s); d.setDate(d.getDate() - (d.getDay() + 6) % 7); return toS(d); };
    var todayS = toS(new Date());
    var setNav = function (p, n) { [["moP", p], ["moN", n]].forEach(function (b) { var el = document.getElementById(b[0]); el.disabled = !b[1]; el.style.opacity = b[1] ? 1 : .35; }); };
    var dname = function (s) { return (+s.slice(8)) + "-" + OY[+s.slice(5, 7) - 1]; };
    var renderWeek = function () {
      var mon = monday(anchor), end = addD(mon, 6), n = 0;
      weekv.innerHTML = "";
      for (var i = 0; i < 7; i++) {
        var ds = addD(mon, i), L = byDay[ds] || [], col = document.createElement("div");
        col.className = "wcol" + (ds === todayS ? " today" : "") + (L.length ? "" : ds > todayS ? " future" : " empty"); n += L.length;
        var h = document.createElement(L.length ? "button" : "div"); h.className = "wd";
        h.innerHTML = '<b>' + (+ds.slice(8)) + "</b>" + (L.length ? "<span>" + L.length + " ta</span>" : "");
        if (L.length) { h.type = "button"; h.setAttribute("aria-label", dname(ds) + ", kun ko'rinishida ochish"); (function (x) { h.onclick = function () { anchor = x; view = "kun"; render(); }; })(ds); }
        col.appendChild(h);
        L.forEach(function (p, j) { col.appendChild(card(p, i + j, function (pp) { showPost(tray, pp, "haftaga qaytish", function () { tray.innerHTML = ""; renderWeek(); document.querySelector(".win").scrollIntoView({ behavior: "smooth", block: "start" }); }); })); });
        if (!L.length && ds <= todayS) { var e = document.createElement("span"); e.className = "nil"; e.textContent = "—"; col.appendChild(e); }
        weekv.appendChild(col);
      }
      var sm = mon.slice(5, 7) === end.slice(5, 7);
      document.getElementById("moT").textContent = (sm ? (+mon.slice(8)) + "–" + dname(end) : dname(mon) + " – " + dname(end)) + ", " + end.slice(0, 4);
      document.getElementById("total").textContent = n + " ta yechim";
      setNav(mon > monday(allDays[0]), mon < monday(allDays[allDays.length - 1]));
    };
    var renderDay = function () {
      if (!byDay[anchor]) { var prev = allDays.filter(function (d) { return d <= anchor; }); anchor = prev.length ? prev[prev.length - 1] : allDays[0]; }
      var L = byDay[anchor], k = allDays.indexOf(anchor), wd = toD(anchor).getDay();
      dayv.innerHTML = '<div class="dayh"><b>' + (+anchor.slice(8)) + "</b><span>" + WDL[wd] + '</span></div><div class="dgrid"></div>';
      var g = dayv.querySelector(".dgrid");
      L.forEach(function (p, j) { g.appendChild(card(p, k + j, function (pp) { showPost(dayv, pp, dname(anchor) + "ga qaytish", function () { renderDay(); dayv.scrollIntoView({ behavior: "smooth", block: "start" }); }); })); });
      document.getElementById("moT").textContent = dname(anchor) + ", " + anchor.slice(0, 4);
      document.getElementById("total").textContent = L.length + " ta yechim";
      setNav(k > 0, k < allDays.length - 1);
    };
    var render = function () {
      segBtns.forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.v === view)); });
      grid.hidden = view !== "oy"; weekv.hidden = view !== "hafta"; dayv.hidden = view !== "kun"; wkh.hidden = view === "kun";
      if (view === "oy" || !anchor) { renderMonth(); return; }
      tray.innerHTML = "";
      if (view === "hafta") renderWeek(); else renderDay();
    };
    segBtns.forEach(function (b) {
      b.onclick = function () {
        if (b.dataset.v === view) return;
        if (view === "oy") { anchor = selKey || (allDays.filter(function (d) { return d.slice(0, 7) === months[mi]; }).pop() || anchor); }
        view = b.dataset.v;
        if (view === "oy" && anchor) { var j = months.indexOf(anchor.slice(0, 7)); if (j > -1) mi = j; }
        render();
      };
    });
    document.getElementById("moP").onclick = function () {
      if (view === "oy") { if (months[mi - 1]) { mi--; renderMonth(); } }
      else if (view === "hafta") { anchor = addD(monday(anchor), -7); renderWeek(); }
      else { var k = allDays.indexOf(anchor); if (k > 0) { anchor = allDays[k - 1]; renderDay(); } }
    };
    document.getElementById("moN").onclick = function () {
      if (view === "oy") { if (months[mi + 1]) { mi++; renderMonth(); } }
      else if (view === "hafta") { anchor = addD(monday(anchor), 7); renderWeek(); }
      else { var k = allDays.indexOf(anchor); if (k < allDays.length - 1) { anchor = allDays[k + 1]; renderDay(); } }
    };
    document.getElementById("moP2").onclick = function () { if (months[mi - 1]) { mi--; renderMonth(); if (view !== "oy") render(); } };
    document.getElementById("moN2").onclick = function () { if (months[mi + 1]) { mi++; renderMonth(); if (view !== "oy") render(); } };
    renderMonth();
    var hm = location.hash.match(/^#loyiha-(.+)$/); if (hm) openInside(hm[1]);
    /* ---- in-page search ---- */
    var qhost = document.getElementById("qhost"), qlist = document.getElementById("list");
    if (qhost) {
      var byId = {}; (D.posts || []).forEach(function (p) { byId[p.id] = p; });
      qlist.querySelectorAll("a.doc[data-kid]").forEach(function (a) { a.addEventListener("click", function (e) { e.preventDefault(); if (window.__openK) window.__openK(a.dataset.kid); }); });
      qlist.querySelectorAll("a.doc[data-id]").forEach(function (a) {
        a.addEventListener("click", function (e) {
          if (e.metaKey || e.ctrlKey) return; e.preventDefault();
          var p = byId[a.dataset.id]; if (!p) return; a.classList.add("tear");
          setTimeout(function () { qlist.hidden = true; showPost(qhost, p, "natijalarga qaytish", function () { qhost.innerHTML = ""; qlist.hidden = false; a.classList.remove("tear"); document.getElementById("qidiruv").scrollIntoView({ behavior: "smooth", block: "start" }); }); }, reduce ? 0 : 420);
        });
      });
    }
  }

  /* ================= PROJECT: tear a document out ================= */
  if (page === "project" || page === "search") {
    document.querySelectorAll("a.doc").forEach(function (a) {
      a.addEventListener("click", function (e) { if (e.metaKey || e.ctrlKey) return; e.preventDefault(); go(a.href, a, "tear"); });
    });
  }

  /* ================= SEARCH ================= */
  if ((page === "search" || page === "home") && document.getElementById("q")) {
    var q = document.getElementById("q"), items = [].slice.call(document.querySelectorAll("#list .doc")), none = document.getElementById("none"), tagBtns = [].slice.call(document.querySelectorAll("#tags button")), tag = "";
    var norm = function (s) { return s.toLowerCase().replace(/[ʻʼ'’`]/g, ""); };
    var qall = document.getElementById("qall"), showAll = false;
    var run = function () {
      var w = norm(q.value).split(/\s+/).filter(Boolean), shown = 0, idle = !w.length && !tag && !showAll && !!qall;
      items.forEach(function (el) { var h = norm(el.dataset.q), ok = !idle && w.every(function (x) { return h.indexOf(x) > -1; }) && (!tag || h.indexOf(norm(tag)) > -1); el.hidden = !ok; if (ok) shown++; });
      none.hidden = idle || shown > 0; if (qall) qall.hidden = !idle;
    };
    if (qall) { document.getElementById("qshow").onclick = function () { showAll = true; run(); }; run(); }
    q.addEventListener("input", run);
    tagBtns.forEach(function (b) { b.addEventListener("click", function () { var on = b.getAttribute("aria-pressed") !== "true"; tagBtns.forEach(function (x) { x.setAttribute("aria-pressed", "false"); }); b.setAttribute("aria-pressed", String(on)); tag = on ? b.dataset.w : ""; run(); }); });
    var h = location.hash.slice(1); if (h && page === "search") { var t = tagBtns.filter(function (b) { return b.dataset.t === h; })[0]; if (t) t.click(); }
    window.__setTag = function (w) {
      var qh = document.getElementById("qhost"), ql = document.getElementById("list"); if (qh) { qh.innerHTML = ""; ql.hidden = false; }
      q.value = ""; var found = false; tagBtns.forEach(function (x) { var on = x.dataset.w === w; if (on) found = true; x.setAttribute("aria-pressed", String(on)); }); tag = w; if (!found) { tag = ""; q.value = w; } run();
      document.getElementById("qidiruv").scrollIntoView({ behavior: "smooth", block: "start" });
    };
  }

  /* ================= KUNDALIK ================= */
  var kfeed = document.getElementById("kfeed");
  if (kfeed) {
    var K = D.kundalik || [], kf = document.getElementById("kfil"), kmore = document.getElementById("kmore"), kst = document.getElementById("kstats");
    var CATS = ["Hammasi", "Kitob", "O'rgandim", "Hayot"], CLS = { "Kitob": "t-kitob", "O'rgandim": "t-org", "Hayot": "t-hayot" };
    var kcat = "Hammasi", klimit = 5;
    var cnt = function (c) { return K.filter(function (k) { return c === "Hammasi" || k.c === c; }).length; };
    var WDL2 = ["yakshanba", "dushanba", "seshanba", "chorshanba", "payshanba", "juma", "shanba"];
    kst.innerHTML = [["Kitob", "ta kitob"], ["O'rgandim", "ta saboq"], ["Hayot", "ta o'zgarish"]].map(function (x) { return '<span class="' + CLS[x[0]] + '"><b>' + cnt(x[0]) + "</b> " + x[1] + "</span>"; }).join("");
    kf.innerHTML = CATS.map(function (c) { return '<button type="button" data-c="' + esc(c) + '" aria-pressed="' + (c === kcat) + '">' + esc(c) + " <i>" + cnt(c) + "</i></button>"; }).join("");
    var kpost = function (k) {
      var dt = new Date(+k.d.slice(0, 4), +k.d.slice(5, 7) - 1, +k.d.slice(8)), meta = [];
      if (k.h) meta.push(k.h + " m"); if (k.joy) meta.push(esc(k.joy));
      var ph = "";
      if (k.sb) ph = '<button type="button" class="kp-sb" data-kid="' + esc(k.id) + '" aria-label="Storyboardni kadrma-kadr ochish"><img src="' + esc(k.sb.c) + '" alt="' + esc(k.t) + ' — storyboard" loading="lazy"><span class="kp-sb-b">▶ ' + k.sb.f.length + ' kadr</span></button>';
      if (!ph && k.img.length) ph = '<div class="kp-ph n' + Math.min(3, k.img.length) + '">' + k.img.slice(0, 3).map(function (src, i) { return '<button type="button" class="kp-img" data-src="' + esc(src) + '" aria-label="Rasmni kattalashtirish"><img src="' + esc(src) + '" alt="' + esc(k.t) + " — " + (i + 1) + '-rasm" loading="lazy"></button>'; }).join("") + "</div>";
      var bk = k.book ? '<div class="kp-book"><span class="kp-cover" style="--c:' + esc(k.book.rang) + ";--t:" + esc(k.book.matn_rang) + '"><b>' + esc(k.book.nom) + "</b></span><span><b>" + esc(k.book.nom) + "</b><br>" + esc(k.book.muallif) + (k.book.holat ? ' <em class="' + (k.book.holat === "o'qilmoqda" ? "now" : "") + '">' + esc(k.book.holat) + "</em>" : "") + "</span></div>" : "";
      var long = k.p.join(" ").length > 260;
      return '<article class="kp" id="' + esc(k.id) + '"><div class="kp-date"><b>' + dt.getDate() + "</b><span>" + OY[dt.getMonth()].slice(0, 3) + "</span><i>" + WDL2[dt.getDay()] + '</i></div><div class="kp-sheet"><div class="kp-top"><span class="kchip ' + CLS[k.c] + '">' + esc(k.c) + "</span>" + (meta.length ? '<span class="kp-meta">' + meta.join(" · ") + "</span>" : "") + (k.demo ? '<span class="demo">namuna</span>' : "") + "</div><h3>" + esc(k.t) + "</h3>" + bk + ph +
        '<div class="kp-body' + (long ? " clamp" : "") + '">' + k.p.map(function (x) { return "<p>" + esc(x) + "</p>"; }).join("") + "</div>" + (long ? '<button type="button" class="kp-more" aria-expanded="false">Davomini o\'qish ↓</button>' : "") +
        (k.x ? '<p class="kp-x"><span aria-hidden="true">→</span> ' + esc(k.x) + "</p>" : "") + "</div></article>";
    };
    var renderK = function () {
      var list = K.filter(function (k) { return kcat === "Hammasi" || k.c === kcat; });
      kfeed.innerHTML = list.slice(0, klimit).map(kpost).join("") || '<p class="empty">Bu toifada hali yozuv yo\'q.</p>';
      kmore.hidden = list.length <= klimit; kmore.textContent = "Yana ko'rsatish (" + (list.length - klimit) + ")";
      [].forEach.call(kf.querySelectorAll("button"), function (b) { b.setAttribute("aria-pressed", String(b.dataset.c === kcat)); });
    };
    kf.addEventListener("click", function (e) { var b = e.target.closest("button"); if (!b) return; kcat = b.dataset.c; klimit = 5; renderK(); });
    kmore.addEventListener("click", function () { klimit += 5; renderK(); });
    kfeed.addEventListener("click", function (e) {
      var m = e.target.closest(".kp-more");
      if (m) { var body = m.previousElementSibling, open = m.getAttribute("aria-expanded") === "true";
        if (!open) { body.style.maxHeight = body.scrollHeight + "px"; body.classList.add("open"); m.textContent = "Yig'ish ↑"; }
        else { body.style.maxHeight = ""; body.classList.remove("open"); m.textContent = "Davomini o'qish ↓"; }
        m.setAttribute("aria-expanded", String(!open)); return; }
      var sbb = e.target.closest(".kp-sb"); if (sbb && window.__story) { var kk = K.filter(function (x) { return x.id === sbb.dataset.kid; })[0]; if (kk) window.__story([{ joy: kk.t, hud: "", dav: "", d: kk.d, x: "", img: kk.sb.f }], 0, sbb); return; }
      var im = e.target.closest(".kp-img"); if (im) lightbox(im.dataset.src);
    });
    var lightbox = function (src) {
      var o = document.createElement("div"); o.className = "lb"; o.setAttribute("role", "dialog"); o.setAttribute("aria-label", "Rasm");
      o.innerHTML = '<img src="' + esc(src) + '" alt=""><button type="button" aria-label="Yopish">×</button>';
      var close = function () { o.classList.remove("on"); setTimeout(function () { o.remove(); }, 250); removeEventListener("keydown", esc2); };
      var esc2 = function (e) { if (e.key === "Escape") close(); };
      o.addEventListener("click", close); addEventListener("keydown", esc2);
      document.body.appendChild(o); requestAnimationFrame(function () { o.classList.add("on"); }); o.querySelector("button").focus();
    };
    window.__kFilter = function (c) { kcat = c; klimit = 5; renderK(); };
    window.__openK = function (id) {
      kcat = "Hammasi"; var idx = K.map(function (k) { return k.id; }).indexOf(id); klimit = Math.max(5, idx + 1); renderK();
      var el = document.getElementById(id); if (!el) return;
      var m = el.querySelector(".kp-more"); if (m && m.getAttribute("aria-expanded") !== "true") m.click();
      el.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); el.classList.add("flash"); setTimeout(function () { el.classList.remove("flash"); }, 1600);
    };
    document.querySelectorAll("[data-kfilter]").forEach(function (a) { a.addEventListener("click", function () { window.__kFilter(a.dataset.kfilter); }); });
    renderK();
  }

  /* ================= SAYOHAT: photo stacks + story viewer ================= */
  var tgrid = document.getElementById("tgrid");
  {
    var T = D.sayohat || [], tmore = document.getElementById("tmore"), tlimit = innerWidth <= 700 ? 6 : 8;
    var TR = ["-3deg", "2deg", "-1.4deg", "3deg", "-2.2deg", "1.4deg"];
    var sdate = function (d, y) { return (+d.slice(8)) + "-" + OY[+d.slice(5, 7) - 1].slice(0, 3) + (y ? ", " + d.slice(0, 4) : ""); };
    var tcard = function (t, i) {
      var im = t.img;
      return '<button type="button" class="tp" data-i="' + i + '" style="--r:' + TR[i % 6] + ";--i:" + (i % 8) + '" aria-label="' + esc(t.joy) + ", " + im.length + ' ta rasm">' +
        (im[2] ? '<span class="tp-b b2"><img src="' + esc(im[2].s) + '" alt="" loading="lazy"></span>' : "") +
        (im[1] ? '<span class="tp-b b1"><img src="' + esc(im[1].s) + '" alt="" loading="lazy"></span>' : "") +
        '<span class="tp-f"><span class="tp-ph"><img src="' + esc(im[0].s) + '" alt="" loading="lazy"></span><span class="tp-cap"><b>' + esc(t.joy) + "</b><i>" + sdate(t.d, true) + "</i></span></span>" +
        (im.length > 1 ? '<span class="tp-n">' + im.length + "</span>" : "") + (t.demo ? '<span class="demo">namuna</span>' : "") + "</button>";
    };
    var renderT = function () {
      tgrid.innerHTML = T.slice(0, tlimit).map(tcard).join("");
      tmore.hidden = T.length <= tlimit; tmore.textContent = "Yana ko'rsatish (" + (T.length - tlimit) + ")";
    };
    if (tgrid) tmore.addEventListener("click", function () { tlimit += 8; renderT(); });
    if (tgrid) tgrid.addEventListener("click", function (e) { var b = e.target.closest(".tp"); if (b) openStory(+b.dataset.i, b); });

    var openStory = function (ti0, from, list) {
      var T = list || D.sayohat || [];
      var ti = -1, pi = 0, held = false, holdT = 0, sx = 0, sy = 0, down = false, pushed = false, closing = false;
      var o = document.createElement("div"); o.className = "st"; o.setAttribute("role", "dialog"); o.setAttribute("aria-modal", "true");
      o.innerHTML = '<div class="st-bg"></div><button type="button" class="st-tp" aria-label="Oldingi sayohat">‹</button>' +
        '<div class="st-fr"><div class="st-blur"></div><div class="st-img"></div><div class="st-bars"></div>' +
        '<div class="st-top"><span class="st-tt"><b></b><i></i></span><button type="button" class="st-x" aria-label="Yopish">×</button></div>' +
        '<p class="st-cap"></p><span class="st-ps" aria-hidden="true"><i></i><i></i></span></div>' +
        '<button type="button" class="st-nt" aria-label="Keyingi sayohat">›</button>';
      var fr = o.querySelector(".st-fr"), bars = o.querySelector(".st-bars"), box = o.querySelector(".st-img"), blur = o.querySelector(".st-blur"), bg = o.querySelector(".st-bg"), cap = o.querySelector(".st-cap");
      var setPause = function (v) { o.classList.toggle("paused", v); };
      var show = function (nti, npi, dir) {
        var t = T[nti];
        if (nti !== ti) {
          ti = nti; o.setAttribute("aria-label", t.joy);
          o.querySelector(".st-tt b").textContent = t.joy;
          o.querySelector(".st-tt i").textContent = [t.hud, t.dav && t.dav !== "O'zbekiston" ? t.dav : "", sdate(t.d, true)].filter(Boolean).join(" · ");
          bars.innerHTML = t.img.map(function () { return "<i><b></b></i>"; }).join("");
          bars.querySelectorAll("b").forEach(function (b) { b.addEventListener("animationend", function () { if (b.parentNode.classList.contains("on")) next(); }); });
          if (dir) { fr.classList.remove("in-l", "in-r"); void fr.offsetWidth; fr.classList.add(dir > 0 ? "in-r" : "in-l"); }
          o.querySelector(".st-tp").disabled = ti === 0; o.querySelector(".st-nt").disabled = ti === T.length - 1;
        }
        pi = npi;
        var ph = t.img[pi];
        [].forEach.call(bars.children, function (el, k) { el.classList.remove("on"); el.classList.toggle("done", k < pi); });
        var cur = bars.children[pi]; void cur.offsetWidth; cur.classList.add("on");
        var img = new Image(); img.src = ph.s; img.alt = t.joy + " — " + (pi + 1) + "-rasm"; img.className = "in";
        [].forEach.call(box.children, function (old) { old.classList.remove("in"); old.classList.add("out"); setTimeout(function () { old.remove(); }, 450); });
        box.appendChild(img);
        blur.style.backgroundImage = bg.style.backgroundImage = 'url("' + ph.s + '")';
        var c = ph.i || (pi === 0 ? t.x : ""); cap.textContent = c; cap.hidden = !c; cap.style.animation = "none"; void cap.offsetWidth; cap.style.animation = "";
        var nx = t.img[pi + 1] || (T[ti + 1] && T[ti + 1].img[0]); if (nx) new Image().src = nx.s;
      };
      var next = function () { if (pi < T[ti].img.length - 1) show(ti, pi + 1); else if (ti < T.length - 1) show(ti + 1, 0, 1); else close(); };
      var prev = function () { if (pi > 0) show(ti, pi - 1); else if (ti > 0) show(ti - 1, 0, -1); else show(ti, 0); };
      var nextT = function () { if (ti < T.length - 1) show(ti + 1, 0, 1); else close(); };
      var prevT = function () { if (ti > 0) show(ti - 1, 0, -1); };
      var close = function (fromPop) {
        if (closing) return; closing = true;
        o.classList.remove("on"); document.documentElement.classList.remove("st-lock");
        removeEventListener("keydown", key); removeEventListener("popstate", pop); document.removeEventListener("visibilitychange", vis);
        setTimeout(function () { o.remove(); }, 300);
        if (pushed && fromPop !== true) { try { history.back(); } catch (e) {} }
        if (from && from.focus) from.focus({ preventScroll: true });
      };
      var key = function (e) {
        if (e.key === "Escape") close(); else if (e.key === "ArrowRight") next(); else if (e.key === "ArrowLeft") prev();
        else if (e.key === " ") { e.preventDefault(); setPause(!o.classList.contains("paused")); }
      };
      var pop = function () { close(true); };
      var vis = function () { if (document.hidden) setPause(true); };
      fr.addEventListener("pointerdown", function (e) {
        if (e.target.closest("button")) return;
        down = true; held = false; sx = e.clientX; sy = e.clientY;
        clearTimeout(holdT); holdT = setTimeout(function () { held = true; setPause(true); }, 220);
      });
      var up = function (e) {
        if (!down) return; down = false; clearTimeout(holdT);
        var dx = e.clientX - sx, dy = e.clientY - sy;
        if (held) { held = false; setPause(false); return; }
        if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) { dx < 0 ? nextT() : prevT(); return; }
        if (dy > 90 && Math.abs(dy) > Math.abs(dx)) { close(); return; }
        if (Math.abs(dx) < 12 && Math.abs(dy) < 12) {
          setPause(false);
          var r = fr.getBoundingClientRect(); (e.clientX - r.left < r.width / 3) ? prev() : next();
        }
      };
      fr.addEventListener("pointerup", up);
      fr.addEventListener("pointercancel", function () { down = false; clearTimeout(holdT); if (held) { held = false; setPause(false); } });
      fr.addEventListener("contextmenu", function (e) { e.preventDefault(); });
      o.querySelector(".st-x").addEventListener("click", function () { close(); });
      o.querySelector(".st-tp").addEventListener("click", prevT);
      o.querySelector(".st-nt").addEventListener("click", nextT);
      o.addEventListener("click", function (e) { if (e.target === o || e.target === bg) close(); });
      addEventListener("keydown", key); document.addEventListener("visibilitychange", vis);
      try { history.pushState({ st: 1 }, ""); pushed = true; addEventListener("popstate", pop); } catch (e) {}
      document.body.appendChild(o); document.documentElement.classList.add("st-lock");
      show(ti0, 0);
      requestAnimationFrame(function () { o.classList.add("on"); });
      o.querySelector(".st-x").focus({ preventScroll: true });
    };
    window.__story = function (list, i, from) { openStory(i || 0, from, list); };
    if (tgrid) renderT();
  }

  /* ================= header: compact, hides on scroll down (phones) ================= */
  (function () {
    var top = document.querySelector(".top"); if (!top) return;
    var last = scrollY, tick = false;
    addEventListener("scroll", function () {
      if (tick) return; tick = true;
      requestAnimationFrame(function () { var y = scrollY; if (innerWidth <= 700) top.classList.toggle("hide", y > 160 && y > last); else top.classList.remove("hide"); last = y; tick = false; });
    }, { passive: true });
  })();

  /* ================= services → search tag ================= */
  (function () {
    var panel = document.getElementById("svcp"); if (!panel || typeof showPost !== "function") return;
    var cards = [].slice.call(document.querySelectorAll(".svc-c[data-tag]")), cur = null;
    var render = function (a) {
      var tag = a.dataset.tag, list = (D.posts || []).filter(function (p) { return p.tags.indexOf(tag) > -1; });
      panel.innerHTML = '<div class="svcp-h"><b>' + esc(a.dataset.nom) + "</b><span>" + list.length + ' ta ish</span><button type="button" class="svcp-x" aria-label="Yopish">×</button></div><div class="dlist" id="svcl"></div>';
      var box = panel.querySelector("#svcl");
      if (!list.length) box.innerHTML = '<p class="empty">Bu yo\'nalishda yozuvlar tez orada paydo bo\'ladi.</p>';
      list.forEach(function (p, i) {
        var b = document.createElement("button"); b.type = "button"; b.className = "doc"; b.style.cssText = "--r:" + ROT[i % 6] + ";--i:" + i;
        b.innerHTML = '<svg class="clip" aria-hidden="true"><use href="#clipS"/></svg><span class="stamp">' + (+p.d.slice(8)) + " " + OY[+p.d.slice(5, 7) - 1].slice(0, 3) + '</span><span class="chip">' + esc(p.pn) + '</span><span class="sk">' + p.sk + "</span><h4>" + esc(p.t) + (p.demo ? '<span class="demo">namuna</span>' : "") + "</h4><p>" + esc(p.m) + '</p><span class="read">O\'qish →</span>';
        b.addEventListener("click", function () { b.classList.add("tear"); setTimeout(function () { showPost(box, p, "ro'yxatga qaytish", function () { render(a); panel.scrollIntoView({ behavior: "smooth", block: "start" }); }); }, reduce ? 0 : 420); });
        box.appendChild(b);
      });
      panel.querySelector(".svcp-x").onclick = close;
    };
    var close = function () { panel.hidden = true; panel.innerHTML = ""; if (cur) cur.classList.remove("on"); cur = null; };
    cards.forEach(function (a) {
      a.addEventListener("click", function (e) {
        e.preventDefault();
        if (cur === a) { close(); return; }
        if (cur) cur.classList.remove("on"); cur = a; a.classList.add("on");
        render(a); panel.hidden = false; panel.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest" });
      });
    });
  })();
})();

/* ===== Telegram Mini App: faqat Telegram ichida ochilganda ishlaydi ===== */
(function () {
  if (!/tgWebApp/.test(location.hash + location.search) && !window.TelegramWebviewProxy) return;
  var s = document.createElement("script");
  s.src = "https://telegram.org/js/telegram-web-app.js";
  s.onload = function () {
    var tg = window.Telegram && window.Telegram.WebApp; if (!tg) return;
    document.documentElement.classList.add("tg");
    try { tg.ready(); tg.expand(); tg.setHeaderColor("#0A4E50"); tg.setBackgroundColor("#0A4E50"); } catch (e) {}
    // story ochiq bo'lsa Telegram'ning "orqaga" tugmasi uni yopadi
    var bb = tg.BackButton;
    new MutationObserver(function () { if (document.querySelector(".st")) bb.show(); else bb.hide(); }).observe(document.body, { childList: true });
    bb.onClick(function () { history.back(); });
  };
  document.head.appendChild(s);
})();

/* ===== post varag'idagi storyboard: bosilsa kadrlar story kabi ochiladi ===== */
document.addEventListener("click", function (e) {
  var im = e.target.closest && e.target.closest(".post .sk-img"); if (!im || !window.__story || !window.D) return;
  var p = (window.D.posts || []).filter(function (x) { return x.id === im.dataset.pid; })[0]; if (!p || !p.sb) return;
  window.__story([{ joy: p.t, hud: p.pn, dav: "", d: p.d, x: "", img: p.sb.f }], 0, im);
});
