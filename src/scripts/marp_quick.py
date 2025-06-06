#!/usr/bin/env python3
"""
Quick slide generator - generate slides from stdin or direct input
"""

import sys
import click
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from marp_slide_generator import SlideGenerator


@click.command()
@click.option('--output', '-o', 'output_dir', default='output',
              help='Output directory for generated slides')
@click.option('--name', '-n', 'presentation_name',
              help='Presentation name (defaults to first title in content)')
@click.option('--theme', '-t', default='gaia',
              type=click.Choice(['default', 'gaia', 'uncover'], case_sensitive=False),
              help='Marp theme to use (default: gaia)')
@click.option('--content', '-c',
              help='Direct content input (alternative to stdin)')
def main(output_dir: str, presentation_name: str, theme: str, content: str):
    """Generate Marp slides from stdin or direct content"""
    
    # Get content from direct input or stdin
    if content:
        slide_content = content
    else:
        # Read from stdin
        slide_content = sys.stdin.read()
    
    if not slide_content.strip():
        click.echo("Error: No content provided", err=True)
        return
    
    # Generate slides
    generator = SlideGenerator(output_dir, presentation_name)
    try:
        num_pages = generator.generate_slides(slide_content, theme)
        actual_output = generator.output_dir
        click.echo(f"✓ Successfully generated {num_pages} slides in '{actual_output}'")
        click.echo(f"  - Master slide: {actual_output}/master_slide.md")
        click.echo(f"  - Index: {actual_output}/index.md")
        click.echo(f"  - Slides: {actual_output}/")
    except Exception as e:
        click.echo(f"Error generating slides: {e}", err=True)
        raise


if __name__ == "__main__":
    main() 