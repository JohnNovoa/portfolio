# Portafolio web de John Novoa

Sitio estático del portafolio de John Novoa, Senior Mechanical Engineer en Colombia. Sirve para postularse a cargos de diseño mecánico, sobre todo remotos con empresas extranjeras. El público son reclutadores e ingenieros que lo revisan en pocos minutos, muchas veces desde el celular.

- Repositorio: https://github.com/JohnNovoa/portfolio (público)
- Web: https://johnnovoa.github.io/portfolio/ (GitHub Pages, rama `main`, carpeta raíz)
- Fuente del contenido: el portafolio de Notion de John, exportado en Markdown en `../Notion_Portfolio/`
- Idioma del sitio: inglés. Con John se habla en español.

## Estructura

```
index.html              Portada: hero, Selected work (4 destacados), More projects, About, contacto
projects/<slug>.html    Un caso de estudio por proyecto
assets/css/site.css     Todo el diseño (editar a mano)
assets/js/site.js       Lightbox de imágenes y botón "Copy email" (editar a mano)
assets/fonts/           Archivo variable (licencia OFL)
assets/img/             Imágenes WebP generadas por el script (no editar a mano)
assets/favicon.svg
tools/build_site.py     Genera index.html, projects/*.html y assets/img/ desde el export de Notion
404.html, README.md, .nojekyll
```

Sin frameworks, sin npm, sin paso de compilación para el visitante. Rutas relativas en todo el sitio, salvo `404.html`, que usa rutas absolutas `/portfolio/...` porque GitHub Pages la sirve desde cualquier URL.

## Cómo se actualiza

El HTML es generado. Los cambios de contenido van por el script, no a mano en el HTML, porque la próxima generación los borra.

1. John actualiza Notion y exporta (··· > Export > Markdown & CSV, con subpáginas). Descomprime el export en `../Notion_Portfolio/`, reemplazando el anterior.
2. Desde la raíz del repo: `.venv/Scripts/python tools/build_site.py` (o `--export "ruta"` si el export está en otro lugar). Requiere Python 3.9+ y Pillow.
   - El entorno virtual `.venv/` vive en la raíz del repo (ignorado por git) y ya tiene Pillow. Si no existe: `python -m venv .venv` y `.venv/Scripts/python -m pip install -r tools/requirements.txt`.
   - Windows necesita rutas largas activadas (`LongPathsEnabled = 1`). Algunas imágenes del export superan los 260 caracteres de ruta. Sin eso, el Explorador no las extrae del zip y el script falla con `FileNotFoundError`.
   - Tras descomprimir, comprobar que no falte nada: el zip y la carpeta deben tener el mismo número de archivos.
3. El script borra y regenera `projects/` y `assets/img/`, y reescribe `index.html`. No toca CSS, JS, fuentes, 404, README ni este archivo.
4. Revisa el resultado en el navegador (abre `index.html`) en escritorio y en móvil (390 px de ancho).

Qué vive dentro de `tools/build_site.py` y no en Notion:
- Experiencia, educación, certificaciones y herramientas de la sección About (listas `experience`, `education`, `certifications`, `skills`).
- Las tres imágenes del hero (Design, Build, Validate) y sus textos.
- El texto del hero, de los encabezados de sección y del bloque de contacto.
- Cuáles proyectos salen destacados: los 4 primeros con imagen según la propiedad Order de Notion.
- Corrección de typos de Notion (`TYPO_FIXES`).

Los textos de cada proyecto (descripción, viñetas, pies de foto) salen de Notion. Si John quiere cambiar uno, lo ideal es cambiarlo en Notion y regenerar. Si es urgente, edita el script o el HTML y avísale que Notion queda desactualizado.

## Diseño

