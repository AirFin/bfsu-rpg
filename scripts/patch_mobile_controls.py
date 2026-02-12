#!/usr/bin/env python3
"""
Post-process Pyxel web HTML and inject a mobile control visibility patch.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ENABLE_MOBILE_CONTROLS_PATCH = True

PATCH_START = "<!-- MOBILE_CONTROLS_PATCH_START -->"
PATCH_END = "<!-- MOBILE_CONTROLS_PATCH_END -->"


def _build_patch_block() -> str:
    if not ENABLE_MOBILE_CONTROLS_PATCH:
        return "\n".join(
            [
                PATCH_START,
                "<!-- Patch disabled by ENABLE_MOBILE_CONTROLS_PATCH -->",
                PATCH_END,
            ]
        )

    style = """
<style id="mobile-controls-visual-patch">
html.pyxel-mobile-controls img#pyxel-gamepad-button,
html.pyxel-mobile-controls img#pyxel-gamepad-menu {
  opacity: 0.98 !important;
  filter: brightness(1.45) contrast(1.55) saturate(1.25)
    drop-shadow(0 0 10px rgba(120, 170, 255, 0.75));
}

html.pyxel-mobile-controls img#pyxel-gamepad-cross {
  opacity: 0.08 !important;
  filter: brightness(1.2) contrast(1.2);
}

html.pyxel-mobile-controls div#pyxel-mobile-overlay {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 40;
}

html.pyxel-mobile-controls div#pyxel-mobile-joystick {
  position: absolute;
  border-radius: 50%;
  box-sizing: border-box;
  border: 2px solid rgba(140, 185, 255, 0.95);
  background: radial-gradient(
    circle,
    rgba(18, 28, 52, 0.65) 0%,
    rgba(8, 14, 28, 0.15) 72%,
    rgba(8, 14, 28, 0.0) 100%
  );
  box-shadow:
    inset 0 0 18px rgba(120, 170, 255, 0.28),
    0 0 14px rgba(120, 170, 255, 0.45);
}

html.pyxel-mobile-controls div#pyxel-mobile-joystick::before {
  content: "";
  position: absolute;
  left: 50%;
  top: 50%;
  width: 42%;
  height: 42%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  border: 2px solid rgba(183, 214, 255, 0.95);
  background: radial-gradient(
    circle,
    rgba(157, 199, 255, 0.95) 0%,
    rgba(75, 122, 206, 0.95) 100%
  );
  box-shadow:
    inset 0 0 10px rgba(231, 244, 255, 0.45),
    0 0 12px rgba(120, 170, 255, 0.65);
}

html.pyxel-mobile-controls div#pyxel-mobile-buttons-layer,
html.pyxel-mobile-controls div#pyxel-mobile-menu-layer {
  position: absolute;
}

html.pyxel-mobile-controls div#pyxel-mobile-button-a,
html.pyxel-mobile-controls div#pyxel-mobile-button-b,
html.pyxel-mobile-controls div#pyxel-mobile-menu-start {
  position: absolute;
  transform: translate(-50%, -50%);
  padding: 2px 7px;
  border-radius: 999px;
  border: 1px solid rgba(170, 210, 255, 0.96);
  background: rgba(6, 12, 26, 0.88);
  color: #d9ecff;
  font: 700 11px/1 monospace;
  letter-spacing: 0.8px;
  text-shadow: 0 0 5px rgba(90, 150, 255, 0.85);
  box-shadow:
    inset 0 0 7px rgba(120, 170, 255, 0.28),
    0 0 8px rgba(120, 170, 255, 0.45);
}

html.pyxel-mobile-controls div#pyxel-mobile-button-a {
  left: 34%;
  top: 76%;
}

html.pyxel-mobile-controls div#pyxel-mobile-button-b {
  left: 78%;
  top: 52%;
}

html.pyxel-mobile-controls div#pyxel-mobile-menu-start {
  left: 76%;
  top: 44%;
}
</style>
""".strip()

    script = f"""
