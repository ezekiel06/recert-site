from PIL import Image, ImageDraw
import pathlib
D = pathlib.Path(__file__).parent
names = [("a-cycle","A  cycle + check"),("a2-cycle-green","A2  cycle, green check"),
         ("b-shield","B  shield"),("c-seal","C  seal"),("d-list","D  review list")]
BIG, MID, SMALL = 220, 96, 48
pad, gap = 28, 34
rowh = BIG + 56
W = pad*2 + BIG + gap + MID + gap + SMALL + 210
H = pad*2 + rowh*len(names)
sheet = Image.new("RGB", (W, H), "#FFFFFF")
d = ImageDraw.Draw(sheet)
for i,(n,label) in enumerate(names):
    y = pad + i*rowh
    im = Image.open(D/f"{n}.png").convert("RGBA")
    for size, x in ((BIG, pad), (MID, pad+BIG+gap), (SMALL, pad+BIG+gap+MID+gap)):
        tile = im.resize((size,size), Image.LANCZOS)
        cy = y + (BIG-size)//2
        bg = Image.new("RGBA",(size,size),(255,255,255,255))
        bg.alpha_composite(tile)
        sheet.paste(bg.convert("RGB"), (x, cy))
    d.text((pad+BIG+gap+MID+gap+SMALL+26, y+BIG//2-8), label, fill="#172B4D")
    d.line([(pad, y+rowh-18),(W-pad, y+rowh-18)], fill="#EBECF0")
d.text((pad, H-20), "sizes shown: 220px   96px   48px (Marketplace tile is 144px)", fill="#6B778C")
sheet.save(D/"contact-sheet.png")
print(D/"contact-sheet.png", sheet.size)
