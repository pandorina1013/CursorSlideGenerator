# Marp Slide Generator

A smart slide generator for creating well-organized Marp presentations. Automatically splits content into properly sized slides with intelligent break points.

## Quick Start in Cursor

### Generate slides from chat content

Paste your content directly in Cursor chat and use:

```bash
# Method 1: Using echo
echo "YOUR SLIDE CONTENT HERE" | uv run marp-quick

# Method 2: Using heredoc (recommended for longer content)
uv run marp-quick << 'EOF'
# Your Title

Your slide content here...

---

# Another slide
More content...
EOF
```

### Generate from a file

```bash
uv run marp-gen -i input.txt -o output -n my-presentation -t gaia
```

### Watch mode (auto-regenerate on file changes)

```bash
uv run marp-watch -i input.txt -o output -n my-presentation
```

### Regenerate master/index after manual edits

```bash
uv run marp-regenerate output/my-presentation
```

### Validate slide quality

```bash
# Check for common issues
uv run marp-validate output/my-presentation

# Strict mode (warnings also fail)
uv run marp-validate output/my-presentation --strict
```

## Output Structure

```
output/
└── presentation-name/
    ├── master_slide.md      # Master file with all slides
    ├── index.md             # Index of all slides
    ├── 01-title/
    │   ├── page.md          # Individual slide content
    │   └── assets/          # Images for this slide
    ├── 02-introduction/
    │   ├── page.md
    │   └── assets/
    └── ...
```

## Features

- **Smart splitting**: Automatically splits content at headers and logical break points
- **Page limits**: Keeps slides under 15 lines for readability
- **Asset management**: Each slide has its own assets folder
- **Live editing**: Watch mode for automatic regeneration
- **Flexible input**: From files, stdin, or direct text
- **Quality validation**: Built-in checks for common slide issues

## Validation Features

The validator checks for:
- **Structure**: Missing files, incorrect folder naming
- **Code blocks**: Unclosed code blocks
- **Mermaid diagrams**: Syntax validation
- **Content quality**: Slide length warnings
- **Consistency**: Matching slide counts across files
- **Assets**: Missing or unused images

## Editing Workflow

1. **Never edit master_slide.md directly** - Always edit individual page.md files
2. To split a slide: Create new folders and move content
3. To reorder: Rename folders (keep NN- prefix)
4. After manual edits: Run `marp-regenerate` to update master/index
5. Always validate after changes: Run `marp-validate`

## Themes

- `default` - Clean, professional
- `gaia` - Bold, high-contrast
- `uncover` - Minimalist

## Tips

- Use `#` for slide titles, `##` for subtitles
- Use `---` for explicit page breaks
- Keep content concise - aim for bullet points
- Place images in the slide's `assets/` folder
- Run validation after editing to catch issues early

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd CursorSlideGenerator

# Install dependencies
uv sync
```

## License

MIT 