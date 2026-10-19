# tools/ — kontent tayyorlash vositalari

Bu papka saytga chiqmaydi (build.mjs faqat `assets/` va `content/media/` ni ko'chiradi).
Har kuni yangi post tayyorlash shu vositalar bilan qilinadi.

## Kerakli narsalar
- Python 3, Pillow, Playwright va Chromium (`pip install playwright pillow`).
- Shriftlar `tools/fonts/` ichida: Space Grotesk, Hanken Grotesk, Caveat. Internet shart emas.

## Har kunlik tartib
1. Jahongir chatga bugungi ishni yuboradi (matn yoki ekran rasmi; ovozni Telegram "→A" bilan matnga o'giradi).
2. Tahlil: mijoz og'rig'i nima, post qilishga arziydimi. Har yangilik post bo'lmaydi.
3. Post sotuv qolipida yoziladi: og'riq → yechim → natija → bitta taklif (Telegram tugmasi, tayyor xabar bilan).
   - Oddiy, odamcha o'zbekcha. Jargon va "AI hidi" yo'q. "yaratmoq" fe'li ishlatilmaydi. Faqat lotin.
   - Isbotsiz raqam yozilmaydi.
4. Storyboard chiziladi (`storyboard/`), oldindan ko'rish artifakti (`mksingle.py`) ko'rsatiladi.
5. "tasdiqlandi" dan keyin `main` ga push → sayt ~20 soniyada yangilanadi.
6. So'ralsa story: `story/` dan tik rasm → "Story joylash (Telegram + Instagram)" workflow.

## Storyboard (qo'lda chizilgan uslub)
- `storyboard/sblib.py` — odamcha (`person`), pufak (`bubble`), kadr (`panel`), `render(sarlavha, o'ng_yozuv, kadrlar, chiqish.html)`.
- `storyboard/v2.py` — sotuv postlari namunasi (oxirgi kadr `offer()`: chizilgan tugma YO'Q, "pastdagi tugmani bosing ↓").
- `storyboard/gen.py` — kundalik namunasi.
- Kesish: `python3 tools/storyboard/crop.py <fayl.html> content/media/loyiha/<slug>/<nom> <balandlik> <kadr soni>`
  - 6 kadr → balandlik 1160; 3 kadr → 650. Natija: `<nom>.jpg` (muqova, 1600px) va `<nom>-1..N.jpg`.

## Story (1080×1920)
- `story/telegram.html` — "Saytni ochish →" tugmali (Telegram'da havola maydoni tugma ustiga qo'yiladi).
- `story/instagram.html` — "AI deb yozing, to'liq maqolani yuboraman" (havola Instagram'da bosilmaydi; AI agent Direct'ga yuboradi).
- Render: `python3 tools/story/shot.py <fayl.html> <chiqish.jpg>` → tugma koordinatalarini chop etadi.
  Havola maydoni foizda: x = (chap + en/2)/1080·100, y = (yuqori + bo'y/2)/1920·100, w = en/1080·100, h = bo'y/1920·100.
- Rasmlar `content/media/story/` ga, keyin workflow `story.yml` (inputs: tg_rasm, ig_rasm, havola, sarlavha, maydon, soat, qayer).
- Instagram story ID → havola avtomat `content/story-map.json` ga yoziladi (AI agent shuni o'qiydi).

## Oldindan ko'rish (bitta fayl)
`node build.mjs && python3 tools/mksingle.py <chiqish.html>` — rasmlar ichiga joylangan bitta HTML.

## Maxfiy kalitlar (GitHub Secrets, hech qachon chatga yozilmaydi)
- `TG_BOT_TOKEN` — @jahongir_on_bot (faqat story ruxsati, Telegram Business orqali @sp_business_agency).
- `IG_TOKEN` — Meta ilova "Jahongir Portfolio" (faqat basic + content_publish). ~60 kunda eskiradi, qo'lda yangilanadi.

## carousel/
- `konveyer.py <papka>` — 10 slaydli karusel panoramasi (10800×1350, doodle uslubi), `render.py` — PNG'ga chizib 10 ta 1080×1350 JPG'ga bo'ladi. Yangi karusel uchun shu faylni nusxalab, slayd matn/rasmlarini almashtiring.
- Joylash: `content/lenta/<post>-ig.json` + `content/lenta-queue.json` (tur: karusel | kanal). Navbatni `story-queue.yml` har 10 daqiqada bajaradi (`scripts/lenta_queue.py`).

## reels/ (O‘sish Nuqtasi, @osish.nuqtasi)
- Tayyor reels Mac'da ~/Osish Nuqtasi Reels papkasiga tashlanadi: video.mp4 + shu nomli video.txt (caption). Navbatga olinganlari Navbatda/ ichiga o'tkaziladi. Partiya: fayllar konteynerga olinadi → `tools/reels/inbox.sh <papka> <izohlar.json>` ularni bo'laklab reels-inbox shoxiga yuboradi, "Reels qabul" ishi (`reels-inbox.yml`) yig'ib Release'ga yuklaydi va `content/reels-queue.json`ga qo'shadi (`yukla.py`). Tayyor bo'lishi bilan navbatga olinadi — kutish chegarasi yo'q.
- Kunlik soni zaxiraga qarab (navbat + papka): 1–20 → 1 ta (14:00), 21–40 → 2 ta (10:00, 19:00), 41+ → 3 ta (09:00, 14:00, 20:00).
- Joylash: `navbat-soqchi.yml` har daqiqada `scripts/reels_queue.py` → `scripts/ig_reel.py` (resumable upload, token: `IG_TOKEN_OSISH`). Mac o'chiq bo'lsa ham ishlaydi.
- Tokenni tekshirish: "Instagram ulanishini tekshirish" workflow'i, akkaunt = osish.
