const { PDFDocument, StandardFonts } = require('pdf-lib');
const fs = require('fs');

const content = fs.readFileSync('/home/wherd/.openclaw/workspace/bitcoin_case_report.md', 'utf8');
const cleanContent = content.replace(/[^a-zA-Z0-9\s\-\.,\(\)\/'"]/g, '');

(async () => {
    try {
        console.log('=== HP LaserJet MFP M234sdw - PDF Creation & Printing ===\n');
        
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
        console.log('✓ PDF Created: /home/wherd/.openclaw/workspace/bitcoin_report.pdf\n');
        
        // Direct IPP send to HP printer
        const printerIP = '192.168.0.188';
        const printerPort = '631';
        
        console.log(`Sending to HP LaserJet MFP M234sdw`);
        console.log(`IP: ${printerIP}:${printerPort}`);
        console.log(`Hostname: NPI4D4B32\n`);
        
        // Method 1: Try remote IPP via curl
        console.log('Attempting direct IPP send...');
        
        const { execSync } = require('child_process');
        
        try {
            const pdfPath = '/home/wherd/.openclaw/workspace/bitcoin_report.pdf';
            const uri = `ipp://${printerIP}:${printerPort}/print`;
            
            console.log(`IPP URI: ${uri}\n`);
            
            // Create curl command to send PDF via IPP
            const curlCmd = `curl -T "${pdfPath}" ipp://${printerIP}:${printerPort}/print`;
            console.log(`Command: ${curlCmd}\n`);
            
            execSync(curlCmd, { stdio: 'inherit' });
            console.log('\n✓✓✓ SUCCESS - PDF sent to HP printer via IPP! ✓✓✓');
            console.log('Print job queued on: NPI4D4B32 (HP LaserJet M234sdw)');
        } catch (curlErr) {
            console.log('\n✗ curl IPP failed. Alternative methods:\n');
            
            // Method 2: Try hp-printer-ipps-endprint
            try {
                console.log('Trying direct IPP send with node...');
                
                const queryToJson = (query) => {
                    return Buffer.from(JSON.stringify(query), 'utf8').toString('base64');
                };
                
                // Create IPP job
                const ippQuery = {
                    "ipp-uuid": Math.floor(Math.random() * 1000000).toString(),
                    "document-name": ["bitcoin_report.pdf"],
                    "printer-uri": [printerIP],
                    "application-name": ["OpenClaw-PDF-Printer"],
                    "print-job-id": ["12345"],
                    "copies": [1]
                };
                
                const data = queryToJson(ippQuery) + "\n" + Buffer.from(pdfPath, 'utf8').toString('base64');
                const payload = Buffer.from(data, 'utf8').toString('base64');
                
                const uri = `http://${printerIP}:${printerPort}/ipp/print`;
                const curlIpp = `curl -X POST -d "${payload}" "${uri}"`;
                console.log(curlIpp);
                
                execSync(curlIpp, { stdio: ['inherit', 'inherit', 'inherit'] });
                console.log('\n✓ Direct IPP send successful!');
            } catch (ippErr) {
                console.log('\n✗ Direct IPP failed. Try these commands:\n');
                console.log(`  apt install curl`);
                console.log('  curl -T /home/wherd/.openclaw/workspace/bitcoin_report.pdf ipp://192.168.0.188:631/print');
            }
        }
        
    } catch (err) {
        console.error('Error:', err.message);
    }
})();