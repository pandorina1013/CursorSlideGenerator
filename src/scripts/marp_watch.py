#!/usr/bin/env python3
"""
Watch for changes and automatically regenerate slides
"""

import os
import sys
import time
import click
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from marp_slide_generator import SlideGenerator


class SlideChangeHandler(FileSystemEventHandler):
    """Handler for file changes"""
    
    def __init__(self, input_file, output_dir, presentation_name, theme):
        self.input_file = input_file
        self.output_dir = output_dir
        self.presentation_name = presentation_name
        self.theme = theme
        self.last_run = 0
        self.debounce_time = 1.0  # 1 second debounce
        
    def on_modified(self, event):
        if event.src_path == self.input_file:
            current_time = time.time()
            if current_time - self.last_run > self.debounce_time:
                self.last_run = current_time
                self.regenerate()
                
    def regenerate(self):
        """Regenerate slides from input file"""
        print(f"\n🔄 File changed, regenerating slides...")
        
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            generator = SlideGenerator(self.output_dir, self.presentation_name)
            num_pages = generator.generate_slides(content, self.theme)
            
            print(f"✓ Generated {num_pages} slides successfully")
            print(f"  Output: {generator.output_dir}")
            
        except Exception as e:
            print(f"❌ Error generating slides: {e}")


@click.command()
@click.option('--input', '-i', 'input_file', required=True,
              help='Input file to watch')
@click.option('--output', '-o', 'output_dir', default='output',
              help='Output directory for generated slides')
@click.option('--name', '-n', 'presentation_name',
              help='Presentation name')
@click.option('--theme', '-t', default='default',
              type=click.Choice(['default', 'gaia', 'uncover'], case_sensitive=False),
              help='Marp theme to use')
def main(input_file: str, output_dir: str, presentation_name: str, theme: str):
    """Watch input file and regenerate slides on changes"""
    
    # Check if input file exists
    if not os.path.exists(input_file):
        click.echo(f"Error: Input file '{input_file}' not found.", err=True)
        return
        
    # Initial generation
    print(f"📝 Generating initial slides from '{input_file}'...")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        generator = SlideGenerator(output_dir, presentation_name)
        num_pages = generator.generate_slides(content, theme)
        
        print(f"✓ Generated {num_pages} slides in '{generator.output_dir}'")
        
    except Exception as e:
        click.echo(f"Error generating slides: {e}", err=True)
        return
        
    # Set up file watcher
    event_handler = SlideChangeHandler(input_file, output_dir, presentation_name, theme)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(input_file) or '.', recursive=False)
    
    print(f"\n👀 Watching '{input_file}' for changes...")
    print("   Press Ctrl+C to stop")
    
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n✋ Stopped watching")
    observer.join()


if __name__ == "__main__":
    main() 