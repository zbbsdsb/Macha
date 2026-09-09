import * as THREE from 'three';
import { SCENES } from './scenes/index.js';
import { Rig, smoothstep, clamp, damp } from './rig.js';
import { applyLang, getLang, setLang, onLangChange } from './i18n.js';
import { NAV_LABELS, STACKS } from './content.js';

const SPACING = 62;   // world units between scene anchors
const DEPTH = 14;     // how far in front of the anchor each stage is centred
const START = -0.45;  // boot glide-in start offset

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const isSmall = window.matchMedia('(max-width: 820px)').matches;
const quality = isSmall || (navigator.hardwareConcurrency || 8) <= 4 ? 'low' : 'high';
const fxEnabled = !new URLSearchParams(location.search).has('nofx') && quality === 'high' && !reducedMotion;

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));

// ---------------------------------------------------------------- renderer
const canvas = $('#gl');
let renderer;
try {
  renderer = new THREE.WebGLRenderer({
    canvas,
    antialias: quality === 'high',
    powerPreference: 'high-performance',
    alpha: false,
  });
} catch (err) {
  renderer = null;
}

if (!renderer) {
  document.body.classList.add('no-webgl');
  $('#boot')?.classList.add('is-hidden');
  $('.fallback-note')?.removeAttribute('hidden');
} else {
  // A failure inside boot() must never leave a dead black screen. If the 3D
  // space can't start, drop to the readable text route instead.
  try {
    boot();
  } catch (err) {
    console.error('[macha] 3D space failed to start — falling back to text route', err);
    document.body.classList.add('no-webgl');
    $('#boot')?.classList.add('is-hidden');
    $('.fallback-note')?.removeAttribute('hidden');
  }
}

