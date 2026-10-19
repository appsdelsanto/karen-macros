"""Genera el PDF "Tu app de comida" para que Karen elija funciones.

Uso: python herramientas/pdf_funciones.py
Crea docs/funciones-karen.html y docs/funciones-karen.pdf (con Microsoft Edge).
"""
import html
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
DOCS = os.path.join(RAIZ, 'docs')
EDGE = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

# Etiquetas de costo
GRATIS = ('gratis', 'Sin costo mensual')
SERV = ('serv', 'Servicio: $0 normalmente')
IA = ('ia', 'IA: ~$20–60 al mes')
# Internet
SIN_RED = ('local', 'Funciona sin internet')
CON_RED = ('red', 'Necesita internet')
# Datos
NO_ENVIA = ('local', 'No envía tus datos')

# (número, nombre, estado, qué hace, en tu día, costo, internet, envío, sugerida, prueba)
GRUPOS = [
    ('Anotar más rápido', 'Lo que más ayuda a no dejar de anotar: no capturar lo mismo dos veces.', [
        (1, 'Comidas guardadas', 'Se agrega',
         'Guarda una combinación, como tu desayuno habitual, para volver a anotarla sin buscar cada alimento. Puedes revisar y cambiar las cantidades.',
         'Tu desayuno de siempre (2 huevos, 1 tortilla y café) se anota completo.', GRATIS, SIN_RED, NO_ENVIA, True, False),
        (2, 'Copiar una comida', 'Se mejora',
         'Copia solo el desayuno, la comida o la cena de otro día, ajusta lo que cambió y, si te equivocas, lo deshaces.',
         'Comiste lo mismo que ayer en la comida: lo copias y cambias la porción de arroz.', GRATIS, SIN_RED, NO_ENVIA, True, False),
        (3, 'Frecuentes que recuerdan tu cantidad', 'Se mejora',
         'Lo que comes seguido aparece primero y ya trae la cantidad que sueles poner.',
         'Tus 3 tortillas de siempre aparecen arriba y ya dicen 3.', GRATIS, SIN_RED, NO_ENVIA, True, False),
        (4, 'Mis recetas caseras', 'Se agrega',
         'Guardas los ingredientes de un guiso (con aceite y todo), cuántas porciones salen, y la app calcula cada porción.',
         'Tu tinga de pollo se calcula una vez; después solo dices cuánto te serviste.', GRATIS, SIN_RED, NO_ENVIA, True, False),
        (5, 'Varios alimentos de una vez', 'Se agrega',
         'Armas tu plato con varios alimentos y lo guardas todo junto, sin abrir y cerrar la pantalla para cada uno.',
         'Pollo, arroz, frijoles y ensalada en un solo paso.', GRATIS, SIN_RED, NO_ENVIA, True, False),
        (6, 'Anotación aproximada', 'Se agrega',
         'Cuando no sabes bien qué comiste, anotas un cálculo aproximado y la app lo marca así. Lo que no sabes queda como “sin dato”, no como cero.',
         'Comiste en una fiesta: anotas “comida aproximada” y sigues con tu día.', GRATIS, SIN_RED, NO_ENVIA, True, False),
        (7, 'Nombrar y ordenar mis comidas', 'Se agrega',
         'Cambias los apartados del día a tu rutina: por ejemplo, “Almuerzo” o “Antes del gym”, y los acomodas a tu gusto.',
         'Tu día tiene desayuno, almuerzo, comida y cena.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (8, 'Planear por adelantado', 'Se mejora',
         'Dejas preparado lo que piensas comer mañana y luego confirmas lo que sí comiste.',
         'En la noche planeas tu comida de mañana para el trabajo.', GRATIS, SIN_RED, NO_ENVIA, False, False),
    ]),
    ('Ayudas con IA y cámara', 'Si eliges “Sí, ahora”, primero hacemos una prueba y después decides si se queda.', [
        (9, 'Describir lo que comiste con IA', 'Se agrega',
         'Escribe o dicta con el teclado algo como “dos tacos al pastor y una horchata”. La app propone alimentos, cantidades y valores aproximados, y muestra qué supuso. Puedes corregirlos antes de guardar.',
         'Sales de la taquería y lo dictas en 10 segundos.', IA, CON_RED, ('envia', 'Envía tu descripción a la IA'), False, True),
        (10, 'Escanear código de barras', 'Se agrega',
         'Apuntas la cámara al código del empaque y la app busca el producto en una base pública. Si no aparece, lo capturas tú.',
         'Tu yogurt o tu barra de proteína se agregan sin copiar la etiqueta.', GRATIS, CON_RED, ('envia', 'Envía solo el código'), False, True),
        (11, 'Foto del plato con IA', 'Se agrega',
         'Tomas foto y la IA propone qué hay y cuánto. Es una estimación que se equivoca seguido en porciones, por eso siempre la revisas.',
         'Un plato en un restaurante del que no sabes la receta.', IA, CON_RED, ('envia', 'Envía la foto a la IA'), False, True),
        (12, 'Foto de la etiqueta', 'Se agrega',
         'Tomas foto de la tabla nutrimental de un producto y la app llena los datos por ti. Tú los confirmas.',
         'Un producto nuevo del súper que no estaba en la lista.', IA, CON_RED, ('envia', 'Envía la foto de la etiqueta'), False, True),
    ]),
    ('Metas, pantalla y planes', 'Cómo quieres ver tu día y hacia dónde vas.', [
        (13, 'Elegir qué ver', 'Se agrega',
         'Tú decides la pantalla: todo (calorías y macros), solo proteína, o un diario sin números (solo lo que comiste, con foto o texto).',
         'Una temporada solo quieres cuidar tu proteína, sin ver calorías.', GRATIS, SIN_RED, NO_ENVIA, True, False),
        (14, 'Calculadora inicial', 'Se agrega',
         'Con tu edad, estatura, peso y actividad, la app sugiere metas de inicio. Es una estimación; tú las ajustas.',
         'No sabes cuánta proteína ponerte: te da un punto de partida.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (15, 'Metas distintas por día', 'Se agrega',
         'Metas diferentes entre semana y fin de semana, o en días de ejercicio.',
         'Los sábados comes más: tu meta de ese día ya lo considera.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (16, 'Ideas de qué comer', 'Se agrega',
         'Te sugiere opciones con tus propios alimentos y gustos, según lo que te queda del día.',
         'Son las 8 pm y te quedan 30 g de proteína: te da 3 ideas de cena.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (17, 'Plan semanal y lista del súper', 'Se agrega',
         'Armas el menú de la semana y la app junta los ingredientes en una lista de compras.',
         'El domingo planeas la semana y vas al súper con la lista.', GRATIS, SIN_RED, NO_ENVIA, False, False),
    ]),
    ('Seguimiento y avances', 'Todo apagado al inicio; activas solo lo que te sirva.', [
        (18, 'Peso y tendencia', 'Se agrega',
         'Anotas tu peso cuando quieras y una línea suave muestra hacia dónde va, sin que un día aislado te confunda.',
         'Subiste medio kilo un lunes, pero la tendencia del mes va bajando.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (19, 'Medidas', 'Se agrega',
         'Guardas cintura, cadera u otras medidas con su fecha.',
         'Una vez al mes te mides la cintura.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (20, 'Agua', 'Se agrega',
         'Cuentas vasos o mililitros con un toque.',
         'Llevas 5 de 8 vasos a media tarde.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (21, 'Fibra, azúcar y sodio', 'Se agrega',
         'Además de los macros, ves estos valores cuando el alimento los tiene. Si no los tiene, dice “sin dato”.',
         'Quieres comer más fibra y ver cuánta llevas.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (22, 'Fotos de progreso', 'Se agrega',
         'Guardas fotos tuyas por fecha para compararlas. Nunca se suben a internet, salvo que tú lo elijas.',
         'Comparas una foto de enero con una de junio.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (23, 'Notas de sueño, ánimo o ciclo', 'Se agrega',
         'Una nota corta del día. Cada una se activa por separado.',
         'Notas que comes distinto los días que duermes mal.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (24, 'Resumen semanal', 'Se agrega',
         'Promedios de la semana y cuántos días tienen registro, porque un día sin anotar no es un día sin comer.',
         'El domingo ves cómo te fue en proteína toda la semana.', GRATIS, SIN_RED, NO_ENVIA, True, False),
        (25, 'Reporte para tu nutrióloga', 'Se agrega',
         'Un PDF con las fechas y datos que tú elijas, para llevarlo a consulta o mandarlo.',
         'Antes de tu cita generas el reporte del último mes.', GRATIS, SIN_RED, NO_ENVIA, False, False),
    ]),
    ('Avisos, atajos y tus datos', 'Algunas usan un servicio en internet (ver página de costos y privacidad).', [
        (26, 'Recordatorios', 'Se agrega',
         'Avisos a la hora que tú elijas, que puedes pausar cuando quieras. Otra opción sin servicio: usar la app Recordatorios del iPhone.',
         'A las 4 pm: “¿Anotas tu comida?”.', SERV, CON_RED, ('envia', 'Envía tus horarios de aviso'), False, False),
        (27, 'Siri: “Anotar comida”', 'Se agrega',
         'Le dices a Siri “Anotar comida” y se abre la app lista para escribir o dictar. Requiere configurar un Atajo una vez.',
         'Con las manos ocupadas en la cocina.', GRATIS, SIN_RED, NO_ENVIA, False, False),
        (28, 'Peso desde Apple Salud', 'Se agrega',
         'Un Atajo del iPhone pasa tu peso de la app Salud a esta app, para no escribirlo dos veces. Se prueba primero en tu teléfono.',
         'Tu báscula guarda el peso en Salud y aquí aparece solo.', SERV, CON_RED, ('envia', 'Envía solo tu peso'), False, True),
        (29, 'Respaldo automático', 'Se agrega',
         'Mientras usas la app con internet, se envían tus cambios para guardar un respaldo fuera del teléfono. Verás la fecha de la última copia confirmada y si quedan cambios pendientes. Podrás restaurar hasta esa copia. Tú eliges si incluye fotos y si lo proteges con tu clave (ver página de privacidad).',
         'Cambias de iPhone y recuperas tu historial.', SERV, CON_RED, ('envia', 'Envía tu diario al respaldo'), True, False),
        (30, 'Usar en otro teléfono o tableta', 'Se agrega',
         'Tu diario aparece igual en otro aparato, por ejemplo un iPad.',
         'Revisas tu semana en la tableta.', SERV, CON_RED, ('envia', 'Envía tu diario al servicio'), False, False),
    ]),
]

