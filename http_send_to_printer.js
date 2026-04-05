#!/usr/bin node
const http = require('http');
const fs = require('fs');

const printerIP = '192.168.0.188';
const printerPort = 631;
const pdfPath = '/home/wherd/.openclaw/workspace/bitcoin_overview.pdf';
const pdfContent = fs.readFileSync(pdfPath);

console.log('=== HTTP POST to HP Printer IPP ===\n');
console.log('IPP Server: ' + printerIP + ':' + printerPort);
console.log('PDF Size: ' + pdfContent.length + ' bytes\n');

const postData = 'OperationUri=/print&ipp-uuid=' + Math.floor(Math.random() * 999999).toString();
const data = Buffer.from("application-uri=" + encodeURIComponent(pdfPath) + "\\r\\n" + "application-name=" + encodeURIComponent("OpenClaw-Bitcoin-Report") + "\\r\\n" + postData + "\\r\\n\\r\\n" + pdfContent.toString('binary'), 'binary');

const obj = {
    hostname: printerIP,
    port: printerPort,
    path: '/',
    method: 'POST',
    headers: {
        'Content-Type': 'application/printer-printing-job',
        'Content-Length': data.length
    }
};

console.log('Sending POST request...');
const req = http.request(obj, function(res) {
    let body = '';
    res.on('data', function(chunk) { body += chunk; });
    res.on('end', function() {
        console.log('Response Code: ' + res.statusCode);
        if (res.statusCode >= 200 && res.statusCode < 300) {
            console.log('\n\succ\succ\succ PDF SENT SUCCESSFULLY! succ\succ\succ\succ');
            console.log('Your HP LaserJet M234sdw should begin printing now.');
        } else {
            console.log('\n\succ Failed to send PDF.');
            console.log('Response: ' + body);
        }
    });
});

req.on('error', function(e) {
    console.error('Request Error: ' + e.message);
});

req.on('data', function(chunk) { /* Handle data */ });
req.write(data);
req.end();