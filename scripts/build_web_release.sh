#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STAGING_DIR="${ROOT_DIR}/release/web_staging"
DIST_DIR="${ROOT_DIR}/release/dist"
PYXAPP_FILE="${ROOT_DIR}/web_staging.pyxapp"
HTML_TARGET="${DIST_DIR}/index.html"

echo "[build] root: ${ROOT_DIR}"

if ! command -v rsync >/dev/null 2>&1; then
  echo "[build] error: rsync not found"
  exit 1
fi

if ! command -v conda >/dev/null 2>&1; then
  echo "[build] error: conda not found"
  exit 1
fi

echo "[build] clean old artifacts"
rm -rf "${STAGING_DIR}" "${DIST_DIR}"
rm -f "${PYXAPP_FILE}" \
      "${ROOT_DIR}/._web_staging.pyxapp" \
      "${ROOT_DIR}/release/web_staging.html" \
      "${ROOT_DIR}/release/web_staging.pyxapp.html" \
      "${ROOT_DIR}/web_staging.html" \
      "${ROOT_DIR}/web_staging.pyxapp.html"
mkdir -p "${STAGING_DIR}" "${DIST_DIR}"

echo "[build] stage runtime files"
rsync -a \
  --exclude "__pycache__/" \
  --exclude "._*" \
  --exclude ".DS_Store" \
  "${ROOT_DIR}/main.py" \
  "${ROOT_DIR}/config.py" \
  "${ROOT_DIR}/src" \
  "${ROOT_DIR}/assets" \
  "${ROOT_DIR}/data" \
  "${STAGING_DIR}/"

echo "[build] pyxel package"
(
  cd "${ROOT_DIR}"
  conda run -n pyxel_env pyxel package release/web_staging release/web_staging/main.py
)

if [[ ! -f "${PYXAPP_FILE}" ]]; then
  echo "[build] error: missing ${PYXAPP_FILE}"
  exit 1
fi

echo "[build] pyxel app2html"
(
  cd "${ROOT_DIR}"
  conda run -n pyxel_env pyxel app2html web_staging.pyxapp
)

HTML_SOURCE=""
for candidate in \
  "${ROOT_DIR}/release/web_staging.html" \
  "${ROOT_DIR}/release/web_staging.pyxapp.html" \
  "${ROOT_DIR}/web_staging.html" \
  "${ROOT_DIR}/web_staging.pyxapp.html"; do
  if [[ -f "${candidate}" ]]; then
    HTML_SOURCE="${candidate}"
    break
  fi
done

if [[ -z "${HTML_SOURCE}" ]]; then
  HTML_SOURCE="$(find "${ROOT_DIR}/release" -maxdepth 1 -type f -name "web_staging*.html" | head -n 1 || true)"
fi

if [[ -z "${HTML_SOURCE}" || ! -f "${HTML_SOURCE}" ]]; then
  echo "[build] error: app2html output not found"
  exit 1
fi

mv "${HTML_SOURCE}" "${HTML_TARGET}"

echo "[build] patch mobile controls overlay"
(
  cd "${ROOT_DIR}"
  conda run -n pyxel_env python scripts/patch_mobile_controls.py "${HTML_TARGET}"
)

if grep -Eq "LLM_API_KEY|sk-[A-Za-z0-9]{10,}" "${HTML_TARGET}"; then
  echo "[build] error: sensitive token pattern found in ${HTML_TARGET}"
  exit 1
fi

echo "[build] done: ${HTML_TARGET}"
echo "[build] local preview:"
echo "  conda run -n pyxel_env python -m http.server 8000"
echo "  open http://localhost:8000/release/dist/"
