(function () {
  "use strict";
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  // Header shadow on scroll
  var header = $(".header");
  if (header) {
    var onScroll = function () { header.classList.toggle("is-scrolled", window.scrollY > 8); };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Mobile menu
  var mnav = $(".mnav"), openBtn = $(".menu-btn"), closeBtn = $(".mnav__close");
  function setMenu(open) {
    if (!mnav) return;
    mnav.classList.toggle("is-open", open);
    document.body.style.overflow = open ? "hidden" : "";
    openBtn && openBtn.setAttribute("aria-expanded", String(open));
    if (open) closeBtn && closeBtn.focus(); else openBtn && openBtn.focus();
  }
  openBtn && openBtn.addEventListener("click", function () { setMenu(true); });
  closeBtn && closeBtn.addEventListener("click", function () { setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && mnav && mnav.classList.contains("is-open")) setMenu(false); });

  // Reveal on scroll
  var reveals = $$(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else { reveals.forEach(function (el) { el.classList.add("is-in"); }); }

  // Animated counters
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var counters = $$("[data-count]");
  function runCounter(el) {
    var end = parseFloat(el.getAttribute("data-count"));
    var dec = (el.getAttribute("data-count").split(".")[1] || "").length;
    var fmt = function (n) { return n.toLocaleString("en-US", { minimumFractionDigits: dec, maximumFractionDigits: dec }); };
    if (reduce) { el.textContent = fmt(end); return; }
    var start = null, dur = 1600;
    function step(t) {
      if (!start) start = t;
      var p = Math.min((t - start) / dur, 1), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = fmt(end * eased);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }
  if ("IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { runCounter(en.target); co.unobserve(en.target); } });
    }, { threshold: 0.4 });
    counters.forEach(function (el) { co.observe(el); });
  } else { counters.forEach(runCounter); }

  // Lightbox for galleries
  var lb = $(".lightbox");
  if (lb) {
    var lbImg = $("img", lb), lbCount = $(".lb-count", lb), items = [], idx = 0, lastFocus = null;
    function show(i) {
      idx = (i + items.length) % items.length;
      var b = items[idx];
      lbImg.src = b.getAttribute("data-full");
      lbImg.alt = $("img", b).alt;
      lbCount.textContent = (idx + 1) + " / " + items.length;
    }
    $$("[data-gallery]").forEach(function (g) {
      $$("button", g).forEach(function (b) {
        b.addEventListener("click", function () {
          items = $$("button", g); lastFocus = b;
          show(items.indexOf(b));
          lb.classList.add("is-open"); document.body.style.overflow = "hidden";
          $(".lb-close", lb).focus();
        });
      });
    });
    function close() { lb.classList.remove("is-open"); document.body.style.overflow = ""; lastFocus && lastFocus.focus(); }
    $(".lb-close", lb).addEventListener("click", close);
    $(".lb-prev", lb).addEventListener("click", function () { show(idx - 1); });
    $(".lb-next", lb).addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb) close(); });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") close();
      if (e.key === "ArrowRight") show(idx + 1);
      if (e.key === "ArrowLeft") show(idx - 1);
    });
  }

  // Donation amount picker
  var amounts = $$(".amount");
  if (amounts.length) {
    var line = $(".impact-line");
    amounts.forEach(function (a) {
      a.addEventListener("click", function () {
        amounts.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        a.setAttribute("aria-pressed", "true");
        if (line) line.innerHTML = a.getAttribute("data-impact");
      });
    });
  }

  // Services finder
  var finder = $("#finder");
  if (finder && window.KOMEN_SERVICIOS) {
    var data = window.KOMEN_SERVICIOS;
    var sel = $("#municipio"), tabs = $$(".tab", finder), out = $("#results"), count = $("#results-count");
    var cat = "Cernimiento y Diagnóstico";
    var towns = {};
    ["Adjuntas","Aguada","Aguadilla","Aguas Buenas","Aibonito","Añasco","Arecibo","Arroyo","Barceloneta","Barranquitas","Bayamón","Cabo Rojo","Caguas","Camuy","Canóvanas","Carolina","Cataño","Cayey","Ceiba","Ciales","Cidra","Coamo","Comerío","Corozal","Culebra","Dorado","Fajardo","Florida","Guánica","Guayama","Guayanilla","Guaynabo","Gurabo","Hatillo","Hormigueros","Humacao","Isabela","Jayuya","Juana Díaz","Juncos","Lajas","Lares","Las Marías","Las Piedras","Loíza","Luquillo","Manatí","Maricao","Maunabo","Mayagüez","Moca","Morovis","Naguabo","Naranjito","Orocovis","Patillas","Peñuelas","Ponce","Quebradillas","Rincón","Río Grande","Sabana Grande","Salinas","San Germán","San Juan","San Lorenzo","San Sebastián","Santa Isabel","Toa Alta","Toa Baja","Trujillo Alto","Utuado","Vega Alta","Vega Baja","Vieques","Villalba","Yabucoa","Yauco"].forEach(function (t) { towns[t] = 1; });
    data.forEach(function (o) { o.towns.forEach(function (t) { towns[t] = 1; }); });
    Object.keys(towns).sort(function (a, b) { return a.localeCompare(b, "es"); }).forEach(function (t) {
      var op = document.createElement("option"); op.value = t; op.textContent = t; sel.appendChild(op);
    });
    var ICON = {
      user: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
      mail: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
      phone: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
    };
    function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    function render() {
      var town = sel.value;
      var list = data.filter(function (o) { return o.cat === cat && (!town || o.towns.indexOf(town) > -1); });
      tabs.forEach(function (t) {
        var c = t.getAttribute("data-cat");
        var n = data.filter(function (o) { return o.cat === c && (!town || o.towns.indexOf(town) > -1); }).length;
        $("small", t).textContent = n;
      });
      count.textContent = list.length + (list.length === 1 ? " organización" : " organizaciones") + (town ? " sirven a " + town : " en todo Puerto Rico");
      if (!list.length) { out.innerHTML = '<div class="empty">No hay organizaciones en esta categoría para ' + esc(town) + '. Llámanos al <a href="tel:+17877519096">787-751-9096</a> y te orientamos.</div>'; return; }
      out.innerHTML = list.map(function (o) {
        var tw = o.towns.map(function (t) { return t === town ? "<mark>" + esc(t) + "</mark>" : esc(t); }).join(" · ");
        var mails = o.email.map(function (m) { return '<a href="mailto:' + esc(m) + '">' + ICON.mail + esc(m) + "</a>"; }).join("");
        var tel = o.tel ? '<span>' + ICON.phone + esc(o.tel) + "</span>" : "";
        var who = o.contact ? '<span>' + ICON.user + esc(o.contact) + "</span>" : "";
        return '<article class="org"><h3>' + esc(o.name) + "</h3><p>" + esc(o.desc) + '</p><div class="org__towns"><strong>Municipios:</strong> ' + tw + '</div><div class="org__contact">' + who + tel + mails + "</div></article>";
      }).join("");
    }
    tabs.forEach(function (t) {
      t.addEventListener("click", function () {
        tabs.forEach(function (x) { x.setAttribute("aria-selected", "false"); });
        t.setAttribute("aria-selected", "true");
        cat = t.getAttribute("data-cat"); render();
      });
    });
    sel.addEventListener("change", render);
    var qm = new URLSearchParams(location.search).get("m");
    if (qm && towns[qm]) sel.value = qm;
    render();
  }

  // Newsletter (static demo — connect to email provider)
  $$("form[data-demo]").forEach(function (f) {
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var msg = f.parentNode.querySelector(".form-note");
      if (msg) msg.textContent = "¡Gracias! Te mantendremos al tanto de eventos y noticias.";
      f.reset();
    });
  });

  // Mapa de Puerto Rico que se pinta de rosa
  var mapsec = $(".mapsec");
  if (mapsec) {
    var svg = $(".prmap", mapsec), munis = $$(".muni", svg);
    var countEl = $("#muni-count"), info = $(".mapinfo", mapsec);
    var nameEl = $(".mapinfo__name", info), metaEl = $(".mapinfo__meta", info), linkEl = $(".btn", info);
    var svc = {};
    (window.KOMEN_SERVICIOS || []).forEach(function (o) {
      o.towns.forEach(function (t) { (svc[t] = svc[t] || {})[o.name] = 1; });
    });
    var order = munis.slice().sort(function (a, b) { return a.dataset.cx - b.dataset.cx; });
    order.forEach(function (m, i) {
      var t = +m.dataset.cx / 1000;
      var d = t * 2.6 + ((i * 37) % 11) / 40;
      m.dataset.d = d;
      m.style.setProperty("--d", d.toFixed(2) + "s");
      m.style.setProperty("--w", (t * 3).toFixed(2) + "s");
      m.classList.add("s" + (1 + (i * 7) % 3));
      m.setAttribute("tabindex", "0");
      m.setAttribute("role", "button");
      m.setAttribute("aria-label", m.dataset.name);
    });
    // Punto que late sobre la oficina (Guaynabo)
    var gy = munis.filter(function (m) { return m.dataset.name === "Guaynabo"; })[0];
    if (gy) {
      var NS = "http://www.w3.org/2000/svg", g = document.createElementNS(NS, "g");
      g.setAttribute("class", "mappin"); g.setAttribute("aria-hidden", "true");
      var px = +gy.dataset.cx, py = +gy.dataset.cy;
      g.innerHTML = '<circle class="ring" cx="' + px + '" cy="' + py + '" r="7"/><circle class="dot" cx="' + px + '" cy="' + py + '" r="5"/><text x="' + (px + 12) + '" y="' + (py - 12) + '">Oficina Komen PR</text>';
      svg.appendChild(g);
    }
    var painted = false;
    function paint() {
      if (painted) return; painted = true;
      if (reduce) { mapsec.classList.add("is-painted", "is-done"); countEl.textContent = "78"; return; }
      mapsec.classList.add("is-painted");
      var n = 0, last = 0;
      order.forEach(function (m) {
        var ms = (+m.dataset.d + 0.25) * 1000; last = Math.max(last, ms);
        setTimeout(function () { n++; countEl.textContent = n; }, ms);
      });
      setTimeout(function () { mapsec.classList.add("is-done"); countEl.textContent = "78"; }, last + 700);
    }
    if ("IntersectionObserver" in window) {
      var mo = new IntersectionObserver(function (en) { if (en[0].isIntersecting) { paint(); mo.disconnect(); } }, { threshold: 0.35 });
      mo.observe(svg);
    } else { paint(); }
    function show(m) {
      munis.forEach(function (x) { x.classList.toggle("is-active", x === m); });
      var name = m.dataset.name, n = Object.keys(svc[name] || {}).length;
      nameEl.textContent = name;
      metaEl.textContent = n ? n + (n === 1 ? " organización aliada ofrece" : " organizaciones aliadas ofrecen") + " servicios aquí." : "Komen te orienta directamente: 787-751-9096.";
      linkEl.href = "ayuda.html?m=" + encodeURIComponent(name);
      linkEl.firstChild.textContent = "Ver ayuda en " + name + " ";
      info.classList.remove("is-idle");
    }
    munis.forEach(function (m) {
      m.addEventListener("mouseenter", function () { show(m); });
      m.addEventListener("focus", function () { show(m); });
      m.addEventListener("click", function () { show(m); });
      m.addEventListener("keydown", function (e) { if (e.key === "Enter") { show(m); location.href = linkEl.href; } });
    });
  }

  var y = $("#year"); if (y) y.textContent = new Date().getFullYear();
})();
