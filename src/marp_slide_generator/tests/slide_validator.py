"""Slide validation tests for Marp presentations."""

import os
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import json


class SlideValidator:
    """Validates Marp slide quality and structure."""
    
    def __init__(self, presentation_dir: str):
        self.presentation_dir = Path(presentation_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def validate_all(self) -> Dict[str, List[str]]:
        """Run all validation checks."""
        self.errors.clear()
        self.warnings.clear()
        
        if not self.presentation_dir.exists():
            self.errors.append(f"Presentation directory does not exist: {self.presentation_dir}")
            return {"errors": self.errors, "warnings": self.warnings}
        
        # Run all validations
        self.validate_master_slide()
        self.validate_index_file()
        self.validate_slide_folders()
        self.validate_individual_slides()
        self.validate_code_blocks()
        self.validate_mermaid_diagrams()
        self.validate_slide_lengths()
        self.validate_markdown_syntax()
        self.validate_assets()
        self.validate_consistency()
        
        return {"errors": self.errors, "warnings": self.warnings}
    
    def validate_master_slide(self):
        """Validate master_slide.md structure."""
        master_file = self.presentation_dir / "master_slide.md"
        
        if not master_file.exists():
            self.errors.append("master_slide.md is missing")
            return
            
        content = master_file.read_text(encoding='utf-8')
        
        # Check Marp frontmatter
        if not content.startswith("---\nmarp: true"):
            self.errors.append("master_slide.md missing Marp frontmatter")
        
        # Check for proper slide separators
        slides = content.split("\n---\n")
        if len(slides) < 2:
            self.errors.append("master_slide.md has no slide separators (---)")
        
        # Check for incomplete code blocks - updated logic
        code_blocks = re.findall(r'```', content)
        if len(code_blocks) % 2 != 0:
            self.errors.append(f"Unclosed code blocks in master_slide.md: {len(code_blocks)} backtick sequences found (should be even)")
    
    def validate_index_file(self):
        """Validate index.md structure."""
        index_file = self.presentation_dir / "index.md"
        
        if not index_file.exists():
            self.errors.append("index.md is missing")
            return
            
        content = index_file.read_text(encoding='utf-8')
        
        # Check if index has proper structure
        lines = content.strip().split('\n')
        if not lines[0].startswith("#"):
            self.errors.append("index.md should start with a header")
        
        # Count slide entries
        slide_entries = [line for line in lines if re.match(r'^\d+\.\s+\*\*.*\*\*\s+-\s+`.*`$', line)]
        if not slide_entries:
            self.errors.append("index.md has no properly formatted slide entries")
    
    def validate_slide_folders(self):
        """Validate slide folder structure."""
        folders = [f for f in self.presentation_dir.iterdir() if f.is_dir()]
        slide_folders = [f for f in folders if re.match(r'^\d{2}-', f.name)]
        
        if not slide_folders:
            self.errors.append("No slide folders found (format: NN-title)")
            return
        
        # Check sequential numbering
        numbers = []
        for folder in slide_folders:
            match = re.match(r'^(\d{2})-', folder.name)
            if match:
                numbers.append(int(match.group(1)))
        
        numbers.sort()
        expected = list(range(1, len(numbers) + 1))
        if numbers != expected:
            self.warnings.append(f"Non-sequential slide numbering: {numbers}")
        
        # Check each folder has page.md
        for folder in slide_folders:
            page_file = folder / "page.md"
            if not page_file.exists():
                self.errors.append(f"Missing page.md in {folder.name}")
    
    def validate_individual_slides(self):
        """Validate individual slide files."""
        folders = [f for f in self.presentation_dir.iterdir() if f.is_dir()]
        slide_folders = [f for f in folders if re.match(r'^\d{2}-', f.name)]
        
        for folder in slide_folders:
            page_file = folder / "page.md"
            if page_file.exists():
                content = page_file.read_text(encoding='utf-8')
                
                # Check if slide has content
                if not content.strip():
                    self.errors.append(f"Empty slide: {folder.name}/page.md")
                
                # Check for title
                if not re.search(r'^#\s+', content, re.MULTILINE):
                    self.warnings.append(f"No title (# header) in {folder.name}/page.md")
    
    def validate_code_blocks(self):
        """Validate code blocks in all slides."""
        all_md_files = list(self.presentation_dir.rglob("*.md"))
        
        for md_file in all_md_files:
            content = md_file.read_text(encoding='utf-8')
            
            # Simple check: count triple backticks
            backticks = re.findall(r'```', content)
            if len(backticks) % 2 != 0:
                self.errors.append(f"Unclosed code blocks in {md_file.relative_to(self.presentation_dir)}")
    
    def validate_mermaid_diagrams(self):
        """Validate Mermaid diagram syntax."""
        all_md_files = list(self.presentation_dir.rglob("*.md"))
        
        for md_file in all_md_files:
            content = md_file.read_text(encoding='utf-8')
            
            # Find Mermaid blocks
            mermaid_blocks = re.findall(r'```mermaid\n(.*?)\n```', content, re.DOTALL)
            
            for i, block in enumerate(mermaid_blocks):
                # Basic Mermaid syntax checks
                if 'graph' in block or 'flowchart' in block:
                    if not re.search(r'(graph|flowchart)\s+(TD|LR|RL|BT|TB)', block):
                        self.warnings.append(f"Mermaid diagram missing direction in {md_file.relative_to(self.presentation_dir)}")
                
                # Check for unclosed quotes
                quotes = re.findall(r'"', block)
                if len(quotes) % 2 != 0:
                    self.errors.append(f"Unclosed quotes in Mermaid diagram in {md_file.relative_to(self.presentation_dir)}")
    
    def validate_slide_lengths(self):
        """Check if slides are within reasonable length limits."""
        MAX_LINES = 30  # Typical screen can show ~20-25 lines
        MAX_CHARS = 1500  # Reasonable character limit per slide
        
        folders = [f for f in self.presentation_dir.iterdir() if f.is_dir()]
        slide_folders = [f for f in folders if re.match(r'^\d{2}-', f.name)]
        
        for folder in slide_folders:
            page_file = folder / "page.md"
            if page_file.exists():
                content = page_file.read_text(encoding='utf-8')
                lines = content.split('\n')
                
                # Count non-empty lines
                non_empty_lines = [line for line in lines if line.strip()]
                
                if len(non_empty_lines) > MAX_LINES:
                    self.warnings.append(f"Slide too long ({len(non_empty_lines)} lines): {folder.name}")
                
                if len(content) > MAX_CHARS:
                    self.warnings.append(f"Slide has too many characters ({len(content)}): {folder.name}")
    
    def validate_markdown_syntax(self):
        """Basic markdown syntax validation."""
        all_md_files = list(self.presentation_dir.rglob("*.md"))
        
        for md_file in all_md_files:
            content = md_file.read_text(encoding='utf-8')
            
            # Check for broken links
            links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for link_text, link_url in links:
                if link_url.startswith('http'):
                    continue  # Skip external URLs
                if link_url.startswith('#'):
                    continue  # Skip anchors
                
                # Check local file references
                if not link_url.startswith('assets/'):
                    full_path = md_file.parent / link_url
                    if not full_path.exists():
                        self.warnings.append(f"Broken link to '{link_url}' in {md_file.relative_to(self.presentation_dir)}")
            
            # Check for unmatched brackets
            open_brackets = len(re.findall(r'\[', content))
            close_brackets = len(re.findall(r'\]', content))
            if open_brackets != close_brackets:
                self.warnings.append(f"Unmatched brackets in {md_file.relative_to(self.presentation_dir)}")
    
    def validate_assets(self):
        """Check for unused or missing assets."""
        # Find all asset references in markdown files
        referenced_assets = set()
        all_md_files = list(self.presentation_dir.rglob("*.md"))
        
        for md_file in all_md_files:
            content = md_file.read_text(encoding='utf-8')
            
            # Find image references
            images = re.findall(r'!\[.*?\]\(([^)]+)\)', content)
            for img in images:
                if img.startswith('assets/'):
                    referenced_assets.add(img)
        
        # Find all actual asset files
        asset_files = set()
        for assets_dir in self.presentation_dir.rglob("assets"):
            if assets_dir.is_dir():
                for asset_file in assets_dir.iterdir():
                    if asset_file.is_file():
                        relative_path = asset_file.relative_to(assets_dir.parent)
                        asset_files.add(str(relative_path).replace('\\', '/'))
        
        # Check for missing assets
        missing = referenced_assets - asset_files
        for asset in missing:
            self.errors.append(f"Referenced asset not found: {asset}")
        
        # Check for unused assets
        unused = asset_files - referenced_assets
        for asset in unused:
            self.warnings.append(f"Unused asset file: {asset}")
    
    def validate_consistency(self):
        """Check consistency between index, folders, and master slide."""
        # Get slide count from different sources
        index_file = self.presentation_dir / "index.md"
        master_file = self.presentation_dir / "master_slide.md"
        
        # Count slides in folders
        folders = [f for f in self.presentation_dir.iterdir() if f.is_dir()]
        slide_folders = [f for f in folders if re.match(r'^\d{2}-', f.name)]
        folder_count = len(slide_folders)
        
        # Count slides in index
        if index_file.exists():
            index_content = index_file.read_text(encoding='utf-8')
            index_entries = len(re.findall(r'^\d+\.\s+\*\*.*\*\*\s+-\s+`.*`$', index_content, re.MULTILINE))
        else:
            index_entries = 0
        
        # Count slides in master
        if master_file.exists():
            master_content = master_file.read_text(encoding='utf-8')
            # Remove frontmatter
            if master_content.startswith('---'):
                master_content = master_content.split('---', 2)[2]
            master_slides = len(master_content.split('\n---\n'))
        else:
            master_slides = 0
        
        # Check consistency
        if folder_count != index_entries:
            self.errors.append(f"Mismatch: {folder_count} folders but {index_entries} index entries")
        
        if folder_count != master_slides:
            self.errors.append(f"Mismatch: {folder_count} folders but {master_slides} slides in master")


def run_validation(presentation_dir: str) -> Tuple[int, int]:
    """Run validation and return (error_count, warning_count)."""
    validator = SlideValidator(presentation_dir)
    results = validator.validate_all()
    
    print(f"\n🔍 Validating presentation: {presentation_dir}")
    print("=" * 60)
    
    if results["errors"]:
        print(f"\n❌ ERRORS ({len(results['errors'])})")
        for error in results["errors"]:
            print(f"   • {error}")
    else:
        print("\n✅ No errors found!")
    
    if results["warnings"]:
        print(f"\n⚠️  WARNINGS ({len(results['warnings'])})")
        for warning in results["warnings"]:
            print(f"   • {warning}")
    else:
        print("\n✅ No warnings found!")
    
    print("\n" + "=" * 60)
    print(f"Summary: {len(results['errors'])} errors, {len(results['warnings'])} warnings\n")
    
    return len(results["errors"]), len(results["warnings"])


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python slide_validator.py <presentation_directory>")
        sys.exit(1)
    
    error_count, warning_count = run_validation(sys.argv[1])
    
    # Exit with error code if there are errors
    if error_count > 0:
        sys.exit(1)
    else:
        sys.exit(0) 