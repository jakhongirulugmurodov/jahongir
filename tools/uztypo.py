# O'zbek lotin imlosi tipografiyasi: o' g' → o‘ g‘ (U+2018), tutuq belgisi → ’ (U+2019).
# typo(matn) — oddiy matn; typo_markup(html/svg) — faqat teglar orasidagi matnga (script/style'ga tegmaydi).
import re
OKINA, TUTUQ = "\u2018", "\u2019"  # barcha shriftlarda bor (Caveat da U+02BB yo‘q)
_A = "['’‘`ʼʻ]"
_L = "A-Za-zʻʼ"
def typo(s):
    s = re.sub(r"(?<=[A-Za-z])(&#39;|&#x27;|&apos;)(?=[A-Za-z])", "'", s)
    s = re.sub(rf"([oOgG]){_A}(?=[A-Za-z])", rf"\1{OKINA}", s)
    s = re.sub(r"(?<=[A-Za-z])['`\u02bc](?=[A-Za-z])", TUTUQ, s)
    return s
def typo_markup(h):
    out, pos = [], 0
    for m in re.finditer(r"<(script|style)\b.*?</\1>|<[^>]+>", h, flags=re.S | re.I):
        out.append(typo(h[pos:m.start()])); out.append(m.group(0)); pos = m.end()
    out.append(typo(h[pos:])); return "".join(out)
if __name__ == "__main__":
    for t in ["o'zi bo'ldi", "G'ayrat", "ma'lumot", "Instagram'da", "To'liq o'qish", "\"narxi qancha?\" deb"]: print(t, "→", typo(t))
