import * as THREE from 'three';
import { gridFloor, dustShell, pointsMaterial, rng } from './_helpers.js';

/**
 * Scene 05 — Field / Application Plan   [stage only, copy pending]
 * Motif: a surveyed grid with three empty pedestals waiting for the
 * experimental worlds. Markers float above each, linked by dashed survey lines.
 */
export default function create({ quality, reducedMotion }) {
  const group = new THREE.Group();
  const r = rng(2026);
  const SLOTS = 3;

  const floor = gridFloor({ size: 220, divisions: 44, color: 0x2f4a18, y: -8 });
  group.add(floor);

  // survey sweep line
  const sweepMat = new THREE.MeshBasicMaterial({
    color: 0xa3e635, transparent: true, opacity: 0.14, side: THREE.DoubleSide, depthWrite: false,
  });
  const sweep = new THREE.Mesh(new THREE.PlaneGeometry(220, 3.5), sweepMat);
  sweep.rotation.x = -Math.PI / 2;
  sweep.position.y = -7.9;
  group.add(sweep);

  // --- three empty pedestals ---------------------------------------------
  const pedestalMat = new THREE.MeshStandardMaterial({
    color: 0x1f2a14,
    emissive: 0x2f4a18,
    emissiveIntensity: 0.6,
    roughness: 0.7,
    metalness: 0.2,
    transparent: true,
    opacity: 0.9,
  });
  const slotMat = new THREE.MeshStandardMaterial({
    color: 0xa3e635,
    emissive: 0xa3e635,
    emissiveIntensity: 0.9,
    roughness: 0.3,
    transparent: true,
    opacity: 0.6,
    wireframe: true,
  });
  const ringMat = new THREE.MeshBasicMaterial({ color: 0xa3e635, transparent: true, opacity: 0.5 });

  const slots = [];
  for (let i = 0; i < SLOTS; i++) {
    const g = new THREE.Group();
    const x = (i - (SLOTS - 1) / 2) * 17;

    const base = new THREE.Mesh(new THREE.CylinderGeometry(5.2, 6.2, 1.4, 6), pedestalMat);
    base.position.set(x, -7.4, 0);
    g.add(base);

    // empty mount: a wireframe volume waiting for a world
    const mount = new THREE.Mesh(new THREE.BoxGeometry(6.4, 6.4, 6.4), slotMat);
    mount.position.set(x, -2.6, 0);
    mount.userData.phase = i * 1.4;
    g.add(mount);

    const haloRing = new THREE.Mesh(new THREE.TorusGeometry(4.6, 0.06, 8, 72), ringMat);
    haloRing.rotation.x = Math.PI / 2;
    haloRing.position.set(x, -7.2, 0);
    haloRing.userData.phase = i * 0.9;
    g.add(haloRing);

    // floating marker
    const markerMat = new THREE.MeshBasicMaterial({ color: 0xd9ff8a, transparent: true, opacity: 0.85 });
    const marker = new THREE.Mesh(new THREE.OctahedronGeometry(0.6, 0), markerMat);
    marker.position.set(x, 5.6, 0);
    marker.userData.phase = i * 2.0;
    g.add(marker);

    // dashed tether from marker down to the mount
    const tether = new THREE.Mesh(
      new THREE.CylinderGeometry(0.025, 0.025, 6, 5),
      new THREE.MeshBasicMaterial({ color: 0xa3e635, transparent: true, opacity: 0.28 })
    );
    tether.position.set(x, 2.2, 0);
    g.add(tether);

    group.add(g);
    slots.push({ mount, haloRing, marker, tether });
  }

  // --- voxel debris (the "sandbox" hint) ----------------------------------
  const voxelGeo = new THREE.BoxGeometry(1, 1, 1);
  const voxelMat = new THREE.MeshStandardMaterial({
    color: 0x4d7c1f, roughness: 0.85, metalness: 0.05, transparent: true, opacity: 0.55,
  });
  const VC = quality === 'low' ? 90 : 240;
  const voxels = new THREE.InstancedMesh(voxelGeo, voxelMat, VC);
  const m4 = new THREE.Matrix4();
  const q = new THREE.Quaternion();
  const e = new THREE.Euler();
  const pv = new THREE.Vector3();
  const sv = new THREE.Vector3();
  for (let i = 0; i < VC; i++) {
    const a = r() * Math.PI * 2;
    const rad = 16 + r() * 70;
    pv.set(Math.cos(a) * rad, -7 + r() * 22, Math.sin(a) * rad);
    e.set(r() * 0.4, r() * Math.PI, r() * 0.4);
    q.setFromEuler(e);
    const s = 0.6 + r() * 2.6;
    sv.set(s, s, s);
    m4.compose(pv, q, sv);
    voxels.setMatrixAt(i, m4);
  }
  voxels.instanceMatrix.needsUpdate = true;
  group.add(voxels);

  // --- survey points scattered across the grid ---------------------------
  const n = quality === 'low' ? 120 : 300;
  const sp = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    sp[i * 3] = (r() - 0.5) * 180;
    sp[i * 3 + 1] = -7.6;
    sp[i * 3 + 2] = (r() - 0.5) * 180;
  }
  const spGeo = new THREE.BufferGeometry();
  spGeo.setAttribute('position', new THREE.BufferAttribute(sp, 3));
  const surveyPts = new THREE.Points(spGeo, pointsMaterial(0xc7f284, 0.16, 0.5));
  group.add(surveyPts);

  const dust = dustShell({ count: quality === 'low' ? 160 : 400, radius: 55, color: 0xd9ff8a, size: 0.2, opacity: 0.3, seed: 66 });
  group.add(dust);

  return {
    group,
    focus: new THREE.Vector3(0, -1, -6),
    env: {
      bg: 0x0a1206,
      fog: 0x0f1c09,
      fogDensity: 0.020,
      hemiSky: 0x4d7c1f,
      hemiGround: 0x060a04,
      hemi: 0.6,
      key: 0xd9ff8a,
      keyIntensity: 1.1,
      exposure: 1.02,
      accent: '#A3E635',
    },
    update(dt, t, reveal) {
      const v = reveal * reveal;
      group.visible = v > 0.002;
      if (!group.visible) return;

      floor.material.opacity = 0.22 * v;
      sweepMat.opacity = 0.14 * v;
      pedestalMat.opacity = 0.9 * v;
      voxelMat.opacity = 0.55 * v;
      surveyPts.material.opacity = 0.5 * v;
      dust.material.opacity = 0.3 * v;

      slots.forEach((s, i) => {
        const pulse = Math.sin(t * 0.9 - i * 0.8) * 0.5 + 0.5;
        s.mount.material.opacity = (0.35 + pulse * 0.35) * v;
        s.haloRing.material.opacity = (0.3 + pulse * 0.4) * v;
        s.marker.material.opacity = 0.85 * v;
        s.tether.material.opacity = 0.28 * v;
        if (!reducedMotion) {
          s.mount.rotation.y += dt * 0.12;
          s.marker.rotation.y += dt * 0.6;
          s.marker.rotation.x += dt * 0.35;
          s.marker.position.y = 5.6 + Math.sin(t * 1.3 + i * 2) * 0.55;
          s.haloRing.scale.setScalar(1 + pulse * 0.08);
        }
      });

      if (!reducedMotion) {
        // survey sweep travels the grid
        sweep.position.z = ((t * 8) % 220) - 110;
        voxels.rotation.y += dt * 0.014;
        dust.rotation.y += dt * 0.011;
      }
    },
    dispose() {
      spGeo.dispose(); surveyPts.material.dispose();
    },
  };
}
