# Repository Initialization Checklist

## 1. Confirm the Directory

```bash
cd "D:/github projects/Macha"
```

> Note: the path contains spaces, so be sure to quote it on the command line.

## 2. Initialize Git (if not already done)

```bash
git init
git add .
git commit -m "chore: initialize Macha repository structure"
```

## 3. Create the Remote Repository and Push

Assuming the remote address is `git@github.com:your-org/Macha.git`:

```bash
git remote add origin git@github.com:your-org/Macha.git
git branch -M main
git push -u origin main
```

## 4. Install the Development Environment

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -e ".[dev]"
```

## 5. Run Tests

```bash
pytest
```

## 6. First Team Alignment

- [ ] Read `docs/research/positioning.md` and confirm the research direction.
- [ ] Read `docs/research/direction.md` and confirm the first MVP scope.
- [ ] Read `docs/roadmap.md` and claim a Phase 1 task (Layer Protocol v0 / Stub Core / environment
      reconnaissance — the agreed sequencing is Layer-first).
