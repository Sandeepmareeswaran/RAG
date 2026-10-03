"""
Professional PDF Generator for RAG_Complete_Beginner_Guide.md
Converts the complete RAG guide into an publication-quality PDF manual.
"""
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether, 
    HRFlowable, Table, TableStyle, Preformatted
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
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header
        self.drawString(54, 750, "Complete RAG Architecture Guide for Beginners — LangChain & Ollama")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 742, 612 - 54, 742)
        
        # Footer
        self.drawRightString(612 - 54, 36, f"Page {self._pageNumber} of {page_count}")
        self.drawString(54, 36, "Open Source AI & RAG Practical Guide")
        self.line(54, 48, 612 - 54, 48)
        self.restoreState()


def clean_inline_markdown(text):
    """Convert common inline markdown to ReportLab HTML tags."""
    # Escape HTML special chars first, except if already part of tags
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    # Bold: **text** or __text__
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)
    
    # Italic: *text* or _text_
    text = re.sub(r'(?<!\*)\*(?!\*)(.*?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
    text = re.sub(r'(?<!_)_(?!_)(.*?)(?<!_)_(?!_)', r'<i>\1</i>', text)
    
    # Inline code: `code`
    text = re.sub(r'`(.*?)`', r'<font name="Courier" color="#805AD5"><b>\1</b></font>', text)
    
    # Links: [text](url) -> text (url)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<u>\1</u>', text)
    
    return text


def build_guide_pdf():
    guides_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "guides"))
    md_path = os.path.join(guides_dir, "RAG_Complete_Beginner_Guide.md")
    pdf_path = os.path.join(guides_dir, "RAG_Complete_Beginner_Guide.pdf")

    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Define custom typography styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=colors.HexColor("#1A365D"),
        alignment=1,
        spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#4A5568"),
        alignment=1,
        spaceAfter=25
    )

    meta_style = ParagraphStyle(
        'CoverMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=16,
        textColor=colors.HexColor("#718096"),
        alignment=1,
    )

    h1_style = ParagraphStyle(
        'GuideH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=22,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=18,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'GuideH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'GuideH3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#2C5282"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'GuideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'GuideBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    quote_style = ParagraphStyle(
        'GuideQuote',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#2C5282"),
        leftIndent=16,
        spaceBefore=6,
        spaceAfter=8
    )

    code_style = ParagraphStyle(
        'GuideCode',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.8,
        leading=10.5,
        textColor=colors.HexColor("#1A202C")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#2D3748")
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.white
    )

    story = []

    # Cover Page
    story.append(Spacer(1, 60))
    story.append(Paragraph("COMPLETE RAG ARCHITECTURE GUIDE FOR BEGINNERS", title_style))
    story.append(Paragraph("Retrieval-Augmented Generation — From Fundamentals to Practical Implementation", subtitle_style))
    story.append(HRFlowable(width="80%", thickness=2, color=colors.HexColor("#3182CE"), spaceAfter=25))
    
    story.append(Paragraph("<b>Author:</b> RAG Learning Project &nbsp;|&nbsp; <b>Level:</b> Absolute Beginner → Intermediate", meta_style))
    story.append(Paragraph("<b>Technology Stack:</b> LangChain 1.x • Ollama • ChromaDB • Python 3.10+", meta_style))
    story.append(Paragraph("<b>Covers:</b> Document Ingestion • Chunking • Embeddings • Vector Stores • Semantic Retrieval • LLM Prompt Chains", meta_style))
    story.append(Spacer(1, 30))

    # Box with Summary
    summary_box_data = [[
        Paragraph(
            "<b>🎯 What this Guide Gives You:</b><br/>"
            "This comprehensive manual demystifies RAG step-by-step. "
            "You will understand why traditional LLMs hallucinate, how chunking preserves semantic meaning, "
            "how mathematical embedding vectors represent concepts, how ChromaDB executes similarity search, "
            "and how LangChain coordinates the full retrieval pipeline with local open-source models using Ollama.",
            body_style
        )
    ]]
    summary_table = Table(summary_box_data, colWidths=[500])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EBF8FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#3182CE")),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(summary_table)
    story.append(PageBreak())

    # Split lines and parse blocks
    lines = md_content.splitlines()
    i = 0
    total_lines = len(lines)

    in_code_block = False
    code_lines = []
    
    while i < total_lines:
        line = lines[i]

        # Handle fenced code block
        if line.strip().startswith("```"):
            if not in_code_block:
                in_code_block = True
                code_lines = []
            else:
                in_code_block = False
                code_text = "\n".join(code_lines)
                # Render code box
                code_cell = [[Preformatted(code_text, code_style)]]
                t = Table(code_cell, colWidths=[500])
                t.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
                    ('BOX', (0,0), (-1,-1), 0.75, colors.HexColor("#CBD5E0")),
                    ('TOPPADDING', (0,0), (-1,-1), 6),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                    ('LEFTPADDING', (0,0), (-1,-1), 8),
                    ('RIGHTPADDING', (0,0), (-1,-1), 8),
                ]))
                story.append(Spacer(1, 4))
                story.append(t)
                story.append(Spacer(1, 6))
            i += 1
            continue

        if in_code_block:
            code_lines.append(line)
            i += 1
            continue

        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            i += 1
            continue

        # Skip main document title if at beginning (already on cover)
        if stripped.startswith("# 📚 Complete RAG Architecture") or stripped.startswith("### Retrieval-Augmented Generation"):
            i += 1
            continue

        # Horizontal rule
        if stripped in ["---", "***", "___"]:
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E2E8F0"), spaceBefore=8, spaceAfter=8))
            i += 1
            continue

        # Headings
        if stripped.startswith("# "):
            text = clean_inline_markdown(stripped[2:])
            story.append(Paragraph(text, h1_style))
            i += 1
            continue
        elif stripped.startswith("## "):
            text = clean_inline_markdown(stripped[3:])
            story.append(Paragraph(text, h1_style))
            i += 1
            continue
        elif stripped.startswith("### "):
            text = clean_inline_markdown(stripped[4:])
            story.append(Paragraph(text, h2_style))
            i += 1
            continue
        elif stripped.startswith("#### "):
            text = clean_inline_markdown(stripped[5:])
            story.append(Paragraph(text, h3_style))
            i += 1
            continue

        # Blockquote
        if stripped.startswith(">"):
            quote_text = clean_inline_markdown(stripped.lstrip("> "))
            # Wrap in styled box
            quote_cell = [[Paragraph(quote_text, quote_style)]]
            t = Table(quote_cell, colWidths=[500])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FFF4") if "Tip" in quote_text or "TIP" in quote_text else colors.HexColor("#EDF2F7")),
                ('LINEBEFORE', (0,0), (0,-1), 3, colors.HexColor("#38A169") if "Tip" in quote_text or "TIP" in quote_text else colors.HexColor("#3182CE")),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            story.append(t)
            story.append(Spacer(1, 4))
            i += 1
            continue

        # Table detection
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines = []
            while i < total_lines and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            
            # Parse table lines
            if len(table_lines) >= 2:
                # Row 0: Headers
                headers = [clean_inline_markdown(c.strip()) for c in table_lines[0].strip("|").split("|")]
                # Row 1 is divider (|---|---|)
                content_rows = []
                for row_line in table_lines[2:]:
                    cols = [clean_inline_markdown(c.strip()) for c in row_line.strip("|").split("|")]
                    content_rows.append(cols)

                col_count = len(headers)
                col_width = 500 / col_count

                table_data = [[Paragraph(f"<b>{h}</b>", table_header_style) for h in headers]]
                for r in content_rows:
                    row_cells = []
                    for c_idx in range(col_count):
                        val = r[c_idx] if c_idx < len(r) else ""
                        row_cells.append(Paragraph(val, table_cell_style))
                    table_data.append(row_cells)

                grid_table = Table(table_data, colWidths=[col_width]*col_count)
                grid_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
                    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                    ('TOPPADDING', (0,0), (-1,-1), 4),
                    ('LEFTPADDING', (0,0), (-1,-1), 6),
                    ('RIGHTPADDING', (0,0), (-1,-1), 6),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
                    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
                ]))
                story.append(Spacer(1, 4))
                story.append(grid_table)
                story.append(Spacer(1, 6))
            continue

        # Bullet list item
        if stripped.startswith("- ") or stripped.startswith("* "):
            bullet_text = clean_inline_markdown("• " + stripped[2:])
            story.append(Paragraph(bullet_text, bullet_style))
            i += 1
            continue

        # Numbered list item
        num_match = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if num_match:
            num = num_match.group(1)
            item_text = clean_inline_markdown(f"<b>{num}.</b> " + num_match.group(2))
            story.append(Paragraph(item_text, bullet_style))
            i += 1
            continue

        # Regular paragraph
        clean_text = clean_inline_markdown(stripped)
        story.append(Paragraph(clean_text, body_style))
        i += 1

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Guide PDF successfully built at: {pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path) / 1024:.1f} KB")

if __name__ == "__main__":
    build_guide_pdf()
