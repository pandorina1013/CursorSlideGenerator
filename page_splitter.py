"""
Page Splitter Module
Intelligently splits content into pages for Marp slides
"""

import re
from typing import List, Tuple


class PageSplitter:
    """Splits content into appropriately sized pages"""
    
    def __init__(self, max_lines_per_page: int = 15, max_chars_per_page: int = 800):
        self.max_lines_per_page = max_lines_per_page
        self.max_chars_per_page = max_chars_per_page
        
    def split_content(self, content: str) -> List[str]:
        """Split content into pages based on various heuristics"""
        # First, try to split by explicit page breaks (---)
        if '---' in content:
            pages = self._split_by_breaks(content)
        else:
            # Otherwise, split intelligently by headers and content length
            pages = self._smart_split(content)
            
        # Ensure no page is too long
        final_pages = []
        for page in pages:
            if self._is_page_too_long(page):
                sub_pages = self._split_long_page(page)
                final_pages.extend(sub_pages)
            else:
                final_pages.append(page)
                
        return [page.strip() for page in final_pages if page.strip()]
        
    def _split_by_breaks(self, content: str) -> List[str]:
        """Split content by explicit page breaks (---)"""
        # Split by --- but preserve it for Marp
        pages = re.split(r'\n---\n', content)
        return pages
        
    def _smart_split(self, content: str) -> List[str]:
        """Intelligently split content based on structure"""
        lines = content.split('\n')
        pages = []
        current_page = []
        current_line_count = 0
        current_char_count = 0
        
        for line in lines:
            # Check if this is a major heading (# or ##)
            is_major_heading = line.strip().startswith(('# ', '## '))
            
            # Start new page on major headings if current page has content
            if is_major_heading and current_page:
                pages.append('\n'.join(current_page))
                current_page = [line]
                current_line_count = 1
                current_char_count = len(line)
            # Check if adding this line would exceed limits
            elif (current_line_count >= self.max_lines_per_page or 
                  current_char_count + len(line) > self.max_chars_per_page):
                # Start new page
                pages.append('\n'.join(current_page))
                current_page = [line]
                current_line_count = 1
                current_char_count = len(line)
            else:
                # Add to current page
                current_page.append(line)
                current_line_count += 1
                current_char_count += len(line)
                
        # Don't forget the last page
        if current_page:
            pages.append('\n'.join(current_page))
            
        return pages
        
    def _is_page_too_long(self, page: str) -> bool:
        """Check if a page exceeds the limits"""
        lines = page.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        return (len(non_empty_lines) > self.max_lines_per_page or 
                len(page) > self.max_chars_per_page)
        
    def _split_long_page(self, page: str) -> List[str]:
        """Split a long page into smaller chunks"""
        lines = page.split('\n')
        sub_pages = []
        current_sub = []
        current_line_count = 0
        
        for line in lines:
            if current_line_count >= self.max_lines_per_page:
                sub_pages.append('\n'.join(current_sub))
                current_sub = [line]
                current_line_count = 1
            else:
                current_sub.append(line)
                current_line_count += 1 if line.strip() else 0
                
        if current_sub:
            sub_pages.append('\n'.join(current_sub))
            
        return sub_pages 