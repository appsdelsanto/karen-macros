# karen-macros

App (PWA) para contar calorías y macros (proteína, carbohidratos y grasa) desde el iPhone.

- **Página:** https://appsdelsanto.github.io/karen-macros/
- **Instalar en el iPhone:** abrir la página en Safari → botón Compartir → "Agregar a pantalla de inicio".

## Qué hace (versión 1)

- Resumen del día: calorías que quedan y barras de proteína, carbohidratos y grasa.
- Comidas: desayuno, comida, cena y colaciones; tocar un alimento para cambiar cantidad o borrarlo.
- Lista de ~80 alimentos comunes (incluye comida mexicana) con valores aproximados por porción, buscador sin acentos y frecuentes.
- Alimentos propios (datos de la etiqueta); si no se ponen calorías, se calculan con 4·4·9.
- Metas del día, "Repetir ayer" y respaldo (guardar/recuperar archivo).
- Funciona sin internet.

## Datos

Todo se guarda solo en el teléfono (localStorage). Nada se sube a GitHub; el repositorio es público pero solo tiene el código. Si se borra la app del iPhone se borran los datos, por eso existe el respaldo.

## Archivos

- `index.html`: toda la app.
- `sw.js`: modo sin internet (primero internet, si no hay, copia guardada).
- `manifest.json` e `icon-*.png`: instalación. Los íconos se generan con `herramientas/iconos.py`.
