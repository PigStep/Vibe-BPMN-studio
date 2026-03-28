---
name: readme-creation
description: Create professional README.md following GitHub best practices
metadata:
  language: en
  best-practices: github-top-100
---

## What I Do

Create comprehensive, professional README.md files following GitHub best practices observed from top 100 most-starred repositories.

## When to Use

- Creating a new project README from scratch
- Improving an existing README
- Refreshing outdated documentation

## Workflow

### 1. Analyze the Project

- Read project structure (main directories, entry points)
- Check package manager (package.json, pyproject.toml, Cargo.toml, etc.)
- Identify tech stack and primary language
- Determine target audience (developers, end-users, contributors)

### 2. Collect Information

Gather these details before writing:

- **Project name**
- **One-line description** (max 10 words)
- **Key features** (4-7 items, focus on benefits not capabilities)
- **Tech stack** (main technologies used)
- **Installation method** (package manager, cloning, Docker)
- **Quick start command** (simplest way to run)
- **Visual assets** (logo, screenshots, GIFs - add placeholder paths)
- **License type** (MIT, Apache, GPL, etc.)

### 3. Apply Best Practices

Structure README in this order:

```
1. Title + Badges (3-5 max)
2. One-line description
3. Demo screenshot/GIF
4. Table of Contents (if >100 lines)
5. Features (4-7 bullet points)
6. Technologies
7. Quick Start
   - Prerequisites
   - Installation
   - Running
   - Docker (optional)
8. Usage (with examples)
9. Project Structure
10. Architecture (use image, not ASCII)
11. API Endpoints (if applicable)
12. Contributing
13. License
```

### 4. Write Content Rules

**Title Section:**
- Use `# ProjectName` format
- Keep description to 10 words or fewer
- Badges: Python, License, Build Status (max 5)

**Features Section:**
- 4-7 items maximum
- Focus on benefits: "Zero configuration" not "Supports config files"
- Use bold for key phrases
- Emojis allowed in bullet points, NOT in section headers

**Quick Start Section:**
- Maximum 5 steps
- Must work on fresh machine
- Include copy-paste commands
- Test the commands yourself

**Code Examples:**
- 2-3 examples progressing from simple to complex
- Include expected output where helpful
- Use proper syntax highlighting

## Anti-Patterns to Avoid

| Anti-Pattern | Fix |
|-------------|-----|
| Mixed languages (EN + RU) | Use English throughout |
| >5 badges | Keep to 3-5 essential badges |
| TO-DO / Roadmap sections | Move to GitHub Issues or separate ROADMAP.md |
| Known Issues | Rename to "Requirements" or "Limitations" |
| ASCII art diagrams | Use images instead |
| Version number in footer | GitHub shows tags automatically |
| Expansion Possibilities | Move to separate ROADMAP.md |
| Emojis in section headers | Use emojis only in bullet points |
| Outdated badges/links | Verify all links work |

## Pain Points Checklist

Before completing, verify:

- [ ] Single language throughout (English preferred)
- [ ] Max 5 badges
- [ ] Demo image/GIF placeholder or actual asset
- [ ] Table of Contents (if README >100 lines)
- [ ] No TO-DO/ROADMAP sections
- [ ] No Known Issues (use Requirements instead)
- [ ] Quick Start works in <5 steps
- [ ] All links are valid
- [ ] Code blocks have syntax highlighting

## Tech Stack Specific Sections

**Python Projects:**
```
### Package Manager
- uv sync
- uv add <package>
- uv remove <package>

### Testing
- pytest
```

**Node.js Projects:**
```
### Package Manager
- npm install
- npm run dev

### Testing
- npm test
```

**Docker Projects:**
```
### Docker
- docker build
- docker run
```

## Output Format

Write complete README.md content. If the user asks to improve an existing README:

1. Read the current README.md
2. Identify pain points
3. Present a list of issues found
4. Offer to fix them one by one or all at once
5. Create the improved version

## Example Prompt

User: "Create README for my Python CLI tool"

Assistant actions:
1. Ask for project name, description, features, tech stack
2. Or analyze existing project structure
3. Generate README following this skill's guidelines
4. Offer to create assets directory for demo images
