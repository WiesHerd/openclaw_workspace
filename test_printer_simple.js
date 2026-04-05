#!/usr/bin/env node
const fs = require('fs');

console.log('=== HP Printer Test ===\n');

// Create test document
const testContent = `HP PRINTER TEST
===============
Time: ${new Date().toDateString()}
Source: OpenClaw Assistant

Test document for: HP LaserJet M234sdw
IP: 192.168.0.188

If you can read this on paper, your printer is working!
OpenClaw verified: 2026-04-04
`;

fs.writeFileSync('/home/wherd/.openclaw/workspace/printer_test.txt', testContent);
console.log('%cPrinter test document created!', 'color: green, font-size: 16px');
console.log('\nDocument path: /home/wherd/.openclaw/workspace/printer_test.txt');
console.log('\nTo print this document, you can:');
console.log('1. Open it in your text editor');
console.log('2. Copy it to your computer and print');
console.log('3. Or upload it to Slack for browser printing');