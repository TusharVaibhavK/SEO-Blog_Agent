#!/usr/bin/env python3
from fpdf import FPDF
import os

class PDFGenerator(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Callus SEO Keyword Research AI Agent - Project Plan', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
    
    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
    
    def chapter_body(self, body):
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 6, body)
        self.ln()

def main():
    pdf = PDFGenerator()
    pdf.add_page()
    
    # Read the markdown content
    with open('1page_plan.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into sections
    sections = content.split('## ')
    
    for section in sections[1:]:  # Skip first empty split
        if section.strip():
            lines = section.split('\n', 1)
            title = lines[0].strip()
            body = lines[1].strip() if len(lines) > 1 else ""
            
            pdf.chapter_title(title)
            pdf.chapter_body(body)
            pdf.ln(5)
    
    # Save PDF
    pdf.output('1page_plan.pdf')
    print("✅ PDF generated: docs/1page_plan.pdf")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()