
import os
import re
import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright


PATH_TO_VIDEO_FOLDER = "./video"


VISUAL_CURSOR_SCRIPT = r"""
(() => {
    if (document.getElementById("custom-cursor-container")) {
        return;
    }

    const container = document.createElement("div");
    container.id = "custom-cursor-container";

    Object.assign(container.style, {
        position: "fixed",
        left: "0px",
        top: "0px",
        width: "64px",
        height: "64px",
        transform: "translate(-50%, -50%)",
        pointerEvents: "none",
        zIndex: "2147483647"
    });

    const highlight = document.createElement("div");

    Object.assign(highlight.style, {
        position: "absolute",
        left: "0px",
        top: "0px",
        width: "64px",
        height: "64px",
        borderRadius: "50%",
        background: "rgba(255, 220, 0, 0.35)",
        pointerEvents: "none"
    });

    const arrow = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "svg"
    );

    arrow.setAttribute("width", "32");
    arrow.setAttribute("height", "32");
    arrow.setAttribute("viewBox", "0 0 32 32");

    Object.assign(arrow.style, {
        position: "absolute",
        left: "29px",
        top: "30px",
        overflow: "visible",
        pointerEvents: "none"
    });

    const arrowPath = document.createElementNS(
        "http://www.w3.org/2000/svg",
        "path"
    );

    arrowPath.setAttribute(
        "d",
        "M3 2 L3 26 L9 20 L14 29 L19 26 L14 17 L24 17 Z"
    );

    arrowPath.setAttribute("fill", "white");
    arrowPath.setAttribute("stroke", "black");
    arrowPath.setAttribute("stroke-width", "1.5");
    arrowPath.setAttribute("stroke-linejoin", "round");

    arrow.appendChild(arrowPath);

    container.appendChild(highlight);
    container.appendChild(arrow);

    document.documentElement.appendChild(container);

    document.addEventListener("mousemove", (event) => {
        container.style.left = event.clientX + "px";
        container.style.top = event.clientY + "px";
    }, true);

    document.addEventListener("click", (event) => {
        const ripple = document.createElement("div");

        Object.assign(ripple.style, {
            position: "fixed",
            left: event.clientX + "px",
            top: event.clientY + "px",
            width: "10px",
            height: "10px",
            border: "3px solid rgba(255, 220, 0, 0.9)",
            borderRadius: "50%",
            transform: "translate(-50%, -50%)",
            pointerEvents: "none",
            zIndex: "2147483646",
            transition: "all 0.45s ease-out",
            opacity: "1"
        });

        document.documentElement.appendChild(ripple);

        requestAnimationFrame(() => {
            ripple.style.width = "64px";
            ripple.style.height = "64px";
            ripple.style.opacity = "0";
        });

        setTimeout(() => {
            ripple.remove();
        }, 500);
    }, true);
})();
"""


def InstallVisualCursor(page):
    page.add_init_script(VISUAL_CURSOR_SCRIPT)
    page.evaluate(VISUAL_CURSOR_SCRIPT)

    page.wait_for_timeout(300)

    print("Visual cursor installed")


def MoveCursor(page, x, y, duration=1000):
    steps = max(10, int(duration / 16))

    page.mouse.move(
        x,
        y,
        steps=steps
    )


def CaptureVideo_Magento(
    url,
    company_name,
    language,
    country,
    postcode,
    city,
    street,
    house_no,
):
    browser = None
    context = None
    video = None

    video_folder = Path(PATH_TO_VIDEO_FOLDER).resolve()
    video_folder.mkdir(parents=True, exist_ok=True)

    safe_company_name = re.sub(
        r'[<>:"/\\|?*]',
        "_",
        str(company_name)
    ).strip()

    if not safe_company_name:
        safe_company_name = "recording"

    final_video_path = video_folder / f"{safe_company_name}.webm"

    temporary_video_path = None

    try:
        with sync_playwright() as playwright:

            print("Launching Chromium")

            browser = playwright.chromium.launch(
                headless=False
            )

            context = browser.new_context(
                record_video_dir=str(video_folder),
                record_video_size={
                    "width": 1280,
                    "height": 720
                },
                viewport={
                    "width": 1280,
                    "height": 720
                }
            )

            page = context.new_page()
            video = page.video

            InstallVisualCursor(page)

            print(f"Opening {url}")

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(1500)

            InstallVisualCursor(page)

            MoveCursor(
                page,
                100,
                100,
                duration=800
            )

            page.wait_for_timeout(500)

            search_query = f"Magento developer in {city}"

            print(f"Search query: {search_query}")

            search_box = page.locator(
                'textarea[name="q"]'
            )

            search_box.wait_for(
                state="visible",
                timeout=30000
            )

            search_box_box = search_box.bounding_box()

            if not search_box_box:
                raise Exception("Search field coordinates not found")

            search_x = (
                search_box_box["x"] +
                search_box_box["width"] / 2
            )

            search_y = (
                search_box_box["y"] +
                search_box_box["height"] / 2
            )

            MoveCursor(
                page,
                search_x,
                search_y,
                duration=1200
            )

            page.wait_for_timeout(300)

            page.mouse.click(
                search_x,
                search_y
            )

            page.wait_for_timeout(300)

            search_box.press_sequentially(
                search_query,
                delay=120
            )

            page.wait_for_timeout(500)

            print("Submitting search with Enter...")

            search_box.press("Enter")

            print("Search submitted")
            print("Waiting for search results...")

            first_result = page.locator(
                'a[data-testid="result-title-a"]'
            ).first

            first_result.wait_for(
                state="visible",
                timeout=60000
            )

            print("Search results loaded")

            page.wait_for_timeout(1000)

            result_box = first_result.bounding_box()

            if not result_box:
                raise Exception("First search result coordinates not found")

            result_x = (
                result_box["x"] +
                result_box["width"] / 2
            )

            result_y = (
                result_box["y"] +
                result_box["height"] / 2
            )

            MoveCursor(
                page,
                result_x,
                result_y,
                duration=1200
            )

            page.wait_for_timeout(400)

            page.mouse.click(
                result_x,
                result_y
            )

            print("First search result clicked")

            page.wait_for_timeout(5000)

            print("Finalizing video...")

            context.close()
            context = None

            temporary_video_path = Path(
                video.path()
            )

            browser.close()
            browser = None

            if final_video_path.exists():
                final_video_path.unlink()

            shutil.move(
                str(temporary_video_path),
                str(final_video_path)
            )

            absolute_video_path = str(
                final_video_path.resolve()
            )

            print(
                f"Video saved successfully: {absolute_video_path}"
            )

            return absolute_video_path

    except Exception as error:

        print(f"Error during video capture: {error}")

        try:
            if context is not None:
                context.close()
                context = None
        except Exception:
            pass

        try:
            if browser is not None:
                browser.close()
                browser = None
        except Exception:
            pass

        return None
