"""Check the rendered book, image freshness, ROC thresholds and table precision."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import parse_qs, unquote, urlsplit


class Page(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[tuple[str, str]] = []
        self.tables: list[list[list[str]]] = []
        self.rows: list[list[str]] | None = None
        self.row: list[str] | None = None
        self.cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if name in ('href', 'src') and value:
                self.links.append((tag, value))
        if tag == 'table':
            self.rows = []
        elif tag == 'tr' and self.rows is not None:
            self.row = []
        elif tag in ('td', 'th') and self.row is not None:
            self.cell = []

    def handle_data(self, data: str) -> None:
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in ('td', 'th') and self.cell is not None:
            assert self.row is not None
            self.row.append(''.join(self.cell).strip())
            self.cell = None
        elif tag == 'tr' and self.row is not None:
            assert self.rows is not None
            self.rows.append(self.row)
            self.row = None
        elif tag == 'table' and self.rows is not None:
            self.tables.append(self.rows)
            self.rows = None


def main() -> None:
    pages = [Path('docs/index.html'), *[Path(f'docs/wyk{i}.html') for i in range(1, 7)]]
    assert Path('docs/.nojekyll').is_file()
    total_cells = 0
    for path in pages:
        text = path.read_text(encoding='utf-8')
        assert not re.search(r'<U\+[0-9A-F]{4}>|\ufffd', text), path
        assert 'Podsumowanie dydaktyczne' not in text, path
        assert not re.search(r'\bbrier(?:_class)?\b', text, re.I), path
        page = Page()
        page.feed(text)
        for tag, link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc or not url.path or url.path.startswith('/'):
                continue
            target = path.parent / unquote(url.path)
            assert target.is_file() or (target.is_dir() and (target / "index.html").is_file()), (path, link)
            if tag == 'img':
                expected = sha256(target.read_bytes()).hexdigest()[:12]
                assert parse_qs(url.query).get('v') == [expected], (path, link)
        cells = [cell for table in page.tables for row in table for cell in row]
        total_cells += len(cells)
        for cell in cells:
            assert not re.search(r'\d+[.,]\d{4,}', cell), (path, cell)
        if path.name == 'wyk2.html':
            assert '1-Specyficzność (FPR)' in text and 'Czułość (TPR)' in text
            thresholds = [table for table in page.tables if any(
                'Progi odcięcia i współrzędne punktów ROC' in cell for row in table for cell in row
            )]
            assert len(thresholds) == 1, 'Brak tabeli progów ROC'
            values = [row for row in thresholds[0] if len(row) == 4 and re.fullmatch(r'0[,.]\d{3}', row[0])]
            assert [float(row[0].replace(',', '.')) for row in values] == [0.3, 0.4, 0.5, 0.6, 0.7]
            for row in values:
                specificity, fpr = [float(value.replace(',', '.')) for value in row[2:]]
                assert abs(specificity + fpr - 1) < 0.0011
            assert 'wyk2-liniowosc-logitu-lwt-1.png' in text
            assert 'wyk2-liniowosc-logitu-age-1.png' in text
    for path in Path('.').glob('wyk[1-6].qmd'):
        for code in re.findall(r'^```\{python\}\n(.*?)^```', path.read_text(), re.M | re.S):
            compile(code, str(path), 'exec')
    print(f'OK: {len(pages)} stron, {total_cells} komórek tabel, obrazy, odnośniki i progi ROC.')


if __name__ == '__main__':
    main()
