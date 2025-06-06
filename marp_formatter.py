"""
Marp Formatter Module
Formats content for Marp slide presentation
"""

from typing import List
from pathlib import Path


class MarpFormatter:
    """Formats content for Marp slides"""
    
    def __init__(self):
        self.themes = {
            'default': {
                'backgroundColor': '#fff',
                'color': '#293742',
                'paginate': True
            },
            'gaia': {
                'class': 'gaia',
                'backgroundColor': '#fff',
                'color': '#000',
                'paginate': True
            },
            'uncover': {
                'class': 'uncover',
                'backgroundColor': '#fff', 
                'color': '#293742',
                'paginate': True
            }
        }
        
    def format_page(self, content: str, page_number: int, 
                   total_pages: int, theme: str = 'default') -> str:
        """Format a single page with Marp directives"""
        # Get theme settings
        theme_settings = self.themes.get(theme, self.themes['default'])
        
        # Build Marp front matter - only for first page
        if page_number == 1:
            front_matter = ['---', 'marp: true']
            
            # Add theme settings
            if 'class' in theme_settings:
                front_matter.append(f"class: {theme_settings['class']}")
            if theme_settings.get('paginate'):
                front_matter.append("paginate: true")
            if 'backgroundColor' in theme_settings:
                front_matter.append(f"backgroundColor: {theme_settings['backgroundColor']}")
            if 'color' in theme_settings:
                front_matter.append(f"color: {theme_settings['color']}")
                
            front_matter.append('---')
            front_matter.append('')
            
            # Combine front matter with content
            formatted_content = '\n'.join(front_matter) + content
        else:
            # For subsequent pages, don't add separator (will be added when combining)
            formatted_content = content
        
        # Add some formatting enhancements
        formatted_content = self._enhance_formatting(formatted_content)
        
        return formatted_content
        
    def format_master_slide(self, page_paths: List[str], theme: str = 'default') -> str:
        """Format the master slide by combining all page contents"""
        theme_settings = self.themes.get(theme, self.themes['default'])
        
        # Build master slide header
        lines = [
            '---',
            'marp: true',
            'paginate: true'
        ]
        
        # Add theme settings
        if 'class' in theme_settings:
            lines.append(f"class: {theme_settings['class']}")
        if 'backgroundColor' in theme_settings:
            lines.append(f"backgroundColor: {theme_settings['backgroundColor']}")
        if 'color' in theme_settings:
            lines.append(f"color: {theme_settings['color']}")
            
        lines.extend([
            '---',
            ''
        ])
        
        # Read and combine all page contents
        master_content = '\n'.join(lines)
        
        for i, page_path in enumerate(page_paths):
            # Read page content
            full_path = Path(page_path)
            if full_path.exists():
                page_content = full_path.read_text(encoding='utf-8')
            else:
                # Try relative to current directory
                page_content = Path(page_path).read_text(encoding='utf-8')
            
            # Remove Marp front matter from all individual pages
            if page_content.startswith('---'):
                # Find the end of front matter
                lines = page_content.split('\n')
                front_matter_end = 0
                for j, line in enumerate(lines[1:], 1):
                    if line.strip() == '---':
                        front_matter_end = j + 1
                        break
                # Skip empty lines after front matter
                while front_matter_end < len(lines) and not lines[front_matter_end].strip():
                    front_matter_end += 1
                page_content = '\n'.join(lines[front_matter_end:])
            
            # Add page separator for all pages after the first
            if i > 0:
                master_content += '\n\n---\n\n'
                
            master_content += page_content.strip()
            
        return master_content
        
    def _enhance_formatting(self, content: str) -> str:
        """Enhance content formatting for better slide presentation"""
        lines = content.split('\n')
        enhanced_lines = []
        
        for line in lines:
            # Make headers more prominent
            if line.startswith('# '):
                enhanced_lines.append(line)
                enhanced_lines.append('')  # Add space after main headers
            elif line.startswith('## '):
                if enhanced_lines and enhanced_lines[-1] != '':
                    enhanced_lines.append('')  # Add space before subheaders
                enhanced_lines.append(line)
            elif line.startswith('- ') or line.startswith('* '):
                # Ensure bullet points have proper spacing
                enhanced_lines.append(line)
            elif line.startswith('```'):
                # Code blocks
                if enhanced_lines and enhanced_lines[-1] != '':
                    enhanced_lines.append('')
                enhanced_lines.append(line)
            else:
                enhanced_lines.append(line)
                
        # Clean up multiple empty lines
        final_lines = []
        prev_empty = False
        for line in enhanced_lines:
            if not line.strip():
                if not prev_empty:
                    final_lines.append(line)
                prev_empty = True
            else:
                final_lines.append(line)
                prev_empty = False
                
        return '\n'.join(final_lines) 