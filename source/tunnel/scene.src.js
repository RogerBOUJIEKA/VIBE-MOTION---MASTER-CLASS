import {
  WebGLRenderer, Scene, PerspectiveCamera, Group, PlaneGeometry, MeshBasicMaterial, CanvasTexture, SRGBColorSpace,
  BufferGeometry, Float32BufferAttribute, Points, PointsMaterial, CapsuleGeometry, MeshStandardMaterial, Mesh,
  AmbientLight, DirectionalLight, DoubleSide, AdditiveBlending, NormalBlending
} from 'three';

/* Hero scene: a ring of real video posters orbiting the Claude spark, with drifting particles.
   Reacts to the pointer and to scroll progress (0 = top of hero, 1 = hero scrolled away). */
export function start(host, opts) {
  const posters = opts.posters || [];
  const mobile = matchMedia('(max-width: 760px)').matches;
  let renderer;
  try {
    renderer = new WebGLRenderer({ antialias: !mobile, alpha: true, powerPreference: 'high-performance' });
  } catch (e) { return null; }
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, mobile ? 1.5 : 2));
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.setClearColor(0x000000, 0);
  host.appendChild(renderer.domElement);

  const scene = new Scene();
  const camera = new PerspectiveCamera(36, 1, 0.1, 100);
  camera.position.set(0, 0.9, 9.2);
  camera.lookAt(0, 0, 0);

  scene.add(new AmbientLight(0xffffff, 1.6));
  const key = new DirectionalLight(0xffffff, 2.2); key.position.set(3, 4, 6); scene.add(key);

  const world = new Group(); scene.add(world);
  const ring = new Group(); world.add(ring);
  ring.rotation.x = 0.16; ring.rotation.z = -0.1;

  /* cards: poster drawn on a canvas with rounded corners and a thin white frame */
  const W = 512, H = 288, R = 28;
  const cardGeo = new PlaneGeometry(1.75, 0.98);
  const count = mobile ? 10 : 14;
  const radius = 3.25;
  const cards = [];
  function roundRect(ctx, x, y, w, h, r) { ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r); ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath(); }
  function makeTexture(img) {
    const c = document.createElement('canvas'); c.width = W; c.height = H;
    const ctx = c.getContext('2d');
    roundRect(ctx, 0, 0, W, H, R); ctx.fillStyle = '#ffffff'; ctx.fill();
    ctx.save(); roundRect(ctx, 8, 8, W - 16, H - 16, R - 8); ctx.clip();
    if (img) {
      const s = Math.max((W - 16) / img.width, (H - 16) / img.height), dw = img.width * s, dh = img.height * s;
      ctx.drawImage(img, 8 + (W - 16 - dw) / 2, 8 + (H - 16 - dh) / 2, dw, dh);
    } else { ctx.fillStyle = '#f1f1f4'; ctx.fillRect(0, 0, W, H); }
    ctx.restore();
    const tex = new CanvasTexture(c); tex.colorSpace = SRGBColorSpace; tex.anisotropy = 4; return tex;
  }
  const blank = makeTexture(null);
  for (let i = 0; i < count; i++) {
    const m = new MeshBasicMaterial({ map: blank, transparent: true, side: DoubleSide });
    const mesh = new Mesh(cardGeo, m);
    const a = (i / count) * Math.PI * 2;
    mesh.position.set(Math.sin(a) * radius, 0, Math.cos(a) * radius);
    mesh.rotation.y = a;
    mesh.userData = { a, phase: Math.random() * Math.PI * 2 };
    ring.add(mesh); cards.push(mesh);
  }
  posters.forEach((src, k) => {
    const img = new Image(); img.decoding = 'async';
    img.onload = () => { const tex = makeTexture(img); cards.forEach((c, i) => { if (i % posters.length === k) { c.material.map = tex; c.material.needsUpdate = true; } }); };
    img.src = src;
  });

  /* Claude spark in the middle: 12 rounded rays */
  const spark = new Group(); world.add(spark);
  const rayMat = new MeshStandardMaterial({ color: 0xe07a56, roughness: 0.35, metalness: 0.1, emissive: 0x6a2a14, emissiveIntensity: 0.35 });
  for (let i = 0; i < 12; i++) {
    const len = i % 2 ? 0.62 : 0.82;
    const ray = new Mesh(new CapsuleGeometry(0.075, len, 6, 12), rayMat);
    const a = (i / 12) * Math.PI * 2 + 0.13;
    ray.position.set(Math.cos(a) * (0.2 + len / 2), Math.sin(a) * (0.2 + len / 2), 0);
    ray.rotation.z = a - Math.PI / 2;
    spark.add(ray);
  }
  spark.scale.setScalar(mobile ? 0.9 : 1);

  /* particles: soft round dots, red and white */
  const dot = document.createElement('canvas'); dot.width = dot.height = 64;
  const g = dot.getContext('2d'); const grd = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  grd.addColorStop(0, 'rgba(255,255,255,1)'); grd.addColorStop(0.4, 'rgba(255,255,255,.6)'); grd.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = grd; g.fillRect(0, 0, 64, 64);
  const dotTex = new CanvasTexture(dot);
  function cloud(n, color, size, spread, blending) {
    const pos = new Float32Array(n * 3);
    for (let i = 0; i < n; i++) {
      const r = spread * (0.35 + Math.random() * 0.65), th = Math.random() * Math.PI * 2, ph = (Math.random() - 0.5) * 1.4;
      pos[i * 3] = Math.cos(th) * r; pos[i * 3 + 1] = Math.sin(ph) * r * 0.55; pos[i * 3 + 2] = Math.sin(th) * r;
    }
    const geo = new BufferGeometry(); geo.setAttribute('position', new Float32BufferAttribute(pos, 3));
    const mat = new PointsMaterial({ color, size, map: dotTex, transparent: true, depthWrite: false, blending, opacity: 0.9 });
    return new Points(geo, mat);
  }
  const redDust = cloud(mobile ? 110 : 260, 0xe3061b, 0.11, 6.5, NormalBlending);
  const glow = cloud(mobile ? 50 : 120, 0xff8a6a, 0.16, 5, AdditiveBlending);
  world.add(redDust, glow);

  /* sizing */
  function resize() {
    const w = host.clientWidth || 1, h = host.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.fov = w / h < 1 ? 48 : 36;
    camera.updateProjectionMatrix();
  }
  resize();
  const ro = 'ResizeObserver' in window ? new ResizeObserver(resize) : null; if (ro) ro.observe(host); else addEventListener('resize', resize);

  /* input */
  let px = 0, py = 0, tx = 0, ty = 0, progress = 0, sp = 0;
  addEventListener('pointermove', e => { tx = (e.clientX / innerWidth - 0.5) * 2; ty = (e.clientY / innerHeight - 0.5) * 2; }, { passive: true });

  /* loop: only while visible */
  let running = false, raf = 0, last = performance.now(), t = 0;
  function frame(now) {
    const dt = Math.min(0.05, (now - last) / 1000); last = now; t += dt;
    px += (tx - px) * 0.05; py += (ty - py) * 0.05; sp += (progress - sp) * 0.08;
    ring.rotation.y += dt * (0.14 + sp * 0.5);
    world.rotation.y = px * 0.22; world.rotation.x = py * 0.1;
    const rad = 1 + sp * 0.45;
    cards.forEach(c => { const a = c.userData.a; c.position.x = Math.sin(a) * radius * rad; c.position.z = Math.cos(a) * radius * rad; c.position.y = Math.sin(t * 0.9 + c.userData.phase) * 0.08; });
    spark.rotation.z = -t * 0.35; spark.rotation.y = Math.sin(t * 0.5) * 0.25;
    const s = (mobile ? 0.9 : 1) * (1 + Math.sin(t * 1.6) * 0.03);
    spark.scale.setScalar(s);
    redDust.rotation.y = t * 0.03; glow.rotation.y = -t * 0.02; glow.position.y = Math.sin(t * 0.4) * 0.1;
    camera.position.z = 9.2 - sp * 2.2; camera.position.y = 0.9 + sp * 0.6; camera.lookAt(0, 0, 0);
    renderer.domElement.style.opacity = String(1 - Math.max(0, sp - 0.55) * 1.8);
    renderer.render(scene, camera);
    if (running) raf = requestAnimationFrame(frame);
  }
  function play() { if (running) return; running = true; last = performance.now(); raf = requestAnimationFrame(frame); }
  function stop() { running = false; cancelAnimationFrame(raf); }
  let visible = true;
  if ('IntersectionObserver' in window) new IntersectionObserver(es => { visible = es[0].isIntersecting; if (visible && !document.hidden) play(); else stop(); }).observe(host);
  document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); else if (visible) play(); });
  play();
  host.classList.add('ready');

  return { setProgress(p) { progress = Math.max(0, Math.min(1, p)); }, stop, play };
}
