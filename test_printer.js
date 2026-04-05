#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');

console.log('=== Testing Print to HP LaserJet M234sdw ===\n');

// Create a simple test text file
const testContent = `TEST PRINT DOCUMENT FROM OPENCLAW
===================================
Date: ${new Date().toDateString()}
Printer: HP LaserJet MFP M234sdw
IP Address: 192.168.0.188

This is a test print job.
If you see this on paper, the printer is working correctly!

Test completed by OpenClaw Assistant.
`;

fs.writeFileSync('/home/wherd/.openclaw/workspace/test_print.txt', testContent);
console.log('✓ Test document created');

// Print using lpr if available
try {
    console.log('Attempting to print test document...');
    const stdout = execSync(`cat /home/wherd/.openclaw/workspace/test_print.txt`, { encoding: 'utf8' });
    console.log('Document content ready to print:');
    console.println(stdout.substring(0, 200) + '...');
    
    console.log('\nSince direct printing requires CUPS/hplip, here are your options:');
    console.log('1. Import the file to your desktop and open it');
    console.log('2. Open in browser: xdg-open /home/wherd/.openclaw/workspace/test_print.txt');
    console.log('3. Then print normally with Ctrl+P');
    
} catch (err) {
    console.error('Error:', err.message);
}