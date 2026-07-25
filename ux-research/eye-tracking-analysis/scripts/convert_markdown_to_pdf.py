#!/usr/bin/env python3
"""
Convert Markdown Report to PDF
Converts the eye-tracking analysis report from Markdown to PDF format.

Required: pip install markdown weasyprint
Alternative: pip install markdown pdfkit (requires wkhtmltopdf binary)
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import markdown
    try:
        from weasyprint import HTML, CSS
        USE_WEASYPRINT = True
        USE_XHTML2PDF = False
    except (ImportError, OSError):
        # WeasyPrint may fail on Windows due to missing system libraries
        try:
            from xhtml2pdf import pisa
            USE_WEASYPRINT = False
            USE_XHTML2PDF = True
        except ImportError:
            try:
                import pdfkit
                USE_WEASYPRINT = False
                USE_XHTML2PDF = False
            except ImportError:
                print("ERROR: No PDF library available.")
                print("Install one of:")
                print("  pip install weasyprint (may require system libraries on Windows)")
                print("  pip install xhtml2pdf (recommended for Windows)")
                print("  pip install pdfkit (requires wkhtmltopdf binary)")
                sys.exit(1)
except ImportError:
    print("ERROR: markdown library not installed.")
    print("Install with: pip install markdown")
    sys.exit(1)


def convert_md_to_pdf(md_file: str, pdf_file: str = None, css_file: str = None) -> bool:
    """
    Convert markdown file to PDF.

    Args:
        md_file: Path to markdown file
        pdf_file: Output PDF path (default: same name with .pdf extension)
        css_file: Optional CSS file for styling

    Returns:
        True if successful, False otherwise
    """
    if not os.path.exists(md_file):
        print(f"ERROR: Markdown file not found: {md_file}")
        return False

    if pdf_file is None:
        pdf_file = os.path.splitext(md_file)[0] + '.pdf'

    try:
        # Read markdown file
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'tables'])
        html_content = md.convert(md_content)

        # Resolve image paths relative to markdown file location
        md_dir = os.path.dirname(os.path.abspath(md_file))
        import re
        # Find all image references in HTML (both <img> tags and markdown image syntax)
        def resolve_image_path(match):
            img_path = match.group(1)
            # If path is relative, resolve it relative to markdown file location
            if not os.path.isabs(img_path):
                # Resolve relative path
                resolved_path = os.path.normpath(os.path.join(md_dir, img_path))
                # Check if file exists
                if os.path.exists(resolved_path):
                    # Convert to absolute path with forward slashes for HTML
                    resolved_path = os.path.abspath(resolved_path).replace('\\', '/')
                    return match.group(0).replace(img_path, resolved_path)
            return match.group(0)

        # Replace image src paths in <img> tags
        html_content = re.sub(r'<img[^>]+src=["\']([^"\']+)["\']', resolve_image_path, html_content)

        # Add basic styling if no CSS provided
        if css_file and os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                css_content = f.read()
        else:
            # Default CSS for professional report styling
            css_content = """
            @page {
                size: A4;
                margin: 2cm;
            }
            body {
                font-family: 'Arial', 'Helvetica', 'Segoe UI', sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 800px;
                margin: 0 auto;
                font-size: 11pt;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
                border-bottom: 2px solid #ecf0f1;
                padding-bottom: 5px;
            }
            h3 {
                color: #7f8c8d;
                margin-top: 20px;
            }
            code {
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
            }
            pre {
                background-color: #f4f4f4;
                padding: 15px;
                border-radius: 5px;
                overflow-x: auto;
            }
            table {
                border-collapse: collapse;
                width: 100%;
                margin: 20px 0;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #3498db;
                color: white;
            }
            img {
                display: block;
                max-width: 100%;
                height: auto;
                margin: 20px auto;
            }
            ul, ol {
                margin: 15px 0;
                padding-left: 30px;
            }
            li {
                margin: 8px 0;
            }
            strong {
                color: #2c3e50;
            }
            """

        # Wrap HTML with proper structure
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
            {css_content}
            </style>
        </head>
        <body>
        {html_content}
        </body>
        </html>
        """

        # Save HTML file as well
        html_file = os.path.splitext(pdf_file)[0] + '.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(full_html)
        print(f"HTML report saved to: {os.path.abspath(html_file)}")

        # Convert HTML to PDF
        if USE_WEASYPRINT:
            HTML(string=full_html).write_pdf(pdf_file)
        elif USE_XHTML2PDF:
            # Using xhtml2pdf (pure Python, works on Windows)
            # Define link callback to handle local image paths
            def link_callback(uri, rel):
                # Convert file:// URLs to local paths
                if uri.startswith('file:///'):
                    uri = uri[8:]  # Remove file:/// prefix
                elif uri.startswith('file://'):
                    uri = uri[7:]  # Remove file:// prefix
                # Convert forward slashes to backslashes on Windows for file access
                if os.name == 'nt' and not os.path.isabs(uri):
                    uri = uri.replace('/', '\\')
                return uri

            with open(pdf_file, 'wb') as pdf:
                pisa_status = pisa.CreatePDF(
                    full_html,
                    dest=pdf,
                    link_callback=link_callback
                )
            if pisa_status.err:
                raise Exception(f"xhtml2pdf error: {pisa_status.err}")
        else:
            # Using pdfkit (requires wkhtmltopdf)
            options = {
                'page-size': 'A4',
                'margin-top': '2cm',
                'margin-right': '2cm',
                'margin-bottom': '2cm',
                'margin-left': '2cm',
                'encoding': "UTF-8",
                'no-outline': None
            }
            pdfkit.from_string(full_html, pdf_file, options=options)

        print(f"PDF generated successfully: {os.path.abspath(pdf_file)}")
        return True

    except Exception as e:
        print(f"ERROR: Failed to convert markdown to PDF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown report to PDF'
    )
    parser.add_argument('md_file', help='Path to markdown file')
    parser.add_argument('--output', '-o', help='Output PDF path (default: same name with .pdf extension)')
    parser.add_argument('--css', help='Optional CSS file for custom styling')

    args = parser.parse_args()

    success = convert_md_to_pdf(args.md_file, args.output, args.css)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
