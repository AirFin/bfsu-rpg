#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_NAME="${REPO_NAME:-bfsu-rpg}"
GITHUB_USERNAME="${GITHUB_USERNAME:-}"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"
GIT_USER_NAME="${GIT_USER_NAME:-$GITHUB_USERNAME}"
GIT_USER_EMAIL="${GIT_USER_EMAIL:-${GITHUB_USERNAME}@users.noreply.github.com}"
GITHUB_API="https://api.github.com"
DEFAULT_BRANCH="main"

require_cmd() {
  local cmd="$1"
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "[publish] error: missing command '$cmd'"
    exit 1
  fi
}

require_env() {
  local key="$1"
  local val="$2"
  if [[ -z "$val" ]]; then
    echo "[publish] error: env '$key' is required"
    exit 1
  fi
}

prompt_missing_inputs() {
  if [[ -z "$GITHUB_USERNAME" && -t 0 ]]; then
    read -r -p "GitHub username: " GITHUB_USERNAME
  fi

  if [[ -z "$GITHUB_TOKEN" && -t 0 ]]; then
    read -r -s -p "GitHub PAT (input hidden): " GITHUB_TOKEN
    echo
  fi
}

api_call() {
  local method="$1"
  local url="$2"
  local data="${3:-}"
  local tmp_file
  tmp_file="$(mktemp)"

  if [[ -n "$data" ]]; then
    local http_code
    http_code="$(curl -sS -o "$tmp_file" -w "%{http_code}" \
      -X "$method" "$url" \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${GITHUB_TOKEN}" \
      -H "X-GitHub-Api-Version: 2022-11-28" \
      -d "$data")"
    echo "$http_code|$tmp_file"
  else
    local http_code
    http_code="$(curl -sS -o "$tmp_file" -w "%{http_code}" \
      -X "$method" "$url" \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: Bearer ${GITHUB_TOKEN}" \
      -H "X-GitHub-Api-Version: 2022-11-28")"
    echo "$http_code|$tmp_file"
  fi
}

print_api_error_and_exit() {
  local http_code="$1"
  local body_file="$2"
  echo "[publish] error: GitHub API returned $http_code"
  python - "$body_file" <<'PY'
import json
import sys

path = sys.argv[1]
try:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    msg = obj.get("message", "")
    errs = obj.get("errors", [])
    print(f"[publish] message: {msg}")
    if errs:
        print(f"[publish] errors: {errs}")
except Exception:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read())
PY
  rm -f "$body_file"
  exit 1
}

require_cmd git
require_cmd curl
require_cmd python
require_cmd conda

prompt_missing_inputs

require_env "GITHUB_USERNAME" "$GITHUB_USERNAME"
require_env "GITHUB_TOKEN" "$GITHUB_TOKEN"

echo "[publish] root: $ROOT_DIR"
echo "[publish] repo: ${GITHUB_USERNAME}/${REPO_NAME}"

cd "$ROOT_DIR"

echo "[publish] build web artifact"
"$ROOT_DIR/scripts/build_web_release.sh"

mkdir -p "$ROOT_DIR/docs"
cp "$ROOT_DIR/release/dist/index.html" "$ROOT_DIR/docs/index.html"

if grep -Eq "LLM_API_KEY|sk-[A-Za-z0-9]{10,}" "$ROOT_DIR/docs/index.html"; then
  echo "[publish] error: sensitive token pattern found in docs/index.html"
  exit 1
fi

if [[ ! -d "$ROOT_DIR/.git" ]]; then
  echo "[publish] init git repository"
  git init -b "$DEFAULT_BRANCH"
fi

current_branch="$(git symbolic-ref --short HEAD 2>/dev/null || true)"
if [[ "$current_branch" != "$DEFAULT_BRANCH" ]]; then
  if git show-ref --verify --quiet "refs/heads/${DEFAULT_BRANCH}"; then
    git checkout "$DEFAULT_BRANCH"
  else
    git checkout -b "$DEFAULT_BRANCH"
  fi
