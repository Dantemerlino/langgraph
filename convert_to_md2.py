#!/usr/bin/env python3
"""
Unified converter for HTML documentation to Markdown format.
Handles both Data Mart documentation and FHIR resource documentation styles.
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


class UnifiedHTMLToMarkdownConverter:
    """Convert various HTML documentation styles to Markdown format."""
    
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
        text = text.replace('&nbsp;', ' ')
        return text
    
    def detect_document_type(self, soup: BeautifulSoup) -> str:
        """Detect if this is a Data Mart or FHIR documentation."""
        # Check for typical Data Mart sections
        if soup.find('h2', {'id': 'dataset-information'}) and soup.find('h2', {'id': 'example-query'}):
            return 'datamart'
        # Check for typical FHIR sections
        elif soup.find('h2', {'id': 'supported-attributes'}) or soup.find('h2', {'id': 'characteristics'}):
            return 'fhir'
        else:
            # Default to datamart style
            return 'datamart'
    
    def extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the main title from H1 tag."""
        h1 = soup.find('h1')
        if h1:
            return self.clean_text(h1.get_text())
        return "Documentation"
    
    def extract_description(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract the description."""
        # For FHIR docs, it's the paragraph after H1
        h1 = soup.find('h1')
        if h1:
            next_sibling = h1.find_next_sibling()
            if next_sibling and next_sibling.name == 'p':
                return self.clean_text(next_sibling.get_text())
                
        # For Data Mart docs, look for description section
        desc_section = soup.find('h2', {'id': 'description'})
        if desc_section:
            return self.extract_section(soup, 'description')
            
        return None
    
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
    
    def extract_dataset_info(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract dataset information section for Data Mart docs."""
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
    
    def extract_details_content(self, details_element) -> Dict[str, str]:
        """Extract content from a details element (FHIR docs)."""
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
                    # Handle code tags in values
                    code_tags = child.find_all('code')
                    if code_tags:
                        # Replace code tags with backticks
                        child_html = str(child)
                        for code in code_tags:
                            child_html = child_html.replace(str(code), f"`{code.get_text()}`")
                        temp_soup = BeautifulSoup(child_html, 'html.parser')
                        value = self.clean_text(temp_soup.get_text())
                    else:
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
        """Extract and format the supported attributes table (FHIR docs)."""
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
    
    def extract_section_with_code_in_list(self, soup: BeautifulSoup, section_id: str) -> Optional[str]:
        """Extract section content that includes code tags within lists (FHIR notes)."""
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
                        li_html = str(li)
                        for code in code_tags:
                            li_html = li_html.replace(str(code), f"`{code.get_text()}`")
                        # Parse the modified text
                        temp_soup = BeautifulSoup(li_html, 'html.parser')
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
            
            # Detect document type
            doc_type = self.detect_document_type(soup)
            logger.info(f"Detected document type: {doc_type}")
            
            # Extract components
            title = self.extract_title(soup)
            
            # Build Markdown content
            md_content = [f"# {title}"]
            
            if doc_type == 'fhir':
                # FHIR document processing
                description = self.extract_description(soup)
                if description:
                    md_content.append(f"\n{description}")
                
                # Extract Characteristics table
                characteristics = self.extract_section_with_table(soup, 'characteristics')
                if characteristics:
                    md_content.append("\n## Characteristics\n")
                    md_content.append(characteristics)
                
                # Extract Notes section with code formatting
                notes = self.extract_section_with_code_in_list(soup, 'notes')
                if notes:
                    md_content.append("\n## Notes\n")
                    md_content.append(notes)
                
                # Extract Supported Attributes
                supported_attrs = self.extract_supported_attributes(soup)
                if supported_attrs:
                    md_content.append("\n## Supported Attributes")
                    md_content.append(supported_attrs)
                
                # Extract Unsupported Attributes
                unsupported = self.extract_section_with_table(soup, 'unsupported-attributes')
                if unsupported:
                    md_content.append("\n## Unsupported Attributes\n")
                    md_content.append(unsupported)
                else:
                    # Check if section exists but has no table
                    section = soup.find('h2', {'id': 'unsupported-attributes'})
                    if section:
                        # Check for content after section
                        has_content = False
                        for sibling in section.find_next_siblings():
                            if sibling.name == 'h2':
                                break
                            if sibling.name and sibling.get_text().strip():
                                has_content = True
                                break
                        if not has_content:
                            md_content.append("\n## Unsupported Attributes\n")
                            md_content.append("None")
                
                # Extract Known Issues
                known_issues = self.extract_section(soup, 'known-issues')
                if known_issues:
                    md_content.append("\n## Known Issues\n")
                    md_content.append(known_issues)
                    
            else:
                # Data Mart document processing
                description = self.extract_section(soup, 'description')
                if description:
                    md_content.append("\n## Description\n")
                    md_content.append(description)
                    
                diagram = self.extract_diagram(soup)
                if diagram:
                    md_content.append("\n## Diagram\n")
                    md_content.append(diagram)
                    
                dataset_info = self.extract_dataset_info(soup)
                if dataset_info:
                    md_content.append("\n## Dataset Information\n")
                    md_content.append(dataset_info)
                    
                mapping_specs = self.extract_section(soup, 'mapping-specifications')
                if mapping_specs:
                    md_content.append("\n## Mapping Specifications\n")
                    md_content.append(mapping_specs)
                    
                example_query = self.extract_example_query(soup)
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
                        
                key_points = self.extract_section(soup, 'key-points')
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
        description="Convert HTML documentation to Markdown format (supports both Data Mart and FHIR styles)"
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
    converter = UnifiedHTMLToMarkdownConverter(args.input_dir, args.output_dir)
    successful, failed = converter.convert_all()
    
    # Print summary
    print(f"\nConversion complete!")
    print(f"Successfully converted: {successful} files")
    print(f"Failed conversions: {failed} files")
    print(f"Output directory: {args.output_dir}")


if __name__ == "__main__":
    main()