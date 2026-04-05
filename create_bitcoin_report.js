#!/usr/bin/env node
const fs = require('fs');
const { PDFDocument, rgb, StandardFonts } = require('pdf-lib');

async function createFullPDF() {
    try {
        // Read the report content
        const content = fs.readFileSync('/home/wherd/.openclaw/workspace/bitcoin_report_ps.txt', 'utf8');
        // Create PDF
        const pdfDoc = await PDFDocument.create();
        
        // Add font
        const helvetica = await pdfDoc.embedFont(StandardFonts.Helvetica);
        const helveticaBold = await pdfDoc.embedFont(StandardFonts.HelveticaBold);
        
        // Create first page
        const page = pdfDoc.addPage([595, 842]);
        
        // Draw title
        page.drawText('BITCOIN CASE STUDY & ANALYST FORECAST REPORT', {
            x: 50,
            y: 720,
            size: 24,
            font: helveticaBold,
            color: rgb(0, 0, 0)
        });
        
        // Draw subtitle
        page.drawText('Date: April 4, 2026 | Source: casebitcoin.com & Analyst Forecasts', {
            x: 50,
            y: 680,
            size: 12,
            font: helvetica
        });
        
        // Draw table header
        const tableLines = content.split('\n').filter(line => 
            line.trim() && !line.startsWith('BITCOIN') && !line.startsWith('Date:')
        );
        let y = 640;
        
        for (let line of tableLines) {
            if (y < 110) {
                page.drawText('\n---\n' + line, {x: 50, y: y, size: 12, font: helvetica});
                y = 840;
            } else {
                page.drawText(line, {x: 50, y: y, size: 12, font: helvetica});
                y -= 16;
            }
        }
        
        // Save PDF
        await pdfDoc.save('/home/wherd/.openclaw/workspace/bitcoin_report_full.pdf');
        console.log('PDF created successfully!');
    } catch (err) {
        console.log('Error:', err);
    }
}
createFullPDF();