const { execSync } = require('child_process');
const fs = require('fs');

const pdfPath = '/home/wherd/.openclaw/workspace/bitcoin_overview.pdf';
const printerIP = '192.168.0.188';

if (!fs.existsSync(pdfPath)) {
    console.error(`PDF file not found: ${pdfPath}`);
    process.exit(1);
}

console.log('=== Sending PDF to HP LaserJet MFP M234sdw ===');
console.log('PDF: ' + pdfPath);
console.log('Printer: HP LaserJet MFP M234sdw @ ' + printerIP);
console.log('Hostname: NPI4D4B32\n');

// Direct IPP send
const curlCmd = 'curl -T "' + pdfPath + '" ipp://' + printerIP + '/print';

console.log('Sending via IPP...');
console.log('IPP URI: ipp://' + printerIP + '/print\n');

try {
    execSync(curlCmd, { stdio: 'inherit' });
    console.log('\n\nSUCCESS! PDF sent to HP printer!');
    console.log('Print job should appear on your HP LaserJet M234sdw shortly.');
} catch (err) {
    console.log('\nFailed to send via curl.');
    console.log('Try manually:');
    console.log('  curl -T ' + pdfPath + ' ipp://' + printerIP + '/print');
    console.log('\nOr visit your printer web interface:');
    console.log('  http://' + printerIP + '/');
}