OTRAS = [
    (31, 'Ayuno', 'Registra a qué hora empiezas y terminas de comer, y cuántas horas pasan. Apagado por defecto.'),
    (32, 'Rachas y logros', 'Cuenta los días seguidos que anotas y muestra logros. Siempre se pueden apagar.'),
]

CONDICIONES = [
    ('Guarda de verdad', 'Solo dice “guardado” cuando sí se guardó, y funciona sin internet.'),
    ('Tus alimentos, bien hechos', 'Buscas, creas y corriges alimentos; cada uno dice de dónde salen sus valores (etiqueta, referencia o estimación).'),
    ('Cantidades reales', 'Gramos, fracciones y medidas caseras (taza, pieza, cucharada) según cada alimento.'),
    ('Sin regaños', 'Sin rojo ni “te pasaste”. Tampoco felicita por comer menos. Solo describe.'),
    ('“Sin dato” no es cero', 'Lo que no se sabe se ve como “sin dato”. Un día sin anotar no cuenta como día sin comer.'),
    ('Tú tienes el control', 'Metas opcionales; respaldo que se puede recuperar; y nada sale del teléfono sin que tú lo actives.'),
]

PREGUNTAS = [
    ('¿Repites desayunos o comidas?', '1, 2 y 3'),
    ('¿Cocinas en casa?', '4 y 5'),
    ('¿Comes fuera seguido?', '6, 9 y 11'),
    ('¿Compras muchos productos empacados?', '10 y 12'),
    ('¿Quieres ver números todo el tiempo?', '13'),
    ('¿Te ayuda ver tu avance?', '18, 24 y 25'),
]

