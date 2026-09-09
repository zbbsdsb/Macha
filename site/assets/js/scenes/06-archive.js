import * as THREE from 'three';
import { cardRing, dustShell, gridFloor, glowDisc } from './_helpers.js';

/**
 * Scene 06 — Archive / Glossary   [stage only, copy pending]
 * Motif: a circular card catalogue. Monolith cards ring the camera; dust
 * rises through a shaft of light from a lantern at the centre.
 */
export default function create({ quality, reducedMotion }) {
  const group = new THREE.Group();

  const ring = cardRing({
    count: quality === 'low' ? 16 : 30,
    radius: 10.5,
    w: 3.0,
    h: 4.4,
    d: 0.24,
    color: 0xe8d9b5,
    seed: 99,
    y: 0.5,
  });
  group.add(ring);

  const inner = cardRing({
    count: quality === 'low' ? 9 : 16,
    radius: 6.2,
    w: 1.9,
    h: 2.8,
    d: 0.18,
    color: 0xd9c79c,
    seed: 111,
    y: -1.5,
  });
  group.add(inner);

  // central lantern
  const lantern = glowDisc(2.6, 0xffe9bd, 0.32);
  lantern.position.set(0, 1.5, 0);
  group.add(lantern);

  const lanternHalo = glowDisc(8, 0xffd28a, 0.07);
  lanternHalo.position.copy(lantern.position);
  group.add(lanternHalo);

  // light shaft
  const shaftMat = new THREE.MeshBasicMaterial({
    color: 0xffe9bd,
    transparent: true,
    opacity: 0.045,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    side: THREE.DoubleSide,
  });
  const shaft = new THREE.Mesh(new THREE.CylinderGeometry(3.2, 9, 26, 32, 1, true), shaftMat);
  shaft.position.y = 8;
  group.add(shaft);

  // rising dust inside the shaft
  const dust = dustShell({ count: quality === 'low' ? 200 : 520, radius: 12, inner: 0.1, color: 0xffe9bd, size: 0.17, opacity: 0.42, seed: 123 });
  dust.position.y = 2;
  group.add(dust);

  const ambient = dustShell({ count: quality === 'low' ? 140 : 340, radius: 28, color: 0xc9b48a, size: 0.2, opacity: 0.26, seed: 222 });
  group.add(ambient);

  const floor = gridFloor({ size: 100, divisions: 20, color: 0x5a4a30, y: -8 });
  group.add(floor);

  // base plinth
  const plinthMat = new THREE.MeshStandardMaterial({
    color: 0x2a2119, roughness: 0.9, metalness: 0.05, transparent: true, opacity: 0.8,
  });
  const plinth = new THREE.Mesh(new THREE.CylinderGeometry(3.4, 4.1, 0.8, 8), plinthMat);
  plinth.position.y = -5.8;
  group.add(plinth);

  return {
    group,
    focus: new THREE.Vector3(0, 1.5, 0),
    env: {
      bg: 0x0e0b08,
      fog: 0x17120c,
      fogDensity: 0.024,
      hemiSky: 0xffe9bd,
      hemiGround: 0x0a0805,
      hemi: 0.5,
      key: 0xffe9bd,
      keyIntensity: 1.0,
      exposure: 0.98,
      bloom: 0.4,
      accent: '#E8D9B5',
    },
    update(dt, t, reveal) {
      const v = reveal * reveal;
      group.visible = v > 0.002;
      if (!group.visible) return;

      ring.userData.mat.opacity = 0.62 * v;
      inner.userData.mat.opacity = 0.56 * v;
      lantern.material.opacity = 0.32 * v;
      lanternHalo.material.opacity = 0.07 * v;
      shaftMat.opacity = 0.045 * v;
      dust.material.opacity = 0.42 * v;
      ambient.material.opacity = 0.26 * v;
      plinthMat.opacity = 0.8 * v;
      floor.material.opacity = 0.22 * v;

      if (!reducedMotion) {
        ring.rotation.y += dt * 0.026;
        inner.rotation.y -= dt * 0.042;
        dust.rotation.y += dt * 0.03;
        dust.position.y = 2 + Math.sin(t * 0.4) * 0.6;
        ambient.rotation.y -= dt * 0.008;
        lantern.scale.setScalar(1 + Math.sin(t * 1.1) * 0.05);
        lanternHalo.scale.setScalar(1 + Math.sin(t * 1.1 + 0.5) * 0.08);
        lantern.lookAt(0, 1.5, 40);
        lanternHalo.lookAt(0, 1.5, 40);
      }
    },
    dispose() {},
  };
}
