import {
  WebGLRenderer, Scene, PerspectiveCamera, Group, PlaneGeometry, MeshBasicMaterial, CanvasTexture, SRGBColorSpace,
  BufferGeometry, Float32BufferAttribute, Points, PointsMaterial, Mesh, Fog, Color, DoubleSide, AdditiveBlending
} from 'three';

/* "La traversée": the camera flies through a tunnel of video frames as the visitor scrolls.
   start(host, { posters }) -> { setProgress(0..1), count } */
export function start(host, opts) {
  const posters = opts.posters || [];
  const mobile = matchMedia('(max-width: 760px)').matches;
  let renderer;
  try { renderer = new WebGLRenderer({ antialias: !mobile, alpha: false, powerPreference: 'high-performance' }); } catch (e) { return null; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, mobile ? 1.5 : 2));
  renderer.outputColorSpace = SRGBColorSpace;
  const BG = 0x0b0b0e;
  renderer.setClearColor(BG, 1);
  host.appendChild(renderer.domElement);

  const scene = new Scene();
  scene.background = new Color(BG);
  scene.fog = new Fog(BG, 3, mobile ? 15 : 19);
  const camera = new PerspectiveCamera(mobile ? 62 : 52, 1, 0.1, 80);
  const rig = new Group(); rig.add(camera); scene.add(rig);

  const N = Math.max(8, posters.length), GAP = 5.2, START = -5;
  const W = 640, H = 360, R = 30;
  function roundRect(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function tex(img) {
    const c = document.createElement('canvas'); c.width = W; c.height = H; const g = c.getContext('2d');
    roundRect(g, 0, 0, W, H, R); g.fillStyle = '#1b1b22'; g.fill();
    g.save(); roundRect(g, 0, 0, W, H, R); g.clip();
    if (img) { const s = Math.max(W / img.width, H / img.height), dw = img.width * s, dh = img.height * s; g.drawImage(img, (W - dw) / 2, (H - dh) / 2, dw, dh); }
    g.restore();
    g.lineWidth = 6; g.strokeStyle = 'rgba(255,255,255,.85)'; roundRect(g, 3, 3, W - 6, H - 6, R - 3); g.stroke();
    const t = new CanvasTexture(c); t.colorSpace = SRGBColorSpace; t.anisotropy = 4; return t;
  }
  const geo = new PlaneGeometry(mobile ? 2.0 : 3.2, mobile ? 1.125 : 1.8);
  const planes = [], blank = tex(null);
  for (let i = 0; i < N; i++) {
    const m = new Mesh(geo, new MeshBasicMaterial({ map: blank, side: DoubleSide, transparent: true }));
    const side = i % 2 ? 1 : -1;
    m.position.set(side * (mobile ? 1.5 : 2.1), ((i % 3) - 1) * (mobile ? 0.7 : 0.45), START - i * GAP);
    m.rotation.y = -side * 0.32; m.rotation.z = side * 0.03;
    m.userData.base = m.position.clone();
    scene.add(m); planes.push(m);
  }
  posters.forEach((src, k) => { const img = new Image(); img.decoding = 'async'; img.onload = () => { const t = tex(img); planes.forEach((p, i) => { if (i % posters.length === k) { p.material.map = t; p.material.needsUpdate = true; } }); }; img.src = src; });

  /* streaks of light along the tunnel */
  const dot = document.createElement('canvas'); dot.width = dot.height = 64;
  const dg = dot.getContext('2d'); const gr = dg.createRadialGradient(32, 32, 0, 32, 32, 32);
  gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.35, 'rgba(255,255,255,.55)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); dg.fillStyle = gr; dg.fillRect(0, 0, 64, 64);
  const dotT = new CanvasTexture(dot);
  const LEN = N * GAP + 20;
  function field(n, color, size) {
    const pos = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) { const a = Math.random() * Math.PI * 2, r = 2.4 + Math.random() * 4.5; pos[i * 3] = Math.cos(a) * r; pos[i * 3 + 1] = Math.sin(a) * r * 0.7; pos[i * 3 + 2] = 4 - Math.random() * LEN; }
    const g = new BufferGeometry(); g.setAttribute('position', new Float32BufferAttribute(pos, 3));
    return new Points(g, new PointsMaterial({ color, size, map: dotT, transparent: true, depthWrite: false, blending: AdditiveBlending, opacity: .9 }));
  }
  scene.add(field(mobile ? 260 : 600, 0xff3347, 0.09), field(mobile ? 120 : 260, 0xffffff, 0.06), field(mobile ? 60 : 140, 0xf08a5d, 0.12));

  function resize() { const w = host.clientWidth || 1, h = host.clientHeight || 1; renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); }
  resize(); if ('ResizeObserver' in window) new ResizeObserver(resize).observe(host); else addEventListener('resize', resize);

  let target = 0, prog = 0, mx = 0, my = 0, tx = 0, ty = 0, t = 0, last = performance.now(), running = false, raf = 0;
  addEventListener('pointermove', e => { tx = (e.clientX / innerWidth - 0.5); ty = (e.clientY / innerHeight - 0.5); }, { passive: true });
  const endZ = START - (N - 1) * GAP + 3.2;
  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now; t += dt;
    prog += (target - prog) * 0.09; mx += (tx - mx) * 0.05; my += (ty - my) * 0.05;
    rig.position.z = 4 + (endZ - 4) * prog;
    rig.position.x = mx * 0.6; rig.position.y = -my * 0.35;
    camera.rotation.y = -mx * 0.12; camera.rotation.x = -my * 0.08;
    planes.forEach((p, i) => { p.position.y = p.userData.base.y + Math.sin(t * 0.8 + i) * 0.06; });
    renderer.render(scene, camera);
    if (running) raf = requestAnimationFrame(frame);
  }
  function play() { if (running) return; running = true; last = performance.now(); raf = requestAnimationFrame(frame); }
  function stop() { running = false; cancelAnimationFrame(raf); }
  let vis = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(es => { vis = es[0].isIntersecting; if (vis && !document.hidden) play(); else stop(); }).observe(host);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); else if (vis) play(); });
  renderer.render(scene, camera); play();
  host.classList.add('ready');
  return { count: N, setProgress(p) { target = Math.max(0, Math.min(1, p)); } };
}
