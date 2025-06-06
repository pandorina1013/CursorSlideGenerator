#!/usr/bin/env python3
"""
Marp Slide Generator CLI
"""

import click
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from marp_slide_generator import SlideGenerator


@click.command()
@click.option('--input', '-i', 'input_file', required=True, 
              help='Input file containing slide content')
@click.option('--output', '-o', 'output_dir', default='output',
              help='Output directory for generated slides')
@click.option('--name', '-n', 'presentation_name',
              help='Presentation name (defaults to first title in content)')
@click.option('--theme', '-t', default='default',
              type=click.Choice(['default', 'gaia', 'uncover'], case_sensitive=False),
              help='Marp theme to use')
def main(input_file: str, output_dir: str, presentation_name: str, theme: str):
    """Generate Marp slides from input content"""
    # Read input content
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        click.echo(f"Error: Input file '{input_file}' not found.", err=True)
        return
        
    # Generate slides
    generator = SlideGenerator(output_dir, presentation_name)
    try:
        num_pages = generator.generate_slides(content, theme)
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