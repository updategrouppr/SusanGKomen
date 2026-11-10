# Komen PR — rediseño del sitio

Sitio estático (HTML + CSS + JS, sin dependencias) basado en el brand board "Propuesta 01".

## Páginas
index · nosotros · cancer-de-seno · ayuda (buscador por municipio) · sobrevivientes · eventos · involucrate · contacto

## Cómo editar
- Textos y estructura: `build.py` (cada página es un bloque). Después de editar: `python3 build.py`
- Estilos: `assets/css/styles.css` (colores en `:root`)
- Interacciones: `assets/js/main.js`
- Servicios del Programa de Ayudas: `data/servicios.json` → `python3 build.py` regenera `data/servicios.js`
- Fotos usadas: `img/photos/` (1600px). Originales de Facebook en `img/_originales/` (no se publican).

## Ver en local
python3 -m http.server 8765   →   http://localhost:8765

## Pendiente antes de publicar
- Conectar el formulario del boletín (Mailchimp u otro) y el de contacto (hoy usa mailto).

## Confirmado
- Ejemplos de impacto por donación ($25/$50/$100/$250), cifra de 206 proyectos y permiso de fotos (Alberto Bartolomei).
- Logo oficial en alta resolución (`img/_originales/logo-oficial-blanco.webp`). Versiones del sitio: `img/site/logo-dark.png` (fondos claros) y `logo-light.png` (fondos oscuros).
- Fotos del Race: principales del post de Komen del 6 oct 2025 (Race 2025); el resto de la biblioteca del sitio actual (2016–2019, 2023). No se usan fotos de 2026 de otras organizaciones.
