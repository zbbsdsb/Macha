import * as THREE from 'three';
import { dustShell, gridFloor, pointsMaterial, rng } from './_helpers.js';

/**
 * Scene 01 — Origin / Design Goals
 * Motif: a memory graph. Nodes + edges in a sphere, wrapped by three
 * slowly rotating rings standing for Memory / Architecture / Character.
 */
export default function create({ quality, reducedMotion }) {
  const group = new THREE.Group();
  const NODE_COUNT = quality === 'low' ? 70 : 150;
  const r = rng(20260816);

  // --- memory graph -------------------------------------------------------
  const pos = new Float32Array(NODE_COUNT * 3);
  const nodes = [];
  for (let i = 0; i < NODE_COUNT; i++) {
    const u = r() * 2 - 1;
    const th = r() * Math.PI * 2;
    const rad = 10 * Math.cbrt(0.25 + r() * 0.75);
    const s = Math.sqrt(1 - u * u);
    const v = new THREE.Vector3(rad * s * Math.cos(th), rad * u * 0.75, rad * s * Math.sin(th));
    nodes.push(v);
    pos[i * 3] = v.x; pos[i * 3 + 1] = v.y; pos[i * 3 + 2] = v.z;
  }
  const nodeGeo = new THREE.BufferGeometry();
  nodeGeo.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const nodeMat = pointsMaterial(0x9beeff, 0.42, 0.95);
  const graphPts = new THREE.Points(nodeGeo, nodeMat);
  group.add(graphPts);

  // edges between near neighbours
  const edgePos = [];
  const MAX_D = 4.6;
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const d = nodes[i].distanceTo(nodes[j]);
      if (d < MAX_D) {
        edgePos.push(nodes[i].x, nodes[i].y, nodes[i].z, nodes[j].x, nodes[j].y, nodes[j].z);
      }
    }
  }
  const edgeGeo = new THREE.BufferGeometry();
  edgeGeo.setAttribute('position', new THREE.Float32BufferAttribute(edgePos, 3));
  const edgeMat = new THREE.LineBasicMaterial({
    color: 0x6ee7f9, transparent: true, opacity: 0.16, depthWrite: false,
  });
  const edges = new THREE.LineSegments(edgeGeo, edgeMat);
  group.add(edges);

  // --- the three pillars (M / A / C) --------------------------------------
  const pillarColors = [0x6ee7f9, 0x8b9dff, 0xffd28a];
  const pillars = [];
  pillarColors.forEach((c, i) => {
    const geo = new THREE.TorusGeometry(5.4 + i * 1.9, 0.055, 8, 96);
    const mat = new THREE.MeshStandardMaterial({
      color: c,
      emissive: new THREE.Color(c).multiplyScalar(0.85),
      roughness: 0.3,
      metalness: 0.6,
      transparent: true,
      opacity: 0.85,
    });
    const m = new THREE.Mesh(geo, mat);
    m.rotation.set(Math.PI / 2 + i * 0.5, i * 0.7, i * 0.35);
    m.userData.spin = new THREE.Vector3(
      (i % 2 ? 1 : -1) * 0.055 * (1 + i * 0.2),
      0.075 * (1 + i * 0.15),
      0.03 * (i + 1)
    );
    pillars.push(m);
    group.add(m);
  });

  // --- core seed ----------------------------------------------------------
  const coreMat = new THREE.MeshStandardMaterial({
    color: 0xdff6ff,
    emissive: 0x6ee7f9,
    emissiveIntensity: 1.4,
    roughness: 0.2,
    metalness: 0.1,
    transparent: true,
    opacity: 0.9,
    wireframe: true,
  });
  const core = new THREE.Mesh(new THREE.IcosahedronGeometry(1.5, 1), coreMat);
  group.add(core);

  const dust = dustShell({ count: quality === 'low' ? 260 : 620, radius: 34, color: 0x7ea6ff, size: 0.22, opacity: 0.5, seed: 5 });
  group.add(dust);

  const floor = gridFloor({ size: 150, divisions: 30, color: 0x2b3550, y: -9 });
  group.add(floor);

  return {
    group,
    focus: new THREE.Vector3(0, 0, 0),
    env: {
      bg: 0x070b1a,
      fog: 0x080e20,
      fogDensity: 0.030,
      hemiSky: 0x2f4a8f,
      hemiGround: 0x05060c,
      hemi: 0.6,
      key: 0x8fe8ff,
      keyIntensity: 1.35,
      exposure: 1.05,
      accent: '#6EE7F9',
    },
    update(dt, t, reveal) {
      const v = reveal * reveal;
      group.visible = v > 0.002;
      if (!group.visible) return;
      nodeMat.opacity = 0.95 * v;
      edgeMat.opacity = 0.16 * v;
      coreMat.opacity = 0.9 * v;
      dust.material.opacity = 0.5 * v;
      floor.material.opacity = 0.22 * v;

      if (!reducedMotion) {
        group.rotation.y += dt * 0.035;
        pillars.forEach((m) => {
          m.rotation.x += m.userData.spin.x * dt;
          m.rotation.y += m.userData.spin.y * dt;
          m.rotation.z += m.userData.spin.z * dt;
          m.material.opacity = 0.85 * v;
        });
        core.rotation.x += dt * 0.18;
        core.rotation.y += dt * 0.13;
        const pulse = 1 + Math.sin(t * 1.4) * 0.06;
        core.scale.setScalar(pulse);
        dust.rotation.y -= dt * 0.012;
      }
      // gentle breathing of the whole graph toward the viewer
      graphPts.scale.setScalar(0.85 + v * 0.15);
      edges.scale.copy(graphPts.scale);
    },
    dispose() {
      nodeGeo.dispose(); nodeMat.dispose();
      edgeGeo.dispose(); edgeMat.dispose();
    },
  };
}
