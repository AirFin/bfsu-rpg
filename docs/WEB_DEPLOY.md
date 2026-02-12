# Pyxel Web Deploy (GitHub Pages, Manual)

This project uses Pyxel scheme B:

1. Build `.pyxapp`
2. Convert to single-file `HTML`
3. Publish `docs/index.html` to GitHub Pages

All commands must run in Conda env `pyxel_env`.

## 1) Build web artifact

From project root:

```bash
chmod +x scripts/build_web_release.sh
./scripts/build_web_release.sh
```

Output file:

`release/dist/index.html`

## 2) Local preview

From project root:

```bash
conda run -n pyxel_env python -m http.server 8000
```

Open:

`http://localhost:8000/release/dist/`

## 3) Publish to GitHub Pages (/docs)

Copy latest web artifact:

```bash
mkdir -p docs
cp release/dist/index.html docs/index.html
```

Commit and push:

```bash
git add docs/index.html
git commit -m "web release: YYYY-MM-DD"
git push
```

GitHub Pages settings:

- Settings -> Pages
- Source: Deploy from a branch
- Branch: `main`
- Folder: `/docs`

Final URL:

`https://<github_username>.github.io/<repo>/`

## LLM policy (web)

- Do not commit `.env`.
- Keep LLM toggle in game UI.
- Players must fill `API Key / Base URL / Model` by themselves.
- If web request fails (for example CORS), game should auto-fallback to preset NPC dialogue.

## 4) Fully automatic upload (PAT + API)

This repo includes:

`scripts/publish_github_pages.sh`

It will run build, sync `docs/index.html`, initialize git (if needed), create GitHub repo, push code, and enable GitHub Pages.

### Required env vars

```bash
export GITHUB_USERNAME="<your_github_username>"
export GITHUB_TOKEN="<your_classic_pat_with_repo_scope>"
export REPO_NAME="bfsu-rpg"
```

Optional identity:

```bash
export GIT_USER_NAME="<display_name>"
export GIT_USER_EMAIL="<email>"
```

Run:

```bash
chmod +x scripts/publish_github_pages.sh
./scripts/publish_github_pages.sh
```

### PAT creation path

GitHub -> Settings -> Developer settings -> Personal access tokens -> Tokens (classic) -> Generate new token (classic)

Select `repo` scope.

### About private repositories

If you want "anyone can play", use a **public repository** for Pages.
Private repository Pages visibility depends on plan/organization policy and is not suitable as the default for fully public access.
