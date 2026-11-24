# Portafolio web de John Novoa

Sitio estático del portafolio de John Novoa, Senior Mechanical Engineer en Colombia. Sirve para postularse a cargos de diseño mecánico, sobre todo remotos con empresas extranjeras. El público son reclutadores e ingenieros que lo revisan en pocos minutos, muchas veces desde el celular.

- Repositorio: https://github.com/JohnNovoa/portfolio (público)
- Web: https://johnnovoa.github.io/portfolio/ (GitHub Pages, rama `main`, carpeta raíz)
- Fuente original: el portafolio de Notion de John (export en `../Notion_Portfolio/`). Desde el 23 nov 2026 el sitio es independiente de Notion: no hay que mantenerlos iguales y el sitio ya no se genera desde el export.
- Idioma del sitio: inglés. Con John se habla en español.

## Estructura

```
index.html              Portada: hero, Selected work (4 destacados), More projects, About, contacto
projects/<slug>.html    Un caso de estudio por proyecto
assets/css/site.css     Todo el diseño
assets/js/site.js       Lightbox de imágenes y botón "Copy email"
assets/fonts/           Archivo variable (licencia OFL)
assets/img/             Imágenes WebP
assets/favicon.svg
tools/add_image.py      Convierte una imagen original en los WebP del sitio
404.html, README.md, .nojekyll
```

Sin frameworks, sin npm, sin paso de compilación para el visitante. Rutas relativas en todo el sitio, salvo `404.html`, que usa rutas absolutas `/portfolio/...` porque GitHub Pages la sirve desde cualquier URL.

## Cómo se actualiza

El HTML es la fuente: los cambios de texto se hacen directamente en `index.html` y `projects/*.html`. Si un dato se repite (por ejemplo, el nombre o el resumen de un proyecto aparece en la portada y en su página), cambiarlo en todos los sitios.

Imágenes nuevas:
1. Originales de John en `../R-Dog/`, `../R_2A/`, `../R-Kiwi_Pizza/`, `../Other/` y `../sin_marcas/`. Nunca subir originales al repo.
2. Antes de convertir, revisar la imagen con las reglas de contenido: recortar personas, pixelar QR y números de robot. Las ediciones se hacen en una copia en el scratchpad.
3. Desde la raíz del repo: `.venv/Scripts/python tools/add_image.py ORIGEN nombre-descriptivo`. Escribe `assets/img/nombre.webp` (hasta 1600 px) y `nombre-sm.webp` (hasta 760 px) e imprime los `width`/`height` para el `<img>`. Avisa si el original mide menos de 1200 px.
4. Actualizar todas las referencias (portada, página del proyecto, `og:image`) y borrar con `git rm` el WebP viejo si ya no se usa.
5. Revisar en el navegador en escritorio y en móvil (390 px de ancho).

El entorno virtual `.venv/` vive en la raíz del repo (ignorado por git) y tiene Pillow con soporte AVIF. Si no existe: `python -m venv .venv` y `.venv/Scripts/python -m pip install -r tools/requirements.txt`.

El generador antiguo desde Notion (`tools/build_site.py`) se retiró el 23 nov 2026. Sigue en el historial de git (commit `1ed29d8`) por si hiciera falta. No volver a usarlo: borraría los cambios hechos a mano.

## Diseño

- Paleta: azul marino `#0E1B2E` (hero, encabezados de proyecto, nav), tinta `#14243B`, gris claro `#F2F4F6`, blanco, amarillo de seguridad `#FFC72C` como único acento.
- Tipografía: Archivo variable en todo el sitio. El ancho (`font-stretch`) da el carácter: nombres y títulos expandidos (110 a 125 %).
- Fondo del hero con cuadrícula fina tipo papel de dibujo.
- Imágenes de render sobre placas blancas con `object-fit: contain`. Fotos reales con `cover` (clase `cover` en el contenedor).
- Una sola animación de entrada en el hero. Respeta `prefers-reduced-motion`. Hover discreto en tarjetas.
- Responsive: cortes en 1000 px y 680 px. Probar siempre a 1440, 1024, 768 y 390 px.
- Accesibilidad: foco visible, textos alternativos (los pies de foto), contraste AA, enlace "Skip to content". El aviso "Email copied" se anuncia a lectores de pantalla.
- El diseño actual es el definitivo (decisión de John, 23 nov 2026). Se probaron y descartaron otras fuentes (ISOCPEUR, osifont) y dos rediseños completos (estilo plano técnico con rótulo y estilo taller con foto grande). No proponer rediseños ni cambios de fuente salvo que John lo pida.
- Skills útiles instaladas en `~/.claude/skills`: `web-design-guidelines` (auditoría de HTML/CSS, se pasó el 23 nov 2026 y se corrigió todo salvo las mayúsculas de títulos) y `frontend-design`. Para texto nuevo en inglés, la skill `humanizer`.

## Reglas de contenido (obligatorias)

Vienen de los acuerdos con John para el portafolio. No se rompen aunque la imagen o el texto vengan de Notion o de los originales de John.

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
- No subir el export de Notion ni imágenes originales sin procesar al repo. Solo los WebP que genera `tools/add_image.py`.
- `.gitignore` excluye `.venv/`, cachés de Python y archivos del sistema.

## Estado al 23 nov 2026

- Sitio publicado en https://johnnovoa.github.io/portfolio/ (GitHub Pages desde `main`, carpeta raíz). John lo revisó en el celular y lo aprobó.
- Hechos el 23 nov 2026: sitio independiente de Notion, foto nueva y nítida del Quadruped (números de robot pixelados, la mano que toca el robot se dejó), About más corto, inglés como "B2, upper intermediate", resultados del Quadruped (2 prototipos) y del Mobile Humanoid (2 unidades) reescritos, y correcciones de la auditoría web.
- Contexto de los proyectos de robots (de John): todos fueron prototipos de pocas unidades, cada uno desarrollado en un mes de trabajo. El trabajo era convertir un concepto en algo real que cumpliera los requisitos estéticos y funcionales, con soportes, ensamble, materiales y procesos elegidos para que se pudiera fabricar y ensamblar. No era optimizar sino encontrar una solución eficaz. No hablar de moldes ni de SLA en los resultados.
- Robot.com figura como "2026 - Present" por decisión de John.

## Pendientes para la próxima sesión

1. CV en PDF. Plan acordado: subirlo como `assets/John-Novoa-CV.pdf` (no como enlace a Drive) y agregar un botón "Download CV" junto a "Email me" en la portada y en el bloque de contacto de todas las páginas. Para actualizarlo, se reemplaza el archivo con el mismo nombre y se hace push.
   Hecho el 23 nov 2026: `assets/John-Novoa-CV.pdf` con botón "Download CV". John decidió publicarlo con su teléfono (excepción a la regla de no poner el teléfono en la web). El Quadruped tuvo 2 prototipos (sitio y CV coinciden).
2. Mayúsculas de títulos: hecho el 23 nov 2026. Los títulos de sección van en sentence case ("Process & tools", "Impact & results"). Los nombres de proyecto siguen en Title Case.
3. Render más grande del Humanoid Robot Dual-Arm Redesign (primer destacado): el original mide 433x738 px y se ve suave en pantallas de alta resolución. John eligió dejar la imagen actual por ahora. El render de Gemini en `../R_2A/` NO se usa: cambia detalles del diseño respecto al CAD real.
4. SOLIDWORKS Automation Tools: en pausa hasta que John tenga capturas de la versión genérica de las herramientas.
5. Opcional, John dijo "por ahora no": dominio propio en lugar de github.io.
