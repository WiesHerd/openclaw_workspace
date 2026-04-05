#!/usr/bin/env node
const fs = require('fs');
const { PDFDocument, StandardFonts } = require('pdf-lib');

async function createPDFAndPrint() {
    const content = fs.readFileSync('/home/wherd/.openclaw/workspace/bitcoin_case_report.md', 'utf8');
    const cleanContent = content.replace(/[^a-zA-Z0-9\s\-\.,\(\)\\\/'"]/g, '');
    
    const pdfDoc = await PDFDocument.create();
    const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);
    const page = pdfDoc.addPage();
    
    page.drawText('BITCOIN CASE STUDY & ANALYST FORECAST REPORT', { x: 50, y: 700, size: 20 });
    
    let y = 680;
    for (const line of cleanContent.split('\n')) {
        if (!line.trim() || line.startsWith('#')) continue;
        if (y < 50) { y = 650; }
        page.drawText(line, { x: 50, y: y, size: 10 });
        y -= 10;
    }
    
    const pdfBytes = pdfDoc.save();
    fs.writeFileSync('/home/wherd/.openclaw/workspace/bitcoin_report.pdf', pdfBytes);
    
    console.log('PDF Created at:');
    console.log('/home/wherd/.openclaw/workspace/bitcoin_report.pdf');
    
    // Print to HP
    try {
        const { execSync } = require('child_process');
        console.log('\nSending to HP Printer...');
        execSync(`lp -d HP_Printer /home/wherd/.openclaw/workspace/bitcoin_report.pdf`, { stdio: 'inherit' });
    } catch (e) {
        console.log('\nlp command failed:');
        console.log('Try: lp -d HP_Printer /home/wherd/.openclaw/workspace/bitcoin_report.pdf');
    }
}

createPDFAndPrint().catch(console.error);