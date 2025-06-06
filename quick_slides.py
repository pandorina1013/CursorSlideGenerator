#!/usr/bin/env python3
"""
Quick Slide Generator for Cursor Chat
Generates slides from text input via stdin or argument
"""

import sys
import click
import tempfile
from pathlib import Path
from slide_generator import SlideGenerator


def generate_from_text(text: str, output_dir: str = "output", 
                      presentation_name: str = None, theme: str = "default"):
    """Generate slides directly from text content"""
    generator = SlideGenerator(output_dir, presentation_name)
    num_pages = generator.generate_slides(text, theme)
    return num_pages, generator.output_dir


@click.command()
@click.option('--output', '-o', 'output_dir', default='output',
              help='Output directory for generated slides')
@click.option('--name', '-n', 'presentation_name',
              help='Presentation name (defaults to first title in content)')
@click.option('--theme', '-t', default='default',
              type=click.Choice(['default', 'gaia', 'uncover'], case_sensitive=False),
              help='Marp theme to use')
@click.option('--text', '-c', 'content', 
              help='Text content directly (alternative to stdin)')
def main(output_dir: str, presentation_name: str, theme: str, content: str = None):
    """
    Quick slide generator that accepts text from stdin or command line.
    
    Examples:
        echo "# My Slide" | uv run python quick_slides.py
        uv run python quick_slides.py -c "# My Slide"
        cat slides.txt | uv run python quick_slides.py -o my_output
    """
    
    # Get content from argument or stdin
    if content:
        text = content
    else:
        # Read from stdin
        if sys.stdin.isatty():
            click.echo("Error: No input provided. Use -c option or pipe text to stdin.", err=True)
            click.echo("Example: echo '# My Slides' | uv run python quick_slides.py", err=True)
            sys.exit(1)
        text = sys.stdin.read()
    
    if not text.strip():
        click.echo("Error: Empty input provided.", err=True)
        sys.exit(1)
    
    try:
        # Generate slides
        num_pages, actual_output = generate_from_text(text, output_dir, presentation_name, theme)
        
        click.echo(f"\n✓ Successfully generated {num_pages} slides in '{actual_output}'")
        click.echo(f"  - Master slide: {actual_output}/master_slide.md")
        click.echo(f"  - Index: {actual_output}/index.md")
        click.echo(f"  - Slides: {actual_output}/")
        
        # Also output the paths for easy copying
        click.echo(f"\nView with Marp:")
        click.echo(f"  marp {actual_output}/master_slide.md --preview")
        
    except Exception as e:
        click.echo(f"Error generating slides: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main() 