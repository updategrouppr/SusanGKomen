#!/usr/bin/env python3
"""Arma las páginas del sitio: header + contenido + footer.
Uso: python3 build.py   (escribe los .html en esta carpeta)"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

DONAR = "https://www.paypal.com/donate/?hosted_button_id=FUBL99RVP8JZC"
TIENDA = "https://susan-g-komen-puerto-rico-4.myshopify.com/"
RESULTADOS = "https://my.raceresult.com/417441/results"
PINKDAY_SHOP = "https://stores.tpxpr.com/pink_day/shop/home"
REGISTRO = "https://komenpr.org/registro-de-sobrevivientes/"
PLAN_CUIDADO = "https://komenpr.org/wp-content/uploads/2016/11/PlandeCuidadoSobrevivientesLetter-8.5x11.pdf"
FB, IG, X, YT = "https://facebook.com/komenpr", "https://instagram.com/komenpr", "https://twitter.com/komenpr", "https://www.youtube.com/@susang.komenpuertorico116"

# ---------- Icons (Lucide style, 24x24 stroke) ----------
S = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
ICONS = {
  "arrow": S + '<path d="M5 12h14M12 5l7 7-7 7"/></svg>',
  "phone": S + '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
  "mail": S + '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg>',
  "pin": S + '<path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>',
  "heart": S + '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>',
  "hands": S + '<path d="M11 14h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 16"/><path d="m7 20 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/><path d="m2 15 6 6"/><path d="M19.5 8.5c.7-.7 1.5-1.6 1.5-2.7A2.73 2.73 0 0 0 16 4a2.78 2.78 0 0 0-5 1.8c0 1.2.8 2 1.5 2.8L16 12Z"/></svg>',
  "users": S + '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>',
  "book": S + '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
  "search": S + '<circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>',
  "calendar": S + '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>',
  "bag": S + '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18M16 10a4 4 0 0 1-8 0"/></svg>',
  "flag": S + '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/></svg>',
  "info": S + '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/></svg>',
  "menu": S + '<path d="M4 7h16M4 12h16M4 17h16"/></svg>',
  "close": S + '<path d="M18 6 6 18M6 6l12 12"/></svg>',
  "left": S + '<path d="m15 18-6-6 6-6"/></svg>',
  "right": S + '<path d="m9 18 6-6-6-6"/></svg>',
  "stetho": S + '<path d="M4.8 2.3A.3.3 0 1 0 5 2H4a2 2 0 0 0-2 2v5a6 6 0 0 0 6 6 6 6 0 0 0 6-6V4a2 2 0 0 0-2-2h-1a.2.2 0 1 0 .3.3"/><path d="M8 15v1a6 6 0 0 0 6 6 6 6 0 0 0 6-6v-4"/><circle cx="20" cy="10" r="2"/></svg>',
  "shield": S + '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/></svg>',
  "run": S + '<circle cx="13" cy="4" r="2"/><path d="m4 22 4-6 3 2v4"/><path d="M14 22v-6l-3-2 2-6"/><path d="M6 12l2-4 5 0 3 4 3 1"/></svg>',
  "gift": S + '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/></svg>',
  "ribbon": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a4 4 0 0 0-4 4c0 1.7.8 3.3 1.8 5L4.5 19.5 7.5 22 12 14.6 16.5 22l3-2.5-5.3-8.5C15.2 9.3 16 7.7 16 6a4 4 0 0 0-4-4Zm0 2.3A1.7 1.7 0 0 1 13.7 6c0 .9-.6 2.2-1.7 4-1.1-1.8-1.7-3.1-1.7-4A1.7 1.7 0 0 1 12 4.3Z"/></svg>',
  "fb": S + '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/></svg>',
  "ig": S + '<rect x="2" y="2" width="20" height="20" rx="5"/><circle cx="12" cy="12" r="4"/><path d="M17.5 6.5h.01"/></svg>',
  "x": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.75 3h3.07l-6.7 7.66L22 21h-6.17l-4.83-6.32L5.47 21H2.4l7.17-8.2L2 3h6.33l4.37 5.77L17.75 3Zm-1.08 16.2h1.7L7.4 4.72H5.58L16.67 19.2Z"/></svg>',
  "yt": S + '<path d="M2.5 17a24.12 24.12 0 0 1 0-10 2 2 0 0 1 1.4-1.4 49.56 49.56 0 0 1 16.2 0A2 2 0 0 1 21.5 7a24.12 24.12 0 0 1 0 10 2 2 0 0 1-1.4 1.4 49.55 49.55 0 0 1-16.2 0A2 2 0 0 1 2.5 17"/><path d="m10 15 5-3-5-3z"/></svg>',
}

def rings(cls="", a="#E776AD", b="#C70772"):
    # Círculos del brand board: anillo exterior "cercanía" + anillo interior "acción"
    return (f'<svg class="rings {cls}" viewBox="1012 152 376 356" aria-hidden="true">'
            f'<circle cx="1190" cy="330" r="150" stroke="{a}" stroke-width="55"/>'
            f'<circle cx="1260" cy="330" r="100" stroke="{b}" stroke-width="55"/></svg>')

def expand(html):
    html = re.sub(r"\{\{i:(\w+)\}\}", lambda m: ICONS[m.group(1)], html)
    html = re.sub(r"\{\{rings:([\w-]*):?([#\w]*):?([#\w]*)\}\}",
                  lambda m: rings(m.group(1), m.group(2) or "#E776AD", m.group(3) or "#C70772"), html)
    for k, v in {"DONAR": DONAR, "TIENDA": TIENDA, "RESULTADOS": RESULTADOS, "PINKDAY_SHOP": PINKDAY_SHOP,
                 "REGISTRO": REGISTRO, "PLAN_CUIDADO": PLAN_CUIDADO}.items():
        html = html.replace("{{" + k + "}}", v)
    return html

NAV = [("nosotros.html", "Nosotros"), ("cancer-de-seno.html", "Cáncer de seno"), ("ayuda.html", "Busca ayuda"),
       ("sobrevivientes.html", "Sobrevivientes"), ("eventos.html", "Eventos"), ("involucrate.html", "Involúcrate"),
       ("contacto.html", "Contacto")]

def header(active):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == active else ""}>{t}</a>' for h, t in NAV)
    return f'''<a class="skip" href="#main">Saltar al contenido</a>
<div class="topbar"><div class="wrap">
  <div class="topbar__info">
    <span>{{{{i:phone}}}}<a href="tel:+17877519096">787-751-9096</a></span>
    <span>{{{{i:mail}}}}<a href="mailto:info@komenpr.org">info@komenpr.org</a></span>
    <span>{{{{i:pin}}}}Guaynabo, Puerto Rico</span>
  </div>
  <div class="social">
    <a href="{FB}" aria-label="Facebook" target="_blank" rel="noopener">{{{{i:fb}}}}</a>
    <a href="{IG}" aria-label="Instagram" target="_blank" rel="noopener">{{{{i:ig}}}}</a>
    <a href="{X}" aria-label="X (Twitter)" target="_blank" rel="noopener">{{{{i:x}}}}</a>
    <a href="{YT}" aria-label="YouTube" target="_blank" rel="noopener">{{{{i:yt}}}}</a>
  </div>
</div></div>
<header class="header"><div class="wrap">
  <a class="brand" href="index.html" aria-label="Susan G. Komen Puerto Rico — inicio"><img src="img/site/logo-dark.png" alt="Susan G. Komen Puerto Rico" width="640" height="306"></a>
  <nav class="nav" aria-label="Principal">{links}</nav>
  <div class="header__cta">
    <a class="btn btn--sm" href="{DONAR}" target="_blank" rel="noopener">{{{{i:heart}}}}Dona ahora</a>
    <button class="menu-btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="mnav">{{{{i:menu}}}}</button>
  </div>
</div></header>
<div class="mnav" id="mnav" role="dialog" aria-modal="true" aria-label="Menú">
  <div class="mnav__top"><img src="img/site/logo-light.png" alt="Susan G. Komen Puerto Rico" width="640" height="306"><button class="mnav__close" aria-label="Cerrar menú">{{{{i:close}}}}</button></div>
  <nav aria-label="Móvil"><a href="index.html"{" aria-current=\"page\"" if active == "index.html" else ""}>Inicio</a>{links}</nav>
  <a class="btn" href="{DONAR}" target="_blank" rel="noopener">{{{{i:heart}}}}Dona ahora</a>
</div>
<main id="main">'''

FOOTER = f'''</main>
<footer class="footer"><div class="wrap">
  <p class="footer__big">Contigo,<br><span>hacia adelante.</span></p>
  <div class="footer__grid">
    <div>
      <img class="flogo" src="img/site/logo-light.png" alt="Susan G. Komen Puerto Rico" width="640" height="306">
      <p>Desde 2003 salvando vidas en los 78 municipios. El 100% de los fondos recaudados se quedan en Puerto Rico.</p>
      <div class="social">
        <a href="{FB}" aria-label="Facebook" target="_blank" rel="noopener">{{{{i:fb}}}}</a>
        <a href="{IG}" aria-label="Instagram" target="_blank" rel="noopener">{{{{i:ig}}}}</a>
        <a href="{X}" aria-label="X (Twitter)" target="_blank" rel="noopener">{{{{i:x}}}}</a>
        <a href="{YT}" aria-label="YouTube" target="_blank" rel="noopener">{{{{i:yt}}}}</a>
      </div>
    </div>
    <div><h4>Organización</h4><ul>
      <li><a href="nosotros.html">Sobre nosotros</a></li>
      <li><a href="nosotros.html#impacto">Nuestro impacto</a></li>
      <li><a href="nosotros.html#equipo">Junta y personal</a></li>
      <li><a href="index.html#noticias">Noticias</a></li>
      <li><a href="contacto.html">Contáctanos</a></li></ul></div>
    <div><h4>Recursos</h4><ul>
      <li><a href="cancer-de-seno.html">El cáncer de seno</a></li>
      <li><a href="ayuda.html">Servicios disponibles</a></li>
      <li><a href="ayuda.html#organizaciones">Fondos para organizaciones</a></li>
      <li><a href="sobrevivientes.html">Sobrevivientes</a></li>
      <li><a href="{PLAN_CUIDADO}" target="_blank" rel="noopener">Plan de cuidado (PDF)</a></li></ul></div>
    <div><h4>Participa</h4><ul>
      <li><a href="eventos.html#race">Race for the Cure®</a></li>
      <li><a href="eventos.html#pinkday">Pink Day</a></li>
      <li><a href="eventos.html#gala">Pink Gala</a></li>
      <li><a href="involucrate.html#voluntarios">Voluntariado</a></li>
      <li><a href="{TIENDA}" target="_blank" rel="noopener">Tienda online</a></li></ul></div>
  </div>
  <div class="footer__bottom">
    <span>© <span id="year">2026</span> Susan G. Komen Puerto Rico® · 27 Ave. González Giusti, Piso 4, Ofic. 403, Guaynabo, PR 00968</span>
    <span>Fotos del Race: Alberto Bartolomei · Tel. <a href="tel:+17877519096">787-751-9096</a> · <a href="mailto:info@komenpr.org">info@komenpr.org</a></span>
  </div>
</div></footer>
<div class="lightbox" role="dialog" aria-modal="true" aria-label="Galería">
  <button class="lb-close" aria-label="Cerrar">{{{{i:close}}}}</button>
  <button class="lb-prev" aria-label="Anterior">{{{{i:left}}}}</button>
  <img src="" alt="">
  <button class="lb-next" aria-label="Siguiente">{{{{i:right}}}}</button>
  <div class="lb-count"></div>
</div>
'''

def page(fname, title, desc, body, scripts=""):
    full_title = "Susan G. Komen Puerto Rico" if fname == "index.html" else f"{title} · Susan G. Komen Puerto Rico"
    html = f'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#C70772">
<meta property="og:title" content="{full_title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="img/photos/r25-celebracion.jpg">
<meta property="og:locale" content="es_PR">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='%23C70772' d='M12 2a4 4 0 0 0-4 4c0 1.7.8 3.3 1.8 5L4.5 19.5 7.5 22 12 14.6 16.5 22l3-2.5-5.3-8.5C15.2 9.3 16 7.7 16 6a4 4 0 0 0-4-4Zm0 2.3A1.7 1.7 0 0 1 13.7 6c0 .9-.6 2.2-1.7 4-1.1-1.8-1.7-3.1-1.7-4A1.7 1.7 0 0 1 12 4.3Z'/%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@500;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
{header(fname)}
{body}
{FOOTER}
{scripts}<script src="assets/js/main.js"></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(expand(html))
    print("✓", fname)

def gallery(items, size_classes):
    out = []
    for (img, alt), cls in zip(items, size_classes):
        out.append(f'<button class="{cls}" data-full="img/photos/{img}.jpg" aria-label="Ver foto: {alt}"><img src="img/photos/{img}.jpg" alt="{alt}" loading="lazy"></button>')
    return '<div class="mosaic" data-gallery>' + "".join(out) + "</div>"

# =====================================================================
# INICIO
# =====================================================================
home_gallery = gallery([
  ("r25-multitud", "Cientos de sobrevivientes celebrando en el Coliseo durante el Race for the Cure 2025"),
  ("gala-pareja", "Invitados en la Pink Gala"),
  ("race-2016-calle", "Corredoras en el Race for the Cure"),
  ("pinkday-amigas", "Participantes del Pink Day en AEELA"),
  ("r25-corazones", "Participantes con corazones rosados en el Race 2025"),
  ("lazo-humano", "Empleados formando un lazo rosado humano en el Pink Day"),
  ("r25-aerea", "Vista aérea del Race for the Cure 2025"),
  ("gala-trio-2", "Invitadas en la Pink Gala Pearls of Hope"),
  ("pinkday-grupo-2", "Equipo de Deco Centro con camisetas del Pink Day"),
], ["m-a", "m-b", "m-c", "m-e", "m-e", "m-d", "m-f", "m-e", "m-e"])

PRMAP = open(os.path.join(ROOT, "data", "pr_map.svg"), encoding="utf-8").read()
home = f'''
<section class="hero"><div class="wrap hero__grid">
  <div>
    <p class="kicker reveal">Puerto Rico · Desde 2003</p>
    <h1 class="reveal reveal-d1"><span class="line">Contigo,</span><span class="line">hacia <span class="accent">adelante.</span></span></h1>
    <p class="lead reveal reveal-d2">Educación, cernimiento, ayuda para tratamiento y apoyo para sobrevivientes en los 78 municipios. Nadie debería enfrentar el cáncer de seno sola.</p>
    <div class="btn-row reveal reveal-d3">
      <a class="btn" href="ayuda.html">Busca ayuda cerca de ti {{{{i:arrow}}}}</a>
      <a class="btn btn--ghost" href="{{{{DONAR}}}}" target="_blank" rel="noopener">Haz tu donación</a>
    </div>
  </div>
  <div class="hero__media reveal reveal-d2">
    {{{{rings:}}}}
    <div class="photo"><img src="img/photos/r25-celebracion.jpg" alt="Sobrevivientes celebrando con corazones rosados en el Race for the Cure 2025" fetchpriority="high" style="object-position:40% 50%"></div>
    <div class="hero__badge"><strong>100%</strong><span>de los fondos recaudados se quedan en Puerto Rico</span></div>
  </div>
</div></section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">
  {"".join(f'<span class="marquee__item">{t}{{{{i:ribbon}}}}</span>' for t in ["Tu apoyo nos mueve", "Detección temprana salva vidas", "78 municipios", "Humano. Claro. Activo.", "En cada paso, juntos por ti"] * 2)}
</div></div>

<section class="section mapsec" id="mapa"><div class="wrap">
  <div class="mapsec__head">
    <div><p class="kicker">Presentes en toda la Isla</p><h2>Puerto Rico, pintado de rosa.</h2></div>
    <div class="mapcount" aria-live="off"><b id="muni-count">0</b><span>de 78 municipios</span></div>
  </div>
  <div class="mapwrap">{PRMAP}</div>
  <div class="mapinfo is-idle">
    <div><div class="mapinfo__name">Toca tu municipio</div><div class="mapinfo__meta">Mira cuántas organizaciones aliadas ofrecen servicios cerca de ti.</div></div>
    <a class="btn btn--sm" href="ayuda.html">Ver ayuda {{{{i:arrow}}}}</a>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">¿Cómo te ayudamos hoy?</p><h2>Empieza por aquí.</h2></div></div>
  <div class="paths">
    <a class="path path--featured reveal" href="ayuda.html"><span class="path__icon">{{{{i:search}}}}</span><h3>Necesito ayuda</h3><p>Mamografías, diagnóstico y asistencia para tratamiento sin costo, según tu municipio.</p><span class="link-arrow">Buscar servicios {{{{i:arrow}}}}</span></a>
    <a class="path reveal reveal-d1" href="cancer-de-seno.html"><span class="path__icon">{{{{i:book}}}}</span><h3>Quiero aprender</h3><p>Señales de alerta, factores de riesgo y qué preguntarle a tu médico.</p><span class="link-arrow">Educación {{{{i:arrow}}}}</span></a>
    <a class="path reveal reveal-d2" href="involucrate.html#voluntarios"><span class="path__icon">{{{{i:hands}}}}</span><h3>Quiero ayudar</h3><p>Únete a la familia de voluntarios Komen en educación, eventos y comunidad.</p><span class="link-arrow">Ser voluntario {{{{i:arrow}}}}</span></a>
    <a class="path reveal reveal-d3" href="sobrevivientes.html"><span class="path__icon">{{{{i:heart}}}}</span><h3>Soy sobreviviente</h3><p>Recursos para cada etapa: diagnóstico, tratamiento, sobrevivencia y familia.</p><span class="link-arrow">Ver recursos {{{{i:arrow}}}}</span></a>
  </div>
</div></section>

<section class="section section--negro" id="impacto"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Nuestro impacto</p><h2>Lo que logramos juntos.</h2><p class="lead">Cada inscripción, camiseta y donación se convierte en servicios para personas reales en nuestra Isla.</p></div>
  <a class="link-arrow" href="nosotros.html#impacto">Conoce más {{{{i:arrow}}}}</a></div>
  <div class="stats">
    <div class="stat reveal"><div class="stat__num"><span data-count="206">206</span></div><div class="stat__label">proyectos de impacto comunitario financiados desde 2010</div></div>
    <div class="stat reveal reveal-d1"><div class="stat__num"><span data-count="10000">10,000</span><em>+</em></div><div class="stat__label">personas recibieron cernimiento, diagnóstico o ayuda en tratamiento libre de costo</div></div>
    <div class="stat reveal reveal-d2"><div class="stat__num"><span data-count="2">2</span><em>M+</em></div><div class="stat__label">personas impactadas por nuestro Programa de Educación</div></div>
    <div class="stat reveal"><div class="stat__num"><span data-count="78">78</span></div><div class="stat__label">municipios servidos en todo Puerto Rico</div></div>
    <div class="stat reveal reveal-d1"><div class="stat__num"><span data-count="100">100</span><em>%</em></div><div class="stat__label">de los fondos recaudados se quedan en la Isla</div></div>
    <div class="stat reveal reveal-d2"><div class="stat__num">2003</div><div class="stat__label">año en que comenzamos a trabajar en Puerto Rico</div></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="split reveal">
    <div class="split__a"><span class="tag">Campaña</span><h2>Tu apoyo<br>nos mueve.</h2><div class="btn-row"><a class="btn btn--white" href="{{{{DONAR}}}}" target="_blank" rel="noopener">Dona ahora {{{{i:arrow}}}}</a></div>{{{{rings::#ffffff:#ffffff}}}}</div>
    <div class="split__b"><span class="tag">Por qué importa</span><h3>El cáncer de seno es el cáncer más diagnosticado en la Isla.</h3><p>Tu donación financia mamografías, biopsias, quimioterapia, transportación y grupos de apoyo a través de organizaciones aliadas en todo Puerto Rico.</p><a class="link-arrow" href="involucrate.html">Otras formas de apoyar {{{{i:arrow}}}}</a></div>
  </div>
</div></section>

<section class="section section--rosa"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Eventos</p><h2>Celebramos la vida en grande.</h2></div><a class="link-arrow" href="eventos.html">Todos los eventos {{{{i:arrow}}}}</a></div>
  <div class="cards">
    <a class="card reveal" href="eventos.html#race"><div class="card__media"><img src="img/photos/r25-aerea.jpg" alt="Vista aérea de la avenida llena de participantes del Race for the Cure" loading="lazy"></div>
      <div class="card__body"><span class="chip">{{{{i:run}}}}Gracias por correr con nosotras</span><h3>Race for the Cure® 2026</h3><p>“En cada paso, juntos por ti.” Miles celebramos a las sobrevivientes en el Coliseo José Miguel Agrelot.</p><span class="link-arrow">Ver resultados {{{{i:arrow}}}}</span></div></a>
    <a class="card reveal reveal-d1" href="eventos.html#pinkday"><div class="card__media"><img src="img/photos/pinkday-guardia.jpg" alt="Grupo con camisetas del Pink Day" loading="lazy"></div>
      <div class="card__body"><span class="chip">{{{{i:ribbon}}}}Empresas y escuelas</span><h3>Pink Day</h3><p>Tu oficina, escuela o agencia se viste de rosa por un día para educar y recaudar fondos.</p><span class="link-arrow">Únete al Pink Day {{{{i:arrow}}}}</span></div></a>
    <a class="card reveal reveal-d2" href="eventos.html#gala"><div class="card__media"><img src="img/photos/gala26-escalera.jpg" alt="Entrada decorada de la Pink Gala 2026" loading="lazy"></div>
      <div class="card__body"><span class="chip">{{{{i:gift}}}}Gala anual</span><h3>Pink Gala</h3><p>Nuestra noche más elegante del año. En 2026 viajamos a “Las Mil y Una Noches”.</p><span class="link-arrow">Ver memorias {{{{i:arrow}}}}</span></div></a>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Momentos</p><h2>Una isla vestida de rosa.</h2><p class="lead">Fotos de nuestra comunidad en el Race for the Cure, el Pink Day y la Pink Gala. Toca cualquier foto para verla en grande.</p></div>
  <a class="link-arrow" href="{FB}" target="_blank" rel="noopener">Más en Facebook {{{{i:arrow}}}}</a></div>
  <div class="reveal">{home_gallery}</div>
</div></section>

<section class="section section--rosa"><div class="wrap quote">
  <div class="quote__img reveal"><img src="img/photos/race-sobreviviente.jpg" alt="Sobreviviente celebrando en el Race for the Cure" loading="lazy" style="object-position:60% 50%"></div>
  <div class="reveal reveal-d1">
    <p class="kicker">Sobrevivientes</p>
    <blockquote>Cada sobreviviente merece sentirse acompañada, celebrada y respaldada en cada paso de su camino.</blockquote>
    <p class="lead">Ya sea que te acaban de diagnosticar, estés en tratamiento o acompañes a un ser querido, tenemos recursos y asistencia para ti.</p>
    <div class="btn-row"><a class="btn btn--dark" href="sobrevivientes.html">Recursos para sobrevivientes {{{{i:arrow}}}}</a><a class="btn btn--ghost" href="{{{{REGISTRO}}}}" target="_blank" rel="noopener">Regístrate</a></div>
  </div>
</div></section>

<section class="section" id="noticias"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Últimas noticias</p><h2>Lo nuevo en Komen PR.</h2></div></div>
  <div class="news">
    <a class="news__main reveal" href="https://komenpr.org/race-for-the-cure-de-susan-g-komen-puerto-rico-en-cada-paso-juntos-por-ti/" target="_blank" rel="noopener">
      {{{{rings::#C70772:#E776AD}}}}
      <span class="meta">20 de agosto de 2026 · Race for the Cure</span>
      <h3>Race for the Cure: “En cada paso, juntos por ti”</h3>
      <p>La periodista Aixa Vázquez, de Noticentro al Amanecer, fue la madrina de la carrera 2026, uniendo su voz al mensaje de solidaridad con las sobrevivientes.</p>
      <span class="link-arrow">Leer más {{{{i:arrow}}}}</span>
    </a>
    <div class="news__side">
      <a class="card reveal reveal-d1" href="{{{{RESULTADOS}}}}" target="_blank" rel="noopener"><div class="card__body"><span class="chip chip--dark">{{{{i:run}}}}Resultados</span><h3>Busca tu tiempo del Race for the Cure</h3><p>Consulta los resultados oficiales de la carrera.</p><span class="link-arrow">Ver resultados {{{{i:arrow}}}}</span></div></a>
      <a class="card reveal reveal-d2" href="{{{{TIENDA}}}}" target="_blank" rel="noopener"><div class="card__body"><span class="chip">{{{{i:bag}}}}Tienda</span><h3>Lleva el rosa contigo</h3><p>Cada compra en la tienda online apoya nuestros programas.</p><span class="link-arrow">Ir a la tienda {{{{i:arrow}}}}</span></div></a>
    </div>
  </div>
</div></section>

<section class="section section--tight"><div class="wrap">
  <div class="cta-band reveal">
    {{{{rings::#C70772:#E776AD}}}}
    <div><p class="kicker">Boletín</p><h2>Mantente informada.</h2><p>Recibe fechas de eventos, clínicas de mamografías y noticias de Komen Puerto Rico.</p></div>
    <div><form class="form-inline" data-demo><label for="nl-email" class="skip">Tu email</label><input id="nl-email" type="email" required placeholder="Tu email" autocomplete="email"><button class="btn" type="submit">Suscribirme</button></form><p class="form-note">Sin spam. Puedes darte de baja cuando quieras.</p></div>
  </div>
</div></section>
'''
page("index.html", "Inicio", "Susan G. Komen Puerto Rico: educación, cernimiento, ayuda para tratamiento y apoyo a sobrevivientes de cáncer de seno en los 78 municipios. El 100% de los fondos se queda en Puerto Rico.", home, scripts='<script src="data/servicios.js"></script>\n')

# =====================================================================
# NOSOTROS
# =====================================================================
nosotros = f'''
<section class="phero phero--img">
  <div class="phero__bg"><img src="img/photos/pinkday-grupo-3.jpg" alt=""></div>
  <div class="wrap"><nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a> / <span>Nosotros</span></nav>
  <p class="kicker">Sobre nosotros</p><h1>Un mundo sin cáncer de seno.</h1>
  <p class="lead">Somos parte de la red comunitaria de sobrevivientes, voluntarios y activistas más grande del mundo que lucha para eliminar esta enfermedad para siempre.</p></div>
</section>

<section class="section"><div class="wrap two two--center">
  <div class="prose reveal">
    <p class="kicker">Nuestra misión</p>
    <h2>Salvar vidas y erradicar el cáncer de seno.</h2>
    <p>Desde el 2003, Susan G. Komen Puerto Rico® se ha mantenido enfocada en su misión: llenar las necesidades de salud de senos de mujeres, hombres y familias en riesgo y en necesidad en nuestra comunidad.</p>
    <p>Creemos firmemente que la detección temprana es parte de la cura. Por eso apoderamos a las personas, aseguramos cuidados de salud de calidad para todos y energizamos la ciencia para buscar curas.</p>
  </div>
  <div class="stack-imgs reveal reveal-d1">
    <div class="img-round"><img src="img/photos/pinkday-amigas.jpg" alt="Participantes del Pink Day" loading="lazy"></div>
    <div class="img-round"><img src="img/photos/race-arco.jpg" alt="Sobreviviente celebrando bajo el arco del Race for the Cure" loading="lazy"></div>
    <div class="img-round"><img src="img/photos/pinkday-equipo.jpg" alt="Equipo con camisetas rosadas" loading="lazy"></div>
  </div>
</div></section>

<section class="section section--negro"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Juntos trabajamos para</p><h2>Cuatro compromisos.</h2></div></div>
  <div class="pillars">
    <div class="pillar reveal"><h3>Salvar vidas</h3><p>Promovemos la detección temprana y el acceso a cernimiento y diagnóstico.</p></div>
    <div class="pillar reveal reveal-d1"><h3>Empoderar</h3><p>Educamos a la comunidad para que cada persona conozca su cuerpo y su riesgo.</p></div>
    <div class="pillar reveal reveal-d2"><h3>Garantizar cuidado</h3><p>Eliminamos barreras para que todos reciban cuidados de calidad.</p></div>
    <div class="pillar reveal reveal-d3"><h3>Energizar la ciencia</h3><p>Impulsamos la investigación para encontrar las curas.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap two">
  <div class="reveal"><p class="kicker">Nuestra historia</p><h2>Una promesa entre hermanas.</h2>
    <p class="lead">Susan G. Komen luchó contra el cáncer de seno con cuerpo, alma y corazón. Su hermana, Nancy G. Brinker, le prometió que haría todo lo posible por erradicar la enfermedad para siempre. Esa promesa es hoy Susan G. Komen®.</p></div>
  <div class="timeline reveal reveal-d1">
    <div class="tl"><b>1982</b><p>Nace Susan G. Komen®. Hoy es líder global del movimiento contra el cáncer de seno, con más de $2,500 millones invertidos.</p></div>
    <div class="tl"><b>2003</b><p>Se establece Susan G. Komen Puerto Rico® para promover la concienciación sobre el cáncer de seno en la Isla.</p></div>
    <div class="tl"><b>2010</b><p>Comienza el Programa de Ayudas, que financia proyectos de organizaciones sin fines de lucro en toda la Isla.</p></div>
    <div class="tl"><b>Hoy</b><p>206 proyectos financiados, más de 10,000 personas atendidas libre de costo y presencia en los 78 municipios.</p></div>
  </div>
</div></section>

<section class="section section--rosa" id="impacto"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Nuestro impacto</p><h2>El 100% se queda aquí.</h2><p class="lead">Los fondos mejoran las condiciones sociales, culturales y financieras que impiden a la población recibir educación, cuidado de los senos y tratamientos de calidad.</p></div></div>
  <div class="cards">
    <div class="card reveal"><div class="card__body"><span class="path__icon">{{{{i:stetho}}}}</span><h3>Programa de Ayudas</h3><p>Financiamos organizaciones sin fines de lucro que ofrecen cernimiento, diagnóstico, asistencia en tratamiento activo y apoyo a pacientes, sobrevivientes y familiares.</p><a class="link-arrow" href="ayuda.html">Servicios disponibles {{{{i:arrow}}}}</a></div></div>
    <div class="card reveal reveal-d1"><div class="card__body"><span class="path__icon">{{{{i:book}}}}</span><h3>Educación en salud de los senos</h3><p>Charlas, mesas educativas y materiales para niños, adolescentes, hombres, sobrevivientes y comunidades en riesgo, incluida la comunidad LGBTTTI.</p><a class="link-arrow" href="cancer-de-seno.html">Aprende {{{{i:arrow}}}}</a></div></div>
    <div class="card reveal reveal-d2"><div class="card__body"><span class="path__icon">{{{{i:flag}}}}</span><h3>Programa Banderas</h3><p>Alianzas con corporaciones, agencias de gobierno e instituciones educativas para llevar recursos educativos a sus empleados y comunidades.</p><a class="link-arrow" href="involucrate.html#banderas">Hazte aliado {{{{i:arrow}}}}</a></div></div>
  </div>
</div></section>

<section class="section" id="equipo"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Nuestro equipo</p><h2>Junta de Directores.</h2></div></div>
  <div class="people reveal">
    <div class="person person--lead"><b>Sra. Lybia Grisselle Vientós Vda. de Báez, M.P.H.</b><span>Presidenta</span></div>
    <div class="person person--lead"><b>Dra. Anna Di Marco</b><span>Vicepresidenta</span></div>
    <div class="person person--lead"><b>Dra. Josefina López</b><span>Secretaria</span></div>
    <div class="person person--lead"><b>Lcda. Annette Nogueras</b><span>Tesorera</span></div>
    <div class="person"><b>Dra. Eva Cruz Jové</b><span>Directora</span></div>
    <div class="person"><b>Dr. Miguel Echenique</b><span>Director</span></div>
    <div class="person"><b>Dr. Carlos González</b><span>Director</span></div>
    <div class="person"><b>Sra. Ixel Rivera</b><span>Directora</span></div>
    <div class="person"><b>Sra. Nahir Toro</b><span>Directora</span></div>
    <div class="person"><b>Dra. Noelani González</b><span>Directora</span></div>
    <div class="person"><b>Dra. Elba Torres Matundan</b><span>Directora</span></div>
  </div>
  <div class="shead reveal" style="margin-top:72px"><div><h2>Personal.</h2></div></div>
  <div class="people reveal">
    <div class="person"><b>Lynnette Rodríguez</b><span>Directora Ejecutiva y Coordinadora de los Programas de Ayuda</span><br><a href="mailto:lrodriguez@komenpr.org">lrodriguez@komenpr.org</a></div>
    <div class="person"><b>Carlos Montañez</b><span>Coordinador de Voluntarios y Pink Day</span><br><a href="mailto:pinkday@komenpr.org">pinkday@komenpr.org</a></div>
    <div class="person"><b>Sandra García</b><span>Oficinista</span><br><a href="mailto:secretaria@komenpr.org">secretaria@komenpr.org</a></div>
  </div>
</div></section>
'''
page("nosotros.html", "Nosotros", "Conoce la misión, historia, impacto y equipo de Susan G. Komen Puerto Rico, al servicio de la Isla desde 2003.", nosotros)

# =====================================================================
# CÁNCER DE SENO (educación)
# =====================================================================
signs = [("Bulto, nudo duro o engrosamiento dentro del seno o la axila", "lump"),
         ("Hinchazón, calor, enrojecimiento u oscurecimiento del seno", "warm"),
         ("Cambio en el tamaño o la forma del seno", "shape"),
         ("Hoyuelos o arrugas en la piel", "dimple"),
         ("Llaga, sarpullido o descamación en el pezón", "rash"),
         ("Pezón que se hunde u otras partes del seno que se retraen", "pull"),
         ("Secreción del pezón que aparece de repente", "drop"),
         ("Dolor nuevo en un área que no desaparece", "pain")]
def sign_icon(k):
    base = '<svg class="sign__ico" viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="27" fill="#FBE3EE"/><circle cx="28" cy="30" r="15" fill="none" stroke="#C70772" stroke-width="2.5"/>'
    extra = {
      "lump": '<circle cx="33" cy="26" r="4" fill="#C70772"/>',
      "warm": '<path d="M22 22c2 3-2 5 0 8M28 20c2 3-2 5 0 8M34 22c2 3-2 5 0 8" stroke="#C70772" stroke-width="2.2" fill="none" stroke-linecap="round"/>',
      "shape": '<circle cx="28" cy="30" r="10" fill="none" stroke="#E776AD" stroke-width="2.5" stroke-dasharray="3 3"/>',
      "dimple": '<path d="M20 30q4 4 8 0t8 0" stroke="#C70772" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
      "rash": '<circle cx="28" cy="30" r="3.5" fill="#C70772"/><path d="M23 25l2 2M33 25l-2 2M23 35l2-2M33 35l-2-2" stroke="#C70772" stroke-width="2" stroke-linecap="round"/>',
      "pull": '<path d="M28 24v8M24 28l4 4 4-4" stroke="#C70772" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>',
      "drop": '<path d="M28 23c3 4 4 6 4 8a4 4 0 0 1-8 0c0-2 1-4 4-8z" fill="#C70772"/>',
      "pain": '<path d="M29 20l-5 10h5l-2 9 7-12h-5l2-7z" fill="#C70772"/>'}[k]
    return base + extra + "</svg>"

edu = f'''
<section class="phero"><div class="wrap">
  {{{{rings:}}}}
  <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a> / <span>Cáncer de seno</span></nav>
  <p class="kicker">Educación</p><h1>Conoce tu cuerpo. Conoce tu riesgo.</h1>
  <p class="lead">La detección temprana es parte de la cura. Aquí tienes lo esencial para cuidar tu salud de los senos y la de quienes amas.</p>
</div></section>

<section class="section section--negro"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Autoconocimiento</p><h2>Cuatro hábitos que salvan vidas.</h2></div></div>
  <div class="pillars">
    <div class="pillar reveal"><h3>Conoce tu riesgo</h3><p>Habla con tu familia sobre su historial de salud y con tu médico sobre tu riesgo personal.</p></div>
    <div class="pillar reveal reveal-d1"><h3>Hazte las pruebas</h3><p>Pregunta qué pruebas de cernimiento son para ti. Si tienes riesgo promedio, la mamografía suele comenzar a los 40 años.</p></div>
    <div class="pillar reveal reveal-d2"><h3>Conoce lo normal para ti</h3><p>Familiarízate con cómo se ven y se sienten tus senos, y reporta cualquier cambio a tu médico.</p></div>
    <div class="pillar reveal reveal-d3"><h3>Estilo de vida saludable</h3><p>Mantén un peso saludable, haz ejercicio, limita el alcohol y considera lactar si puedes.</p></div>
  </div>
</div></section>

<section class="section"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Señales de alerta</p><h2>Cambios que debes reportar.</h2><p class="lead">No todos los cambios son cáncer, pero cualquiera de estos merece una visita al médico.</p></div></div>
  <div class="signs">
    {"".join(f'<div class="sign reveal">{sign_icon(k)}<p>{t}</p></div>' for t, k in signs)}
  </div>
  <div class="notice reveal" style="margin-top:28px">{{{{i:info}}}}<p>Esta información es educativa y no sustituye el consejo de un profesional de la salud. Si notas algún cambio, comunícate con tu médico. ¿No tienes plan médico? <a href="ayuda.html">Busca servicios libre de costo</a>.</p></div>
</div></section>

<section class="section section--rosa"><div class="wrap two">
  <div class="reveal"><p class="kicker">Factores de riesgo</p><h2>Lo que aumenta el riesgo.</h2><p class="lead">Tener un factor de riesgo no significa que vas a desarrollar cáncer de seno. Y muchas personas diagnosticadas no tienen factores conocidos.</p></div>
  <ul class="list-check reveal reveal-d1">
    <li>Ser mujer y aumentar en edad</li>
    <li>Historial familiar de cáncer de seno u ovario</li>
    <li>Mutaciones genéticas heredadas, como BRCA1 y BRCA2</li>
    <li>Tejido mamario denso</li>
    <li>Historial personal de cáncer de seno o ciertas condiciones benignas</li>
    <li>Radioterapia en el pecho a edad temprana</li>
    <li>Sobrepeso después de la menopausia, poca actividad física y consumo de alcohol</li>
  </ul>
</div></section>

<section class="section"><div class="wrap two">
  <div class="reveal"><p class="kicker">Preguntas a tu médico</p><h2>Llega preparada a tu cita.</h2><p class="lead">Lleva estas preguntas escritas y, si puedes, a alguien de confianza que tome notas.</p>
    <div class="btn-row" style="margin-top:24px"><a class="btn btn--dark" href="ayuda.html">Busca servicios {{{{i:arrow}}}}</a></div></div>
  <div class="faq reveal reveal-d1">
    <details><summary>¿Cuál es mi riesgo de cáncer de seno?</summary><div>Pregunta si tu historial familiar, tu edad o tu densidad mamaria cambian tu riesgo, y si debes considerar consejería genética.</div></details>
    <details><summary>¿Qué pruebas de cernimiento me recomienda y cada cuánto?</summary><div>Pregunta a qué edad comenzar, con qué frecuencia y si necesitas pruebas adicionales como sonomamografía o MRI.</div></details>
    <details><summary>Noté un cambio. ¿Qué pasos siguen?</summary><div>Pregunta qué estudios diagnósticos necesitas, cuánto tiempo toman los resultados y a quién llamar si tienes dudas.</div></details>
    <details><summary>Si me diagnostican, ¿cuáles son mis opciones?</summary><div>Pregunta por el tipo y la etapa del cáncer, las opciones de tratamiento, sus efectos secundarios y si es recomendable una segunda opinión.</div></details>
    <details><summary>¿Dónde puedo conseguir ayuda económica?</summary><div>Komen Puerto Rico financia organizaciones que ofrecen cernimiento, diagnóstico y asistencia en tratamiento sin costo. <a href="ayuda.html">Busca por municipio</a>.</div></details>
  </div>
</div></section>
'''
page("cancer-de-seno.html", "El cáncer de seno", "Autoconocimiento, señales de alerta, factores de riesgo y preguntas para tu médico sobre el cáncer de seno.", edu)

# =====================================================================
# AYUDA (servicios + organizaciones)
# =====================================================================
servicios = json.load(open(os.path.join(ROOT, "data", "servicios.json"), encoding="utf-8"))
with open(os.path.join(ROOT, "data", "servicios.js"), "w", encoding="utf-8") as f:
    f.write("window.KOMEN_SERVICIOS = " + json.dumps(servicios, ensure_ascii=False) + ";\n")
cats = ["Cernimiento y Diagnóstico", "Asistencia en Tratamiento", "Programas de Apoyo"]
tabs = "".join(f'<button class="tab" role="tab" data-cat="{c}" aria-selected="{"true" if i == 0 else "false"}">{c}<small></small></button>' for i, c in enumerate(cats))

ayuda = f'''
<section class="phero"><div class="wrap">
  {{{{rings:}}}}
  <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a> / <span>Busca ayuda</span></nav>
  <p class="kicker">Programas de ayuda 2026</p><h1>Ayuda cerca de ti, sin costo.</h1>
  <p class="lead">Organizaciones aliadas ofrecen mamografías, diagnóstico, asistencia para tratamiento y apoyo, financiados por Komen Puerto Rico. Escoge tu municipio para ver quién te puede atender.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap finder" id="finder">
  <aside class="finder__panel">
    <label for="municipio">Tu municipio</label>
    <select id="municipio" class="select"><option value="">Todos los municipios</option></select>
    <div class="tabs" role="tablist" aria-label="Tipo de servicio">{tabs}</div>
    <p class="muted" style="font-size:14px;margin:20px 0 0">¿Dudas? Llámanos al <a href="tel:+17877519096">787-751-9096</a>.</p>
  </aside>
  <div><p class="results__count" id="results-count" aria-live="polite"></p><div class="results" id="results"></div></div>
</div></section>

<section class="section section--rosa"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Cómo funciona</p><h2>Tres pasos.</h2></div></div>
  <div class="steps">
    <div class="step reveal"><h3>Busca tu municipio</h3><p>Filtra la lista para ver las organizaciones que sirven en tu área.</p></div>
    <div class="step reveal reveal-d1"><h3>Comunícate directamente</h3><p>Llama o escribe al contacto de la organización. Ellos coordinan tu cita y evalúan tu elegibilidad.</p></div>
    <div class="step reveal reveal-d2"><h3>Recibe el servicio</h3><p>Los servicios financiados son libres de costo y algunos incluyen transportación.</p></div>
  </div>
</div></section>

<section class="section" id="organizaciones"><div class="wrap two">
  <div class="reveal"><p class="kicker">Para organizaciones</p><h2>¿Tu organización quiere solicitar fondos?</h2>
    <p class="lead">A través del Programa de Ayudas, otorgamos fondos a organizaciones sin fines de lucro con propuestas enfocadas en la salud del seno y el cáncer de seno.</p>
    <div class="btn-row" style="margin-top:24px"><a class="btn" href="https://komenpr.org/como-solicitar-servicios/" target="_blank" rel="noopener">Guía de solicitud {{{{i:arrow}}}}</a><a class="btn btn--ghost" href="contacto.html">Escríbenos</a></div></div>
  <div class="reveal reveal-d1"><h3>Elegibilidad</h3>
    <ul class="list-check">
      <li>Ser una organización sin fines de lucro establecida en Puerto Rico y registrada en el Departamento de Estado.</li>
      <li>Se recomienda estar registrada como Organización Sin Fines de Lucro en el Departamento de Hacienda.</li>
      <li>Tener capacidad de cumplir con los seguros requeridos por Susan G. Komen, o incluirlos en el presupuesto.</li>
      <li>Divulgar cualquier relación directa o indirecta de coordinadores y colaboradores con la organización.</li>
    </ul></div>
</div></section>
'''
page("ayuda.html", "Busca ayuda", "Encuentra mamografías, diagnóstico, asistencia para tratamiento y grupos de apoyo libres de costo en tu municipio, financiados por Susan G. Komen Puerto Rico.", ayuda, scripts='<script src="data/servicios.js"></script>\n')

# =====================================================================
# SOBREVIVIENTES
# =====================================================================
sobrev = f'''
<section class="phero phero--img">
  <div class="phero__bg"><img src="img/photos/race-valiente.jpg" alt=""></div>
  <div class="wrap"><nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a> / <span>Sobrevivientes</span></nav>
  <p class="kicker">Sobrevivientes</p><h1>No estás sola en este camino.</h1>
  <p class="lead">El cáncer de seno es un proceso de muchas etapas. No importa dónde te encuentres, podemos ofrecerte recursos educativos y asistencia económica.</p></div>
</section>

<section class="section"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Tu etapa</p><h2>Apoyo para cada momento.</h2></div></div>
  <div class="cards">
    <div class="card reveal"><div class="card__body"><span class="path__icon">{{{{i:info}}}}</span><h3>Recién diagnosticada</h3><p>Respira. Pide tu diagnóstico por escrito, lleva a alguien a tus citas, haz todas las preguntas y considera una segunda opinión.</p><a class="link-arrow" href="cancer-de-seno.html">Preguntas para tu médico {{{{i:arrow}}}}</a></div></div>
    <div class="card reveal reveal-d1"><div class="card__body"><span class="path__icon">{{{{i:stetho}}}}</span><h3>En tratamiento</h3><p>Hay asistencia para quimioterapia, radioterapia, medicamentos, transportación y gorros hipotérmicos a través de organizaciones aliadas.</p><a class="link-arrow" href="ayuda.html">Asistencia en tratamiento {{{{i:arrow}}}}</a></div></div>
    <div class="card reveal reveal-d2"><div class="card__body"><span class="path__icon">{{{{i:shield}}}}</span><h3>Sobrevivencia</h3><p>Después del tratamiento, un plan de cuidado te ayuda a organizar tus citas de seguimiento y tu bienestar.</p><a class="link-arrow" href="{{{{PLAN_CUIDADO}}}}" target="_blank" rel="noopener">Plan de cuidado (PDF) {{{{i:arrow}}}}</a></div></div>
    <div class="card reveal"><div class="card__body"><span class="path__icon">{{{{i:users}}}}</span><h3>Co-sobrevivientes</h3><p>Familiares y amistades también necesitan apoyo. Hay grupos y programas pensados para quienes acompañan.</p><a class="link-arrow" href="ayuda.html">Programas de apoyo {{{{i:arrow}}}}</a></div></div>
    <div class="card reveal reveal-d1"><div class="card__body"><span class="path__icon">{{{{i:hands}}}}</span><h3>Linfedema</h3><p>Si notas hinchazón, pesadez o tirantez en el brazo, la mano o el pecho después de tu cirugía o radiación, díselo a tu médico pronto.</p><a class="link-arrow" href="https://komenpr.org/sobrevivientes/linfedema/" target="_blank" rel="noopener">Saber más {{{{i:arrow}}}}</a></div></div>
    <div class="card reveal reveal-d2" style="background:var(--accion);border-color:var(--accion);color:#fff"><div class="card__body"><span class="path__icon" style="background:#fff">{{{{i:ribbon}}}}</span><h3 style="color:#fff">Regístrate como sobreviviente</h3><p style="color:rgba(255,255,255,.9)">Únete al registro para recibir invitaciones especiales al Race for the Cure y otras actividades.</p><a class="link-arrow" style="color:#fff" href="{{{{REGISTRO}}}}" target="_blank" rel="noopener">Registro {{{{i:arrow}}}}</a></div></div>
  </div>
</div></section>

<section class="section section--rosa"><div class="wrap quote">
  <div class="quote__img reveal"><img src="img/photos/r25-emocion.jpg" alt="Sobreviviente emocionada en el Race for the Cure 2025" loading="lazy"></div>
  <div class="reveal reveal-d1"><p class="kicker">Galería de sobrevivientes</p>
    <blockquote>Más que una carrera, celebramos la vida y reconocemos a quienes han enfrentado esta enfermedad con valentía.</blockquote>
    <p class="lead">Conoce las historias de sobrevivientes y co-sobrevivientes de nuestra comunidad.</p>
    <div class="btn-row"><a class="btn btn--dark" href="https://komenpr.org/galeria-de-sobrevivientes/" target="_blank" rel="noopener">Ver historias {{{{i:arrow}}}}</a></div></div>
</div></section>
'''
page("sobrevivientes.html", "Sobrevivientes", "Recursos para sobrevivientes de cáncer de seno y co-sobrevivientes en Puerto Rico: diagnóstico, tratamiento, linfedema y plan de cuidado.", sobrev)

# =====================================================================
# EVENTOS
# =====================================================================
gala_gallery = gallery([
  ("gala26-pareja", "Invitados en la Pink Gala 2026"),
  ("gala-coral", "Invitada en vestido coral"),
  ("gala-entrada", "Entrada de la Pink Gala"),
  ("gala-perlas", "Arreglo floral con perlas"),
  ("gala26-rosa", "Invitada de rosa en la alfombra"),
  ("gala-salon", "Salón de la Pink Gala"),
  ("gala-saludo", "Invitados saludándose en la gala"),
  ("gala26-dupla", "Pareja en la alfombra de Las Mil y Una Noches"),
  ("gala-duo", "Dos invitadas en la Pink Gala"),
], ["m-a", "m-b", "m-c", "m-e", "m-e", "m-d", "m-f", "m-e", "m-e"])

race_gallery = gallery([
  ("r25-celebracion", "Sobrevivientes de 6 a 10 años celebrando con corazones rosados"),
  ("r25-abrazo", "Participantes abrazándose emocionadas en el Race 2025"),
  ("r25-alas", "Sobreviviente con alas rosadas y su cartel"),
  ("r25-tambores", "Músicos con tambores animando la carrera"),
  ("r25-emocion", "Sobreviviente emocionada recibiendo apoyo"),
  ("race-sobrevivientes", "Sobrevivientes con carteles de “Soy valiente” bajando del Coliseo"),
  ("r25-meta", "Participantes celebrando en el recorrido"),
  ("race-familia", "Madre e hijo corriendo juntos"),
  ("r25-arco", "Grupo celebrando bajo el arco de caminantes"),
], ["m-a", "m-b", "m-c", "m-e", "m-e", "m-d", "m-f", "m-e", "m-e"])

eventos = f'''
<section class="phero phero--img">
  <div class="phero__bg"><img src="img/photos/r25-aerea.jpg" alt=""></div>
  <div class="wrap"><nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a> / <span>Eventos</span></nav>
  <p class="kicker">Eventos</p><h1>Juntas, en cada paso.</h1>
  <p class="lead">Nuestros eventos recaudan fondos para programas en la Isla y, sobre todo, celebran a las sobrevivientes.</p></div>
</section>

<section class="section section--negro" id="race"><div class="wrap two two--center">
  <div class="reveal"><p class="kicker">Race for the Cure®</p><h2>El 5K más grande de Puerto Rico.</h2>
    <p class="lead">Más que una carrera competitiva, es un evento donde se celebra la vida. Cada participante corre o camina “En honor a” un ser querido que lucha contra la enfermedad, o “En memoria de” alguien que terminó su batalla.</p>
    <ul class="list-check" style="margin:28px 0">
      <li>2026: domingo 4 de octubre, Coliseo de Puerto Rico José Miguel Agrelot</li>
      <li>Lema 2026: “En cada paso, juntos por ti”</li>
      <li>Madrina 2026: la periodista Aixa Vázquez</li>
    </ul>
    <div class="btn-row"><a class="btn" href="{{{{RESULTADOS}}}}" target="_blank" rel="noopener">Resultados {{{{i:arrow}}}}</a><a class="btn btn--ghost-white" href="https://komenpr.org/race-for-the-cure-2021/salon-de-la-fama/" target="_blank" rel="noopener">Salón de la Fama</a></div>
  </div>
  <div class="reveal reveal-d1" style="position:relative;aspect-ratio:1/1;border-radius:28px;overflow:hidden">
    <img src="img/photos/r25-multitud.jpg" alt="Sobrevivientes celebrando en el Coliseo de Puerto Rico" loading="lazy" style="width:100%;height:100%;object-fit:cover">
    <span class="chip chip--dark" style="position:absolute;left:18px;bottom:18px">{{{{i:calendar}}}}Race 2027 · Fecha por anunciar</span>
  </div>
</div>
<div class="wrap" style="margin-top:clamp(56px,7vw,96px)">
  <div class="reveal">{race_gallery}</div>
  <p class="photo-credit">Fotos: Race for the Cure 2025 (Susan G. Komen Puerto Rico) y ediciones anteriores (Alberto Bartolomei).</p>
</div></section>

<section class="section" id="pinkday"><div class="wrap two two--center">
  <div class="stack-imgs reveal">
    <div class="img-round"><img src="img/photos/pinkday-grupo-2.jpg" alt="Empleados de Deco Centro en el Pink Day" loading="lazy"></div>
    <div class="img-round"><img src="img/photos/pinkday-amigas.jpg" alt="Participantes del Pink Day" loading="lazy"></div>
    <div class="img-round"><img src="img/photos/lazo-humano.jpg" alt="Empleados formando un lazo rosado humano" loading="lazy"></div>
  </div>
  <div class="reveal reveal-d1"><p class="kicker">Pink Day</p><h2>Un día. Toda la Isla de rosa.</h2>
    <p class="lead">Empresas, agencias de gobierno, escuelas y grupos se visten con la camiseta oficial del Pink Day para crear conciencia y recaudar fondos. “Cada día es una nueva oportunidad.”</p>
    <ul class="list-check" style="margin:28px 0">
      <li>Ordena las camisetas oficiales para tu equipo</li>
      <li>Coordina una charla educativa en tu lugar de trabajo</li>
      <li>Comparte tu foto y etiqueta a @komenpr</li>
    </ul>
    <div class="btn-row"><a class="btn" href="{{{{PINKDAY_SHOP}}}}" target="_blank" rel="noopener">Tienda Pink Day {{{{i:arrow}}}}</a><a class="btn btn--ghost" href="mailto:pinkday@komenpr.org">pinkday@komenpr.org</a></div>
  </div>
</div></section>

<section class="section section--rosa" id="gala"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Pink Gala</p><h2>Una noche para recordar.</h2><p class="lead">Desde “The Secret Garden” (2024) y “Pearls of Hope” (2025) hasta “Las Mil y Una Noches” (2026), la Pink Gala reúne a la comunidad en nuestra noche más elegante del año.</p></div>
  <a class="link-arrow" href="https://komenpr.org/pink-gala/" target="_blank" rel="noopener">Boletos y detalles {{{{i:arrow}}}}</a></div>
  <div class="reveal">{gala_gallery}</div>
</div></section>
'''
page("eventos.html", "Eventos", "Race for the Cure, Pink Day y Pink Gala: los eventos de Susan G. Komen Puerto Rico que celebran a las sobrevivientes y recaudan fondos para la Isla.", eventos)

# =====================================================================
# INVOLÚCRATE (donar + voluntarios + banderas)
# =====================================================================
inv = f'''
<section class="phero phero--img">
  <div class="phero__bg"><img src="img/photos/pinkday-guardia.jpg" alt=""></div>
  <div class="wrap"><nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a> / <span>Involúcrate</span></nav>
  <p class="kicker">Involúcrate</p><h1>Tu apoyo nos mueve.</h1>
  <p class="lead">Dona, sé voluntario o lleva a tu empresa. Cada forma de ayudar cuenta y se queda en Puerto Rico.</p></div>
</section>

<section class="section" id="donar"><div class="wrap">
  <div class="donate reveal">
    <div class="donate__img"><img src="img/photos/race-2019-a.jpg" alt="Participantes del Race for the Cure" loading="lazy"></div>
    <div class="donate__body"><p class="kicker">Dona</p><h2>Haz tu donación.</h2>
      <p class="muted">Escoge una cantidad para ver qué ayuda a financiar. Completarás tu donación de forma segura en PayPal.</p>
      <div class="amounts" role="group" aria-label="Cantidad sugerida">
        <button class="amount" aria-pressed="false" data-impact="<b>$25</b> ayudan a llevar materiales educativos a una charla comunitaria.">$25</button>
        <button class="amount" aria-pressed="true" data-impact="<b>$50</b> ayudan a cubrir la transportación de una paciente a sus citas.">$50</button>
        <button class="amount" aria-pressed="false" data-impact="<b>$100</b> ayudan a financiar una mamografía para alguien sin plan médico.">$100</button>
        <button class="amount" aria-pressed="false" data-impact="<b>$250</b> ayudan a cubrir pruebas diagnósticas como una sonomamografía.">$250</button>
      </div>
      <p class="impact-line"><b>$50</b> ayudan a cubrir la transportación de una paciente a sus citas.</p>
      <div class="btn-row"><a class="btn" href="{{{{DONAR}}}}" target="_blank" rel="noopener">{{{{i:heart}}}}Donar con PayPal</a><a class="btn btn--ghost" href="{{{{TIENDA}}}}" target="_blank" rel="noopener">{{{{i:bag}}}}Tienda online</a></div>
      <p class="muted" style="font-size:13px;margin-top:16px">El 100% de los fondos apoya programas en Puerto Rico.</p>
    </div>
  </div>
</div></section>

<section class="section section--negro" id="voluntarios"><div class="wrap">
  <div class="shead reveal"><div><p class="kicker">Voluntarios</p><h2>Bienvenido a la familia Komen.</h2><p class="lead">Tenemos muchas oportunidades para que aportes tus destrezas. Es una gran experiencia personal y profesional.</p></div>
  <a class="btn" href="mailto:pinkday@komenpr.org?subject=Quiero%20ser%20voluntario">Quiero ser voluntario {{{{i:arrow}}}}</a></div>
  <div class="pillars" style="grid-template-columns:repeat(3,1fr)">
    <div class="pillar reveal"><h3>Programa de Educación</h3><p>Komen te certifica para representar a la organización en actividades educativas sobre detección temprana.</p></div>
    <div class="pillar reveal reveal-d1"><h3>Programa de Ayudas</h3><p>Sé recurso activo en las actividades educativas de los proyectos de impacto comunitario.</p></div>
    <div class="pillar reveal reveal-d2"><h3>Race for the Cure®</h3><p>Ayuda en inscripción, logística, hidratación y la celebración de sobrevivientes en el 5K más grande de PR.</p></div>
  </div>
</div></section>

<section class="section" id="banderas"><div class="wrap two two--center">
  <div class="reveal"><p class="kicker">Programa Banderas</p><h2>Lleva a tu empresa.</h2>
    <p class="lead">Creamos alianzas con corporaciones privadas, agencias de gobierno e instituciones educativas para llevar recursos educativos a sus empleados y comunidades.</p>
    <div class="btn-row" style="margin-top:24px"><a class="btn btn--dark" href="contacto.html">Hablemos {{{{i:arrow}}}}</a><a class="btn btn--ghost" href="eventos.html#pinkday">Pink Day para empresas</a></div></div>
  <div class="img-round reveal reveal-d1" style="aspect-ratio:4/3"><img src="img/photos/pinkday-equipo.jpg" alt="Equipo de trabajo con camisetas del Pink Day" loading="lazy"></div>
</div></section>
'''
page("involucrate.html", "Involúcrate", "Dona, hazte voluntario o une a tu empresa a Susan G. Komen Puerto Rico. El 100% de los fondos se queda en la Isla.", inv)

# =====================================================================
# CONTACTO
# =====================================================================
contacto = f'''
<section class="phero"><div class="wrap">
  {{{{rings:}}}}
  <nav class="crumbs" aria-label="Ruta"><a href="index.html">Inicio</a> / <span>Contacto</span></nav>
  <p class="kicker">Contáctanos</p><h1>Estamos para ti.</h1>
  <p class="lead">Escríbenos o llámanos. Te orientamos sobre servicios, eventos, voluntariado y alianzas.</p>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap contact-grid">
  <div class="info-list reveal">
    <a class="info" href="tel:+17877519096"><span class="info__ico">{{{{i:phone}}}}</span><div><b>Teléfono</b><span>787-751-9096</span></div></a>
    <a class="info" href="mailto:info@komenpr.org"><span class="info__ico">{{{{i:mail}}}}</span><div><b>Email</b><span>info@komenpr.org</span></div></a>
    <div class="info"><span class="info__ico">{{{{i:pin}}}}</span><div><b>Dirección física</b><span>27 Ave. González Giusti, Piso 4, Oficina 403<br>Guaynabo, PR 00968</span></div></div>
    <div class="info"><span class="info__ico">{{{{i:mail}}}}</span><div><b>Dirección postal</b><span>PO Box 193557<br>San Juan, PR 00919-3557</span></div></div>
  </div>
  <form class="form reveal reveal-d1" action="mailto:info@komenpr.org" method="post" enctype="text/plain">
    <h3 style="margin:0">Envíanos un mensaje</h3>
    <div class="row">
      <div class="field"><label for="c-nombre">Nombre</label><input id="c-nombre" name="nombre" required autocomplete="name"></div>
      <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" required autocomplete="email"></div>
    </div>
    <div class="row">
      <div class="field"><label for="c-tel">Teléfono</label><input id="c-tel" name="telefono" type="tel" autocomplete="tel"></div>
      <div class="field"><label for="c-tema">Tema</label><select id="c-tema" name="tema"><option>Necesito servicios</option><option>Voluntariado</option><option>Pink Day / Empresas</option><option>Race for the Cure</option><option>Donaciones</option><option>Otro</option></select></div>
    </div>
    <div class="field"><label for="c-msg">Mensaje</label><textarea id="c-msg" name="mensaje" required></textarea></div>
    <button class="btn" type="submit">Enviar mensaje {{{{i:arrow}}}}</button>
  </form>
</div></section>

<section class="section section--tight" style="padding-top:0"><div class="wrap">
  <div class="map reveal"><iframe title="Mapa: oficina de Susan G. Komen Puerto Rico" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=27+Ave+Gonzalez+Giusti,+Guaynabo,+PR+00968&output=embed"></iframe></div>
</div></section>
'''
page("contacto.html", "Contacto", "Contacta a Susan G. Komen Puerto Rico: 787-751-9096, info@komenpr.org, 27 Ave. González Giusti, Guaynabo.", contacto)
