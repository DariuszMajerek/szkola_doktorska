"""Regression tests for stale plot images in browser caches."""
from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from finalize_book import version_images


class ImageVersionTests(unittest.TestCase):
    def test_changed_image_gets_new_version_and_processing_is_idempotent(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            image = root / 'roc.png'
            image.write_bytes(b'first version')
            page = root / 'wyk2.html'
            page.write_text('<img src="roc.png"><img src="https://example.org/remote.png">')
            self.assertEqual(version_images(page), 1)
            first = page.read_text()
            self.assertIn('roc.png?v=', first)
            self.assertIn('https://example.org/remote.png', first)
            version_images(page)
            self.assertEqual(page.read_text(), first)
            image.write_bytes(b'updated plot with thresholds')
            version_images(page)
            self.assertNotEqual(page.read_text(), first)
            self.assertEqual(page.read_text().count('?v='), 1)

    def test_missing_image_fails_build(self) -> None:
        with TemporaryDirectory() as directory:
            page = Path(directory) / 'wyk2.html'
            page.write_text('<img src="missing.png">')
            with self.assertRaises(FileNotFoundError):
                version_images(page)


if __name__ == '__main__':
    unittest.main()
