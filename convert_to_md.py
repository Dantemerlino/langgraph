#!/usr/bin/env python3
"""
Convert HTML documentation pages to Markdown format for Data Mart documentation.
This script processes HTML files with a specific structure and extracts key information
including descriptions, dataset info, mapping specifications, and example queries.
"""

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup
import logging
from typing import Dict, List, Optional, Tuple
import argparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HTMLToMarkdownConverter:
    """Convert HTML documentation to Markdown format."""
    
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
        text = text.replace('&nbsp;', ' ')
        return text
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the main title from H1 tag."""
        h1 = soup.find('h1')
        if h1:
            return self.clean_text(h1.get_text())
        return "Data Mart Documentation"
    
    def extract_section(self, soup: BeautifulSoup, section_id: str) -> Optional[str]:
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
                content.append(self.clean_text(sibling.get_text()))
            elif sibling.name == 'ul':
                # Process list items
                for li in sibling.find_all('li'):
                    # Check if it's a link
                    link = li.find('a')
                    if link and link.get('href'):
                        link_text = self.clean_text(link.get_text())
                        link_url = link.get('href')
                        content.append(f"- [{link_text}]({link_url})")
                    else:
                        # Process as regular list item
                        text = self.clean_text(li.get_text())
                        if text:
                            # Check for nested structure (e.g., "User Access | Service Account Access")
                            if '|' in text:
                                parts = text.split('|')
                                formatted_parts = []
                                # Try to find links for each part
                                links = li.find_all('a')
                                for i, part in enumerate(parts):
                                    part = part.strip()
                                    if i < len(links):
                                        href = links[i].get('href', '')
                                        formatted_parts.append(f"[{part}]({href})")
                                    else:
                                        formatted_parts.append(part)
                                content.append(f"  - {' | '.join(formatted_parts)}")
                            else:
                                content.append(f"- {text}")
                                
        return '\n'.join(content) if content else None
    
    def extract_dataset_info(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract dataset information section."""
        section = soup.find('h2', {'id': 'dataset-information'})
        if not section:
            return None
            
        content = []
        
        # Process the content after the h2
        for sibling in section.find_next_siblings():
            if sibling.name == 'h2':
                break
                
            if sibling.name == 'ul':
                for li in sibling.find_all('li', recursive=False):
                    # Extract main text
                    strong = li.find('strong')
                    if strong:
                        label = self.clean_text(strong.get_text())
                        # Get the text after the strong tag
                        code = li.find('code')
                        if code:
                            value = code.get_text()
                            content.append(f"- **{label}** `{value}`")
                        else:
                            # Get remaining text
                            text = li.get_text().replace(label, '', 1).strip()
                            content.append(f"- **{label}** {text}")
                    
                    # Check for nested lists
                    nested_ul = li.find('ul')
                    if nested_ul:
                        for nested_li in nested_ul.find_all('li'):
                            links = nested_li.find_all('a')
                            if links:
                                link_strs = []
                                for link in links:
                                    link_text = self.clean_text(link.get_text())
                                    link_url = link.get('href', '')
                                    link_strs.append(f"[{link_text}]({link_url})")
                                content.append(f"  - {' | '.join(link_strs)}")
                                
            elif sibling.name == 'p':
                text = self.clean_text(sibling.get_text())
                if text:
                    # Parse key-value pairs separated by line breaks
                    parts = text.split('Update Frequency:')
                    if len(parts) > 1:
                        # First part contains other info
                        first_part = parts[0].strip()
                        if 'Former DB2 Database' in first_part:
                            db_match = re.search(r'Former DB2 Database[:\s]+(\w+)', first_part)
                            if db_match:
                                content.append(f"\n**Former DB2 Database:** {db_match.group(1)}")
                        
                        # Second part contains update frequency
                        update_freq = parts[1].split('Support Group:')[0].strip()
                        content.append(f"**Update Frequency:** {update_freq}")
                        
                        # Support group
                        if 'Support Group:' in text:
                            support = text.split('Support Group:')[1].strip()
                            content.append(f"**Support Group:** {support}")
                            
        return '\n'.join(content) if content else None
    
    def extract_diagram(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract diagram section with image and link."""
        section = soup.find('h2', {'id': 'diagram'})
        if not section:
            return None
            
        content = []
        
        # Look for the image link
        for sibling in section.find_next_siblings():
            if sibling.name == 'h2':
                break
                
            if sibling.name == 'p':
                link = sibling.find('a')
                if link:
                    img = link.find('img')
                    if img:
                        alt_text = img.get('alt', 'Data Model')
                        img_src = img.get('src', '')
                        link_href = link.get('href', '')
                        
                        # Create markdown image with link
                        content.append(f"[![{alt_text}]({img_src})]({link_href})")
                        
        return '\n'.join(content) if content else None
    
    def extract_example_query(self, soup: BeautifulSoup) -> Optional[Dict[str, str]]:
        """Extract example query section including indexed columns and sample queries."""
        # Try both singular and plural forms
        section = soup.find('h2', {'id': 'example-query'})
        if not section:
            section = soup.find('h2', {'id': 'example-queries'})
        if not section:
            return None
            
        result = {
            'indexed_columns': [],
            'content_blocks': []  # Store all content in order
        }
        
        # Process content after h2
        for sibling in section.find_next_siblings():
            if sibling.name == 'h2':
                break
                
            if sibling.name == 'p':
                text = self.clean_text(sibling.get_text())
                if 'Fact Table Indexed Columns' in text:
                    result['indexed_columns_intro'] = text
                elif text:
                    result['content_blocks'].append({
                        'type': 'text',
                        'content': text
                    })
                    
            elif sibling.name == 'ul':
                # These are the indexed columns
                columns = []
                for li in sibling.find_all('li'):
                    column = self.clean_text(li.get_text())
                    if column:
                        columns.append(f"- `{column}`")
                if columns:
                    result['indexed_columns'] = columns
                        
            elif 'codeBlockContainer' in sibling.get('class', []):
                # Extract the SQL code
                code_block = sibling.find('code')
                if code_block:
                    # Get all the text from span elements
                    code_lines = []
                    for span in code_block.find_all('span', class_='token-line'):
                        line_text = span.get_text()
                        if line_text:
                            code_lines.append(line_text)
                    
                    if code_lines:
                        result['content_blocks'].append({
                            'type': 'code',
                            'content': '\n'.join(code_lines)
                        })
                    
        return result if result['indexed_columns'] or result['content_blocks'] else None
    
    def extract_key_points(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract key points if present (some docs might have this section)."""
        section = soup.find('h2', {'id': 'key-points'})
        if not section:
            return None
            
        content = []
        
        for sibling in section.find_next_siblings():
            if sibling.name == 'h2':
                break
                
            if sibling.name == 'ul':
                for li in sibling.find_all('li'):
                    text = self.clean_text(li.get_text())
                    if text:
                        content.append(f"- {text}")
                        
        return '\n'.join(content) if content else None
    
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
            description = self.extract_section(soup, 'description')
            diagram = self.extract_diagram(soup)
            dataset_info = self.extract_dataset_info(soup)
            mapping_specs = self.extract_section(soup, 'mapping-specifications')
            example_query = self.extract_example_query(soup)
            key_points = self.extract_key_points(soup)
            
            # Build Markdown content
            md_content = [f"# {title}"]
            
            if description:
                md_content.append("\n## Description\n")
                md_content.append(description)
                
            if diagram:
                md_content.append("\n## Diagram\n")
                md_content.append(diagram)
                
            if dataset_info:
                md_content.append("\n## Dataset Information\n")
                md_content.append(dataset_info)
                
            if mapping_specs:
                md_content.append("\n## Mapping Specifications\n")
                md_content.append(mapping_specs)
                
            if example_query:
                # Count code blocks to determine title
                code_blocks = [block for block in example_query.get('content_blocks', []) if block['type'] == 'code']
                if len(code_blocks) > 1:
                    md_content.append("\n## Example Queries")
                else:
                    md_content.append("\n## Example Query")
                
                if example_query.get('indexed_columns_intro'):
                    md_content.append(f"\n### Fact Table Indexed Columns\n")
                    md_content.append("**Note:** Subject to changes. Please use the following column(s) in your query filter for faster and more efficient data retrieval.\n")
                    
                if example_query.get('indexed_columns'):
                    md_content.append('\n'.join(example_query['indexed_columns']))
                    
                # Process content blocks in order
                query_count = 0
                for block in example_query.get('content_blocks', []):
                    if block['type'] == 'text':
                        md_content.append(f"\n{block['content']}\n")
                    elif block['type'] == 'code':
                        query_count += 1
                        if len(code_blocks) > 1:
                            md_content.append(f"\n### Sample Query {query_count}\n")
                        else:
                            md_content.append("\n### Sample Query\n")
                        
                        # Add intro text for first query if not already present
                        if query_count == 1 and not any('Sample Query:' in b.get('content', '') for b in example_query.get('content_blocks', []) if b['type'] == 'text'):
                            md_content.append("This is a sample query to get you started. Query you need for your use case may be different than this sample.\n")
                            
                        md_content.append("```sql")
                        md_content.append(block['content'])
                        md_content.append("```")
                    
            if key_points:
                md_content.append("\n## Key Points\n")
                md_content.append(key_points)
                
            # Write Markdown file
            output_file = self.output_dir / f"{html_file.stem}.md"
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(md_content))
                
            logger.info(f"Successfully converted: {html_file.name} -> {output_file.name}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing {html_file.name}: {str(e)}")
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
        description="Convert HTML documentation to Markdown format"
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
    converter = HTMLToMarkdownConverter(args.input_dir, args.output_dir)
    successful, failed = converter.convert_all()
    
    # Print summary
    print(f"\nConversion complete!")
    print(f"Successfully converted: {successful} files")
    print(f"Failed conversions: {failed} files")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()