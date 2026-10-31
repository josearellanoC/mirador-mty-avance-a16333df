# Mirador MTY – sitio de avance (estático)

Archivos: `index.html` (generado), `img/` (logo, `t_<id>.jpg` 400 px, `f_<id>.jpg` 1600 px q82, EXIF corregido),
`data.json` (fuente), `template.html`, `build.py`.

## Actualizar cuando llega un reporte nuevo
1. Edita `data.json`:
   - `corte`: fecha del último reporte.
   - `avance`: por lote, `{ "<hito>": % }` con la columna "Avance por hito (% real)" del último reporte de cada lote
     (Sheet 1N2DFznpk1UK74FtAjtvz-xcBwvLLbLD0fLkRxgRGCV8). `null` = lote sin reportes (sale en 0 con nota).
   - `fotos`: por lote, lista `[drive_id, actividad, fecha]`, más reciente primero. Solo datos para cliente
     (sin nombres, cuadrillas, problemas ni costos).
2. Asegura que exista el original en `/workspace/nas_backup/src/<id>` o `/workspace/inf5/h_<id>.jpg`.
3. `python3 build.py` (solo procesa fotos nuevas).
4. Publicar (ver abajo).

## Publicar
Pendiente: el box no tiene ningún host autenticado (`gh` sin login; el conector GitHub no puede crear repos ni subir archivos).
Con `gh auth login` hecho por Jose, una vez:
    cd /workspace/mirador_site && git init -b main && git add . && git commit -m sitio
    gh repo create mirador-mty-avance-<random> --public --source . --push
    gh api -X POST repos/{owner}/mirador-mty-avance-<random>/pages -f 'source[branch]=main' -f 'source[path]=/'
Después de cada rebuild: `git add -A && git commit -m "reporte <fecha>" && git push`
