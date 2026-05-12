# adata-skills

A collection of agent skills for [Claude Code](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview), [GitHub Copilot](https://github.com/features/copilot), [Cursor](https://www.cursor.com/), and other AI coding agents.

## Skills

| Skill | Description | Platform |
|---|---|---|
| [adata-pptx](adata-pptx/) | Create ADATA (威剛科技) branded PowerPoint presentations using the official ADATA design system | Any |

## Installation

Install a specific skill with the [Skills CLI](https://skills.sh/):

```bash
# Install a single skill
npx skills add Yuchen-Cheng/adata-skills@adata-pptx

# Install globally (user-level)
npx skills add Yuchen-Cheng/adata-skills@adata-pptx -g

# List all available skills in this repo
npx skills add Yuchen-Cheng/adata-skills --list
```

## Repository Structure

```
adata-skills/
├── README.md
├── .gitignore
└── adata-pptx/                     # Each skill is a top-level directory
    ├── SKILL.md                    # Required — metadata + instructions
    ├── assets/
    │   └── backgrounds/            # 11 ADATA background JPGs
    ├── layouts/
    │   ├── slides/                 # 5 structural slide layouts
    │   └── patterns/               # 16 body content patterns
    ├── references/                 # Template styles, editing guides, pptxgenjs docs
    └── scripts/                    # PPTX utility scripts (add_slide, pack, unpack, etc.)
```

Each skill lives in its own **top-level directory** containing a `SKILL.md` with YAML frontmatter (`name` and `description` fields). See the [Skills documentation](https://skills.sh/) for authoring details.

## Adding a New Skill

1. Create a new directory at the repo root:
   ```bash
   npx skills init <skill-name>
   ```
2. Edit `<skill-name>/SKILL.md` — add a `name`, `description`, and instructions.
3. (Optional) Add `scripts/`, `references/`, or `assets/` subdirectories for bundled resources.
4. Commit and push.

## License

MIT