"""Regenerate master and index files from existing slide structure"""

from pathlib import Path
from typing import List, Optional
from .marp_formatter import MarpFormatter


class SlideRegenerator:
    """Regenerate master_slide.md and index.md from existing folder structure"""
    
    def __init__(self):
        self.formatter = MarpFormatter()
    
    def get_slide_folders(self, presentation_dir: Path) -> List[Path]:
        """Get all folders containing page.md files, sorted by numeric prefix"""
        folders = []
        for item in presentation_dir.iterdir():
            if item.is_dir() and (item / "page.md").exists():
                folders.append(item)
        
        # Sort folders by their numeric prefix
        folders.sort(key=lambda x: int(x.name.split('-')[0]) if x.name.split('-')[0].isdigit() else 999)
        return folders
    
    def extract_title(self, page_content: str) -> str:
        """Extract title from page content"""
        lines = page_content.split('\n')
        in_frontmatter = False
        
        for line in lines:
            if line.strip() == '---':
                in_frontmatter = not in_frontmatter
                continue
            if not in_frontmatter:
                if line.strip().startswith('# '):
                    return line.strip()[2:].strip()
                elif line.strip().startswith('## '):
                    return line.strip()[3:].strip()
        
        return "Untitled"
    
    def regenerate_master(self, presentation_dir: Path, theme: str = "gaia") -> int:
        """Regenerate master_slide.md from existing slides"""
        folders = self.get_slide_folders(presentation_dir)
        
        # Get absolute paths for all page.md files
        page_paths = []
        for folder in folders:
            page_path = folder / "page.md"
            page_paths.append(str(page_path.absolute()))
        
        # Generate master slide content
        master_content = self.formatter.format_master_slide(page_paths, theme)
        master_file = presentation_dir / "master_slide.md"
        master_file.write_text(master_content, encoding='utf-8')
        
        return len(page_paths)
    
    def regenerate_index(self, presentation_dir: Path) -> int:
        """Regenerate index.md from existing slides"""
        folders = self.get_slide_folders(presentation_dir)
        
        # Generate presentation name from directory
        presentation_name = presentation_dir.name.replace('-', ' ').title()
        index_content = [f"# {presentation_name} - Slide Index", ""]
        
        for i, folder in enumerate(folders, 1):
            # Read page content to extract title
            page_file = folder / "page.md"
            content = page_file.read_text(encoding='utf-8')
            title = self.extract_title(content)
            
            # Get relative path for index
            relative_path = folder.relative_to(presentation_dir)
            index_content.append(f"{i}. **{title}** - `{relative_path}/page.md`")
        
        # Write index file
        index_file = presentation_dir / "index.md"
        index_file.write_text('\n'.join(index_content), encoding='utf-8')
        
        return len(folders)
    
    def regenerate_all(self, presentation_dir: str, theme: str = "gaia") -> None:
        """Regenerate both master_slide.md and index.md"""
        presentation_path = Path(presentation_dir)
        
        if not presentation_path.exists():
            raise ValueError(f"Presentation directory not found: {presentation_dir}")
        
        # Regenerate master slide
        num_slides = self.regenerate_master(presentation_path, theme)
        print(f"✓ Regenerated master_slide.md with {num_slides} slides")
        
        # Regenerate index
        num_indexed = self.regenerate_index(presentation_path)
        print(f"✓ Regenerated index.md with {num_indexed} entries") 