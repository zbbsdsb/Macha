import * as THREE from 'three';
import { tunnelRings, dustShell, glowDisc, pointsMaterial, rng } from './_helpers.js';

/**
 * Scene 04 — Descent / Deep Dive   [stage only, copy pending]
 * Motif: descending through nested rings toward a superposition core —
 * overlapping translucent "fields" whose interference is read as depth.
 */
export default function create({ quality, reducedMotion }) {
  const group = new THREE.Group();

  const tunnel = tunnelRings({
    count: quality === 'low' ? 16 : 28,
    radius: 13,
    spacing: 2.4,
    color: 0xb69cff,
    thickness: 0.07,
    seed: 77,
  });
  tunnel.position.z = -6;
  group.add(tunnel);

  // --- superposition fields: overlapping translucent spheres ---------------
  const fieldColors = [0xb69cff, 0x6ee7f9, 0xff8ad4];
  const fields = [];
  fieldColors.forEach((c, i) => {
    const mat = new THREE.MeshBasicMaterial({
      color: c,
      transparent: true,
      opacity: 0.055,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      side: THREE.DoubleSide,
      wireframe: i === 2,
    });
    const m = new THREE.Mesh(new THREE.IcosahedronGeometry(6.5 + i * 1.7, i === 2 ? 1 : 3), mat);
    m.userData = { base: 0.055, phase: i * 2.1, drift: 0.5 + i * 0.35 };
    fields.push(m);
    group.add(m);
  });

  // interference rings on the ground of the shaft
  const rippleMat = new THREE.MeshBasicMaterial({
    color: 0xc4b0ff, transparent: true, opacity: 0.16, side: THREE.DoubleSide, depthWrite: false,
  });
  const ripples = new THREE.Group();
  for (let i = 0; i < 5; i++) {
    const m = new THREE.Mesh(new THREE.RingGeometry(3 + i * 3.5, 3.15 + i * 3.5, 96), rippleMat);
    m.rotation.x = -Math.PI / 2;
    m.position.y = -12;
    m.userData.phase = i * 0.7;
    ripples.add(m);
  }
  group.add(ripples);

  // descending motes
  const r = rng(404);
  const N = quality === 'low' ? 260 : 620;
  const mp = new Float32Array(N * 3);
  for (let i = 0; i < N; i++) {
    const a = r() * Math.PI * 2;
    const rad = 1 + r() * 14;
    mp[i * 3] = Math.cos(a) * rad;
    mp[i * 3 + 1] = -18 + r() * 36;
    mp[i * 3 + 2] = -r() * 60;
  }
  const moteGeo = new THREE.BufferGeometry();
  moteGeo.setAttribute('position', new THREE.BufferAttribute(mp, 3));
  const motes = new THREE.Points(moteGeo, pointsMaterial(0xd9c9ff, 0.19, 0.7));
  group.add(motes);

  const dust = dustShell({ count: quality === 'low' ? 160 : 380, radius: 42, color: 0x9a7bff, size: 0.22, opacity: 0.34, seed: 55 });
  group.add(dust);

  const portal = glowDisc(9, 0xb69cff, 0.2);
  portal.position.set(0, 0, -62);
  group.add(portal);

  return {
    group,
    focus: new THREE.Vector3(0, 0, -34),
    env: {
      bg: 0x0a0713,
      fog: 0x120b22,
      fogDensity: 0.034,
      hemiSky: 0x5b3fa8,
      hemiGround: 0x07040d,
      hemi: 0.5,
      key: 0xc4b0ff,
      keyIntensity: 1.1,
      exposure: 1.08,
      accent: '#B69CFF',
    },
    update(dt, t, reveal) {
      const v = reveal * reveal;
      group.visible = v > 0.002;
      if (!group.visible) return;

      tunnel.userData.mat.opacity = 0.8 * v;
      rippleMat.opacity = 0.16 * v;
      dust.material.opacity = 0.34 * v;
      motes.material.opacity = 0.7 * v;
      portal.material.opacity = 0.2 * v;

      fields.forEach((f, i) => {
        const p = Math.sin(t * 0.5 + f.userData.phase) * 0.5 + 0.5;
        f.material.opacity = (f.userData.base + p * 0.045) * v;
        if (!reducedMotion) {
          f.rotation.y += dt * 0.06 * (i + 1);
          f.rotation.x += dt * 0.03 * (i % 2 ? -1 : 1);
          f.position.x = Math.sin(t * f.userData.drift * 0.3 + i) * 1.4;
          f.position.y = Math.cos(t * f.userData.drift * 0.24 + i) * 1.1;
          f.scale.setScalar(1 + p * 0.05);
        }
      });

      if (!reducedMotion) {
        tunnel.rotation.z += dt * 0.02;
        ripples.children.forEach((m, i) => {
          const s = 1 + ((t * 0.25 + m.userData.phase) % 1) * 0.55;
          m.scale.setScalar(s);
          m.material.opacity = rippleMat.opacity * (1 - ((t * 0.25 + m.userData.phase) % 1));
        });
        const arr = moteGeo.attributes.position.array;
        for (let i = 1; i < arr.length; i += 3) {
          arr[i] -= dt * (0.6 + (i % 5) * 0.12);
          if (arr[i] < -20) arr[i] = 20;
        }
        moteGeo.attributes.position.needsUpdate = true;
        motes.rotation.y += dt * 0.02;
        dust.rotation.y -= dt * 0.009;
      }
    },
    dispose() {
      moteGeo.dispose(); motes.material.dispose();
    },
  };
}