fi

if [[ -n "$GIT_USER_NAME" ]]; then
  git config user.name "$GIT_USER_NAME"
fi
if [[ -n "$GIT_USER_EMAIL" ]]; then
  git config user.email "$GIT_USER_EMAIL"
fi

echo "[publish] commit local changes"
git add .
if git diff --cached --quiet; then
  echo "[publish] nothing new to commit"
else
  git commit -m "web release: $(date +%F)"
fi

echo "[publish] create GitHub repository if needed"
create_payload="$(python - <<PY
import json
print(json.dumps({
    "name": "${REPO_NAME}",
    "private": False,
    "auto_init": False
}))
PY
)"
create_result="$(api_call "POST" "${GITHUB_API}/user/repos" "$create_payload")"
create_code="${create_result%%|*}"
create_body="${create_result#*|}"

if [[ "$create_code" == "201" ]]; then
  echo "[publish] repository created"
elif [[ "$create_code" == "422" ]]; then
  echo "[publish] repository already exists, continue"
else
  print_api_error_and_exit "$create_code" "$create_body"
fi
rm -f "$create_body"

origin_url="https://github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$origin_url"
else
  git remote add origin "$origin_url"
fi

echo "[publish] push to origin/${DEFAULT_BRANCH}"
auth_push_url="https://${GITHUB_USERNAME}:${GITHUB_TOKEN}@github.com/${GITHUB_USERNAME}/${REPO_NAME}.git"
git push "$auth_push_url" "$DEFAULT_BRANCH"
git branch --set-upstream-to="origin/${DEFAULT_BRANCH}" "$DEFAULT_BRANCH" >/dev/null 2>&1 || true

echo "[publish] enable or update GitHub Pages"
pages_payload='{"source":{"branch":"main","path":"/docs"}}'
pages_create_result="$(api_call "POST" "${GITHUB_API}/repos/${GITHUB_USERNAME}/${REPO_NAME}/pages" "$pages_payload")"
pages_create_code="${pages_create_result%%|*}"
pages_create_body="${pages_create_result#*|}"

if [[ "$pages_create_code" == "201" ]]; then
  echo "[publish] pages created"
  rm -f "$pages_create_body"
elif [[ "$pages_create_code" == "409" || "$pages_create_code" == "422" ]]; then
  rm -f "$pages_create_body"
  pages_update_result="$(api_call "PUT" "${GITHUB_API}/repos/${GITHUB_USERNAME}/${REPO_NAME}/pages" "$pages_payload")"
  pages_update_code="${pages_update_result%%|*}"
  pages_update_body="${pages_update_result#*|}"
  if [[ "$pages_update_code" == "204" || "$pages_update_code" == "201" ]]; then
    echo "[publish] pages updated"
    rm -f "$pages_update_body"
  else
    print_api_error_and_exit "$pages_update_code" "$pages_update_body"
  fi
else
  print_api_error_and_exit "$pages_create_code" "$pages_create_body"
fi

echo "[publish] fetch pages status"
pages_get_result="$(api_call "GET" "${GITHUB_API}/repos/${GITHUB_USERNAME}/${REPO_NAME}/pages")"
pages_get_code="${pages_get_result%%|*}"
pages_get_body="${pages_get_result#*|}"
if [[ "$pages_get_code" != "200" ]]; then
  print_api_error_and_exit "$pages_get_code" "$pages_get_body"
fi

site_url="$(python - "$pages_get_body" <<'PY'
import json
import sys

with open(sys.argv[1], "r", encoding="utf-8") as f:
    obj = json.load(f)
print(obj.get("html_url", ""))
PY
)"
rm -f "$pages_get_body"

echo "[publish] done"
echo "[publish] repository: ${origin_url}"
echo "[publish] pages url: ${site_url}"
echo "[publish] note: first deployment may take a few minutes to become available"
