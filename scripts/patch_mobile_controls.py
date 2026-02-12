#!/usr/bin/env python3
"""
Post-process Pyxel web HTML and inject a custom mobile input layer.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ENABLE_MOBILE_CONTROLS_PATCH = True

PATCH_START = "<!-- MOBILE_CONTROLS_PATCH_START -->"
PATCH_END = "<!-- MOBILE_CONTROLS_PATCH_END -->"


def _disable_builtin_gamepad(html: str) -> str:
    """Force launchPyxel gamepad option to disabled to avoid input conflicts."""
    return re.sub(
        r'gamepad\s*:\s*["\']enabled["\']',
        'gamepad: "disabled"',
        html,
    )


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
<style id="mobile-controls-input-patch">
html.pyxel-mobile-controls img#pyxel-gamepad-cross,
html.pyxel-mobile-controls img#pyxel-gamepad-button,
html.pyxel-mobile-controls img#pyxel-gamepad-menu {
  display: none !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

html.pyxel-mobile-controls #bfsu-mobile-controls {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 90;
  height: 230px;
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 14px 20px 22px;
  box-sizing: border-box;
  background: linear-gradient(
    to top,
    rgba(12, 16, 26, 0.92) 0%,
    rgba(12, 16, 26, 0.78) 52%,
    rgba(12, 16, 26, 0.0) 100%
  );
  touch-action: none;
  user-select: none;
  -webkit-user-select: none;
}

html.pyxel-mobile-controls #bfsu-joystick-base {
  position: relative;
  width: 164px;
  height: 164px;
  border-radius: 50%;
  border: 2px solid rgba(86, 149, 255, 0.95);
  background: radial-gradient(
    circle,
    rgba(34, 70, 136, 0.35) 0%,
    rgba(12, 24, 50, 0.62) 58%,
    rgba(6, 10, 22, 0.82) 100%
  );
  box-shadow:
    inset 0 0 22px rgba(102, 158, 255, 0.28),
    0 0 22px rgba(88, 143, 255, 0.45);
  touch-action: none;
}

html.pyxel-mobile-controls #bfsu-joystick-thumb {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 72px;
  height: 72px;
  margin-left: -36px;
  margin-top: -36px;
  border-radius: 50%;
  border: 2px solid rgba(180, 219, 255, 1);
  background: radial-gradient(
    circle,
    rgba(194, 226, 255, 1) 0%,
    rgba(100, 161, 255, 1) 52%,
    rgba(54, 112, 215, 1) 100%
  );
  box-shadow:
    inset 0 0 10px rgba(226, 243, 255, 0.6),
    0 0 16px rgba(98, 158, 255, 0.68);
  transition: transform 0.04s linear;
  will-change: transform;
  touch-action: none;
}

html.pyxel-mobile-controls #bfsu-mobile-right {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
}

html.pyxel-mobile-controls #bfsu-mobile-abx {
  position: relative;
  width: 180px;
  height: 130px;
}

html.pyxel-mobile-controls .bfsu-btn {
  position: absolute;
  width: 62px;
  height: 62px;
  border-radius: 50%;
  border: 2px solid rgba(133, 192, 255, 0.98);
  background: radial-gradient(
    circle,
    rgba(18, 38, 80, 0.88) 0%,
    rgba(9, 19, 42, 0.96) 100%
  );
  color: #dceeff;
  font: 800 24px/1 "Arial", sans-serif;
  letter-spacing: 0.4px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-shadow: 0 0 8px rgba(88, 160, 255, 0.85);
  box-shadow:
    inset 0 0 12px rgba(122, 184, 255, 0.33),
    0 0 15px rgba(92, 157, 255, 0.56);
  transform: translateZ(0) scale(1);
  transition: transform 0.06s ease, filter 0.06s ease;
  touch-action: none;
}

html.pyxel-mobile-controls .bfsu-btn.active {
  transform: translateZ(0) scale(0.93);
  filter: brightness(1.18);
}

html.pyxel-mobile-controls #bfsu-btn-a {
  left: 8px;
  top: 36px;
}

html.pyxel-mobile-controls #bfsu-btn-b {
  right: 8px;
  top: 36px;
}

html.pyxel-mobile-controls #bfsu-btn-x {
  left: 59px;
  top: 0;
}

html.pyxel-mobile-controls #bfsu-btn-start {
  width: 138px;
  height: 42px;
  border-radius: 14px;
  position: static;
  font: 800 20px/1 "Arial", sans-serif;
}
</style>
""".strip()

    script = f"""
<script id="mobile-controls-input-patch-script">
(function () {{
  const ENABLE_MOBILE_CONTROLS_PATCH = {str(ENABLE_MOBILE_CONTROLS_PATCH).lower()};
  if (!ENABLE_MOBILE_CONTROLS_PATCH) {{
    return;
  }}

  const MOBILE_INPUT_KEY = "__BFSU_MOBILE_INPUT";
  const isTouchDevice = () =>
    "ontouchstart" in window ||
    (navigator.maxTouchPoints || 0) > 0 ||
    (navigator.msMaxTouchPoints || 0) > 0;

  if (!isTouchDevice()) {{
    return;
  }}

  const state = window[MOBILE_INPUT_KEY] || {{}};
  state.active = true;
  state.axes = state.axes || {{ x: 0, y: 0 }};
  state.buttons = state.buttons || {{ a: false, b: false, x: false, start: false }};
  window[MOBILE_INPUT_KEY] = state;

  document.documentElement.classList.add("pyxel-mobile-controls");

  if (document.getElementById("bfsu-mobile-controls")) {{
    return;
  }}

  const controls = document.createElement("div");
  controls.id = "bfsu-mobile-controls";
  controls.innerHTML = `
    <div id="bfsu-joystick-base">
      <div id="bfsu-joystick-thumb"></div>
    </div>
    <div id="bfsu-mobile-right">
      <div id="bfsu-mobile-abx">
        <div id="bfsu-btn-a" class="bfsu-btn" data-btn="a">A</div>
        <div id="bfsu-btn-b" class="bfsu-btn" data-btn="b">B</div>
        <div id="bfsu-btn-x" class="bfsu-btn" data-btn="x">X</div>
      </div>
      <div id="bfsu-btn-start" class="bfsu-btn" data-btn="start">START</div>
    </div>
  `;
  document.body.appendChild(controls);

  const joystickBase = document.getElementById("bfsu-joystick-base");
  const joystickThumb = document.getElementById("bfsu-joystick-thumb");

  const clamp = (value, min, max) => Math.max(min, Math.min(max, value));
  const clearAxes = () => {{
    state.axes.x = 0;
    state.axes.y = 0;
    joystickThumb.style.transform = "translate(0px, 0px)";
  }};
  const clearButtons = () => {{
    state.buttons.a = false;
    state.buttons.b = false;
    state.buttons.x = false;
    state.buttons.start = false;
  }};

  clearAxes();
  clearButtons();

  let joystickTouchId = null;
  const trackedButtonTouches = {{
    a: new Set(),
    b: new Set(),
    x: new Set(),
    start: new Set()
  }};

  function findTouchById(touches, identifier) {{
    for (let i = 0; i < touches.length; i += 1) {{
      if (touches[i].identifier === identifier) {{
        return touches[i];
      }}
    }}
    return null;
  }}

  function updateJoystickByTouch(touch) {{
    const rect = joystickBase.getBoundingClientRect();
    const centerX = rect.left + rect.width * 0.5;
    const centerY = rect.top + rect.height * 0.5;
    const radius = rect.width * 0.33;

    let dx = (touch.clientX - centerX) / radius;
    let dy = (touch.clientY - centerY) / radius;
    const length = Math.hypot(dx, dy);
    if (length > 1) {{
      dx /= length;
      dy /= length;
    }}

    state.axes.x = clamp(dx, -1, 1);
    state.axes.y = clamp(dy, -1, 1);
    joystickThumb.style.transform = `translate(${{state.axes.x * radius}}px, ${{state.axes.y * radius}}px)`;
  }}

  function bindButton(el, key) {{
    if (!el) {{
      return;
    }}
    const setPressed = (pressed) => {{
      state.buttons[key] = pressed;
      if (pressed) {{
        el.classList.add("active");
      }} else {{
        el.classList.remove("active");
      }}
    }};

    el.addEventListener("touchstart", (event) => {{
      event.preventDefault();
      for (let i = 0; i < event.changedTouches.length; i += 1) {{
        trackedButtonTouches[key].add(event.changedTouches[i].identifier);
      }}
      setPressed(true);
    }}, {{ passive: false }});

    const clearTouches = (event) => {{
      event.preventDefault();
      for (let i = 0; i < event.changedTouches.length; i += 1) {{
        trackedButtonTouches[key].delete(event.changedTouches[i].identifier);
      }}
      setPressed(trackedButtonTouches[key].size > 0);
    }};

    el.addEventListener("touchend", clearTouches, {{ passive: false }});
    el.addEventListener("touchcancel", clearTouches, {{ passive: false }});
    el.addEventListener("touchmove", (event) => {{
      event.preventDefault();
    }}, {{ passive: false }});
  }}

  bindButton(document.getElementById("bfsu-btn-a"), "a");
  bindButton(document.getElementById("bfsu-btn-b"), "b");
  bindButton(document.getElementById("bfsu-btn-x"), "x");
  bindButton(document.getElementById("bfsu-btn-start"), "start");

  joystickBase.addEventListener("touchstart", (event) => {{
    event.preventDefault();
    if (joystickTouchId === null && event.changedTouches.length > 0) {{
      joystickTouchId = event.changedTouches[0].identifier;
      updateJoystickByTouch(event.changedTouches[0]);
    }}
  }}, {{ passive: false }});

  document.addEventListener("touchmove", (event) => {{
    if (joystickTouchId === null) {{
      return;
    }}
    const touch = findTouchById(event.touches, joystickTouchId);
    if (touch) {{
      event.preventDefault();
      updateJoystickByTouch(touch);
    }}
  }}, {{ passive: false }});

  const releaseJoystickIfNeeded = (event) => {{
    if (joystickTouchId === null) {{
      return;
    }}
    const touch = findTouchById(event.touches, joystickTouchId);
    if (!touch) {{
      joystickTouchId = null;
      clearAxes();
    }}
  }};

  document.addEventListener("touchend", releaseJoystickIfNeeded, {{ passive: false }});
  document.addEventListener("touchcancel", releaseJoystickIfNeeded, {{ passive: false }});
  window.addEventListener("blur", () => {{
    joystickTouchId = null;
    clearAxes();
    clearButtons();
  }});

  controls.addEventListener("touchstart", (event) => event.preventDefault(), {{ passive: false }});
  controls.addEventListener("touchmove", (event) => event.preventDefault(), {{ passive: false }});
  controls.addEventListener("touchend", (event) => event.preventDefault(), {{ passive: false }});
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
    patched = _disable_builtin_gamepad(original)
    patched = _upsert_patch(patched)
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
