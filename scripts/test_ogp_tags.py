from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parent.parent


def build_site(tmp_path: Path) -> Path:
    public_dir = tmp_path / "public"
    subprocess.run(
        ["hugo", "--destination", str(public_dir)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return public_dir


def read_page(public_dir: Path, relative_path: str) -> str:
    return (public_dir / relative_path / "index.html").read_text()


def test_post_pages_emit_open_graph_metadata(tmp_path: Path) -> None:
    public_dir = build_site(tmp_path)

    cases = [
        (
            "llm-in-the-loop",
            [
                '<meta property="og:site_name" content="kumekay">',
                '<meta property="og:title" content="LLM-in-the-Loop | kumekay">',
                '<meta property="og:type" content="article">',
                '<meta property="og:url" content="https://kumekay.com/llm-in-the-loop/">',
                '<meta property="og:description" content="It is &#34;LLM-in-the-Loop&#34; of human activities, not the other way around.">',
                '<meta property="og:image" content="https://kumekay.com/llm-in-the-loop/loop_hu_',
            ],
        ),
        (
            "utoolek/monitoradlo",
            [
                '<meta property="og:site_name" content="kumekay">',
                '<meta property="og:title" content="monitoradlo | kumekay">',
                '<meta property="og:type" content="article">',
                '<meta property="og:url" content="https://kumekay.com/utoolek/monitoradlo/">',
                '<meta property="og:description" content="I’m using Niri as my Wayland compositor, and Kanshi to manage monitor layouts. However, editing Kanshi’s config files by handis annoying (though I like to practice mental math a bit). I wanted a more …">',
                '<meta property="og:image" content="https://kumekay.com/utoolek/monitoradlo/monitoradlo_hu_',
            ],
        ),
        (
            "drozdi/conf-time",
            [
                '<meta property="og:site_name" content="kumekay">',
                '<meta property="og:title" content="ИИ конференции устарели | kumekay">',
                '<meta property="og:type" content="article">',
                '<meta property="og:url" content="https://kumekay.com/drozdi/conf-time/">',
                '<meta property="og:description" content="Еще одна мысль о конференциях про искусственный интеллект. Они в общем-то устарели. Как какое-то время назад устарели книги об инструментах для программирования, так как к моменту издания книги она …">',
                '<meta property="og:image" content="https://kumekay.com/drozdi/conf-time/time_hu_',
            ],
        ),
    ]

    for relative_path, expected_fragments in cases:
        html = read_page(public_dir, relative_path)
        for fragment in expected_fragments:
            assert fragment in html


def test_head_partial_uses_trimspace_again() -> None:
    head_partial = (ROOT / "layouts" / "partials" / "head.html").read_text()

    assert "strings.TrimSpace" in head_partial
