#!/bin/bash
# Tayyor reels partiyasini reels-inbox shoxi orqali Release'ga yuboradi (sessiyadan Release API yopiq).
# Foydalanish (repo ildizidan): tools/reels/inbox.sh <videolar papkasi> <izohlar.json>
# Videolar 60MB bo'laklarga bo'linadi (GitHub 100MB fayl chegarasi); "Reels qabul" ishi yig'ib, navbatga qo'shadi va shoxni o'chiradi.
set -e
SRC="$1"; CAPS="$2"; REPO=$(pwd); W=$(mktemp -d)
mkdir -p "$W/inbox"; cp "$CAPS" "$W/inbox/izohlar.json"
for f in "$SRC"/*.mp4; do split -b 60m -d -a 2 "$f" "$W/inbox/$(basename "$f").part"; done
cd "$W"; git init -q -b reels-inbox
git -c user.name=reels-bot -c user.email=reels-bot@users.noreply.github.com add . 
git -c user.name=reels-bot -c user.email=reels-bot@users.noreply.github.com commit -qm "reels inbox"
git push -q -f "$(git -C "$REPO" remote get-url origin)" reels-inbox
cd "$REPO"; gh api -X POST repos/jakhongirulugmurodov/jahongir/actions/workflows/reels-inbox.yml/dispatches -f ref=main
echo "yuborildi: $(ls "$SRC"/*.mp4 | wc -l) ta video; 'Reels qabul' ishi navbatga qo'shadi"
