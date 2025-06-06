# Marp Slide Generator

An intelligent slide generator that automatically splits your content into well-organized Marp slides with proper formatting and structure. Optimized for use with Cursor IDE.

## Features

- **Intelligent Content Splitting**: Automatically divides content into appropriately sized pages
- **Smart Break Detection**: Recognizes natural content breaks (headers, sections)
- **Marp Formatting**: Adds proper Marp front matter and styling
- **Organized Structure**: Creates a clean directory structure with presentation and slide folders
- **Theme Support**: Supports multiple Marp themes (default, gaia, uncover)
- **Master Slide Generation**: Creates a master slide that references all individual pages
- **Watch Mode**: Automatically regenerates slides when input file changes
- **Cursor IDE Integration**: Optimized workflow for iterative slide editing
- **Quick Generation**: Generate slides directly from chat or clipboard

## Installation

1. Clone this repository
2. Install `uv` if you haven't already:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
3. Install dependencies:
```bash
uv sync
```

## Usage

### Basic Usage

```bash
uv run marp-gen -i input.txt
```

### With Custom Presentation Name

```bash
uv run marp-gen -i input.txt -n my-presentation
```

### With Theme Selection

```bash
uv run marp-gen -i input.txt -n my-presentation -t gaia
```

### Watch Mode (Recommended for Cursor)

```bash
uv run python watch_slides.py -i input.txt -n my-presentation
```

This will watch your input file and automatically regenerate slides whenever you save changes.

### Quick Generation from Chat/Clipboard

Perfect for when you want to quickly generate slides from content in Cursor's chat:

#### Method 1: Using echo (for short content)
```bash
echo "# My Title\n\nContent here" | uv run python quick_slides.py
```

#### Method 2: Using heredoc (for longer content)
```bash
uv run python quick_slides.py << 'EOF'
# Introduction

Welcome to my presentation

## Topics
- Topic 1
- Topic 2
- Topic 3

---

# Main Content

Details go here...
EOF
```

#### Method 3: With custom presentation name
```bash
uv run python quick_slides.py -n "ai-workshop" << 'EOF'
# AI Workshop

Let's learn about AI together!
EOF
```

#### Method 4: Interactive mode
```bash
./marp-quick
# Then paste your content and press Ctrl+D
```

### Command Line Options

- `-i, --input`: Input file containing slide content (required)
- `-o, --output`: Output directory for generated slides (default: 'output')
- `-n, --name`: Presentation name (defaults to first title in content)
- `-t, --theme`: Marp theme to use (choices: default, gaia, uncover)

## Cursor IDE Workflow

This project is optimized for use with Cursor IDE. See `.cursorrules` for detailed guidelines.

### Recommended Workflow:

1. **Create your content file** (e.g., `my_slides.txt`)
2. **Start watch mode** in a terminal:
   ```bash
   uv run python watch_slides.py -i my_slides.txt -n my-awesome-presentation
   ```
3. **Edit in Cursor**: Make changes to your input file, and slides will auto-regenerate
4. **Preview**: Open `output/my-awesome-presentation/master_slide.md` with Marp preview
5. **Iterate**: Continue editing and see changes in real-time

### Quick Generation in Cursor Chat:

When someone pastes slide content in Cursor's chat, you can quickly generate slides:

```bash
uv run python quick_slides.py -n "presentation-name" << 'EOF'
[Paste the content here]
EOF
```

## Output Structure

The generator creates the following directory structure:

```
output/
└── <presentation-name>/     # Named after first title or custom -n parameter
    ├── master_slide.md      # Master slide file that includes all pages
    ├── index.md            # Index listing all slides with titles
    ├── 01-introduction/    # Slide folders named by number and title
    │   ├── page.md         # Individual slide content
    │   └── assets/         # Images and other assets for this slide
    ├── 02-getting-started/
    │   ├── page.md
    │   └── assets/
    └── ...
```

### Folder Naming Convention

- **Presentation folder**: Uses the first main title or custom name specified with `-n`
- **Slide folders**: Format `NN-slide-title` where:
  - `NN` is the slide number (01, 02, etc.)
  - `slide-title` is derived from the first header in the slide
  - Special characters are removed and spaces become hyphens

## How It Works

1. **Content Analysis**: The generator analyzes your input content to identify natural break points
2. **Smart Splitting**: Content is split based on:
   - Explicit page breaks (`---`)
   - Major headings (# and ##)
   - Content length limits (15 lines or 800 characters per page)
3. **Formatting**: Each page is formatted with:
   - Marp front matter
   - Theme settings
   - Enhanced spacing for readability
4. **Organization**: Creates a presentation folder with individual slide folders
5. **Master Slide**: Combines all pages into a single master slide for presentation

## Example Input

Create a file `example_slides.txt`:

```markdown
# Introduction to Python

Python is a high-level programming language known for its simplicity and readability.

## Key Features

- Easy to learn
- Versatile and powerful
- Large ecosystem of libraries
- Great community support

---

# Getting Started

## Installation

1. Download Python from python.org
2. Install using the installer
3. Verify installation: `python --version`

## First Program

```python
print("Hello, World!")
```

---

# Data Types

Python supports various data types:

- Numbers (int, float)
- Strings
- Lists
- Dictionaries
- Sets
- Tuples
```

Generate slides:
```bash
uv run marp-gen -i example_slides.txt -n python-intro
```

## Rendering Slides

After generating the slides, you can render them using Marp:

### Using Marp CLI

```bash
# Install Marp CLI
npm install -g @marp-team/marp-cli

# Render the master slide (example for python-intro presentation)
marp output/python-intro/master_slide.md -o python-intro.pdf
```

### Using VS Code

1. Install the Marp for VS Code extension
2. Open `master_slide.md` from your presentation folder
3. Preview or export using the extension

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black .
```

### Linting

```bash
uv run pylint *.py
```

## Tips for Best Results

1. **Use Clear Headers**: Start major sections with # or ## headers
2. **Keep Content Concise**: Aim for bullet points and short paragraphs
3. **Use Page Breaks**: Add `---` where you want explicit page breaks
4. **Add Visual Elements**: Include code blocks, lists, and images for engagement
5. **Use Watch Mode**: For iterative editing in Cursor
6. **Name Your Presentations**: Use the `-n` option for meaningful folder names

## License

MIT License 