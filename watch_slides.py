#!/usr/bin/env python3
"""
Watch Mode for Marp Slide Generator
Monitors input file changes and automatically regenerates slides
"""

import os
import time
import click
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from slide_generator import SlideGenerator


class SlideRegenerator(FileSystemEventHandler):
    """Handler for file change events"""
    
    def __init__(self, input_file: str, output_dir: str, 
                 presentation_name: str = None, theme: str = 'default'):
        self.input_file = Path(input_file)
        self.output_dir = output_dir
        self.presentation_name = presentation_name
        self.theme = theme
        self.generator = SlideGenerator(output_dir, presentation_name)
        self.last_modified = 0
        
    def on_modified(self, event):
        """Handle file modification events"""
        if event.is_directory:
            return
            
        # Check if the modified file is our input file
        if Path(event.src_path).resolve() == self.input_file.resolve():
            # Debounce: ignore if modified within 1 second
            current_time = time.time()
            if current_time - self.last_modified < 1:
                return
                
            self.last_modified = current_time
            self.regenerate_slides()
            
    def regenerate_slides(self):
        """Regenerate slides from the input file"""
        click.echo(f"\n🔄 Detected changes in {self.input_file.name}")
        
        try:
            # Read content
            content = self.input_file.read_text(encoding='utf-8')
            
            # Generate slides
            num_pages = self.generator.generate_slides(content, self.theme)
            actual_output = self.generator.output_dir
            
            click.echo(f"✓ Regenerated {num_pages} slides")
            click.echo(f"  Preview: {actual_output}/master_slide.md")
            
        except Exception as e:
            click.echo(f"❌ Error regenerating slides: {e}", err=True)


@click.command()
@click.option('--input', '-i', 'input_file', required=True,
              help='Input file to watch for changes')
@click.option('--output', '-o', 'output_dir', default='output',
              help='Output directory for generated slides')
@click.option('--name', '-n', 'presentation_name',
              help='Presentation name (defaults to first title in content)')
@click.option('--theme', '-t', default='default',
              type=click.Choice(['default', 'gaia', 'uncover'], case_sensitive=False),
              help='Marp theme to use')
def main(input_file: str, output_dir: str, presentation_name: str, theme: str):
    """Watch input file and regenerate slides on changes"""
    
    # Validate input file
    input_path = Path(input_file)
    if not input_path.exists():
        click.echo(f"Error: Input file '{input_file}' not found.", err=True)
        return
        
    # Initial generation
    click.echo(f"🚀 Starting watch mode for: {input_file}")
    click.echo(f"   Output directory: {output_dir}")
    if presentation_name:
        click.echo(f"   Presentation name: {presentation_name}")
    click.echo(f"   Theme: {theme}")
    click.echo("\nPress Ctrl+C to stop watching...\n")
    
    # Create event handler and generate initial slides
    event_handler = SlideRegenerator(input_file, output_dir, presentation_name, theme)
    event_handler.regenerate_slides()
    
    # Set up file watcher
    observer = Observer()
    observer.schedule(event_handler, path=str(input_path.parent), recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        click.echo("\n\n👋 Watch mode stopped.")
        
    observer.join()


if __name__ == "__main__":
    main() 