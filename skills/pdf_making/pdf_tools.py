#!/usr/bin/env python3
"""
PDF Skill Implementation Module
Handles PDF creation from various formats using available tools and libraries.
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
from typing import Union, List, Optional

# Paths
WORKSPACE = Path("/home/wherd/.openclaw/workspace")
SKILL_DIR = WORKSPACE / "skills" / "pdf_making"

def check_dependencies():
    """Check if PDF tools are installed."""
    tools = []
    
    # ReportLab
    try:
        from reportlab.lib.pagesizes import letter
        tools.append("reportlab")
    except ImportError:
        pass
    
    # FPDF2
    try:
        from fpdf import FPDF
        tools.append("fpdf2")
    except ImportError:
        pass
    
    # Pandoc
    try:
        subprocess.run(["pandoc", "--version"], capture_output=True, timeout=5)
        tools.append("pandoc")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # wkhtmltopdf
    try:
        subprocess.run(["wkhtmltopdf", "--version"], capture_output=True, timeout=5)
        tools.append("wkhtmltopdf")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print(f"Available PDF tools: {', '.join(tools)}")
    return tools

def markdown_to_pdf(md_path: str, pdf_path: str, options: Optional[dict] = None):
    """Convert Markdown file to PDF using pandoc or wkhtmltopdf."""
    if not check_dependencies():
        return False, "No PDF conversion tools available"
    
    tools = check_dependencies()
    
    # Use pandoc if available
    if "pandoc" in tools:
        try:
            cmd = ["pandoc", md_path, "-o", pdf_path, "--pdf-engine=xelatex"]
            subprocess.run(cmd, check=True, capture_output=True)
            return True, "PDF created with pandoc"
        except subprocess.CalledProcessError as e:
            return False, f"Failed: {e.stderr.decode()}"
    
    # Fallback to wkhtmltopdf
    if "wkhtmltopdf" in tools:
        try:
            cmd = ["wkhtmltopdf", str(Path(md_path)), pdf_path]
            subprocess.run(cmd, check=True, capture_output=True)
            return True, "PDF created with wkhtmltopdf"
        except subprocess.CalledProcessError as e:
            return False, f"Failed: {e.stderr.decode()}"
    
    return False, "No viable PDF converter found"

def text_to_pdf(text: str, filename: str, style: str = "simple"):
    """Create a PDF from plain text."""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        title = Paragraph("PDF Created by OpenClaw", styles["Title"])
        story.append(title)
        story.append(Spacer(1, 12))
        
        for line in text.split('\n'):
            if line.strip():
                story.append(Paragraph(line, styles["Normal"]))
                story.append(Spacer(1, 6))
        
        doc.build(story)
        return True, f"PDF created: {filename}"
    except ImportError as e:
        return False, f"ReportLab not available: {e}"

def html_to_pdf(html_content: str, filename: str):
    """Convert HTML to PDF."""
    try:
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib.pagesizes import letter
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # HTML parser could go here
        # For simplicity, treat as plain text in paragraphs
        lines = html_content.split('\n')
        for line in lines[:50]:  # Limit lines
            if '<p>' in line:
                line = line.replace('<p>', '').replace('</p>', '')
            if '<br>' in line:
                line = line.replace('<br>', '')
            story.append(Paragraph(line, styles["Normal"]))
            story.append(Spacer(1, 6))
        
        doc.build(story)
        return True, f"PDF created: {filename}"
    except Exception as e:
        return False, f"Failed: {str(e)}"

def image_to_pdf(image_path: str, filename: str):
    """Create PDF from image."""
    try:
        from reportlab.platypus import SimpleDocTemplate, Image
        from reportlab.lib.pagesizes import letter
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        img = Image(image_path, width=letter[0]-40, height=letter[1]*1.5)
        doc.build([img])
        return True, f"PDF created: {filename}"
    except Exception as e:
        return False, f"Failed: {str(e)}"

def merge_pdfs(files: List[str], output: str):
    """Merge multiple PDF files into one."""
    try:
        if "gs" in subprocess.run(["gs", "--version"], capture_output=True, timeout=5).stdout.decode():
            # Ghostscript method
            cmd = ["gs", "-o", output]
            for f in files:
                cmd.extend(["-dBATCH", "-dNOPAUSE", "-q", f])
            # Add blank page between documents
            cmd.extend(["-sDEVICE=pdfwrite", "-sOutputFile=", output])
            subprocess.run(cmd, check=True, capture_output=True)
            return True, "PDFs merged"
        else:
            # wkhtmltopdf can merge with --filename-only
            try:
                cmd = ["wkhtmltopdf", "--no-pdfa", "--multi-page", "--enable-local-file-access", output]
                for f in files:
                    cmd.append(f)
                subprocess.run(cmd, check=True, capture_output=True)
                return True, "PDFs merged with wkhtmltopdf"
            except subprocess.CalledProcessError:
                return False, "No merge tool available"
    except Exception as e:
        return False, f"Failed: {str(e)}"

def main():
    """CLI interface for PDF Skil1s."""
    if len(sys.argv) < 2:
        print("Usage: pdf_tools <command> [args]")
        print("Commands:")
        print("  md-to-pdf <input.md> <output.pdf>   Convert markdown")
        print("  text-to-pdf <text> <filename.pdf>   Create from text")
        print("  merge <pdf1> <pdf2> ... <output>    Merge PDFs")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "md-to-pdf" and len(sys.argv) >= 4:
        success, msg = markdown_to_pdf(sys.argv[2], sys.argv[3])
    elif cmd == "text-to-pdf" and len(sys.argv) >= 4:
        text = sys.argv[2]
        file = sys.argv[3]
        success, msg = text_to_pdf(text, file)
    elif cmd == "merge" and len(sys.argv) >= 4:
        files = sys.argv[2:-1]
        output = sys.argv[-1]
        success, msg = merge_pdfs(files, output)
    else:
        print(f"Unknown command: {cmd}")
        return
    
    print(msg)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()