RUTA_CORTA = [1, 2, 3, 4, 5, 6, 13, 24, 29]

NO_DISPONIBLE = [
    ('Widget con tus macros en la pantalla de inicio', 'Un Atajo puede poner un botón para abrir la app.'),
    ('App propia en el Apple Watch', 'Se pueden probar Atajos desde el reloj.'),
    ('Leer Apple Salud directamente', 'El peso puede llegar con un Atajo (función 28).'),
    ('Medir el plato con el sensor 3D del iPhone', 'La foto con IA (11) da una estimación.'),
]


def e(t):
    return html.escape(t)


def chip(par):
    clase, texto = par
    return f'<span class="chip {clase}">{e(texto)}</span>'


def tarjeta(f):
    n, nom, estado, que, dia, costo, red, envio, sug, prueba = f
    cls_estado = {'Se agrega': 'nuevo', 'Se mejora': 'mejora', 'Ya existe': 'existe'}[estado]
    extra = '<span class="sug">★ Sugerida</span>' if sug else ''
    extra += '<span class="prueba">Primero se prueba</span>' if prueba else ''
    return f'''<div class="card">
  <div class="card-top"><span class="num">{n}</span><h3>{e(nom)}</h3></div>
  <div class="marcas"><span class="estado {cls_estado}">{e(estado)}</span>{extra}</div>
  <p>{e(que)}</p>
  <p class="dia"><b>En tu día:</b> {e(dia)}</p>
  <div class="chips">{chip(costo)}{chip(red)}{chip(envio)}</div>
</div>'''


