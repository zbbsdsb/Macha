import origin from './01-origin.js';
import horizon from './02-horizon.js';
import core from './03-core.js';
import descent from './04-descent.js';
import field from './05-field.js';
import archive from './06-archive.js';

/** Ordered scene registry. Index === camera path index === DOM panel index. */
export const SCENES = [
  { id: 'origin', factory: origin },
  { id: 'horizon', factory: horizon },
  { id: 'core', factory: core },
  { id: 'descent', factory: descent },
  { id: 'field', factory: field },
  { id: 'archive', factory: archive },
];