<script id="mobile-controls-visual-patch-script">
(function () {{
  const ENABLE_MOBILE_CONTROLS_PATCH = {str(ENABLE_MOBILE_CONTROLS_PATCH).lower()};
  if (!ENABLE_MOBILE_CONTROLS_PATCH) {{
    return;
  }}

  const isTouchDevice = () =>
    "ontouchstart" in window ||
    (navigator.maxTouchPoints || 0) > 0 ||
    (navigator.msMaxTouchPoints || 0) > 0;

  if (!isTouchDevice()) {{
    return;
  }}

  document.documentElement.classList.add("pyxel-mobile-controls");

  let overlay = null;
  let joystickLayer = null;
  let buttonsLayer = null;
  let menuLayer = null;

  function ensureOverlay(screen) {{
    if (overlay && overlay.isConnected) {{
      return;
    }}

    overlay = document.createElement("div");
    overlay.id = "pyxel-mobile-overlay";

    joystickLayer = document.createElement("div");
    joystickLayer.id = "pyxel-mobile-joystick";

    buttonsLayer = document.createElement("div");
    buttonsLayer.id = "pyxel-mobile-buttons-layer";
    const labelA = document.createElement("div");
    labelA.id = "pyxel-mobile-button-a";
    labelA.textContent = "A";
    const labelB = document.createElement("div");
    labelB.id = "pyxel-mobile-button-b";
    labelB.textContent = "B";
    buttonsLayer.appendChild(labelA);
    buttonsLayer.appendChild(labelB);

    menuLayer = document.createElement("div");
    menuLayer.id = "pyxel-mobile-menu-layer";
    const labelStart = document.createElement("div");
    labelStart.id = "pyxel-mobile-menu-start";
    labelStart.textContent = "START";
    menuLayer.appendChild(labelStart);

    overlay.appendChild(joystickLayer);
    overlay.appendChild(buttonsLayer);
    overlay.appendChild(menuLayer);
    screen.appendChild(overlay);
  }}

  function alignRect(target, rect, screenRect) {{
    target.style.left = `${{rect.left - screenRect.left}}px`;
    target.style.top = `${{rect.top - screenRect.top}}px`;
    target.style.width = `${{rect.width}}px`;
    target.style.height = `${{rect.height}}px`;
  }}

  function syncOverlay() {{
    const screen = document.getElementById("pyxel-screen");
    const cross = document.getElementById("pyxel-gamepad-cross");
    const button = document.getElementById("pyxel-gamepad-button");
    const menu = document.getElementById("pyxel-gamepad-menu");

    if (screen && cross && button && menu) {{
      ensureOverlay(screen);
      const screenRect = screen.getBoundingClientRect();
      alignRect(joystickLayer, cross.getBoundingClientRect(), screenRect);
      alignRect(buttonsLayer, button.getBoundingClientRect(), screenRect);
      alignRect(menuLayer, menu.getBoundingClientRect(), screenRect);
    }}

    window.requestAnimationFrame(syncOverlay);
  }}

  window.addEventListener("resize", () => window.requestAnimationFrame(syncOverlay), {{ passive: true }});
  window.addEventListener("orientationchange", () => window.requestAnimationFrame(syncOverlay), {{ passive: true }});
  window.requestAnimationFrame(syncOverlay);
}})();
</script>
""".strip()

    return "\n".join([PATCH_START, style, script, PATCH_END])


def _upsert_patch(html: str) -> str:
    block = _build_patch_block()
    pattern = re.compile(
        re.escape(PATCH_START) + r".*?" + re.escape(PATCH_END),
        flags=re.DOTALL,
    )

    if pattern.search(html):
        return pattern.sub(block, html, count=1)

    body_close_pattern = re.compile(r"</body\s*>", flags=re.IGNORECASE)
    match = body_close_pattern.search(html)
    if match:
        return html[: match.start()] + block + "\n" + html[match.start() :]

    return html.rstrip() + "\n" + block + "\n"


def patch_html_file(target: Path) -> None:
    original = target.read_text(encoding="utf-8")
    patched = _upsert_patch(original)
    if patched != original:
        target.write_text(patched, encoding="utf-8")
        print(f"[patch-mobile-controls] patched: {target}")
    else:
        print(f"[patch-mobile-controls] already up-to-date: {target}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inject mobile control visual patch into generated web HTML."
    )
    parser.add_argument(
        "html_path",
        nargs="?",
        default="release/dist/index.html",
        help="Target HTML file path (default: release/dist/index.html)",
    )
    args = parser.parse_args()

    target = Path(args.html_path).expanduser().resolve()
    if not target.is_file():
        print(f"[patch-mobile-controls] error: file not found: {target}")
        return 1

    patch_html_file(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
