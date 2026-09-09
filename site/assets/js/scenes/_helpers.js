import * as THREE from 'three';

/** Deterministic PRNG so the layout is identical on every load. */
export function rng(seed = 1) {
  let s = seed >>> 0 || 1;
  return () => {
    s ^= s << 13; s >>>= 0;
    s ^= s >> 17;
    s ^= s << 5; s >>>= 0;
    return s / 4294967296;
  };
}

/** Soft round sprite used for every particle system on the site. */
let _sprite = null;
export function dotTexture() {
  if (_sprite) return _sprite;
  const c = document.createElement('canvas');
  c.width = c.height = 64;
  const g = c.getContext('2d');
  const grad = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  grad.addColorStop(0, 'rgba(255,255,255,1)');
  grad.addColorStop(0.35, 'rgba(255,255,255,0.55)');
  grad.addColorStop(1, 'rgba(255,255,255,0)');
  g.fillStyle = grad;
  g.fillRect(0, 0, 64, 64);
  _sprite = new THREE.CanvasTexture(c);
  _sprite.colorSpace = THREE.SRGBColorSpace;
  return _sprite;
}

export function pointsMaterial(color, size, opacity = 1) {
  return new THREE.PointsMaterial({
    color,
    size,
    map: dotTexture(),
    transparent: true,
    opacity,
    depthWrite: false,
    blending: THREE.AdditiveBlending,
    sizeAttenuation: true,
  });
}

/** Nebula / dust shell: points scattered in a spherical shell. */
export function dustShell({ count, radius, inner = 0.35, color, size, opacity = 0.8, seed = 7 }) {
  const r = rng(seed);
  const pos = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    const u = r() * 2 - 1;
    const th = r() * Math.PI * 2;
    const rad = radius * (inner + (1 - inner) * Math.cbrt(r()));
    const s = Math.sqrt(1 - u * u);
    pos[i * 3] = rad * s * Math.cos(th);
    pos[i * 3 + 1] = rad * u * 0.7;
    pos[i * 3 + 2] = rad * s * Math.sin(th);
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  return new THREE.Points(geo, pointsMaterial(color, size, opacity));
}

/** Fading ground grid — the cheapest way to give a scene a floor plane. */
export function gridFloor({ size = 160, divisions = 40, color = 0x2b3550, y = -8 }) {
  const g = new THREE.GridHelper(size, divisions, color, color);
  g.position.y = y;
  g.material.transparent = true;
  g.material.opacity = 0.22;
  g.material.depthWrite = false;
  return g;
}

/** Ring of thin "card" monoliths around the camera. */
export function cardRing({ count, radius, w = 3.2, h = 4.6, d = 0.22, color, seed = 3, y = 0 }) {
  const group = new THREE.Group();
  const geo = new THREE.BoxGeometry(w, h, d);
  const mat = new THREE.MeshStandardMaterial({
    color,
    roughness: 0.55,
    metalness: 0.1,
    transparent: true,
    opacity: 0.55,
    emissive: new THREE.Color(color).multiplyScalar(0.12),
  });
  const mesh = new THREE.InstancedMesh(geo, mat, count);
  const m = new THREE.Matrix4();
  const q = new THREE.Quaternion();
  const e = new THREE.Euler();
  const pos = new THREE.Vector3();
  const scl = new THREE.Vector3(1, 1, 1);
  const r = rng(seed);
  for (let i = 0; i < count; i++) {
    const a = (i / count) * Math.PI * 2;
    pos.set(Math.cos(a) * radius, y + (r() - 0.5) * 1.6, Math.sin(a) * radius);
    e.set(0, -a + Math.PI / 2, (r() - 0.5) * 0.12);
    q.setFromEuler(e);
    const s = 0.8 + r() * 0.45;
    scl.set(s, s, s);
    m.compose(pos, q, scl);
    mesh.setMatrixAt(i, m);
  }
  mesh.instanceMatrix.needsUpdate = true;
  group.add(mesh);
  group.userData.mat = mat;
  return group;
}

/** Nested torus tunnel. */
export function tunnelRings({ count, radius, spacing, color, thickness = 0.09, seed = 11 }) {
  const group = new THREE.Group();
  const r = rng(seed);
  const mat = new THREE.MeshStandardMaterial({
    color,
    emissive: new THREE.Color(color).multiplyScalar(0.5),
    roughness: 0.4,
    metalness: 0.3,
    transparent: true,
    opacity: 0.8,
  });
  for (let i = 0; i < count; i++) {
    const rad = radius * (0.45 + (i / count) * 0.85);
    const geo = new THREE.TorusGeometry(rad, thickness + r() * 0.03, 8, 64);
    const m = new THREE.Mesh(geo, mat);
    m.position.z = -i * spacing;
    m.rotation.z = r() * Math.PI;
    group.add(m);
  }
  group.userData.mat = mat;
  return group;
}

/** Vertical particle stream that wraps — used for "data flowing upward". */
export function flowStream({ count, radius, height, color, size = 0.16, speed = 2, seed = 21 }) {
  const r = rng(seed);
  const pos = new Float32Array(count * 3);
  const spd = new Float32Array(count);
  for (let i = 0; i < count; i++) {
    const a = r() * Math.PI * 2;
    const rad = radius * (0.25 + r() * 0.75);
    pos[i * 3] = Math.cos(a) * rad;
    pos[i * 3 + 1] = -height / 2 + r() * height;
    pos[i * 3 + 2] = Math.sin(a) * rad;
    spd[i] = 0.5 + r();
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const pts = new THREE.Points(geo, pointsMaterial(color, size, 0.9));
  pts.userData = { spd, height, speed };
  return pts;
}

export function updateFlowStream(pts, dt) {
  const { spd, height, speed } = pts.userData;
  const arr = pts.geometry.attributes.position.array;
  for (let i = 0; i < spd.length; i++) {
    let y = arr[i * 3 + 1] + spd[i] * speed * dt;
    if (y > height / 2) y -= height;
    arr[i * 3 + 1] = y;
  }
  pts.geometry.attributes.position.needsUpdate = true;
}

/** Additive glow disc (sun, portal, core). */
export function glowDisc(radius, color, opacity = 0.9) {
  const mat = new THREE.MeshBasicMaterial({
    color,
    transparent: true,
    opacity,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    side: THREE.DoubleSide,
  });
  return new THREE.Mesh(new THREE.CircleGeometry(radius, 64), mat);
}

/** Dispose everything under an object3d. */
export function disposeTree(root) {
  root.traverse((o) => {
    if (o.geometry) o.geometry.dispose();
    if (o.material) {
      const mats = Array.isArray(o.material) ? o.material : [o.material];
      mats.forEach((m) => m.dispose());
    }
  });
}
