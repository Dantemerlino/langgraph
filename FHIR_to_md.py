#!/usr/bin/env python3
"""
Convert FHIR HTML documentation pages to Markdown format.
This script processes HTML files with FHIR resource documentation structure
including complex nested tables and expandable details sections.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString
import logging
from typing import Dict, List, Optional, Tuple
import argparse
import html

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FHIRHTMLToMarkdownConverter:
    """Convert FHIR HTML documentation to Markdown format."""
    
    def __init__(self, input_dir: str, output_dir: str):
        """
        Initialize converter with input and output directories.
        
        Args:
            input_dir: Directory containing HTML files
            output_dir: Directory where Markdown files will be saved
        """
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove any remaining HTML entities
        text = html.unescape(text)
        return text
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the main title from H1 tag."""
        h1 = soup.find('h1')
        if h1:
            return self.clean_text(h1.get_text())
        return "FHIR Resource Documentation"
    
    def extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the description paragraph after H1."""
        h1 = soup.find('h1')
        if h1:
            # Get the next sibling that's a paragraph
            next_sibling = h1.find_next_sibling()
            if next_sibling and next_sibling.name == 'p':
                return self.clean_text(next_sibling.get_text())
        return None
    
    def extract_section_content(self, soup: BeautifulSoup, section_id: str) -> Optional[str]:
        """Extract content from a specific section by ID."""
        section = soup.find('h2', {'id': section_id})
        if not section:
            return None
            
        content = []
        
        # Get all siblings until the next h2
        for sibling in section.find_next_siblings():
            if sibling.name == 'h2':
                break
                
            if sibling.name == 'p':
                text = self.clean_text(sibling.get_text())
                if text:
                    content.append(text)
            elif sibling.name == 'ul':
                # Process list items
                for li in sibling.find_all('li'):
                    # Check if it contains code tags
                    code_tags = li.find_all('code')
                    if code_tags:
                        # Replace code tags with backticks in the text
                        li_text = str(li)
                        for code in code_tags:
                            li_text = li_text.replace(str(code), f"`{code.get_text()}`")
                        # Parse the modified text
                        temp_soup = BeautifulSoup(li_text, 'html.parser')
                        text = self.clean_text(temp_soup.get_text())
                    else:
                        # Check for links
                        link = li.find('a')
                        if link and link.get('href'):
                            link_text = self.clean_text(link.get_text())
                            link_url = link.get('href')
                            text = f"[{link_text}]({link_url})"
                        else:
                            text = self.clean_text(li.get_text())
                    
                    if text:
                        content.append(f"- {text}")
                        
        return '\n'.join(content) if content else None
    
    def extract_table(self, table_element) -> Optional[str]:
        """Convert HTML table to Markdown table."""
        if not table_element:
            return None
            
        rows = []
        
        # Extract headers
        thead = table_element.find('thead')
        if thead:
            header_row = thead.find('tr')
            if header_row:
                headers = []
                for th in header_row.find_all('th'):
                    headers.append(self.clean_text(th.get_text()))
                if headers:
                    rows.append('| ' + ' | '.join(headers) + ' |')
                    rows.append('|' + '|'.join(['---' for _ in headers]) + '|')
        
        # Extract body rows
        tbody = table_element.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                cells = []
                for td in tr.find_all('td'):
                    # Check for links in cells
                    link = td.find('a')
                    if link and link.get('href'):
                        link_text = self.clean_text(link.get_text())
                        link_url = link.get('href')
                        cells.append(f"[{link_text}]({link_url})")
                    else:
                        cells.append(self.clean_text(td.get_text()))
                if cells:
                    rows.append('| ' + ' | '.join(cells) + ' |')
                    
        return '\n'.join(rows) if rows else None
    
    def extract_details_content(self, details_element) -> Dict[str, str]:
        """Extract content from a details element."""
        result = {}
        
        # Get the summary (attribute name)
        summary = details_element.find('summary')
        if summary:
            result['name'] = self.clean_text(summary.get_text())
        
        # Extract the definition list content
        dl = details_element.find('dl')
        if dl:
            current_key = None
            for child in dl.children:
                if child.name == 'dt':
                    current_key = self.clean_text(child.get_text())
                elif child.name == 'dd' and current_key:
                    value = self.clean_text(child.get_text())
                    if current_key in result:
                        # Handle multiple values for same key
                        if isinstance(result[current_key], list):
                            result[current_key].append(value)
                        else:
                            result[current_key] = [result[current_key], value]
                    else:
                        result[current_key] = value
                        
        return result
    
    def extract_supported_attributes(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract and format the supported attributes table."""
        section = soup.find('h2', {'id': 'supported-attributes'})
        if not section:
            return None
            
        content = []
        
        # Find the table
        table = None
        for sibling in section.find_next_siblings():
            if sibling.name == 'h2':
                break
            if sibling.name == 'table':
                table = sibling
                break
                
        if not table:
            return None
            
        # Process the complex table structure
        tbody = table.find('tbody')
        if tbody:
            for tr in tbody.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    # First td contains the attribute details
                    details = tds[0].find('details')
                    cardinality = self.clean_text(tds[1].get_text())
                    
                    if details:
                        attr_info = self.extract_details_content(details)
                        
                        # Format the attribute entry
                        if 'name' in attr_info:
                            content.append(f"\n### {attr_info['name']}")
                            content.append(f"**Cardinality:** {cardinality}\n")
                            
                            # Add other details
                            for key, value in attr_info.items():
                                if key != 'name':
                                    if isinstance(value, list):
                                        content.append(f"- **{key}:**")
                                        for v in value:
                                            content.append(f"  - {v}")
                                    else:
                                        content.append(f"- **{key}:** {value}")
                    else:
                        # Simple attribute without details
                        attr_name = self.clean_text(tds[0].get_text())
                        if attr_name:
                            content.append(f"\n### {attr_name}")
                            content.append(f"**Cardinality:** {cardinality}")
                            
        return '\n'.join(content) if content else None
    
    def extract_section_with_table(self, soup: BeautifulSoup, section_id: str) -> Optional[str]:
        """Extract a section that contains a table."""
        section = soup.find('h2', {'id': section_id})
        if not section:
            return None
            
        # Find the next table after this section
        table = None
        for sibling in section.find_next_siblings():
            if sibling.name == 'h2':
                break
            if sibling.name == 'table':
                table = sibling
                break
                
        if table:
            return self.extract_table(table)
        return None
    
    def convert_file(self, html_file: Path) -> bool:
        """
        Convert a single HTML file to Markdown.
        
        Args:
            html_file: Path to the HTML file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Processing: {html_file.name}")
            
            # Read HTML content
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
                
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract components
            title = self.extract_title(soup)
            description = self.extract_description(soup)
            
            # Build Markdown content
            md_content = [f"# {title}"]
            
            if description:
                md_content.append(f"\n{description}")
            
            # Extract Characteristics table
            characteristics = self.extract_section_with_table(soup, 'characteristics')
            if characteristics:
                md_content.append("\n## Characteristics\n")
                md_content.append(characteristics)
            
            # Extract Notes section
            notes = self.extract_section_content(soup, 'notes')
            if notes:
                md_content.append("\n## Notes\n")
                md_content.append(notes)
            
            # Extract Supported Attributes
            supported_attrs = self.extract_supported_attributes(soup)
            if supported_attrs:
                md_content.append("\n## Supported Attributes")
                md_content.append(supported_attrs)
            
            # Extract Unsupported Attributes table
            unsupported = self.extract_section_with_table(soup, 'unsupported-attributes')
            if unsupported:
                md_content.append("\n## Unsupported Attributes\n")
                md_content.append(unsupported)
            else:
                # Check if there's just a section with no table
                section = soup.find('h2', {'id': 'unsupported-attributes'})
                if section:
                    md_content.append("\n## Unsupported Attributes\n")
                    md_content.append("None")
            
            # Extract Known Issues
            known_issues = self.extract_section_content(soup, 'known-issues')
            if known_issues:
                md_content.append("\n## Known Issues\n")
                md_content.append(known_issues)
            
            # Check for other sections (like Example Query, Dataset Information)
            # These might exist in some FHIR docs
            dataset_info = self.extract_section_content(soup, 'dataset-information')
            if dataset_info:
                md_content.append("\n## Dataset Information\n")
                md_content.append(dataset_info)
                
            # Write Markdown file
            output_file = self.output_dir / f"{html_file.stem}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(md_content))
                
            logger.info(f"Successfully converted: {html_file.name} -> {output_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing {html_file.name}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def convert_all(self) -> Tuple[int, int]:
        """
        Convert all HTML files in the input directory.
        
        Returns:
            Tuple of (successful_count, failed_count)
        """
        html_files = list(self.input_dir.glob('*.html'))
        
        if not html_files:
            logger.warning(f"No HTML files found in {self.input_dir}")
            return 0, 0
            
        logger.info(f"Found {len(html_files)} HTML files to process")
        
        successful = 0
        failed = 0
        
        for html_file in html_files:
            if self.convert_file(html_file):
                successful += 1
            else:
                failed += 1
                
        return successful, failed


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Convert FHIR HTML documentation to Markdown format"
    )
    parser.add_argument(
        'input_dir',
        help='Directory containing HTML files'
    )
    parser.add_argument(
        'output_dir',
        help='Directory where Markdown files will be saved'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create converter and process files
    converter = FHIRHTMLToMarkdownConverter(args.input_dir, args.output_dir)
    successful, failed = converter.convert_all()
    
    # Print summary
    print(f"\nConversion complete!")
    print(f"Successfully converted: {successful} files")
    print(f"Failed conversions: {failed} files")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()