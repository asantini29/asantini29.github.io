import contextlib
import io
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sync_cv import (  # noqa: E402
    SyncError,
    fetch_bibtex,
    main,
    read_accent_color,
    transform_bibtex,
)

PUBLISHED = r'''@article{Santini:2025iuj,
    author = "Santini, Alessandro and Muratore, Martina",
    title = "{Flexible, GPU-accelerated approach}",
    eprint = "2507.06300",
    archivePrefix = "arXiv",
    primaryClass = "gr-qc",
    doi = "10.1103/csx9-9trp",
    journal = "Phys. Rev. D",
    volume = "112",
    year = "2025"
}
'''
PREPRINT = r'''@article{X:2026abc,
    author = "Santini, Alessandro",
    title = "{Mergers could explain the observed q-{\ensuremath{\chi}}eff correlation}",
    eprint = "2601.00001",
    archivePrefix = "arXiv",
    primaryClass = "gr-qc",
    year = "2026"
}
'''
FIXTURE = PUBLISHED + "\n" + PREPRINT


def entry(bib, key):
    """The text of one BibTeX entry, from its @ line to the next @."""
    start = bib.index(key)
    end = bib.find("\n@", start)
    return bib[start:] if end == -1 else bib[start:end]


class AccentColorTest(unittest.TestCase):
    def test_reads_mycolor_ignoring_trailing_comment(self):
        self.assertEqual(
            read_accent_color(r"\newcommand{\mycolor}{0969da}%088395}"), "#0969da"
        )

    def test_missing_color_raises(self):
        with self.assertRaises(SyncError):
            read_accent_color(r"\newcommand{\myname}{Alessandro Santini}")


class TransformTest(unittest.TestCase):
    def test_adds_arxiv_from_eprint(self):
        out = transform_bibtex(FIXTURE, [])
        self.assertIn('arxiv = "2507.06300"', entry(out, "Santini:2025iuj"))
        self.assertIn('arxiv = "2601.00001"', entry(out, "X:2026abc"))

    def test_preprint_without_journal_becomes_unpublished(self):
        out = transform_bibtex(FIXTURE, [])
        self.assertIn("@unpublished{X:2026abc,", out)
        self.assertIn("@article{Santini:2025iuj,", out)

    def test_strips_ensuremath(self):
        out = transform_bibtex(FIXTURE, [])
        self.assertNotIn(r"\ensuremath", out)
        self.assertIn(r"q-{{\chi}}eff", out)

    def test_injects_extras_into_matching_entry_only(self):
        out = transform_bibtex(
            FIXTURE,
            [{"arxiv": "2507.06300", "selected": True, "code": "https://github.com/x"}],
        )
        published = entry(out, "Santini:2025iuj")
        self.assertIn('selected = "true"', published)
        self.assertIn('code = "https://github.com/x"', published)
        self.assertNotIn("selected", entry(out, "X:2026abc"))

    def test_unknown_arxiv_raises_and_mentions_quotes(self):
        with self.assertRaises(SyncError) as ctx:
            transform_bibtex(FIXTURE, [{"arxiv": 2507.063}])
        self.assertIn("2507.063", str(ctx.exception))
        self.assertIn("quote", str(ctx.exception))


class FetchTest(unittest.TestCase):
    def test_unreachable_raises(self):
        with self.assertRaises(SyncError):
            fetch_bibtex("http://127.0.0.1:9/")

    def test_zero_entries_raises(self):
        with tempfile.NamedTemporaryFile("w", suffix=".bib", delete=False) as f:
            f.write("\n")
        try:
            with self.assertRaises(SyncError):
                fetch_bibtex(pathlib.Path(f.name).as_uri())
        finally:
            os.unlink(f.name)


class MainTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = pathlib.Path(self.tmp.name)
        self.cv = root / "myCV"
        self.site = root / "site"
        (self.cv / "data").mkdir(parents=True)
        (self.site / "_data").mkdir(parents=True)
        (self.site / "assets").mkdir()
        for name in ("talks.yml", "outreach.yml", "education.yml"):
            (self.cv / "data" / name).write_text("# %s\n- event: E\n" % name)
        (self.cv / "data" / "papers.yml").write_text(
            '- arxiv: "2507.06300"\n  selected: true\n'
        )
        (self.cv / "personalinfo.tex").write_text(r"\newcommand{\mycolor}{0969da}%088395}")
        bib = root / "inspire.bib"
        bib.write_text(FIXTURE)
        self.inspire = bib.as_uri()

    def tearDown(self):
        self.tmp.cleanup()

    def run_main(self, *extra):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = main(["--cv", str(self.cv), "--site", str(self.site), *extra])
        return code, err.getvalue()

    def test_missing_cv_dir_returns_1(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            code = main(["--cv", "/nonexistent", "--site", str(self.site)])
        self.assertEqual(code, 1)

    def test_writes_outputs(self):
        code, _ = self.run_main("--inspire-url", self.inspire)
        self.assertEqual(code, 0)
        self.assertEqual(
            (self.site / "_data" / "talks.yml").read_text(), "# talks.yml\n- event: E\n"
        )
        self.assertTrue((self.site / "_data" / "outreach.yml").exists())
        self.assertTrue((self.site / "_data" / "education.yml").exists())
        ref = (self.site / "assets" / "ref.bib").read_text()
        self.assertIn('selected = "true"', entry(ref, "Santini:2025iuj"))
        self.assertIn('accent_color: "#0969da"', (self.site / "_config_cv.yml").read_text())

    def test_inspire_failure_writes_nothing(self):
        (self.site / "assets" / "ref.bib").write_text("OLD")
        code, err = self.run_main("--inspire-url", "http://127.0.0.1:9/")
        self.assertEqual(code, 1)
        self.assertTrue(err)
        self.assertEqual((self.site / "assets" / "ref.bib").read_text(), "OLD")
        self.assertFalse((self.site / "_data" / "talks.yml").exists())
        self.assertFalse((self.site / "_config_cv.yml").exists())


if __name__ == "__main__":
    unittest.main()
