"""OG 이미지 합성 — 사진 + 좌측 그라디언트 + 워드마크/심전도 + 헤드라인.

문구를 바꾸려면 맨 아래 build() 인자만 고치고 실행한다. 글자 크기는 자동으로 맞는다.
가변 폰트는 저장소에 두지 않는다. 실행 전 같은 폴더에 내려받을 것:
  NotoSerifKR.ttf  https://github.com/google/fonts/raw/main/ofl/notoserifkr/NotoSerifKR%5Bwght%5D.ttf
  Newsreader.ttf   https://github.com/google/fonts/raw/main/ofl/newsreader/Newsreader%5Bopsz%2Cwght%5D.ttf
  Manrope.ttf      https://github.com/google/fonts/raw/main/ofl/manrope/Manrope%5Bwght%5D.ttf

모든 요소를 소스에서 다시 그리므로 문구는 언제든 바꿀 수 있다.
심전도 파형은 public/brand/emiclear-mark.svg 의 path 를 그대로 옮긴 것이다.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PHOTO = ("/Users/minkyo/Documents/Non-Profit/emiclear-site/public/images/"
         "medical-desk-pexels-5407251.jpg")

NAVY = (4, 25, 50)
TEAL = (15, 157, 148)
CORAL = (255, 107, 95)
WHITE = (255, 255, 255)

TEXT_X = 74
WORD_BASE = 209          # 워드마크 베이스라인
SIG_Y = 197              # 심전도 중심선
HEAD_BASE = 330          # 헤드라인 첫 줄 베이스라인
MAX_RIGHT = 726         # 헤드라인 오른쪽 한계

GRAD_SOLID = 470        # 이 x까지 배경 완전 불투명
GRAD_FADE = 330         # 이후 사진이 드러나는 폭


def font(path, size, name):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_name(name)
    return f


def ease(t):
    return (1 - math.cos(math.pi * min(max(t, 0.0), 1.0))) / 2


def base_image():
    """사진을 1200x630으로 채우고 좌측 네이비 그라디언트를 얹는다."""
    im = Image.open(PHOTO).convert("RGB")
    # 청진기와 노트가 오른쪽에 오도록 아래쪽 중앙을 쓴다.
    r = max(W / im.width, H / im.height)
    im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    top = round(im.height * 0.34)
    im = im.crop((0, top, W, top + H))

    # 히어로(.story-hero)의 좌→우 그라디언트와 같은 구조. 스톱만 조금 옅게 잡았다.
    #   히어로  .83 / .63 / .23   →   OG  .78 / .58 / .20
    stops = [(0.00, 0.84), (0.46, 0.62), (0.78, 0.22), (1.00, 0.22)]
    layer = Image.new("RGBA", (W, H), NAVY + (0,))
    px = layer.load()
    for x in range(W):
        t = x / (W - 1)
        for i in range(len(stops) - 1):
            (t0, a0), (t1, a1) = stops[i], stops[i + 1]
            if t0 <= t <= t1:
                a = a0 + (a1 - a0) * ((t - t0) / (t1 - t0) if t1 > t0 else 0)
                break
        v = NAVY + (round(255 * a),)
        for y in range(H):
            px[x, y] = v
    return Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")


def quad(p0, p1, p2, n=18):
    """2차 베지어를 점열로."""
    return [(round((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]),
             round((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
            for t in (i / n for i in range(n + 1))]


def draw_signal(d, x0, x1, cy, amp=0.52, width=3):
    """emiclear-mark.svg 의 파형 path 를 x0~x1 구간에 옮겨 그린다.

    원본 path 는 viewBox 128 기준 x31~99, 중심 y64, 끝에 x108 코럴 점.
    가로 배너에서는 세로 진폭을 눌러야 가느다란 신호선으로 읽힌다.
    """
    s = (x1 - x0) / (99 - 31)
    def X(v): return x0 + (v - 31) * s
    def Y(v): return cy + (v - 64) * s * amp

    pts = [(X(31), Y(64)), (X(40), Y(64))]
    pts += quad((X(40), Y(64)), (X(47), Y(53)), (X(54), Y(64)))
    pts += [(X(57.5), Y(64)), (X(59.5), Y(69)), (X(62), Y(30)),
            (X(64.5), Y(76)), (X(66.5), Y(64)), (X(75), Y(64))]
    pts += quad((X(75), Y(64)), (X(84), Y(52)), (X(93), Y(64)))
    pts += [(X(99), Y(64))]
    d.line(pts, fill=TEAL, width=width, joint="curve")

    r = 6.5
    cx, cyy = X(108), Y(64)
    d.ellipse([cx - r, cyy - r, cx + r, cyy + r], fill=CORAL)


def tracked(d, xy, text, f, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += d.textlength(ch, font=f) + tracking
    return x - tracking


def fit(lines, path, name, start):
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for size in range(start, 30, -1):
        f = font(path, size, name)
        if TEXT_X + max(probe.textlength(l, font=f) for l in lines) <= MAX_RIGHT:
            return f, size
    raise SystemExit("맞는 크기 없음")


def build(out, lines, serif, name, start, lh_ratio):
    im = base_image()
    d = ImageDraw.Draw(im)

    end = tracked(d, (TEXT_X, WORD_BASE), "EM-I-CLEAR",
                  font("Manrope.ttf", 27, "ExtraBold"), WHITE, 3.6)
    draw_signal(d, end + 28, end + 196, SIG_Y)

    f, size = fit(lines, serif, name, start)
    lh = round(size * lh_ratio)
    for i, ln in enumerate(lines):
        d.text((TEXT_X, HEAD_BASE + i * lh), ln, font=f, fill=WHITE, anchor="ls")

    im.save(out, quality=92)
    print("%s  헤드라인 %dpx" % (out, size))


if __name__ == "__main__":
    build("../public/og.png", ["아무도 아프지 않은", "세상을 위해."],
          "NotoSerifKR.ttf", "SemiBold", start=86, lh_ratio=1.26)
    build("../public/og-en.png", ["For a world where", "no one has to suffer."],
          "Newsreader.ttf", "SemiBold", start=100, lh_ratio=1.18)
