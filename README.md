# Jahongir | O'N — portfolio sayt

Har kuni hal qilingan muammolar yozib boriladigan portfolio. Statik sayt, server kerak emas, GitHub Pages'da bepul ishlaydi.

## Tuzilma

```
content/
  site.json                 ism, bio, Telegram, domen, rasm
  projects/projects.json    loyihalar (nom, soha, holat: faol / yakunlangan)
  posts/YYYY-MM-DD-nom.json har bir yangilik = bitta fayl
  kundalik.json             shaxsiy blog: Kitob / O'rgandim / Hayot yozuvlari
  sayohat.json              sayohatlar: joy, sana, rasmlar (story kabi ochiladi)
  media/                    rasmlar (masalan jahongir.jpg, sayohat/...)
assets/site.css, site.js    butun dizayn va harakatlar (papkalar, taqvim, kundalik, sayohat)
build.mjs                   sayt generatori → dist/
.github/workflows/deploy.yml  main'ga push bo'lsa sayt o'zi yangilanadi
```

## Brend (O'N brendbuki asosida)

- Nom: **O'N — O'sish Nuqtasi**. Saytdagi brend: `Jahongir | O'N` (`site.json` → `brend`).
- Logotip: "ON", O harfining o'ng yelkasida teal nuqta. Space Grotesk 700; nuqta `top:.05em; right:.06em; 0.15em`; N oldida `0.07em`. Soya, burish, rang almashtirish yo'q.
- Ranglar: Deep `#0A4E50`, Primary `#0E7E80`, Bright `#16A6A9` (faqat nuqtalar: logotip, pin boshlari, son belgilari), Soft `#9AD2D2`, Ink `#17211F`, Paper `#F5F5F3`. Boshqa ranglar faqat post chizmalarida (qizil "oldin", yashil "keyin") va loyiha uslubida.
- Shriftlar: sarlavha Space Grotesk, matn Hanken Grotesk. Caveat (qo'lyozma) faqat qog'oz ustidagi shaxsiy yozuvlarda: stiker, polaroid, story izohi, xulosa qatori.
- Sarlavhalar oddiy gap ko'rinishida, oxirida nuqta bilan ("Loyihalar papkasi."). Bo'lim belgisi: `01 • NOM`.
- Ovoz: aniq, ishonchli, rag'batlantiruvchi, kamtarona. Har bir xizmat matnida o'lchanadigan natija bo'lsin.

## Yangi post qo'shish (hozircha qo'lda, 2-bosqichda bot qiladi)

`content/posts/` ichiga yangi fayl qo'shing:

```json
{
  "id": "2026-10-16-qisqa-nom",
  "sana": "2026-10-16",
  "loyiha": "it-oquv-markazi",
  "sarlavha": "Bir jumlada: qanday muammo hal bo'ldi",
  "teglar": ["lid", "sotuv"],
  "tur": "Lid va sotuv",
  "muammo": "Nima bo'layotgan edi",
  "yechim": "Nima qildik",
  "natija": "Nima o'zgardi (raqamsiz yoki ruxsat bilan)",
  "vizual": { "shablon": "muammo-yechim", "oldin": ["..."], "keyin": ["..."] }
}
```

`id` fayl nomi bilan bir xil bo'lsin. `"chop": false` qo'shsangiz, post saytga chiqmaydi (qoralama).

`tur` — loyiha ichidagi "Qaysi muammolar" grafigi uchun muammo turi.

## 6 ta vizual shablon (mini chizma shulardan avtomatik chiziladi)

| shablon | maydonlar |
|---|---|
| `muammo-yechim` | `oldin: [matn]`, `keyin: [matn]` |
| `jarayon` | `qadamlar: [{t, d}]` |
| `sxema` | `tugunlar: [{t, d}]` (chapdan o'ngga zanjir) |
| `ozgarish` | `korsatkichlar: [{nom, yonalish: "yuqori"/"past", qiymat, yaxshi: true/false}]` |
| `kreativ` | `elementlar: [{nom, rasm?}]` (rasm: `media/...jpg`) |
| `iqtibos` | `matn`, `izoh` |

## Maxfiylik qoidasi

- Mijoz nomi saytda faqat taxallus bilan: "IT o'quv markazi", "Xususiy klinika".
- Raqamlar faqat mijoz ruxsati bilan. Ruxsat yo'q bo'lsa, `ozgarish` shablonida faqat yo'nalish.
- Bu repo **ochiq**. Kunlik xom yozuvlar va mijozning haqiqiy nomi bu yerga hech qachon tushmasin.

## Rasmingizni qo'yish

`content/media/jahongir.jpg` faylini qo'shing va `site.json` ichida `"rasm": "media/jahongir.jpg"` qiling.

## Birinchi joylash

1. GitHub'da yangi **ochiq** repo oching (masalan `portfolio`) va shu papkani push qiling.
2. Repo → Settings → Pages → Source: **GitHub Actions**.
3. Domen: DNS'da `jahongir` uchun CNAME yozuvi → `<github-login>.github.io`. Keyin Settings → Pages → Custom domain: `jahongir.onagy.app`, "Enforce HTTPS" ni yoqing.
4. Telegram mini app: @BotFather → botingiz → Bot Settings → Menu Button → URL: `https://jahongir.onagy.app`.

Domen hali ulanmagan bo'lsa, `site.json` dagi `domen` ni bo'sh qoldiring (`""`): sayt `<login>.github.io/portfolio` manzilida ochiladi.

## Mahalliy ko'rish

```
node build.mjs
npx serve dist
```

## Kundalik yozuvi (shaxsiy blog)

`content/kundalik.json` ro'yxatiga qo'shiladi:

```json
{
  "id": "k-2026-10-18-qisqa-nom",
  "sana": "2026-10-18",
  "toifa": "Hayot",
  "sarlavha": "Sarlavha",
  "matn": ["1-xatboshi", "2-xatboshi"],
  "xulosa": "Bitta jumlali xulosa"
}
```

`toifa`: `Kitob`, `O'rgandim` yoki `Hayot`. Kitob uchun `"kitob": {"nom", "muallif", "rang", "matn_rang", "holat"}` qo'shiladi.

## Sayohat (rasm bilan, uzun matnsiz)

Rasmlar `content/media/sayohat/` ichiga, yozuv `content/sayohat.json` ro'yxatiga:

```json
{
  "id": "s-2026-10-11-chimyon",
  "sana": "2026-10-11",
  "joy": "Chimyon",
  "hudud": "Toshkent viloyati",
  "davlat": "O'zbekiston",
  "izoh": "bitta qisqa qator (ixtiyoriy)",
  "rasmlar": ["media/sayohat/chimyon-1.jpg", {"src": "media/sayohat/chimyon-2.jpg", "izoh": "shu rasm uchun bir qator"}]
}
```

- Kartochkada faqat joy nomi, sana va rasmlar soni chiqadi. Bosilsa, rasmlar story kabi ochiladi (5 soniyadan, surish mumkin).
- Tepadagi hisob (`N ta joy`, `N ta hudud`, `N ta rasm`) o'zi sanaladi. `davlat` 2 tadan oshsa, davlatlar soni ham chiqadi.
- Rasm hajmi: uzun tomoni 1200–1600 px, JPG. Kamida bitta rasm shart.