def pagina(contenido, clase=''):
    return f'<section class="page {clase}">{contenido}<div class="pie">Tu app de comida · para Karen</div></section>'


def construir():
    todas = {f[0]: f for _, _, fs in GRUPOS for f in fs}
    p = []
    # Portada
    p.append(f'''<section class="page portada">
  <div class="anillo"><svg viewBox="0 0 120 120" width="150" height="150">
    <circle cx="60" cy="60" r="44" fill="none" stroke="#1d3a68" stroke-width="12"/>
    <circle cx="60" cy="60" r="44" fill="none" stroke="#7fe0c0" stroke-width="12" stroke-dasharray="100 300" transform="rotate(-90 60 60)"/>
    <circle cx="60" cy="60" r="44" fill="none" stroke="#d4af37" stroke-width="12" stroke-dasharray="85 300" stroke-dashoffset="-106" transform="rotate(-90 60 60)"/>
    <circle cx="60" cy="60" r="44" fill="none" stroke="#e8a0bf" stroke-width="12" stroke-dasharray="50 300" stroke-dashoffset="-197" transform="rotate(-90 60 60)"/>
    <circle cx="60" cy="60" r="9" fill="#f5ecd7"/></svg></div>
  <h1>Tu app de comida</h1>
  <p class="sub">Escoge cómo quieres que funcione tu app para contar calorías y macros.</p>
  <div class="portada-caja">
    <p>Revisamos las apps más usadas (MyFitnessPal, MacroFactor, Cronometer, Yazio, Fitia y otras), lo que dicen las personas que las usan y lo que se puede hacer en tu iPhone.</p>
    <p>Aquí están las <b>{len(todas)} funciones</b> que encontramos, explicadas en palabras sencillas. <b>Tú decides cuáles quieres.</b> No hay respuestas correctas, y lo que elijas hoy se puede cambiar después.</p>
  </div>
  <p class="fecha">Octubre 2026</p>
</section>''')

    # Cómo leer
    p.append(pagina(f'''<h2>Cómo leer este documento</h2>
<div class="dos-col">
<div>
<h4>Cada función trae</h4>
<ul class="lista">
<li><span class="estado nuevo">Se agrega</span> es nueva · <span class="estado mejora">Se mejora</span> tu app ya tiene una parte.</li>
<li><span class="sug">★ Sugerida</span> es nuestra recomendación, nada más. Tú decides.</li>
<li><span class="prueba">Primero se prueba</span> si la eliges, primero hacemos una prueba en tu iPhone y luego decides si se queda.</li>
</ul>
<h4>Tres etiquetas</h4>
<ul class="lista">
<li><b>Costo:</b> {chip(GRATIS)} {chip(SERV)} {chip(IA)}</li>
<li><b>Internet:</b> {chip(SIN_RED)} {chip(CON_RED)}</li>
<li><b>Tus datos:</b> {chip(NO_ENVIA)} {chip(('envia', 'Envía algo, y dice qué'))}</li>
</ul>
</div>
<div>
<h4>Cómo escoger</h4>
<p>Al final hay una <b>hoja para marcar</b>. Para cada función eliges una de tres:</p>
<div class="tres"><span>Sí, ahora</span><span>Quizá después</span><span>No me interesa</span></div>
<p>Solo marcas en esa hoja; las tarjetas solo llevan su número.</p>
<div class="caja-oro"><h4>Si solo tienes 5 minutos</h4>
<p>Lee estas tarjetas, que son las que más ayudan a no dejar de anotar:</p>
<p class="ruta">{" · ".join(f"<b>{n}</b> {e(todas[n][1])}" for n in RUTA_CORTA)}</p></div>
</div></div>'''))

    # Condiciones + preguntas
    conds = ''.join(f'<div class="cond"><b>{e(t)}</b><span>{e(d)}</span></div>' for t, d in CONDICIONES)
    pregs = ''.join(f'<tr><td>{e(q)}</td><td>Mira las tarjetas <b>{e(r)}</b></td></tr>' for q, r in PREGUNTAS)
    p.append(pagina(f'''<h2>Condiciones que debe cumplir la app</h2>
<p class="intro">Esto no se elige: la app debe cumplirlo, elijas lo que elijas. Algunas cosas ya están y otras se van a mejorar.</p>
<div class="conds">{conds}</div>
<h2 class="mt">¿Cómo comes tú?</h2>
<p class="intro">Estas preguntas te ayudan a saber qué tarjetas leer primero. No esconden nada: puedes leer todas.</p>
<table class="preg">{pregs}</table>'''))

    # Grupos (2 por página cuando son cortos)
    for titulo, desc, fs in GRUPOS:
        cards = ''.join(tarjeta(f) for f in fs)
        p.append(pagina(f'<h2>{e(titulo)}</h2><p class="intro">{e(desc)}</p><div class="grid">{cards}</div>'))

    # Otras ideas + no disponible
    otras = ''.join(f'<div class="card chica"><div class="card-top"><span class="num">{n}</span><h3>{e(t)}</h3></div><p>{e(d)}</p>'
                    f'<div class="chips">{chip(GRATIS)}{chip(SIN_RED)}{chip(NO_ENVIA)}</div></div>' for n, t, d in OTRAS)
    nod = ''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td></tr>' for a, b in NO_DISPONIBLE)
    p.append(pagina(f'''<h2>Otras ideas</h2>
<p class="intro">Las tienen otras apps. No las recomendamos ni las descartamos; están aquí por si te interesan.</p>
<div class="grid">{otras}</div>
<h2 class="mt">No disponible directamente en tu app</h2>
<p class="intro">Tu app es una página instalada en el iPhone (no viene de la App Store), así que hay cosas que Apple no le permite. Para algunas hay una alternativa.</p>
<table class="preg"><tr><th>Lo que no puede</th><th>Alternativa</th></tr>{nod}</table>'''))

    # Costos y privacidad
    p.append(pagina(f'''<h2>Costos y privacidad</h2>
<div class="dos-col">
<div>
<h4>Lo que cuesta</h4>
<ul class="lista">
<li>{chip(GRATIS)} La mayoría de las funciones viven en tu teléfono y no cuestan nada al mes.</li>
<li>{chip(SERV)} Respaldo, recordatorios y otro aparato usan <b>un solo servicio en internet</b> que comparten. Su plan gratuito debería alcanzar para una persona; si algún día no alcanza, cuesta unos 5 dólares al mes.</li>
<li>{chip(IA)} Las funciones con IA usan el mismo servicio y pagan por uso. Calculamos unos <b>$20 a $60 pesos al mes</b> anotando 6 comidas al día. Es un estimado, no un precio fijo, y se le pone un límite de gasto.</li>
</ul>
</div>
<div>
<h4>Quién puede ver tu diario</h4>
<p><b>Tú, en tu teléfono.</b> Nada sale de ahí hasta que actives una función que lo diga en su etiqueta.</p>
<p>Si activas el respaldo, eliges una de dos formas:</p>
<div class="cond"><b>Respaldo normal</b><span>Fácil de recuperar. Quien administra el servicio (Emmanuel) técnicamente podría verlo. Él se compromete a no hacerlo, pero la app no lo impide.</span></div>
<div class="cond"><b>Respaldo con tu clave</b><span>Tu teléfono cifra la copia con una frase que solo tú sabes, antes de enviarla. El servicio no recibe tu frase, así que la copia guardada no se puede leer. Si olvidas la frase, ese respaldo no se puede recuperar. Tu teléfono y la app siguen necesitando cuidado.</span></div>
<p>Las funciones con IA mandan solo lo necesario para esa consulta (tu descripción o tu foto) a la empresa de IA. Tu peso, tus notas y tus fotos de progreso <b>nunca</b> se mandan a la IA.</p>
</div></div>'''))

    # Hoja resumen
    circulos = '<td class="o"><i></i></td>' * 3
    filas = ''
    for titulo, _, fs in GRUPOS:
        filas += f'<tr class="g"><td colspan="5">{e(titulo)}</td></tr>'
        filas += ''.join(f'<tr><td class="n">{f[0]}</td><td>{e(f[1])}{" <b>★</b>" if f[8] else ""}</td>{circulos}</tr>' for f in fs)
    filas += '<tr class="g"><td colspan="5">Otras ideas</td></tr>'
    filas += ''.join(f'<tr><td class="n">{n}</td><td>{e(t)}</td>{circulos}</tr>' for n, t, _ in OTRAS)
    p.append(pagina(f'''<h2>Tu hoja para marcar</h2>
<p class="intro">Rellena un círculo por renglón. ★ = sugerida.</p>
<table class="hoja"><tr><th></th><th>Función</th><th>Sí, ahora</th><th>Quizá después</th><th>No me interesa</th></tr>{filas}</table>
<div class="notas"><b>Notas o ideas tuyas:</b></div>''', 'resumen'))

    css = open(os.path.join(AQUI, 'pdf_funciones.css'), encoding='utf-8').read()
    doc = f'<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Tu app de comida</title><style>{css}</style></head><body>{"".join(p)}</body></html>'
    os.makedirs(DOCS, exist_ok=True)
    ruta_html = os.path.join(DOCS, 'funciones-karen.html')
    with open(ruta_html, 'w', encoding='utf-8') as f:
        f.write(doc)
    ruta_pdf = os.path.join(DOCS, 'funciones-karen.pdf')
    # Perfil aparte: si Edge ya está abierto, sin esto le pasa el trabajo a la ventana abierta y no crea el PDF.
    perfil = os.path.join(os.environ.get('TEMP', DOCS), 'edge-pdf-karen')
    subprocess.run([EDGE, '--headless', '--disable-gpu', '--no-pdf-header-footer', f'--user-data-dir={perfil}',
                    f'--print-to-pdf={ruta_pdf}', 'file:///' + ruta_html.replace('\\', '/')], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(ruta_pdf)


if __name__ == '__main__':
    construir()
