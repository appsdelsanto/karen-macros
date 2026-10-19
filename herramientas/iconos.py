"""Genera los íconos de la app (azul marino con anillo de macros)."""
from PIL import Image, ImageDraw
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.dirname(AQUI)

def icono(t):
    g = t * 4  # dibujar grande y reducir para suavizar
    im = Image.new('RGB', (g, g), '#0b1d3a')
    d = ImageDraw.Draw(im)
    m, w = g * 0.2, g * 0.09
    caja = [m, m, g - m, g - m]
    d.arc(caja, 0, 360, fill='#1d3a68', width=int(w))
    for ini, fin, col in [(-90, 40, '#7fe0c0'), (50, 170, '#d4af37'), (180, 245, '#e8a0bf')]:
        d.arc(caja, ini, fin, fill=col, width=int(w))
    r = g * 0.07
    d.ellipse([g/2 - r, g/2 - r, g/2 + r, g/2 + r], fill='#f5ecd7')
    return im.resize((t, t), Image.LANCZOS)

for t in (180, 192, 512):
    icono(t).save(os.path.join(SALIDA, f'icon-{t}.png'))
