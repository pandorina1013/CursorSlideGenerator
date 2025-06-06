"""
Page Splitter Module
Intelligently splits content into pages for Marp slides
"""

import re
from typing import List, Tuple


class PageSplitter:
    """Splits content into appropriately sized pages"""
    
    def __init__(self, max_lines_per_page: int = 12, max_chars_per_page: int = 600):
        # Reduced limits for better vertical space management
        self.max_lines_per_page = max_lines_per_page
        self.max_chars_per_page = max_chars_per_page
        
    def split_content(self, content: str) -> List[str]:
        """Split content into pages based on various heuristics"""
        # Always use smart splitting regardless of --- presence
        # This ensures vertical space constraints are respected
        if '---' in content:
            # First split by explicit breaks, then intelligently re-split if needed
            initial_pages = self._split_by_breaks(content)
            pages = []
            for page in initial_pages:
                if self._is_page_too_long(page):
                    sub_pages = self._smart_split_single_page(page)
                    pages.extend(sub_pages)
                else:
                    pages.append(page)
        else:
            # Smart split from the beginning
            pages = self._smart_split(content)
            
        # Final pass: ensure no page exceeds limits with weighted line counting
        final_pages = []
        for page in pages:
            if self._is_page_too_long_weighted(page):
                sub_pages = self._split_long_page_smart(page)
                final_pages.extend(sub_pages)
            else:
                final_pages.append(page)
                
        return [page.strip() for page in final_pages if page.strip()]
        
    def _split_by_breaks(self, content: str) -> List[str]:
        """Split content by explicit page breaks (---)"""
        # Split by --- but preserve it for Marp
        pages = re.split(r'\n---\n', content)
        return pages
        
    def _smart_split_single_page(self, content: str) -> List[str]:
        """Intelligently split a single page that might be too long"""
        lines = content.split('\n')
        
        # Look for natural breakpoints
        breakpoints = []
        for i, line in enumerate(lines):
            # Major headings (# ##)
            if line.strip().startswith(('# ', '## ')):
                breakpoints.append(i)
            # Code block boundaries
            elif line.strip().startswith('```'):
                breakpoints.append(i)
            # List items after a gap
            elif (line.strip().startswith(('- ', '* ', '1. ')) and 
                  i > 0 and not lines[i-1].strip()):
                breakpoints.append(i)
                
        # If no natural breakpoints, fall back to line-based splitting
        if not breakpoints:
            return self._split_long_page_smart(content)
            
        # Create pages using breakpoints
        pages = []
        start = 0
        for bp in breakpoints:
            if bp > start:
                candidate_page = '\n'.join(lines[start:bp])
                if candidate_page.strip():
                    pages.append(candidate_page)
                start = bp
                
        # Add remaining content
        if start < len(lines):
            remaining = '\n'.join(lines[start:])
            if remaining.strip():
                pages.append(remaining)
                
        return pages
        
    def _smart_split(self, content: str) -> List[str]:
        """Intelligently split content based on structure"""
        lines = content.split('\n')
        pages = []
        current_page = []
        current_weighted_lines = 0
        
        for line in lines:
            # Calculate weighted line value
            line_weight = self._calculate_line_weight(line)
            
            # Check if this is a major heading (# or ##)
            is_major_heading = line.strip().startswith(('# ', '## '))
            
            # Start new page on major headings if current page has content
            if is_major_heading and current_page and current_weighted_lines > 3:
                pages.append('\n'.join(current_page))
                current_page = [line]
                current_weighted_lines = line_weight
            # Check if adding this line would exceed weighted limits
            elif current_weighted_lines + line_weight > self.max_lines_per_page:
                # Start new page
                if current_page:  # Only if we have content
                    pages.append('\n'.join(current_page))
                current_page = [line]
                current_weighted_lines = line_weight
            else:
                # Add to current page
                current_page.append(line)
                current_weighted_lines += line_weight
                
        # Don't forget the last page
        if current_page:
            pages.append('\n'.join(current_page))
            
        return pages
        
    def _calculate_line_weight(self, line: str) -> float:
        """Calculate weighted line value based on content type"""
        if not line.strip():
            return 0.1  # Empty lines take minimal space
        elif line.strip().startswith('```'):
            return 0.5  # Code block delimiters
        elif '|' in line and line.count('|') >= 2:
            return 1.3  # Table rows take more space
        elif re.match(r'!\[.*?\]\(.*?\)', line):
            return 3.0  # Images take significant space
        elif line.strip().startswith('#'):
            return 1.2  # Headings are larger
        else:
            return 1.0  # Regular content
            
    def _is_page_too_long_weighted(self, page: str) -> bool:
        """Check if a page exceeds limits using weighted line counting"""
        lines = page.split('\n')
        weighted_lines = sum(self._calculate_line_weight(line) for line in lines)
        
        # Check both weighted lines and character count
        return (weighted_lines > self.max_lines_per_page or 
                len(page) > self.max_chars_per_page)
        
    def _is_page_too_long(self, page: str) -> bool:
        """Check if a page exceeds the limits"""
        lines = page.split('\n')
        non_empty_lines = [line for line in lines if line.strip()]
        return (len(non_empty_lines) > self.max_lines_per_page or 
                len(page) > self.max_chars_per_page)
        
    def _split_long_page_smart(self, page: str) -> List[str]:
        """Split a long page into smaller chunks with smart breakpoints"""
        lines = page.split('\n')
        sub_pages = []
        current_sub = []
        current_weighted_lines = 0
        
        for i, line in enumerate(lines):
            line_weight = self._calculate_line_weight(line)
            
            # Look for good breakpoint opportunities
            is_good_breakpoint = (
                line.strip().startswith(('# ', '## ', '### ')) or  # Headers
                line.strip().startswith('```') or  # Code blocks
                (line.strip().startswith(('- ', '* ')) and i > 0 and not lines[i-1].strip()) or  # List starts
                line.strip() == '' and i > 0 and lines[i-1].strip()  # Natural paragraph breaks
            )
            
            # If we're near the limit and find a good breakpoint, split here
            if (current_weighted_lines + line_weight > self.max_lines_per_page * 0.8 and 
                is_good_breakpoint and current_sub):
                sub_pages.append('\n'.join(current_sub))
                current_sub = [line]
                current_weighted_lines = line_weight
            # Hard limit: must split even without good breakpoint
            elif current_weighted_lines + line_weight > self.max_lines_per_page:
                if current_sub:
                    sub_pages.append('\n'.join(current_sub))
                current_sub = [line]
                current_weighted_lines = line_weight
            else:
                current_sub.append(line)
                current_weighted_lines += line_weight
                
        if current_sub:
            sub_pages.append('\n'.join(current_sub))
            
        return sub_pages 