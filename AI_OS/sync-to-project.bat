@echo off
REM AI_OS Sync Script — copies master template into a project's AI_OS/ folder
REM Usage: sync-to-project.bat C:\path\to\your\project
REM
REM This pulls latest from GitHub first, then copies template files.
REM Project-specific files in the target AI_OS/ folder are NOT overwritten
REM if they don't exist in the master template.

if "%~1"=="" (
    echo Usage: sync-to-project.bat ^<project-path^>
    echo Example: sync-to-project.bat C:\Users\maria\Projects\jocril
    exit /b 1
)

set "PROJECT=%~1"
set "MASTER=C:\Users\maria\Desktop\AI_OS"
set "TARGET=%PROJECT%\AI_OS"

echo === Pulling latest AI_OS from GitHub ===
cd /d "%MASTER%"
git pull origin main

echo === Syncing AI_OS to %TARGET% ===
if not exist "%TARGET%" mkdir "%TARGET%"

REM Use robocopy to mirror template files (won't delete extra project-specific files)
robocopy "%MASTER%" "%TARGET%" /E /XF *.js *.json clipboard_* setup-ai-os-repo.bat check-git-status.bat sync-to-project.bat .gitignore /XD .git SESSION-PROMPTS\SESSIONS /NFL /NDL /NJH /NJS

echo === Syncing .claude/ structural files ===
set "CLAUDE_SRC=C:\Users\maria\Desktop\.claude"
set "CLAUDE_DST=%PROJECT%\.claude"

if not exist "%CLAUDE_DST%" mkdir "%CLAUDE_DST%"
if not exist "%CLAUDE_DST%\rules" mkdir "%CLAUDE_DST%\rules"
if not exist "%CLAUDE_DST%\hooks" mkdir "%CLAUDE_DST%\hooks"
if not exist "%CLAUDE_DST%\commands" mkdir "%CLAUDE_DST%\commands"

REM Copy settings.json (overwrite — this is template-managed)
if exist "%CLAUDE_SRC%\settings.json" copy /Y "%CLAUDE_SRC%\settings.json" "%CLAUDE_DST%\settings.json"

REM Copy rules (overwrite — template-managed)
if exist "%CLAUDE_SRC%\rules" robocopy "%CLAUDE_SRC%\rules" "%CLAUDE_DST%\rules" *.md /NFL /NDL /NJH /NJS

REM Copy hooks (overwrite — template-managed)
if exist "%CLAUDE_SRC%\hooks" robocopy "%CLAUDE_SRC%\hooks" "%CLAUDE_DST%\hooks" * /NFL /NDL /NJH /NJS

REM Copy commands (overwrite — template-managed)
if exist "%CLAUDE_SRC%\commands" robocopy "%CLAUDE_SRC%\commands" "%CLAUDE_DST%\commands" *.md /NFL /NDL /NJH /NJS

REM Copy context-essentials.md if present (overwrite — template-managed, then adapt per project if needed)
if exist "%CLAUDE_SRC%\context-essentials.md" copy /Y "%CLAUDE_SRC%\context-essentials.md" "%CLAUDE_DST%\context-essentials.md"

REM Create CLAUDE.local.md if it doesn't exist (personal, not overwritten)
if not exist "%CLAUDE_DST%\CLAUDE.local.md" (
    echo # Personal Overrides ^(gitignored^) > "%CLAUDE_DST%\CLAUDE.local.md"
)

REM Ensure root .gitignore contains local override entries
if exist "%PROJECT%\.gitignore" (
    findstr /X /C:"CLAUDE.local.md" "%PROJECT%\.gitignore" >nul || echo CLAUDE.local.md>>"%PROJECT%\.gitignore"
    findstr /X /C:"settings.local.json" "%PROJECT%\.gitignore" >nul || echo settings.local.json>>"%PROJECT%\.gitignore"
) else (
    (
        echo CLAUDE.local.md
        echo settings.local.json
    ) > "%PROJECT%\.gitignore"
)

echo === Done! AI_OS + .claude/ synced to %PROJECT% ===
