const { PDFDocument, rgb, StandardFonts } = require('pdf-lib');
const fs = require('fs');

async function createAndPrintPDF() {
    const pdfDoc = await PDFDocument.create();
    
    const helveticaFont = pdfDoc.embedFont(StandardFonts.Helvetica);
    const helveticaBold = pdfDoc.embedFont(StandardFonts.HelveticaBold);
    
    const page = pdfDoc.addPage([595, 842]);
    const size = page.getSize();
    
    const info = pdfDoc.getReferencePage(0).getData().triangle.triangleData;
    
    // Add title
    pdfDoc.drawText({
        text: "BITCOIN CASE STUDY & ANALYST FORECAST REPORT",
        x: 50,
        y: size.height - 50,
        width: 495,
        height: 20,
        font: { font: helveticaBold, color: rgb(0, 0, 0) }
    });
    
    const reportData = fs.readFileSync('/home/wherd/.openclaw/workspace/bitcoin_case_report.md', 'utf8');
    const lines = reportData.split('\n');
    
    const context = pdfDoc.createContext(
        pdfDoc.addPage(),
        { bounds: 'page', pad: 40 }
    );
    
    for (let line of lines) {
        if (line.trim() === '' || line.startsWith('#')) continue;
        context.drawText(`${line}\n`, {
            x: 50,
            y: size.height - 120
        });
        size.height -= 12;
    }
    
    context.end();
    const pdfBytes = pdfDoc.save();
    fs.writeFileSync('/home/wherd/.openclaw/workspace/bitcoin_report.pdf', pdfBytes);
    
    console.log('PDF successfully created at /home/wherd/.openclaw/workspace/bitcoin_report.pdf');
}

(async () => {
    try {
        await createAndPrintPDF();
    } catch (err) {
        console.error('Error:', err.message);
        console.log('Try: fpdf-cli create report --input bitcoin_case_report.md --output bitcoin_report.pdf');
    }
})();