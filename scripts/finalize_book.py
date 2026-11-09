"""Finalize Quarto HTML with content-versioned images for GitHub Pages."""
from hashlib import sha256
from pathlib import Path
import re
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit, urlunsplit


def version_images(page: Path) -> int:
    count = 0

    def replace_tag(match: re.Match[str]) -> str:
        nonlocal count
        tag = match.group(0)
        source = re.search(r'\bsrc="([^"]+)"', tag)
        if source is None:
            return tag
        url = urlsplit(source[1])
        if url.scheme or url.netloc or not url.path:
            return tag
        image = (page.parent / unquote(url.path)).resolve()
        if not image.is_file():
            raise FileNotFoundError(f'{page}: {image}')
        query = [(key, value) for key, value in parse_qsl(url.query) if key != 'v']
        query.append(('v', sha256(image.read_bytes()).hexdigest()[:12]))
        versioned = urlunsplit((url.scheme, url.netloc, url.path, urlencode(query), url.fragment))
        count += 1
        return tag[:source.start(1)] + versioned + tag[source.end(1):]

    original = page.read_text(encoding='utf-8')
    updated = re.sub(r'<img\b[^>]*>', replace_tag, original)
    if updated != original:
        page.write_text(updated, encoding='utf-8')
    return count


def remove_unused_figures(pages: list[Path]) -> int:
    referenced: set[Path] = set()
    for page in pages:
        for source in re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', page.read_text(encoding='utf-8')):
            url = urlsplit(source)
            if not url.scheme and not url.netloc:
                referenced.add((page.parent / unquote(url.path)).resolve())
    removed = 0
    for image in Path('docs').glob('wyk[1-6]_files/figure-*/*'):
        if image.is_file() and image.suffix.lower() in {'.png', '.jpg', '.jpeg', '.svg', '.webp'} and image.resolve() not in referenced:
            image.unlink()
            removed += 1
    return removed


def main() -> None:
    directory = Path('docs')
    pages = list(directory.glob('*.html'))
    if not pages:
        raise RuntimeError('Brak wyrenderowanych stron książki.')
    count = sum(version_images(page) for page in pages)
    removed = remove_unused_figures(pages)
    (directory / '.nojekyll').touch()
    print(f'Wersjonowanie obrazów: {count}; usunięte stare wykresy: {removed}; .nojekyll obecny.')


if __name__ == '__main__':
    main()
