# Personal AI Agent Skills

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-6E56CF)](https://agentskills.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validated with skills-ref](https://img.shields.io/badge/validated-skills--ref-brightgreen)](https://pypi.org/project/skills-ref/)

A personal, curated collection of [Agent Skills](https://agentskills.io) — portable, version-controlled capabilities for AI coding agents. Every skill in this repository follows the open `SKILL.md` specification and works across any compatible agent: Claude Code, OpenAI Codex, OpenCode, Pi Coding Agent, Hermes Agent, Cursor, Gemini CLI, GitHub Copilot, and more.

---

## What are Agent Skills?

[Agent Skills](https://agentskills.io) is an open, vendor-neutral format originally developed by Anthropic and adopted across the AI agent ecosystem. A skill is a folder containing a `SKILL.md` file (metadata + instructions) plus optional `scripts/`, `references/`, and `assets/` directories. Agents load skills on demand through **progressive disclosure** — only the name and description are loaded at startup, and the full instructions load only when a task actually needs them. This keeps context lean while giving agents deep, reusable, task-specific expertise.

## Repository Structure

```
Personal-AI-Agent-Skills/
└── skills/
    └── triad/
        ├── SKILL.md          # Skill metadata + instructions
        ├── assets/
        │   └── template.py   # Reusable scaffold template
        └── references/
            ├── go.md          # Go-specific reference
            ├── python.md      # Python-specific reference
            └── rust.md        # Rust-specific reference
```

Each top-level directory under `skills/` is a self-contained, independently installable skill.

## Available Skills

| Skill                   | Description                                                                                                                                                                                                                                                                | Stack              | Path            |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------ | --------------- |
| [`triad`](skills/triad) | Scaffolds and standardizes new service projects across Go, Python, and Rust, applying consistent project structure, tooling conventions, and boilerplate for each language through dedicated per-language reference guides. <!-- TODO: confirm/refine this description --> | Go · Python · Rust | `skills/triad/` |

> More skills will be added over time — this table is the single source of truth for what's available in this repository.

## Installation

### Recommended: Skills CLI

The fastest way to install any skill from this repository into your agent of choice is with the official [Skills CLI](https://github.com/vercel-labs/skills), which auto-detects your agent and installs to the correct path.

```bash
# Install every skill in this repo
npx skills add amirk1998/Personal-AI-Agent-Skills

# Install a specific skill only
npx skills add amirk1998/Personal-AI-Agent-Skills --skill triad

# Install for a specific agent
npx skills add amirk1998/Personal-AI-Agent-Skills --skill triad -a claude-code

# Install globally (user-level, not just the current project)
npx skills add amirk1998/Personal-AI-Agent-Skills --skill triad -g
```

### Manual Installation

If you'd rather not use the CLI, clone this repository and copy (or symlink) the skill folder into your agent's skill directory:

```bash
git clone https://github.com/amirk1998/Personal-AI-Agent-Skills.git
cp -r Personal-AI-Agent-Skills/skills/triad ~/.claude/skills/triad
```

| Agent                                  | Skill directory                                                                           |
| -------------------------------------- | ----------------------------------------------------------------------------------------- |
| Claude Code                            | `.claude/skills/` (project) or `~/.claude/skills/` (global)                               |
| OpenAI Codex CLI                       | `.codex/skills/`                                                                          |
| OpenCode                               | `.opencode/skills/` (project) or `~/.config/opencode/skills/` (global)                    |
| Pi Coding Agent                        | `.pi/skills/` (project) or `~/.pi/agent/skills/` (global)                                 |
| Hermes Agent                           | `~/.hermes/skills/`                                                                       |
| Cursor                                 | `.cursor/skills/`                                                                         |
| Gemini CLI                             | `.gemini/skills/`                                                                         |
| GitHub Copilot / VS Code               | native Agent Skills support                                                               |
| Roo Code / Cline / Windsurf / OpenClaw | see each agent's docs, listed at [agentskills.io/clients](https://agentskills.io/clients) |

> **Note (Claude Code):** Claude Code only scans one directory level deep for `SKILL.md` files, so each skill folder must sit directly under the skills directory (not nested further).

## Validation

Every skill in this repository is checked against the official [Agent Skills specification](https://agentskills.io/specification) using the reference validator before being published.

```bash
pip install skills-ref

agentskills validate skills/triad
agentskills read-properties skills/triad
```

## Adding a New Skill

1. Create a new directory: `skills/<skill-name>/`
2. Add a `SKILL.md` with valid frontmatter (`name`, `description`, at minimum):
   ```yaml
   ---
   name: skill-name
   description: What this skill does and when an agent should use it.
   ---
   ```
3. Keep the main `SKILL.md` under ~500 lines; move detailed material into `references/`.
4. Validate: `agentskills validate skills/<skill-name>`
5. Add a row to the [Available Skills](#available-skills) table above.
6. Record the change in [`CHANGELOG.md`](CHANGELOG.md).

## Changelog

All notable changes to this repository are documented in [`CHANGELOG.md`](CHANGELOG.md), following [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## License

Released under the [MIT License](LICENSE).

## Author

**Amir** ([@amirk1998](https://github.com/amirk1998))
