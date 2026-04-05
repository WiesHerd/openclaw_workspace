#!/usr/bin/env node
const { spawn } = require('child_process');

// HPLIP Installation and Printer Script
const hplipInstall = spawn('sudo', ['apt-get', 'update', '-qq'], { stdio: ['inherit', 1, 2] });

hplipInstall.on('close', (code) => {
    if (code !== 0) return;
    
    const hplipInstall2 = spawn('sudo', ['apt-get', 'install', '-y', 'hplip', 'hplip-data', 'hplip-utils', 'hplip-cups']);
    hplipInstall2.on('close', (code) => {
        if (code !== 0) return;
        
        const detectPrinter = spawn('hp-check', ['-printers', '-casesensitive'], { stdio: ['inherit', 1, 2] });
        detectPrinter.on('exit', (code) => {
            console.log('Detection completed. Code:', code);
        });
    });
});

hplipInstall.on('error', (err) => {
    console.error('Error initiating HPLIP:', err);
});

hplipInstall2.on('error', (err) => {
    console.error('Cannot install without sudo');
});