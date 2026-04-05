const fs = require('fs');
const doc = require('pdfkit');

const content = fs.readFileSync('/home/wherd/.openclaw/workspace/bitcoin_report_ps.txt', 'utf8');

const docCreator = doc('/home/wherd/.openclaw/workspace/bitcoin_report_final.pdf');

doc.fontSize(24).text('BITCOIN CASE STUDY', { align: 'center' }).moveDown();
doc.fontSize(12).text('Report compiled by OpenClaw | Date: April 4, 2026', { align: 'center' }).moveDown();
doc.moveDown();

doc.fontSize(18).text('EXECUTIVE SUMMARY').moveDown();
doc.fontSize(12).text(content);

doc.end();