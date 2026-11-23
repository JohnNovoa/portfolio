"""Convert a source image into the WebP files the site uses.

Usage (from the repo root):
    .venv/Scripts/python tools/add_image.py SOURCE NAME [--no-small]

Writes assets/img/NAME.webp (longest side up to 1600 px) and
assets/img/NAME-sm.webp (up to 760 px, for cards and srcset), then prints the
sizes to paste into the <img> width/height attributes.

Transparent images are flattened onto white. Crop, blur faces and pixelate
QR codes or robot numbers BEFORE running this: it only resizes and converts.
"""
import argparse
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'assets', 'img')


def load(path):
    im = Image.open(path)
    if im.mode in ('RGBA', 'LA', 'P'):
        im = im.convert('RGBA')
        bg = Image.new('RGB', im.size, (255, 255, 255))
        bg.paste(im, mask=im.split()[3])
        return bg
    return im.convert('RGB')


def save(im, name, limit):
    im = im.copy()
    im.thumbnail((limit, limit), Image.LANCZOS)
    path = os.path.join(OUT, name + '.webp')
    im.save(path, 'WEBP', quality=84, method=6)
    return path, im.size


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('source')
    ap.add_argument('name', help='file name without extension, for example quadruped-field')
    ap.add_argument('--no-small', action='store_true', help='skip the -sm version')
    args = ap.parse_args()

    im = load(args.source)
    if max(im.size) < 1200:
        print(f'Warning: source is only {im.size[0]}x{im.size[1]} px and may look soft.', file=sys.stderr)
    results = [save(im, args.name, 1600)]
    if not args.no_small:
        results.append(save(im, args.name + '-sm', 760))
    for path, (w, h) in results:
        print(f'{os.path.relpath(path, ROOT)}  width="{w}" height="{h}"')


if __name__ == '__main__':
    main()
