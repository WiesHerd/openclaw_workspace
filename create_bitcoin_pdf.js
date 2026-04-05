#!/usr/bin/env node
const fs = require('fs');
const { PDFDocument, StandardFonts } = require('pdf-lib');

async function createPDF() {
    const content = fs.readFileSync('/home/wherd/.openclaw/workspace/bitcoin_case_report.md', 'utf8');
    
    // Remove problematic characters (Chinese characters) by replacing them
    const cleanContent = content.replace(/[^a-zA-Z0-9\s\-\.,\(\)\\\/'"]/g, '');
    
    const pdfDoc = await PDFDocument.create();
    const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);
    const page = pdfDoc.addPage();
    
    const title = "BITCOIN CASE STUDY & ANALYST FORECAST REPORT";
    page.drawText(title, { x: 50, y: 700, size: 20 });
    
    let y = 680;
    const lines = cleanContent.split('\n');
    for (const line of lines) {
        if (!line.trim() || line.startsWith('#')) continue;
        if (y < 50) { y = 650; }
        page.drawText(line, { x: 50, y: y, size: 10 });
        y -= 10;
    }
    
    await pdfDoc.save('/home/wherd/.openclaw/workspace/bitcoin_report.pdf');
    console.log('PDF created successfully at /home/wherd/.openclaw/workspace/bitcoin_report.pdf');
}

createPDF().catch(err => {
    console.error('Error:', err.message);
});