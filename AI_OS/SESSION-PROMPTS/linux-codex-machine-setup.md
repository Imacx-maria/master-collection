# Linux Codex Machine Setup Prompt

> Use this prompt on a Linux machine when the Codex setup files and the master AI_OS have been staged in a temporary folder and need to be installed into the real Codex paths.
> This is for machine setup, not project setup.
> Date: 2026-04-05

---

## Runtime Inputs

Fill these in before use:

- `STAGING_DIR=/tmp/codex-setup`  
  or whatever temporary folder contains the copied files
- `CODEX_HOME=~/.codex`
- `AI_OS_TARGET=~/AI_OS`

Expected staged contents:

- `STAGING_DIR/skills/`
- `STAGING_DIR/AGENTS.md`
- `STAGING_DIR/config.toml`
- `STAGING_DIR/AI_OS/`

---

## The Prompt

You are setting up Codex global configuration on a Linux machine using files that were already copied into a staging directory.

Staging directory:
`STAGING_DIR`

Target Codex home:
`CODEX_HOME`

Target AI_OS location:
`AI_OS_TARGET`

Objective:
Install the staged Codex global setup into the real Linux Codex paths and verify that the machine is ready to use the same AI brain and Codex skills.

Rules:
1. Treat the staging directory as transfer-only, not as the final install location.
2. Install Codex global files into `CODEX_HOME`, not into `/tmp`.
3. Place the AI_OS master copy in a stable location, not only in `/tmp`.
4. Do not overwrite unrelated local machine files outside the target Codex setup.
5. Do not commit or push anything.
6. Verify before claiming completion.

Steps:

### Phase 1: Inspect staging

1. Confirm these exist:
   - `STAGING_DIR/skills/`
   - `STAGING_DIR/AGENTS.md`
   - `STAGING_DIR/config.toml`
   - `STAGING_DIR/AI_OS/`
2. List the staged contents briefly.
3. Report anything missing before continuing.

### Phase 2: Install Codex global files

1. Create `CODEX_HOME` if missing.
2. Copy:
   - `STAGING_DIR/skills/` -> `CODEX_HOME/skills/`
   - `STAGING_DIR/AGENTS.md` -> `CODEX_HOME/AGENTS.md`
   - `STAGING_DIR/config.toml` -> `CODEX_HOME/config.toml`
3. Preserve reasonable Linux-local differences only if they are clearly machine-specific and necessary.

### Phase 3: Install master AI_OS

1. Copy `STAGING_DIR/AI_OS/` to `AI_OS_TARGET`
2. If `AI_OS_TARGET` already exists, adapt carefully rather than deleting blindly
3. Ensure the final AI_OS location is stable and not under `/tmp`

### Phase 4: Verify

Run checks:

```bash
test -d "$CODEX_HOME/skills"
test -f "$CODEX_HOME/AGENTS.md"
test -f "$CODEX_HOME/config.toml"
test -d "$AI_OS_TARGET"
find "$CODEX_HOME/skills" -maxdepth 2 -name 'SKILL.md' | sort | head -50
```

If possible, also check:

```bash
python3 - <<'PY'
import tomllib, pathlib, os
config = pathlib.Path(os.path.expanduser("~/.codex/config.toml"))
tomllib.loads(config.read_text())
print("config.toml parses")
PY
```

### Phase 5: Final report

Return:

1. Files installed
2. Anything skipped or adapted
3. Verification performed
4. Whether Codex needs restart

Final note:
State clearly that Codex should be restarted so the newly installed global skills are discovered in fresh sessions.