- Paleta: azul marino `#0E1B2E` (hero, encabezados de proyecto, nav), tinta `#14243B`, gris claro `#F2F4F6`, blanco, amarillo de seguridad `#FFC72C` como único acento.
- Tipografía: Archivo variable en todo el sitio. El ancho (`font-stretch`) da el carácter: nombres y títulos expandidos (110 a 125 %).
- Fondo del hero con cuadrícula fina tipo papel de dibujo.
- Imágenes de render sobre placas blancas con `object-fit: contain`. Fotos reales con `cover` (el script detecta fotos por las esquinas).
- Una sola animación de entrada en el hero. Respeta `prefers-reduced-motion`. Hover discreto en tarjetas.
- Responsive: cortes en 1000 px y 680 px. Probar siempre a 1440, 1024, 768 y 390 px.
- Accesibilidad: foco visible, textos alternativos (los pies de foto), contraste AA, enlace "Skip to content".

## Reglas de contenido (obligatorias)

Vienen de los acuerdos con John para el portafolio. No se rompen aunque la imagen o el texto estén en Notion.

- Proyectos en términos generales: tipo de producto, rol de John, procesos y resultado. Sin nombres internos de proyectos (R-Dog, R2-A, R-Kiwi, R-Top).
- Materiales generales permitidos (aluminum, PETG). Sin dimensiones ni valores de especificación.
- Sin nombres de proveedores, clientes ni marcas de componentes. Se mantienen las marcas de los empleadores que aparecen en los robots o en los planos.
- Fotos sin personas, pantallas ni marcas no públicas. QR y números de robot pixelados.
- Toda imagen lleva pie de foto corto en inglés.
- Sin teléfono en la web. Contacto: email (johnenovoap@gmail.com) y LinkedIn.
- No mencionar ningún emprendimiento propio de John.
- No inventar experiencia, cifras, herramientas, certificaciones ni fechas. Si falta un dato, preguntar a John.
- Nada en el sitio que anuncie búsqueda de empleo ("open to work", "available for hire").

## Reglas de escritura (texto nuevo en inglés)

- Frases claras y cortas, voz activa, verbos concretos (designed, built, tested, cut).
- Sin guiones largos (em dash) ni guiones medios (en dash). Sin punto y coma. Rangos de años con guion normal: `2024-2025`.
- Sin metáforas, frases inspiracionales ni adjetivos de relleno sobre John.
- Palabras prohibidas: passionate, results-driven, dynamic, self-starter, synergy, leverage, spearheaded, cutting-edge, innovative, robust, seamless, delve, utilize, harness, unlock, game-changer, proven track record, team player, Furthermore, Moreover.
- Revisar todo texto nuevo con la skill humanizer si está disponible.

## Publicación y git

- Nunca hacer `git push`, cambiar la configuración de GitHub Pages ni publicar nada sin un "sí" explícito de John para esa acción concreta.
- Commits pequeños, con mensaje en inglés que diga qué cambió.
- No subir el export de Notion ni imágenes originales sin procesar al repo. Solo lo que genera el script.
- `.gitignore` excluye `.venv/`, cachés de Python y archivos del sistema.

## Estado al 22 nov 2026

- Sitio publicado en https://johnnovoa.github.io/portfolio/ (GitHub Pages desde `main`, carpeta raíz, activado el 22 nov 2026). Portada, las 11 páginas de proyecto y la 404 verificadas en línea, sin enlaces ni imágenes rotas. Falta que John lo revise visualmente en el celular.
- El script escribe el HTML con finales de línea LF, así que regenerar con el mismo export no deja diff.
- Rutas largas activadas en Windows. El export en `../Notion_Portfolio/` está completo (103 archivos, igual que `../n.zip`) y regenerar el sitio con él no deja diff.
- Pendiente en Notion (avisar a John, no se arregla aquí): el typo "Industrial desing concept" en Humanoid Service Robot y Mobile Humanoid Robot. El sitio ya lo corrige con `TYPO_FIXES`.
- SOLIDWORKS Automation Tools está en pausa: John está convirtiendo las herramientas en plantillas genéricas. Hoy sale la versión corta, sin imágenes. Cuando John tenga capturas de la versión genérica, se rehace esa página.
- Robot.com figura como "2026 - Present" por decisión de John.
