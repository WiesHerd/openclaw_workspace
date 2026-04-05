#!/usr/bin/env node
const { PDFDocument, StandardFonts } = require('pdf-lib');
const fs = require('fs');
const { execSync } = require('child_process');

const content = fs.readFileSync('/home/wherd/.openclaw/workspace/bitcoin_case_report.md', 'utf8');
const cleanContent = content.replace(/[^a-zA-Z0-9\s\-\.,\(\)\/'"]/g, '');

(async () => {
    try {
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
        
        await pdfDoc.save({ path: '/home/wherd/.openclaw/workspace/bitcoin_report.pdf' });
        
        console.log('PDF Created! File: /home/wherd/.openclaw/workspace/bitcoin_report.pdf\n');
        
        // Print to HP printer
        console.log('Sending to HP Printer...');
        try {
            execSync(`lp -d HP_Printer /home/wherd/.openclaw/workspace/bitcoin_report.pdf`, { stdio: 'inherit' });
            console.log('\n✓ Printed successfully to HP_Printer!');
        } catch (lpErr) {
            console.log('\nlp not found - Try installing CUPS tools:');
            console.log('  sudo apt-get install cups-common');
            console.log('\nManual print command:');
            console.log('  lp -d HP_Printer /home/wherd/.openclaw/workspace/bitcoin_report.pdf');
        }
    } catch (err) {
        console.error('Error:', err.message);
    }
})();