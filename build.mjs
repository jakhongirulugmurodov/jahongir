// Portfolio sayt generatori. Bog'liqliksiz: `node build.mjs` → dist/
// Kontent: content/site.json, content/projects/projects.json, content/posts/*.json, content/kundalik.json, content/sayohat.json
import { readFileSync, writeFileSync, mkdirSync, readdirSync, rmSync, cpSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";

const ROOT = dirname(new URL(import.meta.url).pathname);
const OUT = join(ROOT, "dist");
const read = (p) => JSON.parse(readFileSync(join(ROOT, p), "utf8"));
const readOpt = (p, d) => (existsSync(join(ROOT, p)) ? read(p) : d);

const site = read("content/site.json");
const projects = read("content/projects/projects.json");
const projBy = Object.fromEntries(projects.map((p) => [p.slug, p]));
const posts = readdirSync(join(ROOT, "content/posts"))
  .filter((f) => f.endsWith(".json"))
  .map((f) => read(join("content/posts", f)))
  .filter((p) => p.chop !== false)
  .sort((a, b) => (a.sana < b.sana ? 1 : a.sana > b.sana ? -1 : a.id < b.id ? 1 : -1));
const kundalik = readOpt("content/kundalik.json", []).filter((k) => k.chop !== false).sort((a, b) => (a.sana < b.sana ? 1 : a.sana > b.sana ? -1 : 0));
const KT = ["Kitob", "O'rgandim", "Hayot"];
const sayohat = readOpt("content/sayohat.json", []).filter((t) => t.chop !== false).sort((a, b) => (a.sana < b.sana ? 1 : a.sana > b.sana ? -1 : 0));


// --- tekshiruv: buzilgan kontent saytga chiqmasin
const errors = [];
for (const p of posts) {
  for (const k of ["id", "sana", "loyiha", "sarlavha", "muammo", "yechim", "natija"]) if (!p[k]) errors.push(`${p.id || "?"}: "${k}" yo'q`);
  if (p.loyiha && !projBy[p.loyiha]) errors.push(`${p.id}: noma'lum loyiha "${p.loyiha}"`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(p.sana || "")) errors.push(`${p.id}: sana YYYY-MM-DD bo'lishi kerak`);
}
for (const k of kundalik) { if (!KT.includes(k.toifa)) errors.push(`${k.id}: toifa ${KT.join(" / ")} bo'lishi kerak`); if (!k.sarlavha || !k.sana) errors.push(`${k.id}: sarlavha va sana kerak`); }
for (const t of sayohat) { if (!t.joy || !t.sana) errors.push(`${t.id || "?"}: joy va sana kerak`); if (!(t.rasmlar || []).length) errors.push(`${t.id}: kamida bitta rasm kerak`); for (const r of t.rasmlar || []) { const src = typeof r === "string" ? r : r.src; if (!existsSync(join(ROOT, "content", src))) errors.push(`${t.id}: rasm topilmadi ${src}`); } }
if (errors.length) { console.error("Kontent xatolari:\n- " + errors.join("\n- ")); process.exit(1); }

// --- yordamchilar
const esc = (s = "") => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const slug = (s) => String(s).toLowerCase().replace(/[ʻʼ'’`]/g, "").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
const OY = ["yanvar", "fevral", "mart", "aprel", "may", "iyun", "iyul", "avgust", "sentabr", "oktabr", "noyabr", "dekabr"];
const day = (d) => +d.slice(8), mon = (d) => +d.slice(5, 7);
const sana = (d) => `${day(d)}-${OY[mon(d) - 1]}, ${d.slice(0, 4)}`;
const ROT = ["-2.4deg", "1.8deg", "-1.2deg", "2.6deg", "-1.8deg", "1deg"];
// O'zbek imlosi: o' g' → o‘ g‘ (U+2018, aylangan vergul), tutuq belgisi → ’ (U+2019). Barcha shriftlarda bor. Faqat ko'rinadigan matnga.
const typo = (s) => String(s).replace(/([A-Za-z])(&#39;|&#x27;|&apos;)(?=[A-Za-z])/g, "$1'").replace(/([oOgG])['\u2019\u2018`\u02bc\u02bb](?=[A-Za-z\u02bb\u02bc])/g, "$1\u2018").replace(/(?<=[A-Za-z])['`\u02bc](?=[A-Za-z])/g, "\u2019");
const typoAttr = (tag) => tag.replace(/\b(aria-label|alt|title|placeholder|data-cap|content)="([^"]*)"/g, (m, a, v) => `${a}="${typo(v)}"`);
const typoMarkup = (h) => String(h).replace(/(<(script|style)\b[\s\S]*?<\/\2>)|(<[^>]+>)|([^<]+)/gi, (m, blk, _t, tag, text) => (blk ? blk : tag ? typoAttr(tag) : typo(text)));
const isPath = (v) => /^(https?:|media\/|post\/|loyiha\/|#|\.\.\/|tg:)/.test(v) || /\.(jpe?g|png|svg|webp|html)$/.test(v);
const typoData = (v, k) => (typeof v === "string" ? (isPath(v) || ["id", "ps", "slug", "pid", "tg", "page"].includes(k) ? v : v.includes("<") ? typoMarkup(v) : typo(v)) : Array.isArray(v) ? v.map((x) => typoData(x, k)) : v && typeof v === "object" ? Object.fromEntries(Object.entries(v).map(([kk, x]) => [kk, typoData(x, kk)])) : v);
const write = (rel, html) => { const f = join(OUT, rel); mkdirSync(dirname(f), { recursive: true }); writeFileSync(f, rel.endsWith(".html") ? typoMarkup(html) : html); };
const short = (s, n = 1) => esc(String(s).split(/\s+/).slice(0, n).join(" ").toLowerCase());
const byProj = (s) => posts.filter((p) => p.loyiha === s);

// --- mini chizma (qalam uslubi), post shablon ma'lumotidan
function sketch(v = {}) {
  switch (v.shablon) {
    case "muammo-yechim":
      return '<div class="bx red"><div>Oldin</div><div class="ln" style="width:56px"><i></i><i style="width:70%"></i></div></div><span class="ar">→</span><div class="bx grn"><div>Keyin</div><div class="ln" style="width:56px"><i></i><i style="width:82%"></i></div></div>';
    case "jarayon":
      return (v.qadamlar || []).slice(0, 4).map((q, i) => `${i ? '<span class="dash"></span>' : ""}<div class="col"><span class="circ">${i + 1}</span>${short(q.t)}</div>`).join("");
    case "sxema": {
      const t = (v.tugunlar || []).slice(0, 4), hl = Math.max(0, t.length - 2);
      return t.map((n, i) => `${i ? '<span class="ar">→</span>' : ""}<div class="bx${i === hl ? " tl" : ""}">${esc((w => w.length > 8 ? w.slice(0, 7) + "." : w)(String(n.t).split(/\s+/)[0]))}</div>`).join("");
    }
    case "ozgarish":
      return (v.korsatkichlar || []).slice(0, 3).map((k) => `<div class="col"><span style="font-size:34px;line-height:1;color:${k.yaxshi === false ? "#C0392B" : "#1E8C5A"}">${k.yonalish === "past" ? "↓" : "↑"}</span>${short(k.nom.replace(/^ariza\s+/i, ""))}</div>`).join("");
    case "kreativ":
      return Array.from({ length: Math.min(5, (v.elementlar || []).length || 3) }, (_, i) => `<span class="fr"${i % 2 ? ' style="transform:rotate(2deg)"' : ""}></span>`).join("");
    case "iqtibos":
      return `<div class="q">${esc(String(v.matn || "").split(/\s+/).slice(0, 8).join(" "))}</div>`;
    default:
      return '<div class="bx">yechim</div>';
  }
}

// storyboard bo'lsa: kartochkada kadrlar mini-film bo'lib almashadi (butun blok bo'ylab)
const film = (p, r = "") => {
  const K = p.storyboard.kadrlar || [];
  if (!K.length) return `<img class="sk-img" src="${r}${esc(p.storyboard.rasm)}" alt="${esc(p.sarlavha)} — storyboard" data-pid="${esc(p.id)}" loading="lazy">`;
  return `<span class="film" data-pid="${esc(p.id)}">${K.map((k, i) => `<img class="film-f${i ? "" : " on"}" src="${r}${esc(k.src)}" alt="${i ? "" : esc(p.sarlavha) + " — storyboard"}" loading="lazy">`).join("")}<span class="film-n" aria-hidden="true">${K.map((_, i) => `<i${i ? "" : ' class="on"'}></i>`).join("")}</span></span>`;
};
const vis = (p, r = "") => (p.storyboard ? film(p, r) : sketch(p.vizual));
// post sahifasida: kadrlar "chizilib" chiqadigan pleyer (SVG bo'lsa jonli, bo'lmasa rasm)
const svgOf = (k) => (k.svg && existsSync(join(ROOT, "content", k.svg)) ? readFileSync(join(ROOT, "content", k.svg), "utf8") : "");
const player = (p, r = "") => {
  if (!p.storyboard) return `<div class="sk">${sketch(p.vizual)}</div>`;
  const K = p.storyboard.kadrlar || [];
  if (!K.length) return `<div class="sk">${film(p, r)}</div>`;
  return `<div class="player" data-pid="${esc(p.id)}"><div class="pl-stage" role="button" tabindex="0" aria-label="Storyboard'ni katta ochish">${K.map((k, i) => `<div class="pl-f${i ? "" : " on"}" data-cap="${esc(k.izoh || "")}">${svgOf(k) || `<img src="${r}${esc(k.src)}" alt="${esc(k.izoh || p.sarlavha)}" loading="lazy">`}</div>`).join("")}</div>
<div class="pl-bar"><span class="pl-dots">${K.map((_, i) => `<button type="button" aria-label="${i + 1}-kadr"${i ? "" : ' class="on"'}></button>`).join("")}</span><span class="pl-cap">${esc(K[0].izoh || "")}</span><button type="button" class="pl-re" aria-label="Qayta ko'rish">↻</button></div></div>`;
};

const fonts = `<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&family=Hanken+Grotesk:wght@400;500;600;700&family=Caveat:wght@500;700&family=Fraunces:wght@900&family=Patrick+Hand&display=swap">`;
const SVGDEFS = `<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="metal" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F4F7F7"/><stop offset=".35" stop-color="#A9B4B4"/><stop offset=".55" stop-color="#E9EEEE"/><stop offset="1" stop-color="#7E8A8A"/></linearGradient><radialGradient id="pinHead" cx=".35" cy=".3" r=".75"><stop offset="0" stop-color="#9AD2D2"/><stop offset=".35" stop-color="#16A6A9"/><stop offset="1" stop-color="#0A4E50"/></radialGradient><symbol id="clipS" viewBox="0 0 26 78"><path d="M9 70 V16 a7 7 0 0 1 14 0 V58 a5 5 0 0 1 -10 0 V22" fill="none" stroke="url(#metal)" stroke-width="2.6" stroke-linecap="round"/></symbol><symbol id="pinS" viewBox="0 0 26 38"><path d="M13 22 L14.2 37" stroke="#8C9898" stroke-width="1.6" stroke-linecap="round"/><ellipse cx="13" cy="21.5" rx="7.5" ry="2.6" fill="#0A4E50"/><path d="M8 20 C8 14, 9 11, 10 9 L16 9 C17 11, 18 14, 18 20 Z" fill="url(#pinHead)"/><ellipse cx="13" cy="8" rx="8.5" ry="6.5" fill="url(#pinHead)"/><ellipse cx="10.5" cy="6" rx="2.6" ry="1.6" fill="#fff" opacity=".7"/></symbol></defs></svg>`;

const contactBand = () => `<section class="contact-band gut" id="boglanish"><div class="in">
  <div><h2>Shunga o'xshash muammo bormi?</h2><p>Telegram'da yozing va qaysi muammo ustida ishlayotganingizni ayting.</p></div>
  <div><span class="handle">@${esc(site.telegram)}</span><a class="f-btn" href="https://t.me/${esc(site.telegram)}" target="_blank" rel="noopener">Telegram'da yozish →</a></div>
</div></section>`;

function layout({ title, desc, r, page, active = "", body, data, contact = true }) {
  const full = title ? `${title} — ${site.brend}` : site.brend;
  const nav = [["index.html#loyihalar", "Loyihalar", "loyihalar"], ["index.html#taqvim", "Taqvim", "taqvim"], ["index.html#kundalik", "Kundalik", "kundalik"], ...(sayohat.length ? [["index.html#sayohat", "Sayohat", "sayohat"]] : [])];
  return `<!doctype html>
<html lang="uz">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(full)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="${esc(desc || site.bio)}">
<meta property="og:title" content="${esc(full)}">
<meta property="og:description" content="${esc(desc || site.bio)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="${esc(site.brend)}">
${site.og && site.domen ? `<meta property="og:image" content="${site.domen}/${site.og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="${site.domen}/${site.og}">` : ""}
<meta name="theme-color" content="#0A4E50">
${fonts}
<link rel="stylesheet" href="${r}assets/site.css">
</head>
<body data-page="${page}">
${SVGDEFS}
<header class="top"><div class="in gut">
  <a class="brand" href="${r}index.html" aria-label="${esc(site.brend)}"><span class="bn">${esc(site.ism)}</span><span class="bsep" aria-hidden="true"></span><span class="logo" aria-hidden="true"><span class="lo">O</span><span class="ln">N</span></span></a>
  <nav class="nav" aria-label="Asosiy">${nav.map(([h, t, k]) => `<a href="${r}${h}"${active === k ? ' aria-current="page"' : ""}>${t}</a>`).join("")}</nav>
</div></header>
<main>
${body}
</main>
${contact ? contactBand() : ""}
<footer class="foot gut">© ${new Date().getFullYear()} ${esc(site.brend)} · Mijoz nomlari va raqamlari ularning roziligisiz ko'rsatilmaydi.</footer>
${data ? `<script>window.D=${JSON.stringify(typoData(data)).replace(/</g, "\\u003c")};</script>` : ""}
<script src="${r}assets/site.js" defer></script>
</body>
</html>
`;
}

const docCard = (p, r, k) => `<a class="doc" data-id="${p.id}" href="${r}post/${p.id}.html" style="--r:${ROT[k % 6]};--i:${k}" data-q="${esc([p.sarlavha, p.muammo, p.yechim, p.natija, projBy[p.loyiha].nom, ...(p.teglar || [])].join(" ").toLowerCase())}" data-loyiha="${p.loyiha}">
  <svg class="clip" aria-hidden="true"><use href="#clipS"/></svg><span class="stamp">${day(p.sana)} ${OY[mon(p.sana) - 1].slice(0, 3)}</span>
  <span class="chip">${esc(p.tur || projBy[p.loyiha].nom)}</span><div class="sk">${vis(p, r)}</div>
  <h4>${esc(p.sarlavha)}${p.namuna ? '<span class="demo">namuna</span>' : ""}</h4><p>${esc(p.muammo)}</p><span class="read">O'qish →</span></a>`;

const kCard = (k, n) => `<a class="doc" data-kid="${k.id}" href="#kundalik" style="--r:${ROT[n % 6]};--i:${n}" data-q="${esc([k.sarlavha, ...(Array.isArray(k.matn) ? k.matn : [k.matn || ""]), k.xulosa, k.toifa, ...(k.teglar || [])].join(" ").toLowerCase())}">
  <svg class="clip" aria-hidden="true"><use href="#clipS"/></svg><span class="stamp">${day(k.sana)} ${OY[mon(k.sana) - 1].slice(0, 3)}</span>
  <span class="chip">Kundalik · ${esc(k.toifa)}</span>
  <h4>${esc(k.sarlavha)}${k.namuna ? '<span class="demo">namuna</span>' : ""}</h4><p>${esc((Array.isArray(k.matn) ? k.matn[0] : k.matn) || "")}</p><span class="read">O'qish →</span></a>`;

// --- chiqish
rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });
cpSync(join(ROOT, "assets"), join(OUT, "assets"), { recursive: true });
if (existsSync(join(ROOT, "content/media"))) cpSync(join(ROOT, "content/media"), join(OUT, "media"), { recursive: true });

// papkalar tartibi: eng oxirgi faol loyiha oldinda (ro'yxat oxirida)
const lastDate = (s) => byProj(s)[0]?.sana || "0000";
const folderOrder = projects.slice().sort((a, b) => (lastDate(a.slug) < lastDate(b.slug) ? -1 : 1));
// highlightlar: mavzu bo'yicha guruh (loyiha yoki kundalik), eng yangi faollik oldinda
const ctaOf = (p) => (p.taklif ? { t: p.taklif.tugma, h: `https://t.me/${site.telegram}?text=${encodeURIComponent(typo(p.taklif.xabar || ""))}` } : null);
const frames = (sb) => (sb.kadrlar || []).map((r) => ({ s: r.src, i: r.izoh || "" }));
const hlGroups = [
  ...projects.map((pr) => {
    const L = byProj(pr.slug).filter((p) => p.storyboard);
    return L.length ? { id: "p-" + pr.slug, n: pr.qisqa || pr.nom, c: (L[0].storyboard.kadrlar?.[0]?.src || L[0].storyboard.rasm), d: L[0].sana, it: L.map((p) => ({ id: p.id, joy: p.sarlavha, hud: pr.nom, dav: "", d: p.sana, x: "", img: frames(p.storyboard), cta: ctaOf(p), read: `post/${p.id}.html` })) } : null;
  }),
  (() => {
    const L = kundalik.filter((k) => k.storyboard);
    return L.length ? { id: "kundalik", n: "Kundalik", c: (L[0].storyboard.kadrlar?.[0]?.src || L[0].storyboard.rasm), d: L[0].sana, it: L.map((k) => ({ id: k.id, joy: k.sarlavha, hud: "Kundalik", dav: "", d: k.sana, x: "", img: frames(k.storyboard), cta: null, read: "#kundalik" })) } : null;
  })(),
].filter(Boolean).sort((a, b) => (a.d < b.d ? 1 : a.d > b.d ? -1 : 0));
const homeData = {
  r: "",
  projects: folderOrder.map((p) => {
    const L = byProj(p.slug)[0];
    return { slug: p.slug, n: p.nom, q: p.qisqa || p.nom, s: p.soha, x: p.xizmat, t: p.tavsif, since: p.qachondan || "", xs: p.xizmatlar || [], c: byProj(p.slug).length, holat: p.holat, last: L ? { t: L.sarlavha, sk: vis(L) } : null };
  }),
  posts: posts.map((p) => ({ id: p.id, d: p.sana, ps: p.loyiha, pn: projBy[p.loyiha].nom, t: p.sarlavha, m: p.muammo, y: p.yechim, n: p.natija, g: p.tur || "Umumiy", tags: p.teglar || [], sk: vis(p), pl: player(p), cta: p.taklif ? { t: p.taklif.tugma, h: `https://t.me/${site.telegram}?text=${encodeURIComponent(typo(p.taklif.xabar || ""))}` } : null, sb: p.storyboard ? { c: p.storyboard.rasm, f: (p.storyboard.kadrlar || []).map((r) => ({ s: r.src, i: r.izoh || "" })) } : null, demo: !!p.namuna })),
  tg: site.telegram,
  hl: hlGroups.map((g) => ({ id: g.id, it: g.it })),
  sayohat: sayohat.map((t) => ({ id: t.id, d: t.sana, joy: t.joy, hud: t.hudud || "", dav: t.davlat || "", x: t.izoh || "", img: t.rasmlar.map((r) => (typeof r === "string" ? { s: r, i: "" } : { s: r.src, i: r.izoh || "" })), demo: !!t.namuna })),
  kundalik: kundalik.map((k) => ({ id: k.id, d: k.sana, c: k.toifa, t: k.sarlavha, p: Array.isArray(k.matn) ? k.matn : [k.matn || ""], x: k.xulosa || "", img: k.rasmlar || [], h: k.balandlik || 0, joy: k.joy || "", book: k.kitob || null, sb: k.storyboard ? { c: k.storyboard.rasm, f: (k.storyboard.kadrlar || []).map((r) => ({ s: r.src, i: r.izoh || "" })) } : null, demo: !!k.namuna })),
};
const uniq = (f) => new Set(sayohat.map(f).filter(Boolean)).size;
const tStat = { joy: uniq((t) => t.joy), hud: uniq((t) => t.hudud), dav: uniq((t) => t.davlat), img: sayohat.reduce((n, t) => n + t.rasmlar.length, 0) };
const photo = site.rasm ? `<img src="${esc(site.rasm)}" alt="${esc(site.ism)}">` : esc(site.ism[0]);

write("index.html", layout({
  r: "", page: "home", data: homeData, contact: false,
  body: `
${site.hero ? `<section class="hero-cv${hlGroups.length ? " has-hl" : ""}" aria-label="${esc(site.ism)}">
  <picture class="cv-img"><source media="(max-width: 700px)" srcset="${esc(site.hero_m || site.hero)}"><img src="${esc(site.hero)}" alt="${esc(site.ism)} tog'da" fetchpriority="high"></picture>
  <div class="cv-shade" aria-hidden="true"></div>
${hlGroups.length ? `  <nav class="cv-hl" aria-label="Qisqa story'lar"><div class="hl-row gut">${hlGroups.map((g) => `<button type="button" class="hl" data-g="${esc(g.id)}"><span class="hl-ring"><img src="${esc(g.c)}" alt="" loading="lazy"></span><span class="hl-n">${esc(g.n)}</span></button>`).join("")}</div></nav>
` : ""}${sayohat.length ? `  <a class="cv-note" href="#sayohat"><span class="pin-dot" aria-hidden="true"></span>${tStat.joy} ta joyda bo'ldim<i>Sayohatlar →</i></a>` : ""}
  <div class="cv-in gut"><div class="cv-txt">
    <p class="kick"><i></i>salom, men</p>
    <h1>${esc(site.ism)}.</h1>
    <p class="cv-role">${esc(site.lavozim)}</p>
    <p class="cv-bio">${esc(site.bio)}</p>
    <div class="cv-cta"><a class="f-btn" href="#loyihalar">Ishlarimni ko'rish ↓</a><a class="ghost" href="https://t.me/${esc(site.telegram)}" target="_blank" rel="noopener">Telegram</a></div>
  </div></div>
  <svg class="tear-edge" viewBox="0 0 1200 40" preserveAspectRatio="none" aria-hidden="true"><defs><linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="#064E4F"/><stop offset=".22" stop-color="#0B6668"/><stop offset=".5" stop-color="#0E7274"/><stop offset=".78" stop-color="#0B6668"/><stop offset="1" stop-color="#064E4F"/></linearGradient></defs><path fill="url(#tg)" d="${(() => { let d = "M0 40 L0 18", x = 0, s = 7; while (x < 1200) { x = Math.min(1200, x + 14 + ((x * 37) % 23)); const y = 8 + ((x * 53) % 19); d += ` L${x} ${y}`; } return d + " L1200 40 Z"; })()}"/></svg>
</section>
` : ""}<section class="desk gut" id="loyihalar" aria-labelledby="dh">
${site.hero ? "" : `  <div class="mehero"><div class="ph">${photo}</div><div><b>${esc(site.ism)}</b><p>${esc(site.bio)}</p></div></div>
`}  ${(site.xizmatlar || []).length ? `<div class="sh"><p class="kick"><b>01</b><i></i>Nima qila olamiz</p><h2 class="h2s">O'sish nuqtangizni shu to'rt joydan qidiramiz.</h2></div>
  <div class="svc">${site.xizmatlar.map((x, i) => `<a class="svc-c" href="#svcp" data-tag="${esc(x.teg)}" data-nom="${esc(x.nom)}" style="--r:${ROT[i % 6]}"><svg class="pin" aria-hidden="true"><use href="#pinS"/></svg><b>${esc(x.nom)}</b><span>${esc(x.tavsif)}</span><i>Misollar →</i></a>`).join("")}</div>
  <div class="svc-panel" id="svcp" hidden></div>` : ""}
  <div class="desk-h"><p class="kick"><b>02</b><i></i>Mana shunday ishlaymiz</p><h2 class="dh1" id="dh">Loyihalar papkasi.</h2></div>
  <div class="stack" id="stack"></div>
  <noscript><ul>${projects.map((p) => `<li><a style="color:#fff" href="loyiha/${p.slug}.html">${esc(p.nom)}</a></li>`).join("")}</ul></noscript>
  <p class="desk-note"><span class="mouse">Papka ustiga olib boring yoki bosing.</span><span class="touch">Bosib turing va barmoqni yuring: papkalar varaqlanadi.</span></p>
</section>

<section class="inside gut" id="inside" hidden aria-label="Papka ichi"><div class="of" id="of"></div></section>

<section class="wall gut" id="taqvim" aria-labelledby="wh">
  <div class="wall-h" id="wh"><p class="kick"><b>03</b><i></i>Taqvim</p><h2 class="h2l">Har kuni bitta yechim.</h2></div>
  <div class="win">
    <div class="bar">
      <div class="lights"><i></i><i></i><i></i></div>
      <div class="seg" role="group" aria-label="Ko'rinish"><button type="button" data-v="kun" aria-pressed="false">Kun</button><button type="button" data-v="hafta" aria-pressed="false">Hafta</button><button type="button" data-v="oy" aria-pressed="true">Oy</button></div>
    </div>
    <div class="mo"><b id="moT"></b><span class="mnav"><button type="button" id="moP" aria-label="Oldingi oy">←</button><span id="total"></span><button type="button" id="moN" aria-label="Keyingi oy">→</button></span></div>
    <div class="wk"><span>Du</span><span>Se</span><span>Ch</span><span>Pa</span><span>Ju</span><span>Sh</span><span>Ya</span></div>
    <div class="grid" id="grid"></div>
    <div class="weekv" id="weekv" hidden></div>
    <div class="dayv" id="dayv" hidden></div>
  </div>
  <div class="tray" id="tray"><p class="hint">pinlangan kunni bosing ↑</p></div>
  <div class="mob">
    <div class="mo" style="padding:0 2px 8px"><b id="moT2"></b><span class="mnav"><button type="button" id="moP2" aria-label="Oldingi oy">←</button><button type="button" id="moN2" aria-label="Keyingi oy">→</button></span></div>
    <div class="strip" id="strip" aria-label="Kunlar"></div>
    <div id="mhost"></div>
    <div class="pages" id="pages"></div>
  </div>
</section>

${contactBand()}

<section class="jr gut" id="kundalik" aria-labelledby="kdh">
  <div class="jr-h"><p class="kick"><b>04</b><i></i>Ishdan tashqari</p><h2 id="kdh">Kundalik.</h2><p>O'qigan kitoblarim, o'rganganlarim va hayotdagi o'zgarishlar. Har birining oxirida bitta xulosa.</p></div>
  <div class="kd-stats" id="kstats"></div>
  <div class="kd-filters" id="kfil" role="group" aria-label="Toifa bo'yicha saralash"></div>
  <div class="kd-feed" id="kfeed"></div>
  <div class="kd-more"><button type="button" id="kmore" hidden>Yana ko'rsatish</button></div>
</section>
${sayohat.length ? `
<section class="tr gut" id="sayohat" aria-labelledby="trh">
  <div class="tr-h"><p class="kick"><b>05</b><i></i>Qayerlarda bo'ldim</p><h2 class="dh1" id="trh">Sayohatlar.</h2></div>
  <div class="tr-stats">${[[tStat.joy, "ta joy"], [tStat.hud, tStat.hud === 1 ? "hudud" : "ta hudud"], ...(tStat.dav > 1 ? [[tStat.dav, "ta davlat"]] : []), [tStat.img, "ta rasm"]].map(([n, t], i) => `<span class="tstamp" style="--r:${["-5deg", "3deg", "-2deg", "5deg"][i % 4]};--c:${["#9AD2D2", "#F5F5F3", "#9AD2D2", "#F5F5F3"][i % 4]}"><b>${n}</b>${t}</span>`).join("")}</div>
  <div class="tr-grid" id="tgrid"></div>
  <div class="tr-more"><button type="button" id="tmore" hidden>Yana ko'rsatish</button></div>
  <p class="tr-note">Rasmni bosing: story kabi ochiladi.</p>
</section>` : ""}`,
}));

// loyiha ichi
for (const p of projects) {
  const list = byProj(p.slug);
  const types = {};
  list.forEach((x) => { const k = x.tur || "Umumiy"; types[k] = (types[k] || 0) + 1; });
  const mx = Math.max(1, ...Object.values(types));
  const groups = [];
  list.forEach((x) => { const k = x.sana.slice(0, 7); let g = groups.find((g) => g.k === k); if (!g) groups.push((g = { k, items: [] })); g.items.push(x); });
  let n = 0;
  write(`loyiha/${p.slug}.html`, layout({
    r: "../", page: "project", active: "loyihalar", title: p.nom, desc: p.tavsif,
    body: `
<section class="inside gut" aria-labelledby="inh">
  <div class="of">
    <div class="of-tab" id="inh">${esc(p.nom)}<span class="badge">${list.length}</span></div>
    <div class="of-body">
      <aside class="info"><svg class="clip" aria-hidden="true"><use href="#clipS"/></svg>
        <a class="close" href="../index.html#loyihalar">← Papkalarga qaytish</a>
        <div class="f-meta"><span class="live">${p.holat === "faol" ? "Faol" : "Yakunlangan"}</span><span>${esc(p.qachondan || "")}</span></div>
        <h2>${esc(p.nom)}</h2><p>${esc(p.tavsif)}</p>
        <div class="chips">${(p.xizmatlar || []).map((c) => `<span>${esc(c)}</span>`).join("")}</div>
        <div class="bignum"><b>${list.length}</b><span>ta muammo hal qilindi${list[0] ? `<br>oxirgisi: ${day(list[0].sana)}-${OY[mon(list[0].sana) - 1]}` : ""}</span></div>
        ${list.length ? `<div class="types"><h5>Qaysi muammolar</h5>${Object.entries(types).sort((a, b) => b[1] - a[1]).map(([k, v]) => `<div class="trow"><span>${esc(k)}</span><i style="width:${Math.round((v / mx) * 100)}%"></i><em>${v}</em></div>`).join("")}</div>` : ""}
        <a class="f-btn ask" href="https://t.me/${esc(site.telegram)}" target="_blank" rel="noopener">Menda ham shunday muammo bor →</a>
      </aside>
      <div class="docs">${groups.map((g) => `<div class="mon">${OY[+g.k.slice(5) - 1][0].toUpperCase() + OY[+g.k.slice(5) - 1].slice(1)} ${g.k.slice(0, 4)}</div><div class="dlist">${g.items.map((x) => docCard(x, "../", n++)).join("")}</div>`).join("") || '<p class="empty">Bu papkaga hali hujjat tushmagan.</p>'}</div>
    </div>
  </div>
</section>`,
  }));
}

// post varag'i
for (const p of posts) {
  const pr = projBy[p.loyiha], same = byProj(p.loyiha), k = same.findIndex((x) => x.id === p.id);
  const newer = same[k - 1], older = same[k + 1];
  write(`post/${p.id}.html`, layout({
    r: "../", page: "post", title: p.sarlavha, desc: p.muammo,
    body: `
<section class="wallpage post-page gut">
  <article class="post"><div class="sheet">
    <a class="back" href="../loyiha/${pr.slug}.html">← ${esc(pr.nom)} papkasi</a>
    <div class="f-meta">${p.raqam ? `<span>#${p.raqam}</span><span>·</span>` : ""}<span>${sana(p.sana)}</span><span>· ${esc(pr.nom)}</span>${p.tur ? `<span>· ${esc(p.tur)}</span>` : ""}${p.namuna ? '<span class="demo">namuna</span>' : ""}</div>
    <h3>${esc(p.sarlavha)}</h3>
    ${player(p, "../")}
    ${p.hook ? `<p class="p-hook">${esc(p.hook)}</p>` : ""}
    <div class="blocks"><div><b>Muammo</b><p>${esc(p.muammo)}</p>${p.royxat ? `<ol class="p-list">${p.royxat.map((x) => `<li>${esc(x)}</li>`).join("")}</ol>` : ""}</div><div><b>Yechim</b><p>${esc(p.yechim)}</p></div><div><b>Natija</b><p>${esc(p.natija)}</p></div></div>
    ${p.xulosa ? `<p class="p-xul">${esc(p.xulosa)}</p>` : ""}
    ${p.taklif ? `<a class="post-cta" href="https://t.me/${esc(site.telegram)}?text=${esc(encodeURIComponent(typo(p.taklif.xabar || "")))}" target="_blank" rel="noopener">${esc(p.taklif.tugma)} →</a>` : ""}
    <div class="tags">${(p.teglar || []).map((t) => `<span>#${esc(t)}</span>`).join("")}</div>
  </div></article>
  <nav class="pn" aria-label="Shu papkadagi boshqa hujjatlar"><span>${older ? `<a href="${older.id}.html">← ${esc(older.sarlavha)}</a>` : ""}</span><span style="text-align:right">${newer ? `<a href="${newer.id}.html">${esc(newer.sarlavha)} →</a>` : ""}</span></nav>
</section>`,
  }));
}


// 404, sitemap, robots, CNAME
write("404.html", layout({ r: "/", page: "404", title: "Topilmadi", body: `<section class="wallpage gut"><div class="page-h"><h1>Bu sahifa yo'q</h1><p><a href="/index.html">Bosh sahifaga qaytish</a></p></div></section>` }));
const urls = ["index.html", ...projects.map((p) => `loyiha/${p.slug}.html`), ...posts.map((p) => `post/${p.id}.html`)];
write("sitemap.xml", `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.map((u) => `  <url><loc>${site.domen}/${u}</loc></url>`).join("\n")}\n</urlset>\n`);
write("robots.txt", `User-agent: *\nAllow: /\nSitemap: ${site.domen}/sitemap.xml\n`);
write(".nojekyll", "");
// AI agent uchun: Instagram story ID → post havolasi
if (existsSync(join(ROOT, "content/story-map.json"))) cpSync(join(ROOT, "content/story-map.json"), join(OUT, "story-map.json"));
// O'sish Nuqtasi "90 reels" paneli uchun ochiq ma'lumot (navbat, statistika, Mac papka holati)
mkdirSync(join(OUT, "data"), { recursive: true });
for (const f of ["reels-queue.json", "reels-stats.json", "reels-papka.json"]) if (existsSync(join(ROOT, "content", f))) cpSync(join(ROOT, "content", f), join(OUT, "data", f));
if (site.domen) write("CNAME", site.domen.replace(/^https?:\/\//, "") + "\n");

console.log(`Tayyor: ${posts.length} post, ${projects.length} loyiha, ${kundalik.length} kundalik yozuvi, ${sayohat.length} sayohat → dist/`);
