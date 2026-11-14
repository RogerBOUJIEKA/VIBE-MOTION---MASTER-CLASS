# Share image (1200 x 630) in the site's style, rendered from HTML with the site's own font and assets.
import math
import os
SP = os.path.dirname(os.path.abspath(__file__)) + '/'
rays = ''.join(f'<line x1="{50+14*math.cos(a):.1f}" y1="{50+14*math.sin(a):.1f}" x2="{50+(46 if i%2==0 else 40)*math.cos(a):.1f}" y2="{50+(46 if i%2==0 else 40)*math.sin(a):.1f}"/>' for i, a in enumerate([k*math.pi/6+0.13 for k in range(12)]))
spark = f'<svg viewBox="0 0 100 100"><g stroke="currentColor" stroke-width="9" stroke-linecap="round">{rays}</g></svg>'
PAY = ['pay/momo.webp', 'pay/wave.webp', 'moov-money.svg', 'pay/tmoney.webp', 'orange-money.svg', 'pay/celtiis.webp', 'pay/airtel.webp', 'pay/freemoney.webp', 'mastercard.svg', 'visa.svg']
BG = {'moov-money.svg': '#ea6607', 'orange-money.svg': '#000', 'mastercard.svg': '#fff', 'visa.svg': '#fff'}
pays = ''.join(f'<span class="pm" style="background:{BG.get(f, "transparent")}"><img src="{f}" style="width:{"100%" if f.startswith("pay/") else ("94%" if "orange" in f else "116%")}"></span>' for f in PAY)
html = f'''<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:U;src:url(fonts/urbanist.woff2) format("woff2");font-weight:100 900}}
*{{box-sizing:border-box;margin:0}}
body{{width:1200px;height:630px;overflow:hidden;background:#f6f4f1;font-family:U,sans-serif;color:#121214;position:relative}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(18,18,20,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(18,18,20,.07) 1px,transparent 1px);background-size:48px 48px;-webkit-mask-image:radial-gradient(ellipse 80% 90% at 50% 0%,#000 25%,rgba(0,0,0,.4) 60%,transparent 90%)}}
.glow{{position:absolute;inset:0;background:radial-gradient(34% 52% at 24% 58%,rgba(227,6,27,.22),transparent 70%),radial-gradient(30% 40% at 78% 30%,rgba(224,122,86,.14),transparent 70%)}}
.giant{{position:absolute;left:18px;top:-14px;font-weight:300;font-size:236px;line-height:1;letter-spacing:-.07em;background:linear-gradient(180deg,#ff3347,#e3061b 55%,#9c0212);-webkit-background-clip:text;color:transparent;white-space:nowrap}}
.ph{{position:absolute;left:0;bottom:0;width:612px;height:612px}}
.chip{{position:absolute;display:inline-flex;align-items:center;gap:9px;padding:8px 15px 8px 8px;border-radius:999px;background:#fff;font-weight:500;font-size:16px;box-shadow:0 12px 30px rgba(0,0,0,.16)}}
.chip i{{display:grid;place-items:center;width:32px;height:32px;border-radius:50%;background:#fdf0ea;color:#e07a56}}
.chip i svg,.chip i img{{width:19px;height:19px}}
.stamp{{position:absolute;left:478px;top:236px;width:86px;height:86px;border-radius:50%;display:grid;place-items:center;background:radial-gradient(circle at 32% 26%,#ff4d5e,#e3061b 55%,#a50314);box-shadow:0 12px 26px rgba(227,6,27,.35),0 0 0 6px rgba(227,6,27,.12)}}
.stamp>*{{grid-area:1/1}}
.stamp svg.t{{width:86px;height:86px}}
.stamp .r{{width:50px;height:50px;border-radius:50%;border:1px dashed rgba(255,255,255,.6)}}
.stamp .c{{display:grid;place-items:center;width:34px;height:34px;border-radius:50%;background:#fff;color:#e07a56}}
.stamp .c svg{{width:23px;height:23px}}
.tx{{position:absolute;left:628px;top:192px;width:550px}}
.pill{{display:inline-flex;align-items:center;gap:10px;padding:10px 16px;border-radius:999px;background:#fff;box-shadow:0 1px 2px rgba(18,18,20,.05),0 10px 28px rgba(18,18,20,.08);font-weight:500;font-size:14px;letter-spacing:.15em}}
.pill i{{width:8px;height:8px;border-radius:50%;background:#e3061b}}
h1{{margin-top:16px;font-weight:300;font-size:58px;line-height:.98;letter-spacing:-.055em}}
h1 em{{font-style:normal;color:#cf0418}}
.sub{{margin-top:14px;font-weight:400;font-size:19px;line-height:1.4;color:#5e5b58}}
.sub b{{font-weight:500;color:#121214}}
.offer{{display:flex;align-items:center;gap:12px;margin-top:16px}}
.price{{display:inline-flex;align-items:baseline;gap:8px;padding:10px 18px;border-radius:999px;background:#121214;color:#fff}}
.price b{{font-weight:400;font-size:28px;letter-spacing:-.03em}}.price small{{font-weight:500;font-size:14px;color:rgba(255,255,255,.7)}}
.price s{{font-size:16px;color:rgba(255,255,255,.55);text-decoration-color:#ff3347}}
.off{{padding:8px 12px;border-radius:999px;background:#fbe6e8;color:#cf0418;font-weight:500;font-size:16px}}
.life{{font-weight:500;font-size:16px;color:#15803d}}
.strip{{position:absolute;left:0;right:0;bottom:0;height:58px;display:flex;align-items:center;justify-content:space-between;padding:0 26px;background:#0b0b0e;color:#fff}}
.strip .lg{{height:30px}}
.pays{{display:flex;gap:6px}}
.pm{{display:grid;place-items:center;width:28px;height:28px;border-radius:50%;overflow:hidden}}
.pm img{{max-width:none;height:auto}}
.url{{font-weight:500;font-size:18px;letter-spacing:.01em}}
</style></head><body>
<div class="grid"></div><div class="glow"></div>
<div class="giant">MOTION</div>
<img class="ph" src="roger-v3.webp">
<span class="chip" style="left:24px;top:392px"><i>{spark}</i>Claude Opus 5.5</span>
<span class="chip" style="left:418px;top:470px"><i><img src="izivoice-icon.png"></i>iziVoice</span>
<div class="stamp"><svg class="t" viewBox="0 0 120 120"><defs><path id="p" d="M60,60 m-48,0 a48,48 0 1,1 96,0 a48,48 0 1,1 -96,0"/></defs><text dominant-baseline="central" fill="#fff" font-family="U" font-weight="500" font-size="9.6"><textPath href="#p" textLength="301" lengthAdjust="spacing">ACCÈS À VIE – ACCÈS À VIE – ACCÈS À VIE –&#160;</textPath></text></svg><span class="r"></span><span class="c">{spark}</span></div>
<div class="tx">
  <span class="pill"><i></i>FORMATION VIBE MOTION</span>
  <h1>Créez des<br><em>vidéos pro</em><br>avec l'IA.</h1>
  <p class="sub"><b>Claude Opus 5.5</b> monte. <b>iziVoice</b> prête sa voix.<br>Vous dirigez, sur smartphone ou ordinateur.</p>
  <div class="offer"><span class="price"><b>5 500</b><small>FCFA</small><s>25 000</s></span><span class="off">−78 %</span><span class="life">✓ Accès à vie</span></div>
</div>
<div class="strip"><img class="lg" src="logo_rb.png"><div class="pays">{pays}</div><span class="url">rogerboujieka.com</span></div>
</body></html>'''
open(SP + 'og.html', 'w', encoding='utf-8').write(html)
print('ok')
