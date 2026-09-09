import * as THREE from 'three';

/**
 * Piecewise Catmull-Rom camera path.
 *
 * Why piecewise instead of one global curve: with a single curve the parameter
 * p = i does NOT land exactly on anchor i (arc length is not uniform), so the
 * camera would "park crooked" at every scene. Evaluating per-segment keeps
 * p = i exactly on anchor i, and still extrapolates smoothly for p < 0
 * (the boot glide-in) and p > n-1.
 */

function cr(p0, p1, p2, p3, t, out) {
  const t2 = t * t;
  const t3 = t2 * t;
  const ax = -p0.x + 3 * p1.x - 3 * p2.x + p3.x;
  const bx = 2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x;
  const cx = -p0.x + p2.x;
  const ay = -p0.y + 3 * p1.y - 3 * p2.y + p3.y;
  const by = 2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y;
  const cy = -p0.y + p2.y;
  const az = -p0.z + 3 * p1.z - 3 * p2.z + p3.z;
  const bz = 2 * p0.z - 5 * p1.z + 4 * p2.z - p3.z;
  const cz = -p0.z + p2.z;
  return out.set(
    0.5 * (2 * p1.x + cx * t + bx * t2 + ax * t3),
    0.5 * (2 * p1.y + cy * t + by * t2 + ay * t3),
    0.5 * (2 * p1.z + cz * t + bz * t2 + az * t3)
  );
}

export class Rig {
  constructor(anchors) {
    this.anchors = anchors.map((v) => v.clone());
    this.n = this.anchors.length;
    this.pad = [];
    for (let i = -1; i <= this.n; i++) this.pad.push(this._raw(i));
    // pad[k] === anchor[k-1];  segment i needs pad[i..i+3] === anchor[i-1..i+2]
    this._tmp = new THREE.Vector3();
  }

  _raw(i) {
    const P = this.anchors;
    const n = this.n;
    if (i < 0) {
      // mirror behind the start
      return P[0].clone().add(P[0].clone().sub(P[1]).multiplyScalar(-i));
    }
    if (i >= n) {
      return P[n - 1].clone().add(P[n - 1].clone().sub(P[n - 2]).multiplyScalar(i - n + 1));
    }
    return P[i].clone();
  }

  positionAt(p, out) {
    let i = Math.floor(p);
    if (i < 0) i = 0;
    if (i > this.n - 2) i = this.n - 2;
    const f = p - i;
    return cr(this.pad[i], this.pad[i + 1], this.pad[i + 2], this.pad[i + 3], f, out);
  }

  /** Slight lateral sway so travel never feels like a straight rail. */
  static buildAnchors(count, spacing, origin = new THREE.Vector3()) {
    const out = [];
    for (let i = 0; i < count; i++) {
      out.push(
        new THREE.Vector3(
          origin.x + Math.sin(i * 1.32) * 3.6,
          origin.y + Math.cos(i * 0.88) * 1.6,
          origin.z - i * spacing
        )
      );
    }
    return out;
  }
}

export const smoothstep = (t) => {
  const x = Math.min(1, Math.max(0, t));
  return x * x * (3 - 2 * x);
};

export const clamp = (v, a, b) => Math.min(b, Math.max(a, v));

/** Frame-rate independent damping. */
export const damp = (current, target, lambda, dt) =>
  current + (target - current) * (1 - Math.exp(-lambda * dt));
