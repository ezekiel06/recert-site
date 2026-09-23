import math, subprocess, pathlib
D = pathlib.Path(__file__).parent
NAVY, BLUE, GREEN, RED = "#0B3D91", "#0C66E4", "#22A06B", "#DE350B"

def tile(inner, c1=NAVY, c2=BLUE, rx=112):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" width="512" height="512">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>
<rect width="512" height="512" rx="{rx}" fill="url(#g)"/>
{inner}</svg>'''

# --- A: recertification cycle (open ring + arrowhead) around a check -----------
def ring_arrow(r=168, w=34, col="#FFFFFF"):
    t0, t1 = math.radians(-30), math.radians(285)
    p0 = (256 + r*math.cos(t0), 256 + r*math.sin(t0))
    p1 = (256 + r*math.cos(t1), 256 + r*math.sin(t1))
    d = (-math.sin(t1), math.cos(t1)); n = (math.cos(t1), math.sin(t1))
    tip  = (p1[0] + 46*d[0], p1[1] + 46*d[1])
    b1   = (p1[0] + 40*n[0], p1[1] + 40*n[1])
    b2   = (p1[0] - 40*n[0], p1[1] - 40*n[1])
    return (f'<path d="M {p0[0]:.1f} {p0[1]:.1f} A {r} {r} 0 1 1 {p1[0]:.1f} {p1[1]:.1f}" '
            f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} {b1[0]:.1f},{b1[1]:.1f} {b2[0]:.1f},{b2[1]:.1f}" fill="{col}"/>')

def check(col="#FFFFFF", w=48):
    return (f'<path d="M 172 262 L 232 322 L 346 198" fill="none" stroke="{col}" '
            f'stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')

(D/"a-cycle.svg").write_text(tile(ring_arrow() + check()), encoding="utf-8")
(D/"a2-cycle-green.svg").write_text(tile(ring_arrow() + check(GREEN, 52), "#0A2E6B", "#0B3D91"), encoding="utf-8")

# --- B: shield + check --------------------------------------------------------
shield = ('<path d="M256 62 L 424 124 V 266 C 424 358 344 418 256 450 '
          'C 168 418 88 358 88 266 V 124 Z" fill="#FFFFFF"/>')
(D/"b-shield.svg").write_text(tile(shield + check(BLUE, 46)), encoding="utf-8")

# --- C: certification seal (scalloped) + check --------------------------------
def scallop(n=14, r=150, bump=26):
    pts = []
    for i in range(n*2):
        a = math.pi*2*i/(n*2) - math.pi/2
        rr = r + (bump if i % 2 == 0 else 0)
        pts.append(f"{256+rr*math.cos(a):.1f},{256+rr*math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="#FFFFFF"/>'
(D/"c-seal.svg").write_text(tile(scallop() + check(BLUE, 44)), encoding="utf-8")

# --- D: review list, top row approved -----------------------------------------
rows = '<rect x="104" y="96" width="304" height="320" rx="30" fill="#FFFFFF"/>'
y = 168
for i, col in enumerate([GREEN, "#C1C7D0", "#C1C7D0"]):
    rows += f'<circle cx="164" cy="{y}" r="26" fill="{col}"/>'
    rows += f'<rect x="206" y="{y-14}" width="152" height="28" rx="14" fill="#DFE1E6"/>'
    if i == 0:
        rows += (f'<path d="M 151 {y} L 161 {y+11} L 179 {y-11}" fill="none" stroke="#FFFFFF" '
                 f'stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    y += 88
(D/"d-list.svg").write_text(tile(rows), encoding="utf-8")

names = ["a-cycle", "a2-cycle-green", "b-shield", "c-seal", "d-list"]
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
for n in names:
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--force-device-scale-factor=1",
                    f"--screenshot={D/(n+'.png')}", "--window-size=512,512",
                    "--default-background-color=00000000", str(D/(n+".svg"))],
                   check=True, capture_output=True)
print("rendered:", ", ".join(names))
