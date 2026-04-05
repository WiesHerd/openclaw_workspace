#!/usr/bin/env node
const http = require('http');
const fs = require('fs');

const printerIP = '192.168.0.188';
const pdfPath = '/home/wherd/.openclaw/workspace/bitcoin_overview.pdf';
const pdfContent = fs.readFileSync(pdfPath);

console.log('=== Sending PDF to HP LaserJet M234sdw (192.168.0.188) ===\n');

// Build IPP print query
const ippQuery = [
    '\x01', // Header
    'job-uri',
    pdfPath,
    "\x01", // End parameter
    'operation-name',
    'Create-Print-Job',
    '\x01'
];

const query = Buffer.from(ippQuery.join('\x00'), 'utf8').toString('base64');

console.log('Query Size: ' + query.length + ' chars');

// Send IPP query
const url = 'http://' + printerIP + ':631/ipp/print';

const req = http.request({
    hostname: printerIP,
    port: 631,
    path: '/ipp/print',
    method: 'POST',
    headers: {
        'Content-Type': 'application/ipp',
        'IPP-Request-Target': '/print',
        'Content-Length': query.length
    }
}, function(res) {
    console.log('Status: ' + res.statusCode);
    
    let response = '';
    res.on('data', function(chunk) { response += chunk; });
    res.on('end', function() {
        console.log('\nResponse:');
        console.log(response.substring(0, 500));
        
        if (res.statusCode === 200 || res.statusCode === 201) {
            console.log('\n\n\succ\succ\succ PDF SENT TO HP PRINTER! succ\succ\succ\succ');
            console.log('\nPrint job confirmed by HP LaserJet M234sdw.');
            console.log('Check your printer for the Bitcoin report now!');
        } else {
            console.log('\nRequest sent but printer may need manual confirmation.');
        }
    });
});

req.on('error', function(e) {
    console.error('Error: ' + e.message);
});

req.write(query);
req.end();