function boot() {
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1;
  renderer.outputColorSpace = THREE.SRGBColorSpace;

  const scene = new THREE.Scene();
  const bg = new THREE.Color(0x000000);
  scene.background = bg;
  scene.fog = new THREE.FogExp2(0x000000, 0.03);

  const camera = new THREE.PerspectiveCamera(
    58, window.innerWidth / window.innerHeight, 0.1, 600
  );

  // global atmosphere — one fog, one light rig. This is what makes the
  // transitions continuous instead of a hard cut between worlds.
  const hemi = new THREE.HemisphereLight(0xffffff, 0x000000, 0.6);
  scene.add(hemi);
  const key = new THREE.DirectionalLight(0xffffff, 1.1);
  const keyTarget = new THREE.Object3D();
  scene.add(key, keyTarget);
  key.target = keyTarget;
  const KEY_OFFSET = new THREE.Vector3(-8, 12, 10);
  const fill = new THREE.DirectionalLight(0xffffff, 0.25);
  scene.add(fill);
  fill.target = keyTarget;

  // ------------------------------------------------------------ build stages
  const anchors = Rig.buildAnchors(SCENES.length, SPACING);
  const rig = new Rig(anchors);

  const stages = SCENES.map((entry, i) => {
    const s = entry.factory({ quality, reducedMotion });
    scene.add(s.group);
    const focus = new THREE.Vector3();
    const env = {
      bg: new THREE.Color(s.env.bg),
      fog: new THREE.Color(s.env.fog),
      fogDensity: s.env.fogDensity,
      hemiSky: new THREE.Color(s.env.hemiSky),
      hemiGround: new THREE.Color(s.env.hemiGround),
      hemi: s.env.hemi,
      key: new THREE.Color(s.env.key),
      keyIntensity: s.env.keyIntensity,
      exposure: s.env.exposure,
      bloom: s.env.bloom ?? 0.55,
      accent: new THREE.Color(s.env.accent),
    };
    return { ...entry, api: s, focus, env, reveal: 0 };
  });

  // On wide screens the copy sits in a right-hand column, so push the 3D
  // content left to keep the stage centre clear of the text.
  function layoutStages() {
    const lateral = window.innerWidth > 1024 ? -3.6 : 0;
    stages.forEach((st, i) => {
      st.api.group.position.set(
        anchors[i].x * 0.25 + lateral,
        anchors[i].y * 0.25,
        anchors[i].z - DEPTH
      );
      st.focus.copy(st.api.group.position).add(st.api.focus);
    });
  }
  layoutStages();

  // ------------------------------------------------------------- env lerper
  const cur = {
    bg: new THREE.Color(), fog: new THREE.Color(), hemiSky: new THREE.Color(),
    hemiGround: new THREE.Color(), key: new THREE.Color(), accent: new THREE.Color(),
    fogDensity: 0.03, hemi: 0.6, keyIntensity: 1, exposure: 1, bloom: 0.55,
  };
  const lerpEnv = (a, b, t) => {
    cur.bg.lerpColors(a.bg, b.bg, t);
    cur.fog.lerpColors(a.fog, b.fog, t);
    cur.hemiSky.lerpColors(a.hemiSky, b.hemiSky, t);
    cur.hemiGround.lerpColors(a.hemiGround, b.hemiGround, t);
    cur.key.lerpColors(a.key, b.key, t);
    cur.accent.lerpColors(a.accent, b.accent, t);
    cur.fogDensity = a.fogDensity + (b.fogDensity - a.fogDensity) * t;
    cur.hemi = a.hemi + (b.hemi - a.hemi) * t;
    cur.keyIntensity = a.keyIntensity + (b.keyIntensity - a.keyIntensity) * t;
    cur.exposure = a.exposure + (b.exposure - a.exposure) * t;
    cur.bloom = a.bloom + (b.bloom - a.bloom) * t;
  };

  // --------------------------------------------------------------- post fx
  let composer = null;
  let bloomPass = null;
  if (fxEnabled) {
    Promise.all([
      import('three/addons/postprocessing/EffectComposer.js'),
      import('three/addons/postprocessing/RenderPass.js'),
      import('three/addons/postprocessing/UnrealBloomPass.js'),
      import('three/addons/postprocessing/OutputPass.js'),
    ]).then(([EC, RP, BP, OP]) => {
      const c = new EC.EffectComposer(renderer);
      c.addPass(new RP.RenderPass(scene, camera));
      bloomPass = new BP.UnrealBloomPass(
        new THREE.Vector2(window.innerWidth, window.innerHeight), 0.55, 0.9, 0.2
      );
      c.addPass(bloomPass);
      c.addPass(new OP.OutputPass());
      c.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.75));
      c.setSize(window.innerWidth, window.innerHeight);
      composer = c;
    }).catch((e) => {
      console.warn('[macha] post-processing unavailable — direct render', e);
      composer = null;
    });
  }

  // ------------------------------------------------------------------- state
  let p = START;
  let target = START;
  let lastInput = -1e9;
  let entered = false;

  const camPos = new THREE.Vector3();
  const lookAt = new THREE.Vector3();
  const tmpA = new THREE.Vector3();
  const tmpB = new THREE.Vector3();
  const parallax = new THREE.Vector2();
  const parallaxTarget = new THREE.Vector2();

  // -------------------------------------------------------------- DOM refs
  const panels = $$('.panel');
  const dots = $$('.dot');
  const bar = $('#progress-fill');
  const sceneNo = $('#scene-no');
  const sceneName = $('#scene-name');
  const readout = $('#cam-readout');
  const accentStyle = document.documentElement.style;

  // ----------------------------------------------------------------- inputs
  const MAXP = SCENES.length - 1 + 0.2;
  const setTarget = (v) => { target = clamp(v, START, MAXP); lastInput = performance.now(); };

  const normWheel = (e) => {
    let d = e.deltaY;
    if (e.deltaMode === 1) d *= 16;        // lines
    else if (e.deltaMode === 2) d *= 100;  // pages
    return d;
  };

  const onWheel = (e) => {
    if (!entered) return;
    // let long scene copy scroll natively when the cursor is over the panel
    if (e.target instanceof Element && e.target.closest('.panel.is-active')) return;
    e.preventDefault();
    setTarget(target + normWheel(e) * 0.0016);
  };
  window.addEventListener('wheel', onWheel, { passive: false });

  // drag / swipe
  let dragging = false;
  let dragY = 0;
  let dragStartTarget = 0;
  canvas.addEventListener('pointerdown', (e) => {
    dragging = true; dragY = e.clientY; dragStartTarget = target;
    canvas.setPointerCapture?.(e.pointerId);
    canvas.classList.add('is-grabbing');
  });
  window.addEventListener('pointermove', (e) => {
    if (dragging && entered) {
      setTarget(dragStartTarget + (dragY - e.clientY) * 0.0055);
    }
    if (!reducedMotion) {
      parallaxTarget.set(
        (e.clientX / window.innerWidth - 0.5) * 2,
        (e.clientY / window.innerHeight - 0.5) * 2
      );
    }
  });
  window.addEventListener('pointerup', (e) => {
    dragging = false;
    canvas.releasePointerCapture?.(e.pointerId);
    canvas.classList.remove('is-grabbing');
  });
  window.addEventListener('pointercancel', () => { dragging = false; canvas.classList.remove('is-grabbing'); });

  window.addEventListener('keydown', (e) => {
    if (!entered) return;
    if (e.target instanceof HTMLInputElement) return;
    const step = () => setTarget(Math.round(target) + (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ' ? 1 : -1));
    switch (e.key) {
      case 'ArrowRight': case 'ArrowDown': case ' ': e.preventDefault(); step(); break;
      case 'ArrowLeft': case 'ArrowUp': e.preventDefault(); step(); break;
      case 'PageDown': setTarget(Math.round(target) + 1); break;
      case 'PageUp': setTarget(Math.round(target) - 1); break;
      case 'Home': setTarget(0); break;
      case 'End': setTarget(SCENES.length - 1); break;
      case 'l': case 'L': toggleLang(); break;
      default: {
        const n = Number(e.key);
        if (n >= 1 && n <= SCENES.length) setTarget(n - 1);
      }
    }
  });

  $('#prev')?.addEventListener('click', () => setTarget(Math.round(target) - 1));
  $('#next')?.addEventListener('click', () => setTarget(Math.round(target) + 1));
  dots.forEach((d, i) => d.addEventListener('click', () => setTarget(i)));

  const toggleLang = () => setLang(getLang() === 'en' ? 'zh' : 'en');
  $$('.lang-btn').forEach((b) => b.addEventListener('click', () => setLang(b.dataset.lang)));

  // ------------------------------------------------------------------- boot
  const bootEl = $('#boot');
  const enterBtn = $('#boot-enter');
  const enter = () => {
    if (entered) return;
    entered = true;
    document.body.classList.add('is-entered');
    bootEl.classList.add('is-hidden');
    setTimeout(() => bootEl.remove(), 900);
    setTarget(0);
  };
  enterBtn?.addEventListener('click', enter);
  bootEl?.addEventListener('click', (e) => { if (e.target === bootEl) enter(); });
  window.addEventListener('keydown', (e) => { if (!entered && (e.key === 'Enter' || e.key === ' ')) enter(); });

  // ----------------------------------------------------------------- resize
  const onResize = () => {
    const w = window.innerWidth, h = window.innerHeight;
    camera.aspect = w / h;
    // widen the lens a little on portrait so content still fits
    camera.fov = h > w ? 68 : 58;
    camera.updateProjectionMatrix();
    renderer.setSize(w, h);
    composer?.setSize(w, h);
    layoutStages();
  };
  window.addEventListener('resize', onResize);
  onResize();

  // ------------------------------------------------------------------- loop
  const clock = new THREE.Clock();
  let fpsAcc = 0, fpsFrames = 0, fps = 0, running = true, raf = 0;

  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { running = false; cancelAnimationFrame(raf); }
    else if (!running) { running = true; clock.getDelta(); raf = requestAnimationFrame(frame); }
  });

  function frame() {
    raf = requestAnimationFrame(frame);
    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;

    // --- idle snap: settle onto the nearest scene once the user stops ------
    if (entered && performance.now() - lastInput > 700) {
      const nearest = clamp(Math.round(target), 0, SCENES.length - 1);
      if (Math.abs(target - nearest) > 0.001 && Math.abs(target - nearest) < 0.5) target = nearest;
    }

    p = damp(p, target, 3.1, dt);
    parallax.x = damp(parallax.x, parallaxTarget.x, 2.4, dt);
    parallax.y = damp(parallax.y, parallaxTarget.y, 2.4, dt);

    // --- camera -----------------------------------------------------------
    rig.positionAt(p, camPos);
    if (!reducedMotion) {
      // parallax in camera-local space, so it reads as a head movement
      tmpA.set(parallax.x * 1.15, -parallax.y * 0.75, 0).applyQuaternion(camera.quaternion);
      camPos.add(tmpA);
    }
    camPos.y += Math.sin(t * 0.55) * 0.16;   // idle breathing
    camera.position.copy(camPos);

    let i = Math.floor(p);
    if (i < 0) i = 0;
    if (i > SCENES.length - 2) i = SCENES.length - 2;
    const f = smoothstep(clamp(p - i, 0, 1));
    lookAt.copy(stages[i].focus).lerp(stages[i + 1].focus, f);
    camera.lookAt(lookAt);
    camera.rotation.z += parallax.x * 0.012;

    // --- atmosphere -------------------------------------------------------
    lerpEnv(stages[i].env, stages[i + 1].env, f);
    bg.copy(cur.bg);
    scene.fog.color.copy(cur.fog);
    scene.fog.density = cur.fogDensity;
    hemi.color.copy(cur.hemiSky);
    hemi.groundColor.copy(cur.hemiGround);
    hemi.intensity = cur.hemi;
    key.color.copy(cur.key);
    key.intensity = cur.keyIntensity;
    fill.color.copy(cur.key);
    key.position.copy(camPos).add(KEY_OFFSET);
    keyTarget.position.copy(camPos);
    fill.position.copy(camPos).add(tmpB.set(6, -6, -12));
    renderer.toneMappingExposure = cur.exposure;
    if (bloomPass) bloomPass.strength = cur.bloom;
    accentStyle.setProperty('--accent', `#${cur.accent.getHexString()}`);

    // --- stages -----------------------------------------------------------
    for (let k = 0; k < stages.length; k++) {
      const st = stages[k];
      const raw = 1 - Math.abs(p - k) / 1.15;
      st.reveal = smoothstep(raw);
      st.api.update(dt, t, st.reveal);
      const panel = panels[k];
      if (panel) {
        panel.style.setProperty('--r', st.reveal.toFixed(3));
        // Text uses a much steeper window than the 3D stage. If both used the
        // same curve, the outgoing scene's copy would sit at ~8% opacity
        // underneath the incoming scene's copy and read as a ghost double-exposure.
        const textR = smoothstep((st.reveal - 0.42) / 0.4);
        panel.style.opacity = textR.toFixed(3);
        panel.classList.toggle('is-active', st.reveal > 0.55);
        panel.setAttribute('aria-hidden', st.reveal > 0.02 ? 'false' : 'true');
      }
      dots[k]?.classList.toggle('is-active', Math.abs(p - k) < 0.5);
    }

    // --- hud --------------------------------------------------------------
    const span = SCENES.length - 1 - START + 0.2;
    if (bar) bar.style.transform = `scaleX(${clamp((p - START) / span, 0, 1).toFixed(4)})`;
    const near = clamp(Math.round(p), 0, SCENES.length - 1);
    if (sceneNo) sceneNo.textContent = String(near + 1).padStart(2, '0');
    if (sceneName) sceneName.textContent = NAV_LABELS[near][getLang()];
    if (readout) {
      fpsAcc += dt; fpsFrames++;
      if (fpsAcc > 0.4) { fps = Math.round(fpsFrames / fpsAcc); fpsAcc = 0; fpsFrames = 0; }
      readout.textContent =
        `POS ${camPos.x.toFixed(1)} ${camPos.y.toFixed(1)} ${camPos.z.toFixed(0)}` +
        `  ·  FOV ${camera.fov.toFixed(0)}  ·  T ${p.toFixed(2)}  ·  ${fps} FPS`;
    }

    if (composer) composer.render();
    else renderer.render(scene, camera);
  }

  raf = requestAnimationFrame(frame);
}

// ------------------------------------------------------------ dynamic copy
function renderDynamic() {
  const lang = getLang();
  // nav labels
  $$('.dot').forEach((d, i) => {
    const label = d.querySelector('.dot-label');
    if (label && NAV_LABELS[i]) label.textContent = NAV_LABELS[i][lang];
    const num = d.querySelector('.dot-num');
    if (num) num.textContent = String(i + 1).padStart(2, '0');
  });
  // structure chips on the pending scenes
  Object.entries(STACKS).forEach(([id, items]) => {
    const host = document.querySelector(`[data-stack="${id}"]`);
    if (!host) return;
    host.innerHTML = '';
    items.forEach((it) => {
      const li = document.createElement('li');
      li.className = 'chip';
      li.innerHTML =
        `<span class="chip-k">${it.k}</span><span class="chip-v"></span>`;
      li.querySelector('.chip-v').textContent = it[lang];
      host.appendChild(li);
    });
  });
}

// ------------------------------------------------------------------- init
applyLang();
renderDynamic();
onLangChange(renderDynamic);
