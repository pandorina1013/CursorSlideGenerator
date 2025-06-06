#!/usr/bin/env python3
"""
Regenerate master_slide.md and index.md from existing folder structure
"""

import click
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from marp_slide_generator.regenerator import SlideRegenerator


@click.command()
@click.argument('presentation_dir', required=True)
@click.option('--theme', '-t', default='gaia',
              type=click.Choice(['default', 'gaia', 'uncover'], case_sensitive=False),
              help='Marp theme to use (default: gaia)')
def main(presentation_dir: str, theme: str):
    """Regenerate master_slide.md and index.md for an existing presentation
    
    PRESENTATION_DIR: Path to the presentation directory containing slide folders
    """
    regenerator = SlideRegenerator()
    
    try:
        regenerator.regenerate_all(presentation_dir, theme)
    except ValueError as e:
        click.echo(f"Error: {e}", err=True)
        return 1
    except Exception as e:
        click.echo(f"Error regenerating files: {e}", err=True)
        raise


if __name__ == "__main__":
    main() 