import math
import swisseph as swe

swe.set_sid_mode(swe.SIDM_LAHIRI)
jd = swe.julday(2000, 8, 4, 15.5)
flags = swe.FLG_MOSEPH | swe.FLG_SIDEREAL

signs = ['Aries','Taurus','Gemini','Cancer','Leo','Virgo','Libra','Scorpio','Sagittarius','Capricorn','Aquarius','Pisces']
sign_glyphs = ['\u2648','\u2649','\u264A','\u264B','\u264C','\u264D','\u264E','\u264F','\u2650','\u2651','\u2652','\u2653']

def lon_of(p):
    return swe.calc_ut(jd, p, flags)[0][0]

planets = [
    ('Sun', '\u2609', lon_of(swe.SUN), 236, False),
    ('Moon', '\u263D', lon_of(swe.MOON), 205, False),
    ('Mercury', '\u263F', lon_of(swe.MERCURY), 196, False),
    ('Venus', '\u2640', lon_of(swe.VENUS), 205, False),
    ('Mars', '\u2642', lon_of(swe.MARS), 148, True),
    ('Jupiter', '\u2643', lon_of(swe.JUPITER), 238, True),
    ('Saturn', '\u2644', lon_of(swe.SATURN), 182, False),
]
rahu = swe.calc_ut(jd, swe.TRUE_NODE, flags)[0][0]
planets.append(('Rahu', '\u260A', rahu, 250, False))
planets.append(('Ketu', '\u260B', (rahu + 180) % 360, 205, False))
asc = swe.houses_ex(jd, 25.90, 81.94, b'W', swe.FLG_SIDEREAL)[1][0]

C = 330
R_OUT, R_ZI, R_HUB = 318, 270, 100

def pt(theta_deg, r):
    rad = math.radians(theta_deg)
    return C + r * math.cos(rad), C - r * math.sin(rad)

def theta_of(lon):
    return (180 + ((lon - 330) % 360)) % 360

def dms(lon):
    d = lon % 30
    return f"{int(d)}\u00B0{int(round((d % 1) * 60)):02d}\u2032"

def wedge(t1, t2, r1, r2, color):
    pts = [pt(t1 + i, r2) for i in range(0, 31)] + [pt(t2 - i, r1) for i in range(0, 31)]
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts) + ' Z'
    return f'<path d="{d}" fill="{color}"/>'

