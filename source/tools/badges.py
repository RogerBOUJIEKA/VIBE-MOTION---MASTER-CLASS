# Outil ponctuel qui a produit pay/*.webp à partir de logos de dépôts GitHub publics (jacktembo/PaymentAssets, yessalerp wavesn_woocommerce_pay, bienvenuelisis/flutter_paygateglobal). Les images finales sont dans pay/. Chemins à adapter si relancé.
# Round HD payment badges (256 px, shown at 44-48 px) built from the source logo files.
from PIL import Image, ImageDraw, ImageChops
SP = '/tmp/claude-0/-home-user/86aa9d93-3569-51fa-b7ca-8789a11c3cd6/scratchpad/'
OUT = '/home/user/vibe-motion---master-class/pay/'
PA = SP + 'payassets/img/'
BIG, OUTS = 1024, 256
import os
os.makedirs(OUT, exist_ok=True)


def circle(bg, art, scale, dy=0.0):
    """bg colour circle with art (RGBA) centred, art width = scale * diameter."""
    c = Image.new('RGBA', (BIG, BIG), bg)
    a = art.copy()
    w = int(BIG * scale); h = int(a.height * w / a.width)
    a = a.resize((w, h), Image.LANCZOS)
    c.alpha_composite(a, ((BIG - w) // 2, (BIG - h) // 2 + int(dy * BIG)))
    return c


def finish(img, name):
    m = Image.new('L', (BIG, BIG), 0); ImageDraw.Draw(m).ellipse((0, 0, BIG - 1, BIG - 1), fill=255)
    img = img.copy(); img.putalpha(ImageChops.multiply(img.getchannel('A'), m))
    img = img.resize((OUTS, OUTS), Image.LANCZOS)
    img.save(OUT + name + '.webp', 'WEBP', quality=92, method=6)
    img.save(SP + 'v4/badge-' + name + '.png')


def bbox_where(img, fn):
    px = img.load(); W, H = img.size; xs = []; ys = []
    for y in range(0, H, max(1, H // 600)):
        for x in range(0, W, max(1, W // 600)):
            if fn(px[x, y]): xs.append(x); ys.append(y)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


# 1 MoMo (MTN): the figure on MoMo blue, with the yellow band as the bottom cap
m = Image.open(PA + 'MTN_MOMO_Layer_1-2-p-500.png').convert('RGBA')
fig = m.crop((0, 0, 195, 160))
cm = Image.new('RGBA', (BIG, BIG), (1, 81, 115, 255))
fw = int(BIG * 0.94); fh = int(fig.height * fw / fig.width)
cm.alpha_composite(fig.resize((fw, fh), Image.LANCZOS), ((BIG - fw) // 2 + int(BIG * 0.03), int(BIG * 0.05)))
ImageDraw.Draw(cm).rectangle((0, int(BIG * 0.85), BIG, BIG), fill=(252, 199, 0, 255))
finish(cm, 'momo')

# 2 Wave: the round logo itself, cut along its blue disc
w = Image.open(SP + 'gh/yessalerp_wavesn_woocommerce_pay/assets/images/wave-logo.png').convert('RGBA')
b = bbox_where(w, lambda p: p[2] > 150 and p[0] < 120)
d = w.crop(b)
cx = (b[2] - b[0]) * 0.012
d = d.crop((int(cx), int(cx), d.width - int(cx), d.height - int(cx))).resize((BIG, BIG), Image.LANCZOS)
finish(d, 'wave')

# 3 TMoney (Togo): red word mark on its yellow
t = Image.open(SP + 'gh/t_bienvenuelisis_flutter_paygateglobal/example/assets/tmoney.png').convert('RGBA')
tb = bbox_where(t, lambda p: p[3] > 200 and p[0] > 180 and p[1] < 90)
pad = 20
art = t.crop((tb[0] - pad, tb[1] - pad, tb[2] + pad, tb[3] + pad))
finish(circle((250, 219, 22, 255), art, 0.80, 0.0), 'tmoney')

# 4 Celtiis: blue square without its white border
c = Image.open(PA + 'celtiis_Group 610-p-500.png').convert('RGBA')
inner = c.crop((22, 22, 478, 478))
finish(circle((18, 60, 118, 255), inner, 0.90, 0.0), 'celtiis')

# 5 Airtel Money: the red logo turned white on Airtel red
a = Image.open(PA + 'AIRTEL MONEY-p-500.png').convert('RGBA')
ab = a.getchannel('A').getbbox(); a = a.crop(ab)
white = Image.new('RGBA', a.size, (255, 255, 255, 255)); white.putalpha(a.getchannel('A'))
finish(circle((235, 26, 34, 255), white, 0.64, 0.0), 'airtel')

# 6 Free Money: the red and grey word mark from inside the white pill, on white
f = Image.open(PA + 'FreeMoney-1-p-500.png').convert('RGBA')
word = f.crop((217, 126, 434, 211))
ImageDraw.Draw(word).rectangle((0, 0, 11, 28), fill=(255, 255, 255, 255))
finish(circle((255, 255, 255, 255), word, 0.80, 0.0), 'freemoney')
print('done', sorted(os.listdir(OUT)))
