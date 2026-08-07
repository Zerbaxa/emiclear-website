"""인스타 카드뉴스 생성 — 1080x1080 캐러셀.

결과물은 scripts/cards/ 에 저장된다. 사이트에 배포되지 않는다.
가변 폰트는 저장소에 두지 않는다. 실행 전 같은 폴더에 내려받을 것:
  NotoSerifKR.ttf  https://github.com/google/fonts/raw/main/ofl/notoserifkr/NotoSerifKR%5Bwght%5D.ttf
  NotoSansKR.ttf   https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf

헤드라인은 Noto Serif KR, 본문은 Noto Sans KR. 사이트와 같은 브랜드 색을 쓴다.
문구를 바꾸려면 맨 아래 CARDS 만 고치면 된다.
"""
from PIL import Image, ImageDraw, ImageFont

S = 1080
PAD = 96

NAVY = (11, 31, 51)
OFFWHITE = (247, 245, 239)
TEAL = (15, 157, 148)
TEAL_DARK = (10, 110, 104)
CORAL = (255, 107, 95)
WHITE = (255, 255, 255)
MUTED_ON_NAVY = (150, 170, 186)
MUTED_ON_LIGHT = (82, 95, 107)

SERIF, SANS = "NotoSerifKR.ttf", "NotoSansKR.ttf"


def font(path, size, name):
    f = ImageFont.truetype(path, size)
    f.set_variation_by_name(name)
    return f


def quad(p0, p1, p2, n=18):
    return [(round((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]),
             round((1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
            for t in (i / n for i in range(n + 1))]


def signal(d, x0, x1, cy, color, amp=0.55, width=5):
    """emiclear-mark.svg 파형 path."""
    s = (x1 - x0) / (99 - 31)
    X = lambda v: x0 + (v - 31) * s
    Y = lambda v: cy + (v - 64) * s * amp
    pts = [(X(31), Y(64)), (X(40), Y(64))]
    pts += quad((X(40), Y(64)), (X(47), Y(53)), (X(54), Y(64)))
    pts += [(X(57.5), Y(64)), (X(59.5), Y(69)), (X(62), Y(30)),
            (X(64.5), Y(76)), (X(66.5), Y(64)), (X(75), Y(64))]
    pts += quad((X(75), Y(64)), (X(84), Y(52)), (X(93), Y(64)))
    pts += [(X(99), Y(64))]
    d.line(pts, fill=color, width=width, joint="curve")
    r = 10
    d.ellipse([X(108) - r, Y(64) - r, X(108) + r, Y(64) + r], fill=CORAL)


def tracked(d, xy, text, f, fill, tracking):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += d.textlength(ch, font=f) + tracking
    return x - tracking


def block(d, lines, x, top, f, fill, lh):
    for i, ln in enumerate(lines):
        d.text((x, top + i * lh), ln, font=f, fill=fill, anchor="la")
    return top + len(lines) * lh


def card(kind, head=None, body=None, label=None, dark=True, index=None, total=None):
    bg, fg = (NAVY, WHITE) if dark else (OFFWHITE, NAVY)
    muted = MUTED_ON_NAVY if dark else MUTED_ON_LIGHT
    im = Image.new("RGB", (S, S), bg)
    d = ImageDraw.Draw(im)

    if kind == "cover":
        signal(d, PAD, PAD + 250, 300, TEAL if dark else TEAL_DARK)
        f = font(SERIF, 92, "SemiBold")
        block(d, head, PAD, 420, f, fg, 122)
        fs = font(SANS, 32, "Medium")
        d.text((PAD, S - PAD - 40), body[0], font=fs, fill=muted, anchor="ls")
        return im

    if kind == "end":
        signal(d, PAD, PAD + 250, 330, TEAL if dark else TEAL_DARK)
        f = font(SERIF, 62, "SemiBold")
        block(d, head, PAD, 440, f, fg, 90)
        fs = font(SANS, 34, "Medium")
        y = S - PAD - 96
        for i, ln in enumerate(body):
            d.text((PAD, y + i * 50), ln, font=fs, fill=muted if i else fg, anchor="la")
        return im

    # 본문 카드
    if label:
        fl = font(SANS, 27, "Bold")
        tracked(d, (PAD, PAD + 40), label, fl, TEAL if dark else TEAL_DARK, 2.4)
    fh = font(SERIF, 68, "SemiBold")
    y = block(d, head, PAD, 300, fh, fg, 96)
    if body:
        fb = font(SANS, 35, "Regular")
        block(d, body, PAD, y + 56, fb, muted, 58)
    if index:
        fi = font(SANS, 26, "Medium")
        d.text((S - PAD, S - PAD - 20), "%d / %d" % (index, total),
               font=fi, fill=muted, anchor="rs")
    return im


CARDS = [
    dict(kind="cover", dark=True,
         head=["아무도 아프지 않은", "세상을 위해."],
         body=["응급의학혁신교육연구회 · EM-I-CLEAR"]),

    dict(kind="body", dark=False, label="우리가 보는 문제",
         head=["새벽 두 시,", "응급실 전화가", "쉬지 않고 울립니다."],
         body=["전국의 구급대에서 걸려오는", "수용 문의입니다."]),

    dict(kind="body", dark=False, label=None,
         head=["수용하고 싶지 않아서", "수용하지 못하는 것이", "아닙니다."],
         body=["수술 하나에도 수술실, 마취 인력,", "집도할 과, 병동 주치의, 중환자실 자리가",
               "동시에 있어야 합니다."]),

    dict(kind="body", dark=False, label=None,
         head=["병원 밖에서는", "그 안이 보이지", "않습니다."],
         body=["아이는 울고 힘들어하는데", "받아주는 곳은 없습니다."]),

    dict(kind="body", dark=True, label=None,
         head=["누가 잘못해서", "벌어지는 일이", "아닙니다."],
         body=["사람과 사람을 이어주어야 할", "시스템이 작동하지 않기 때문입니다.",
               "그 자리에 틈이 생겼습니다."]),

    dict(kind="body", dark=True, label="우리의 방식",
         head=["우리는", "그 틈에 섭니다."],
         body=["교육으로 감당할 사람을 늘리고,", "기술로 자기 상태를 전할 수 있게 돕습니다.",
               "양쪽에서 한 발짝씩 좁힙니다."]),

    dict(kind="end", dark=True,
         head=["그 틈을", "함께 메웁니다."],
         body=["EM-I-CLEAR · 응급의학혁신교육연구회", "독립적 비영리단체 · emiclear.org"]),
]

if __name__ == "__main__":
    n = len(CARDS)
    for i, c in enumerate(CARDS, 1):
        kw = dict(c)
        if kw["kind"] == "body":
            kw.update(index=i, total=n)
        card(**kw).save("cards/card-%02d.png" % i)
    print("%d장 생성" % n)
