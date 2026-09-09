import { STRINGS } from './content.js';

const KEY = 'macha.lang';
let lang = 'en';
try {
  const saved = localStorage.getItem(KEY);
  if (saved === 'en' || saved === 'zh') lang = saved;
} catch (_) { /* private mode */ }

const listeners = new Set();

export const getLang = () => lang;

export function t(key) {
  const e = STRINGS[key];
  if (!e) return key;
  return (lang === 'zh' ? e.zh ?? e.en : e.en ?? e.zh) ?? key;
}

export function onLangChange(fn) {
  listeners.add(fn);
  return () => listeners.delete(fn);
}

/**
 * The English copy lives in index.html so crawlers and no-JS readers get the
 * full text. We cache that initial text per node and treat it as the source of
 * truth for `en`, which keeps content.js from drifting away from the markup.
 */
export function applyLang() {
  document.documentElement.lang = lang === 'zh' ? 'zh-CN' : 'en';
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    if (el._en === undefined) el._en = el.textContent.trim();
    const key = el.dataset.i18n;
    const dict = STRINGS[key];
    if (lang === 'zh') {
      el.textContent = dict?.zh ?? el._en;
    } else {
      el.textContent = dict?.en ?? el._en;
    }
  });
  document.querySelectorAll('.lang-btn').forEach((b) => {
    b.classList.toggle('is-active', b.dataset.lang === lang);
    b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
  });
  listeners.forEach((fn) => fn(lang));
}

export function setLang(next) {
  if (next === lang) return;
  lang = next;
  try { localStorage.setItem(KEY, lang); } catch (_) { /* ignore */ }
  applyLang();
}

export function toggleLang() {
  setLang(lang === 'en' ? 'zh' : 'en');
}