def build(theme):
    s = []
    s.append(f'<svg class="natal" viewBox="0 0 660 660" xmlns="http://www.w3.org/2000/svg" font-family="Inter, sans-serif">')
    s.append(f'<circle cx="{C}" cy="{C}" r="{R_OUT}" fill="{theme["fill"]}" stroke="{theme["ring"]}" stroke-width="1.5"/>')
    s.append(wedge(300, 330, R_HUB, R_ZI, theme['wedge']))    # 5H stellium
    s.append(wedge(240, 270, R_HUB, R_ZI, theme['wedge2']))   # 3H forge
    for k in range(12):
        a = 180 + 30 * k
        x1, y1 = pt(a, R_HUB); x2, y2 = pt(a, R_OUT)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{theme["spoke"]}" stroke-width="1"/>')
    for a in range(0, 360, 5):
        if a % 30 == 0: continue
        x1, y1 = pt(a, R_ZI); x2, y2 = pt(a, R_ZI - 6)
        s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{theme["tick"]}" stroke-width=".75"/>')
    s.append(f'<circle cx="{C}" cy="{C}" r="{R_ZI}" fill="none" stroke="{theme["ring"]}" stroke-width="1"/>')
    for i in range(1, 13):
        mid = 180 + 30 * (i - 1) + 15
        sg = (11 + (i - 1)) % 12
        gx, gy = pt(mid, 293)
        s.append(f'<text x="{gx:.1f}" y="{gy + 6:.1f}" text-anchor="middle" font-size="17" fill="{theme["sign"]}">{sign_glyphs[sg]}\ufe0e</text>')
        hx, hy = pt(mid, 116)
        s.append(f'<text x="{hx:.1f}" y="{hy + 3:.1f}" text-anchor="middle" font-size="10" font-weight="700" fill="{theme["hnum"]}">{i}</text>')
    # ASC marker
    ta = theta_of(asc)
    x1, y1 = pt(ta, R_HUB); x2, y2 = pt(ta, R_OUT)
    s.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{theme["gold"]}" stroke-width="1.5" stroke-dasharray="4 3"/>')
    ax, ay = pt(ta, 165)
    s.append(f'<text x="{ax:.1f}" y="{ay - 6:.1f}" text-anchor="middle" font-size="8" font-weight="800" letter-spacing="1.5" fill="{theme["gold"]}">ASC</text>')
    s.append(f'<text x="{ax:.1f}" y="{ay + 4:.1f}" text-anchor="middle" font-size="7" fill="{theme["gold"]}">{dms(asc)}</text>')
    # planets
    for name, glyph, lon, r, gold in planets:
        t = theta_of(lon)
        e1x, e1y = pt(t, R_ZI); e2x, e2y = pt(t, R_ZI - 12)
        s.append(f'<line x1="{e1x:.1f}" y1="{e1y:.1f}" x2="{e2x:.1f}" y2="{e2y:.1f}" stroke="{theme["accent"]}" stroke-width="1.5"/>')
        px, py = pt(t, r)
        col = theme['gold'] if gold else theme['body']
        s.append(f'<text x="{px:.1f}" y="{py:.1f}" text-anchor="middle" font-size="17" fill="{col}">{glyph}</text>')
        s.append(f'<text x="{px:.1f}" y="{py + 11:.1f}" text-anchor="middle" font-size="6.5" font-weight="700" letter-spacing="1" fill="{theme["name"]}">{name.upper()}</text>')
        s.append(f'<text x="{px:.1f}" y="{py + 20:.1f}" text-anchor="middle" font-size="6.5" fill="{theme["gold"]}">{dms(lon)}</text>')
    # hub
    s.append(f'<circle cx="{C}" cy="{C}" r="{R_HUB}" fill="{theme["hub_fill"]}" stroke="{theme["ring"]}" stroke-width="1"/>')
    s.append(f'<text x="{C}" y="320" text-anchor="middle" font-size="16" font-weight="800" letter-spacing="3" fill="{theme["ink"]}" font-family="{theme["hubfont"]}">SAURABH</text>')
    s.append(f'<text x="{C}" y="336" text-anchor="middle" font-size="7" font-weight="700" letter-spacing="2.5" fill="{theme["accent"]}">PISCES RISING</text>')
    s.append(f'<text x="{C}" y="350" text-anchor="middle" font-size="6.5" letter-spacing="1.5" fill="{theme["muted"]}">04 \u00B7 08 \u00B7 2000 \u2014 21:00 IST</text>')
    s.append(f'<text x="{C}" y="361" text-anchor="middle" font-size="6" letter-spacing="1.2" fill="{theme["muted"]}">PRATAPGARH \u00B7 25.9\u00B0N 81.9\u00B0E</text>')
    s.append('</svg>')
    return '\n    '.join(s)

dark = dict(fill='#10151D', ring='#2B3442', spoke='#232A34', hub_fill='#161B22', sign='#7EB0FA',
            hnum='#4E5D70', body='#E2E8F0', name='#8B98A9', gold='#F59E0B', accent='#3B82F6',
            wedge='rgba(59,130,246,.09)', wedge2='rgba(245,158,11,.05)', tick='#3B4657',
            ink='#FFFFFF', muted='#8B98A9', hubfont='Inter, sans-serif')
sakura = dict(fill='#FDF4F7', ring='#EFCFD9', spoke='#F3DBE2', hub_fill='#FFFFFF', sign='#D6336C',
              hnum='#C9A5B1', body='#43333A', name='#8A7078', gold='#C9861F', accent='#D6336C',
              wedge='rgba(214,51,108,.07)', wedge2='rgba(201,134,31,.06)', tick='#E8C7D1',
              ink='#3D2530', muted='#8A7078', hubfont='Fraunces, Georgia, serif')

for path, theme in [('/app/saurabh-master-chart.html', dark), ('/app/saurabh-master-chart-sakura.html', sakura)]:
    with open(path) as f:
        html = f.read()
    assert '<!-- PAGE2_WHEEL -->' in html, path
    html = html.replace('<!-- PAGE2_WHEEL -->', build(theme))
    with open(path, 'w') as f:
        f.write(html)
    print('injected wheel into', path)
