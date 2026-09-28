"""PPT 슬라이드 PNG를 웹용 webp로 변환한다 (#131).

deck_u2.LESSONS / deck_u3.LESSONS 안에서 실제로 쓰는 슬라이드 번호만 모아,
원본 PNG(가로 1280 근처)를 web/assets/slides/u{2,3}/s{NN|NNN}.webp로 만든다.
build.py는 이 webp만 참조한다 — 원본 PNG는 저장소에 들어가지 않는다.

사용법
------
    /tmp/mlenv/bin/python tools/web/slide_images.py
    /tmp/mlenv/bin/python tools/web/slide_images.py --src /path/to/slides

원본 경로는 --src 인자 또는 SLIDE_SRC 환경 변수로 바꿀 수 있다(기본 /tmp/slides).
원본 PNG가 없으면(예: 다른 컴퓨터, 원본 정리 후) 그 슬라이드는 조용히
건너뛴다 — 이미 있는 web/assets/slides의 webp는 그대로 둔다. build.py는
webp가 없어도 실패하지 않지만(파손된 페이지가 되므로) 커밋 전에는 반드시
이 스크립트로 채워야 한다.
"""
import argparse
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from PIL import Image
except ImportError:  # pragma: no cover
    raise SystemExit(
        "Pillow가 필요합니다. 예: /tmp/mlenv/bin/python tools/web/slide_images.py"
    )

ROOT = Path(__file__).resolve().parents[2]
WEB = ROOT / 'web'
MAX_WIDTH = 1280
QUALITY = 80


def digits(unit):
    return 2 if unit == 2 else 3


def used_slides(unit):
    import deck_u2, deck_u3
    lessons = (deck_u2.LESSONS if unit == 2 else deck_u3.LESSONS).values()
    return sorted({s['n'] for lesson in lessons for s in lesson.get('slides', ())})


def convert_one(src_png, dst_webp):
    dst_webp.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src_png) as im:
        im = im.convert('RGB')
        if im.width > MAX_WIDTH:
            ratio = MAX_WIDTH / im.width
            im = im.resize((MAX_WIDTH, round(im.height * ratio)), Image.LANCZOS)
        im.save(dst_webp, 'WEBP', quality=QUALITY)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', default=os.environ.get('SLIDE_SRC', '/tmp/slides'))
    args = parser.parse_args()
    src_root = Path(args.src)

    total_converted = 0
    total_skipped = 0
    for unit in (2, 3):
        w = digits(unit)
        src_dir = src_root / f'u{unit}'
        dst_dir = WEB / 'assets/slides' / f'u{unit}'
        for n in used_slides(unit):
            src = src_dir / f's-{n:0{w}d}.png'
            dst = dst_dir / f's{n:0{w}d}.webp'
            if not src.is_file():
                total_skipped += 1
                if not dst.exists():
                    print(f'[경고] 원본도 기존 webp도 없음: {dst.relative_to(WEB)}')
                continue
            convert_one(src, dst)
            total_converted += 1
    print(f'변환 {total_converted}개, 원본 없어 건너뜀 {total_skipped}개')


if __name__ == '__main__':
    main()
