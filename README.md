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

## Editing Workflow

1. **Never edit master_slide.md directly** - Always edit individual page.md files
2. To split a slide: Create new folders and move content
3. To reorder: Rename folders (keep NN- prefix)
4. After manual edits: Run `marp-regenerate` to update master/index

## Themes

- `default` - Clean, professional
- `gaia` - Bold, high-contrast
- `uncover` - Minimalist

## Tips

- Use `#` for slide titles, `##` for subtitles
- Use `---` for explicit page breaks
- Keep content concise - aim for bullet points
- Place images in the slide's `assets/` folder

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