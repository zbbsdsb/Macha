import * as THREE from 'three';
import { flowStream, updateFlowStream, dustShell, gridFloor, glowDisc } from './_helpers.js';

/**
 * Scene 03 — Core / Macha Core Architecture   [stage only, copy pending]
 * Motif: four translucent plates stacked on an axis
 * (Perception → Memory → Reasoning → Action) with particles flowing upward
 * through them, wrapped by a wireframe shell and a pulsing core octahedron.
 */
export default function create({ quality, reducedMotion }) {
  const group = new THREE.Group();
  const LAYERS = ['Perception', 'Memory', 'Reasoning', 'Action'];
  const baseY = -5.4;
  const stepY = 3.6;

  const plates = [];
  LAYERS.forEach((name, i) => {
    const radius = 6.6 - i * 0.8;
    const geo = new THREE.CylinderGeometry(radius, radius, 0.16, 72, 1, true);
    const mat = new THREE.MeshStandardMaterial({
      color: 0x7cf5c4,
      emissive: new THREE.Color(0x7cf5c4).multiplyScalar(0.22),
      roughness: 0.35,
      metalness: 0.5,
      transparent: true,
      opacity: 0.34,
      side: THREE.DoubleSide,
    });
    const mesh = new THREE.Mesh(geo, mat);
    mesh.position.y = baseY + i * stepY;
    mesh.userData = { i, name };
    plates.push(mesh);
    group.add(mesh);

    // rim ring, brighter
    const rim = new THREE.Mesh(
      new THREE.TorusGeometry(radius, 0.045, 8, 96),
      new THREE.MeshBasicMaterial({ color: 0x7cf5c4, transparent: true, opacity: 0.75 })
    );
    rim.rotation.x = Math.PI / 2;
    rim.position.y = mesh.position.y;
    rim.userData.baseOpacity = 0.75;
    mesh.userData.rim = rim;
    group.add(rim);
  });

  // vertical axis
  const axis = new THREE.Mesh(
    new THREE.CylinderGeometry(0.05, 0.05, stepY * 3 + 4, 6),
    new THREE.MeshBasicMaterial({ color: 0x7cf5c4, transparent: true, opacity: 0.4 })
  );
  axis.position.y = baseY + (stepY * 3) / 2;
  group.add(axis);

  // data flowing up the stack
  const flow = flowStream({
    count: quality === 'low' ? 160 : 320,
    radius: 7,
    height: stepY * 3 + 6,
    color: 0xa8ffe0,
    size: 0.15,
    speed: 2.2,
    seed: 33,
  });
  flow.position.y = baseY + (stepY * 3) / 2;
  group.add(flow);

  // pulsing core
  const coreMat = new THREE.MeshStandardMaterial({
    color: 0xd9fff1,
    emissive: 0x7cf5c4,
    emissiveIntensity: 1.2,
    wireframe: true,
    transparent: true,
    opacity: 0.75,
  });
  const core = new THREE.Mesh(new THREE.OctahedronGeometry(1.9, 1), coreMat);
  core.position.y = baseY + (stepY * 3) / 2;
  group.add(core);

  const halo = glowDisc(5, 0x7cf5c4, 0.14);
  halo.position.copy(core.position);
  group.add(halo);

  // outer shell
  const shellMat = new THREE.MeshStandardMaterial({
    color: 0x7cf5c4,
    wireframe: true,
    transparent: true,
    opacity: 0.1,
  });
  const shell = new THREE.Mesh(new THREE.IcosahedronGeometry(10.5, 2), shellMat);
  shell.position.y = baseY + (stepY * 3) / 2;
  group.add(shell);

  const dust = dustShell({ count: quality === 'low' ? 180 : 420, radius: 26, color: 0x7cf5c4, size: 0.2, opacity: 0.32, seed: 44 });
  group.add(dust);

  const floor = gridFloor({ size: 110, divisions: 22, color: 0x1f4a3c, y: -9.5 });
  group.add(floor);

  return {
    group,
    focus: new THREE.Vector3(0, baseY + (stepY * 3) / 2, 0),
    env: {
      bg: 0x08100e,
      fog: 0x0a1712,
      fogDensity: 0.021,
      hemiSky: 0x2f7f66,
      hemiGround: 0x040806,
      hemi: 0.6,
      key: 0x9dffdd,
      keyIntensity: 1.25,
      exposure: 1.0,
      bloom: 0.45,
      accent: '#7CF5C4',
    },
    update(dt, t, reveal) {
      const v = reveal * reveal;
      group.visible = v > 0.002;
      if (!group.visible) return;

      flow.material.opacity = 0.75 * v;
      coreMat.opacity = 0.75 * v;
      shellMat.opacity = 0.1 * v;
      dust.material.opacity = 0.32 * v;
      axis.material.opacity = 0.4 * v;
      halo.material.opacity = 0.14 * v;
      floor.material.opacity = 0.22 * v;

      plates.forEach((p, i) => {
        // sequential shimmer: each plate lights in turn
        const phase = Math.sin(t * 1.1 - i * 0.9) * 0.5 + 0.5;
        p.material.opacity = (0.2 + phase * 0.28) * v;
        p.userData.rim.material.opacity = (0.4 + phase * 0.45) * v;
        if (!reducedMotion) p.rotation.y += dt * (0.05 + i * 0.02);
      });

      if (!reducedMotion) {
        updateFlowStream(flow, dt);
        shell.rotation.y += dt * 0.03;
        shell.rotation.x += dt * 0.012;
        core.rotation.y += dt * 0.22;
        core.rotation.x += dt * 0.09;
        core.scale.setScalar(1 + Math.sin(t * 1.8) * 0.07);
        halo.lookAt(0, 0, 0);
        dust.rotation.y += dt * 0.01;
      }
    },
    dispose() {
      plates.forEach((p) => { p.geometry.dispose(); p.material.dispose(); p.userData.rim.geometry.dispose(); p.userData.rim.material.dispose(); });
    },
  };
}
