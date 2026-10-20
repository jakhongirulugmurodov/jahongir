# Karusel slaydlaridan Reels (jahongir.olmos, "reels-birinchi"). Foydalanish: python3 scripts/ig_slideshow_reel.py content/lenta/<post>-ig.json
# Nega: kichik akkauntda karusel deyarli faqat obunachilarga ko'rinadi; Reels esa obuna bo'lmaganlarga ham tavsiya qilinadi.
# Slaydlar 1080x1920 vertikal videoga yig'iladi (har slayd ~3.5 s, yumshoq o'tish), GitHub Release'ga yuklanadi va scripts/ig_reel.py bilan joylanadi.
# Muvaffaqiyatli bo'lsa post ID → havola content/story-map.json ga yoziladi (izohga "AI" yozganga maqola ketadi).
import json, os, re, shutil, subprocess, sys, tempfile, urllib.request
spec = json.load(open(sys.argv[1]))
slug = re.sub(r"[^a-z0-9-]", "", os.path.basename(sys.argv[1]).replace("-ig.json", "").lower()) or "post"
REPO = os.environ.get("GITHUB_REPOSITORY", "jakhongirulugmurodov/jahongir"); REL = "lenta-reels"
SEC, FADE = 3.5, 0.4

def ffmpeg():
    p = shutil.which("ffmpeg")
    if p: return p
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "imageio-ffmpeg"], check=True)
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()

d = tempfile.mkdtemp()
imgs = []
for i, u in enumerate(spec["rasmlar"]):
    f = os.path.join(d, f"{i:02d}.jpg")
    urllib.request.urlretrieve(u, f); imgs.append(f)
if not imgs: sys.exit("slayd yo'q")

# Har slayd: 1080 kenglikka sig'diriladi, vertikal kadr markazida, fon — o'sha slaydning xira kattalashtirilgani
ff = ffmpeg(); out = os.path.join(d, f"{slug}.mp4")
args = [ff, "-y", "-loglevel", "error"]
for f in imgs: args += ["-loop", "1", "-t", str(SEC), "-i", f]
args += ["-f", "lavfi", "-t", str(SEC * len(imgs)), "-i", "anullsrc=r=44100:cl=stereo"]  # jim audio yo'lagi (ba'zi pleerlar audiosiz videoni yoqtirmaydi)
parts = []
for i in range(len(imgs)):
    parts.append(f"[{i}:v]split[a{i}][b{i}];[a{i}]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:5,eq=brightness=-0.15[bg{i}];"
                 f"[b{i}]scale=1080:-2:force_original_aspect_ratio=decrease[fg{i}];[bg{i}][fg{i}]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=30,format=yuv420p[v{i}]")
chain, last, off = "", "[v0]", SEC - FADE
for i in range(1, len(imgs)):
    chain += f";{last}[v{i}]xfade=transition=fade:duration={FADE}:offset={off:.2f}[x{i}]"; last = f"[x{i}]"; off += SEC - FADE
chain += f";{last}scale=out_range=tv,format=yuv420p[vout]"  # Instagram uchun standart (tv) rang diapazoni
args += ["-filter_complex", ";".join(parts) + chain, "-map", "[vout]", "-map", f"{len(imgs)}:a", "-shortest",
         "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out]
r = subprocess.run(args, capture_output=True, text=True)
if r.returncode or not os.path.exists(out): sys.exit("video yig'ilmadi: " + r.stderr[-400:])

# GitHub Release'ga yuklash (ochiq havola kerak — Instagram videoni o'zi yuklab oladi)
env = dict(os.environ)
if subprocess.run(["gh", "release", "view", REL, "-R", REPO], capture_output=True, env=env).returncode:
    subprocess.run(["gh", "release", "create", REL, "-R", REPO, "--title", "Lenta reels (karuseldan)", "--notes", "Avtomatik: karusel slaydlaridan yig'ilgan reels videolar"], check=True, env=env)
subprocess.run(["gh", "release", "upload", REL, out, "-R", REPO, "--clobber"], check=True, env=env)
url = f"https://github.com/{REPO}/releases/download/{REL}/{slug}.mp4"

cap = os.path.join(d, "cap.txt"); open(cap, "w").write(spec["izoh"])
r = subprocess.run([sys.executable, "scripts/ig_reel.py", url, cap, "1000"], capture_output=True, text=True, env=env)
print(r.stdout.strip()); print(r.stderr.strip()[-300:])
m = re.search(r'"id": "(\d+)"', r.stdout)
if r.returncode or not m: sys.exit(1)
if spec.get("havola"):
    sm = json.load(open("content/story-map.json"))
    sm.setdefault("stories", {})[m.group(1)] = {"url": spec["havola"], "title": spec.get("sarlavha", ""), "tur": "reels"}
    json.dump(sm, open("content/story-map.json", "w"), ensure_ascii=False, indent=2)
