import os
import tempfile
import time
from pathlib import Path

from playwright.sync_api import sync_playwright
import moviepy.editor as mp
from terminhtml.main import TerminHTML

PROJECT_ROOT = Path(__file__).parent
DOCS_IMAGES = PROJECT_ROOT / "docsrc" / "source" / "_static" / "images"
VIDEOS_DIR = PROJECT_ROOT / "videos"


def create_demo_output_gif(out_folder: Path = DOCS_IMAGES):
    out_path = out_folder / f"demo-output.gif"
    is_ci = os.getenv("CI")
    delay = 3 if is_ci else 1.1
    if out_path.exists():
        print(f"{out_path} already exists, skipping")
        return
    print("Creating demo output gif")
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir)
        term = TerminHTML.from_commands(
            ["python -m terminhtml.demo_output"],
            cwd=PROJECT_ROOT,
            prompt_matchers=["\\[0m: "],
            input=["Nick DeRobertis"],
        )
        html_path = temp_path / "termin.html"
        html_path.write_text(term.to_html())

        with sync_playwright() as p:
            browser = p.chromium.launch()
            dimensions = dict(width=800, height=530)
            context = browser.new_context(
                viewport=dimensions,
                record_video_dir=str(temp_path.resolve()),
                record_video_size=dimensions,
            )
            page = context.new_page()
            page.goto(html_path.as_uri())
            speed_up = page.locator("text=►")
            speed_down = page.locator("text=◄")
            time.sleep(1)
            speed_up.click()
            time.sleep(1)
            speed_up.click()
            time.sleep(0.5)
            speed_down.click()
            page.locator("text=restart ↻").wait_for()
            context.close()
            browser.close()

        for video in temp_path.glob("*.webm"):
            clip = mp.VideoFileClip(str(video.resolve()))
            # Remove first portion of clip before terminhtml-js loads
            clip = clip.subclip(delay, clip.duration)
            clip.write_gif(str(out_path.resolve()))
            print(f"Demo output gif saved to {out_path}")


if __name__ == "__main__":
    create_demo_output_gif()
