#!/usr/bin/env python3
"""
Marp Slide Generator
Automatically splits content into well-organized Marp slides
"""

import os
import re
import shutil
import click
from pathlib import Path
from typing import List, Tuple

from page_splitter import PageSplitter
from marp_formatter import MarpFormatter


class SlideGenerator:
    """Main class for generating Marp slides from content"""
    
    def __init__(self, output_dir: str = "output", presentation_name: str = None):
        self.base_output_dir = Path(output_dir)
        self.presentation_name = presentation_name
        if presentation_name:
            self.output_dir = self.base_output_dir / presentation_name
        else:
            self.output_dir = self.base_output_dir
        self.splitter = PageSplitter()
        self.formatter = MarpFormatter()
        
    def setup_directories(self):
        """Create the necessary directory structure"""
        # Clean and create output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
        
    def _extract_title(self, content: str, page_number: int) -> str:
        """Extract title from page content for folder naming"""
        lines = content.strip().split('\n')
        
        # Look for the first header (# or ##)
        for line in lines:
            if line.strip().startswith('# '):
                title = line.strip()[2:].strip()
                break
            elif line.strip().startswith('## '):
                title = line.strip()[3:].strip()
                break
        else:
            # No header found, use default
            title = f"page{page_number}"
            
        # Clean title for filesystem use
        # Remove special characters and replace spaces with hyphens
        clean_title = re.sub(r'[^\w\s-]', '', title.lower())
        clean_title = re.sub(r'[-\s]+', '-', clean_title)
        clean_title = clean_title.strip('-')
        
        # Ensure title is not empty
        if not clean_title:
            clean_title = f"page{page_number}"
            
        # Add page number prefix to ensure uniqueness
        folder_name = f"{page_number:02d}-{clean_title}"
        
        return folder_name
        
    def _extract_presentation_name(self, content: str) -> str:
        """Extract presentation name from the first title in content"""
        lines = content.strip().split('\n')
        
        # Look for the first main header
        for line in lines:
            if line.strip().startswith('# '):
                title = line.strip()[2:].strip()
                # Clean for filesystem
                clean_name = re.sub(r'[^\w\s-]', '', title.lower())
                clean_name = re.sub(r'[-\s]+', '-', clean_name)
                clean_name = clean_name.strip('-')
                return clean_name if clean_name else "presentation"
                
        return "presentation"
        
    def generate_slides(self, content: str, theme: str = "default"):
        """Generate slides from content"""
        # If no presentation name was provided, extract from content
        if not self.presentation_name:
            self.presentation_name = self._extract_presentation_name(content)
            self.output_dir = self.base_output_dir / self.presentation_name
            
        # Setup directories
        self.setup_directories()
        
        # Split content into pages
        pages = self.splitter.split_content(content)
        
        # Generate individual page files
        page_paths = []
        folder_names = []
        
        for i, page_content in enumerate(pages, 1):
            # Extract title and create folder name
            folder_name = self._extract_title(page_content, i)
            folder_names.append(folder_name)
            
            page_dir = self.output_dir / folder_name
            page_dir.mkdir()
            
            # Create assets directory for the page
            assets_dir = page_dir / "assets"
            assets_dir.mkdir()
            
            # Format and write page content
            formatted_content = self.formatter.format_page(
                page_content, 
                page_number=i, 
                total_pages=len(pages),
                theme=theme
            )
            
            page_file = page_dir / "page.md"
            page_file.write_text(formatted_content, encoding='utf-8')
            # Store relative path from output dir for master slide generation
            page_paths.append(str(page_file.relative_to(self.base_output_dir)))
            
        # Generate master slide file
        self._generate_master_slide(page_paths, theme)
        
        # Generate index file for easy navigation
        self._generate_index_file(folder_names, pages)
        
        return len(pages)
        
    def _generate_master_slide(self, page_paths: List[str], theme: str):
        """Generate the master slide file that includes all pages"""
        # Adjust paths to be absolute from base output dir
        full_paths = [str(self.base_output_dir / path) for path in page_paths]
        master_content = self.formatter.format_master_slide(full_paths, theme)
        master_file = self.output_dir / "master_slide.md"
        master_file.write_text(master_content, encoding='utf-8')
        
    def _generate_index_file(self, folder_names: List[str], pages: List[str]):
        """Generate an index file listing all slides with their titles"""
        index_content = [f"# {self.presentation_name.replace('-', ' ').title()} - Slide Index", ""]
        
        for i, (folder_name, page_content) in enumerate(zip(folder_names, pages), 1):
            # Extract the actual title from content
            lines = page_content.strip().split('\n')
            title = f"Page {i}"
            
            for line in lines:
                if line.strip().startswith('# '):
                    title = line.strip()[2:].strip()
                    break
                elif line.strip().startswith('## '):
                    title = line.strip()[3:].strip()
                    break
                    
            index_content.append(f"{i}. **{title}** - `{folder_name}/page.md`")
            
        index_file = self.output_dir / "index.md"
        index_file.write_text('\n'.join(index_content), encoding='utf-8')


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