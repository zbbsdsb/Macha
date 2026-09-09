import * as THREE from 'three';
import { rng, dustShell, glowDisc, pointsMaterial } from './_helpers.js';

/**
 * Scene 02 — Horizon / Industry Goals & Vision
 * Motif: a low sun over a plain studded with distant monoliths (the many
 * worlds). Thin threads link them: one standard, many engines.
 */
export default function create({ quality, reducedMotion }) {
  const group = new THREE.Group();
  const r = rng(88);
  const MONO = quality === 'low' ? 18 : 34;

  // --- ground -------------------------------------------------------------
  const groundGeo = new THREE.PlaneGeometry(400, 400, 60, 60);
  groundGeo.rotateX(-Math.PI / 2);
  const pa = groundGeo.attributes.position;
  for (let i = 0; i < pa.count; i++) {
    const x = pa.getX(i), z = pa.getZ(i);
    const d = Math.hypot(x, z);
    pa.setY(i, Math.sin(x * 0.06) * Math.cos(z * 0.05) * 1.3 * Math.min(1, d / 30));
  }
  groundGeo.computeVertexNormals();
  const groundMat = new THREE.MeshStandardMaterial({
    color: 0x352a3a,
    roughness: 0.95,
    metalness: 0.05,
    transparent: true,
    opacity: 0.9,
    wireframe: true,
  });
  const ground = new THREE.Mesh(groundGeo, groundMat);
  ground.position.y = -10;
  group.add(ground);

  // --- monoliths ----------------------------------------------------------
  const monoMat = new THREE.MeshStandardMaterial({
    color: 0x241d26,
    roughness: 0.8,
    metalness: 0.2,
    transparent: true,
    opacity: 0.95,
    emissive: 0x3a2418,
    emissiveIntensity: 0.35,
  });
  const monoliths = new THREE.InstancedMesh(new THREE.BoxGeometry(1, 1, 1), monoMat, MONO);
  const m4 = new THREE.Matrix4();
  const q = new THREE.Quaternion();
  const e = new THREE.Euler();
  const pv = new THREE.Vector3();
  const sv = new THREE.Vector3();
  for (let i = 0; i < MONO; i++) {
    const a = r() * Math.PI * 2;
    const rad = 26 + r() * 56;
    const h = 8 + r() * 46;
    const w = 3 + r() * 7;
    pv.set(Math.cos(a) * rad, -10 + h / 2, Math.sin(a) * rad);
    e.set(0, r() * Math.PI, (r() - 0.5) * 0.06);
    q.setFromEuler(e);
    sv.set(w, h, w * (0.6 + r() * 0.8));
    m4.compose(pv, q, sv);
    monoliths.setMatrixAt(i, m4);
  }
  monoliths.instanceMatrix.needsUpdate = true;
  group.add(monoliths);

  // --- threads linking the worlds ----------------------------------------
  const threadPts = [];
  const anchors = [];
  for (let i = 0; i < 12; i++) {
    const a = (i / 12) * Math.PI * 2 + r() * 0.2;
    anchors.push(new THREE.Vector3(Math.cos(a) * (30 + r() * 44), 2 + r() * 16, Math.sin(a) * (30 + r() * 44)));
  }
  for (let i = 0; i < anchors.length; i++) {
    const a = anchors[i], b = anchors[(i + 1) % anchors.length];
    const seg = 12;
    for (let s = 0; s < seg; s++) {
      const t0 = s / seg, t1 = (s + 1) / seg;
      const p0 = a.clone().lerp(b, t0);
      const p1 = a.clone().lerp(b, t1);
      const arc = Math.sin(t0 * Math.PI) * 6;
      p0.y += arc; p1.y += Math.sin(t1 * Math.PI) * 6;
      threadPts.push(p0.x, p0.y, p0.z, p1.x, p1.y, p1.z);
    }
  }
  const threadGeo = new THREE.BufferGeometry();
  threadGeo.setAttribute('position', new THREE.Float32BufferAttribute(threadPts, 3));
  const threadMat = new THREE.LineBasicMaterial({
    color: 0xffb37a, transparent: true, opacity: 0.22, depthWrite: false,
  });
  const threads = new THREE.LineSegments(threadGeo, threadMat);
  group.add(threads);

  // --- sun + light shafts -------------------------------------------------
  const sun = glowDisc(14, 0xffc48a, 0.85);
  sun.position.set(0, -1.5, -62);
  group.add(sun);

  const halo = glowDisc(34, 0xff9a4d, 0.16);
  halo.position.copy(sun.position).setZ(-63);
  group.add(halo);

  const shaftMat = new THREE.MeshBasicMaterial({
    color: 0xffc48a,
    transparent: true,
    opacity: 0.07,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    side: THREE.DoubleSide,
  });
  const shafts = new THREE.Group();
  for (let i = 0; i < 7; i++) {
    const w = 1.6 + r() * 5;
    const g = new THREE.PlaneGeometry(w, 110);
    const m = new THREE.Mesh(g, shaftMat);
    m.position.set((r() - 0.5) * 70, 20, -60 + r() * 6);
    m.rotation.z = (r() - 0.5) * 0.16;
    shafts.add(m);
  }
  group.add(shafts);

  const dust = dustShell({ count: quality === 'low' ? 200 : 480, radius: 60, color: 0xffc48a, size: 0.26, opacity: 0.4, seed: 12 });
  dust.position.y = 4;
  group.add(dust);

  const embers = new THREE.Points(
    (() => {
      const n = quality === 'low' ? 90 : 220;
      const p = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) {
        p[i * 3] = (r() - 0.5) * 120;
        p[i * 3 + 1] = -10 + r() * 46;
        p[i * 3 + 2] = (r() - 0.5) * 120;
      }
      const g = new THREE.BufferGeometry();
      g.setAttribute('position', new THREE.BufferAttribute(p, 3));
      return g;
    })(),
    pointsMaterial(0xffd9a8, 0.2, 0.55)
  );
  group.add(embers);

  return {
    group,
    focus: new THREE.Vector3(0, 4, -46),
    env: {
      bg: 0x1a1318,
      fog: 0x2a1c1c,
      fogDensity: 0.0088,
      hemiSky: 0xffb37a,
      hemiGround: 0x1a1013,
      hemi: 0.9,
      key: 0xffc48a,
      keyIntensity: 1.35,
      exposure: 1.16,
      bloom: 0.5,
      accent: '#FFB37A',
    },
    update(dt, t, reveal) {
      const v = reveal * reveal;
      group.visible = v > 0.002;
      if (!group.visible) return;
      groundMat.opacity = 0.9 * v;
      monoMat.opacity = 0.95 * v;
      threadMat.opacity = 0.22 * v;
      sun.material.opacity = 0.85 * v;
      halo.material.opacity = 0.14 * v;
      shaftMat.opacity = 0.05 * v;
      dust.material.opacity = 0.4 * v;
      embers.material.opacity = 0.55 * v;

      if (!reducedMotion) {
        group.rotation.y = Math.sin(t * 0.06) * 0.03;
        sun.position.y = -1.5 + Math.sin(t * 0.18) * 0.6;
        halo.position.y = sun.position.y;
        dust.rotation.y += dt * 0.008;
        const arr = embers.geometry.attributes.position.array;
        for (let i = 1; i < arr.length; i += 3) {
          arr[i] += dt * (0.4 + (i % 7) * 0.05);
          if (arr[i] > 40) arr[i] = -10;
        }
        embers.geometry.attributes.position.needsUpdate = true;
      }
    },
    dispose() {
      groundGeo.dispose(); groundMat.dispose();
      threadGeo.dispose(); threadMat.dispose();
      embers.geometry.dispose(); embers.material.dispose();
    },
  };
}
