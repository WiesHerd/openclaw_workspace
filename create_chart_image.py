#!/usr/bin/env python3
from PIL import Image, ImageDraw

# Create chart
width = 800
height = 600
img = Image.new('RGB', (width, height), color='white')
draw = ImageDraw.Draw(img)

# Title
title = "Bitcoin 5-Year Price Chart (2021-2026)"
draw.text((50, 50), title, fill='#333333', font=None)

# Draw simplified price line
points = [(100, 500), (250, 420), (400, 380), (550, 180), (700, 120), (800, 200)]

for i in range(len(points)-1):
    x1, y1 = points[i]
    x2, y2 = points[i+1]
    draw.line([(x1, y1), (x2, y2)], fill='#f7931a', width=3)

# Draw year labels
for i, (x, y) in enumerate(points):
    price_k = int(points[i][1] / 1000)
    draw.text((x, y - 10), str(price_k) + 'k', fill='#000000')

# Stats box
draw.rectangle([(50, 450), (250, 700)], fill='#2c3e50')
draw.text((60, 460), 'Bitcoin Report', fill='white', font=None, align='center')

# Current stats
stats = [
    ("Current Price", "$65,706"),
    ("5-Year ROI", "+293%"),
    ("Market Cap", "$1.24T"),
    ("24h Change", "-3.96%")
]

color = 'white'
for idx, (label, value) in enumerate(stats):
    y = 480 + (idx * 30)
    draw.text((65, y), label, fill=color, font=None, align='right')
    draw.text((175-80, y), value, fill='#00f7ff', font=None, align='right')

# Legend
draw.rectangle((0, 0, 50, 40), fill='#f7931a')
draw.text((60, 10), 'Bitcoin Price', fill='#333333', font=None)

# Save to PNG
img.save('/home/wherd/.openclaw/workspace/bitcoin_chart.png')
print('Chart image created successfully!')
print('Location: /home/wherd/.openclaw/workspace/bitcoin_chart.png')