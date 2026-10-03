"""
Script to generate as_a_man_thinketh.pdf from as_a_man_thinketh.txt
Uses ReportLab to create a clean, elegant PDF book.
"""
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header
        self.drawString(54, 750, "As a Man Thinketh — James Allen")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Footer
        self.drawRightString(612 - 54, 36, f"Page {self._pageNumber} of {page_count}")
        self.drawString(54, 36, "Public Domain (Project Gutenberg)")
        self.line(54, 48, 612 - 54, 48)
        self.restoreState()

def build_book_pdf():
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    txt_path = os.path.join(data_dir, "as_a_man_thinketh.txt")
    pdf_path = os.path.join(data_dir, "as_a_man_thinketh.pdf")
    
    with open(txt_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Clean Gutenberg preamble and postamble
    start_match = re.search(r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*", content)
    if start_match:
        content = content[start_match.end():]
    end_match = re.search(r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK", content)
    if end_match:
        content = content[:end_match.start()]
    
    content = content.strip()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#1A365D"),
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=30
    )
    
    author_style = ParagraphStyle(
        'CoverAuthor',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#2B6CB0"),
        alignment=1,
        spaceAfter=40
    )
    
    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#718096"),
        alignment=1,
    )
    
    h1_style = ParagraphStyle(
        'BookHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BookBody',
        parent=styles['Normal'],
        fontName='Times-Roman',
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=10
    )

    story = []

    # Cover Page
    story.append(Spacer(1, 100))
    story.append(Paragraph("AS A MAN THINKETH", title_style))
    story.append(Paragraph("A Classic Philosophical & Mindset Essay", subtitle_style))
    story.append(Paragraph("BY JAMES ALLEN", author_style))
    story.append(HRFlowable(width="60%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=30))
    story.append(Paragraph("Published 1903 • 100% Free & Open Public Domain Document", meta_style))
    story.append(Paragraph("Complete Text for RAG Document Ingestion & Vector Search Experiments", meta_style))
    story.append(PageBreak())

    # Process paragraphs
    paragraphs = content.split("\n\n")
    for para in paragraphs:
        text = para.strip()
        if not text:
            continue
        # Escape XML special chars
        text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        
        # Check if line looks like chapter header
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        if len(lines) == 1 and (
            lines[0].isupper() or 
            lines[0].startswith("Chapter") or 
            lines[0].startswith("CHAPTER") or
            lines[0] in [
                "THOUGHT AND CHARACTER",
                "EFFECT OF THOUGHT ON CIRCUMSTANCES",
                "EFFECT OF THOUGHT ON HEALTH AND THE BODY",
                "THOUGHT AND PURPOSE",
                "THE THOUGHT-FACTOR IN ACHIEVEMENT",
                "VISIONS AND IDEALS",
                "SERENITY"
            ]
        ):
            story.append(Spacer(1, 14))
            story.append(Paragraph(lines[0], h1_style))
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
        else:
            joined = " ".join(lines)
            story.append(Paragraph(joined, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Book PDF successfully built at: {pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path) / 1024:.1f} KB")

if __name__ == "__main__":
    build_book_pdf()
