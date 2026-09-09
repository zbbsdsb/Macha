# Site

Deployment source for the Macha website / paper showcase (statically hostable).

**Repo-internal on purpose.** The paper is the product, so the site's lifecycle is tied
to `papers/` and `announcements/`; keeping it in this repository makes "update the paper,
then the site" a single change.

---

## What it is

A single continuous 3D space. The visitor **is** a camera that travels between six
scenes; scene changes are gradient transitions (fog, light, exposure, geometry) rather
than page loads.

| # | Scene | Copy |
|---|---|---|
| 01 | Origin — Design Goals | ✅ written |
| 02 | Horizon — Industry Goals & Vision | ✅ written |
| 03 | Core — Core Architecture | ⬜ staged, copy pending |
| 04 | Descent — Deep Dive | ⬜ staged, copy pending |
| 05 | Field — Application Plan | ⬜ staged, copy pending |
| 06 | Archive — Glossary | ⬜ staged, copy pending |

Full design rationale: [`DESIGN.md`](DESIGN.md).

## Run locally

No build step — it is plain ESM over an import map.

```bash
cd site
python -m http.server 8000
# open http://localhost:8000
```

Any static server works. Three.js is loaded from jsDelivr, so the first load needs
network access.

## Deploy

GitHub Pages → *Settings → Pages → Deploy from branch* → folder `/site`.

## Editing copy

- **Prose** lives in `index.html` (English is the no-JS / crawler-facing source of truth).
- **Translations and strings** live in `assets/js/content.js` (`STRINGS`).
- **Structure chips** on the pending scenes live in `STACKS` in the same file.

Filling a pending scene = edit `content.js` + drop the `panel--pending` block from that
`<article>` in `index.html`. No 3D code changes.

## Editing a scene's look

Each scene is one module under `assets/js/scenes/`, exporting:

```js
{ group, focus, env, update(dt, t, reveal), dispose() }
```

`env` is interpolated between neighbours every frame — that is the entire transition
mechanism. Register new scenes in `assets/js/scenes/index.js`.

## Flags

- `?nofx` — disable bloom post-processing.
- `prefers-reduced-motion` — disables parallax, drift and scene rotation.
- `L` — toggle EN / 中文.
