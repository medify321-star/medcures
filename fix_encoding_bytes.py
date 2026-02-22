#!/usr/bin/env python3
import re

file_path = r'c:\Users\ASUS\OneDrive\Documents\my website\.emergent\.emergent\backend\pharmacopoeia.json'

with open(file_path, 'rb') as f:
    content = f.read()

# Replace the problematic encoded characters with dashes and quotes
# â€" is UTF-8 for en-dash, we want to replace with regular dash
content = content.replace(b'\xc3\xa2\xc2\x80\xc2\x93', b'-')  # â€"  -> -
content = content.replace(b'\xc3\xa2\xc2\x80\xc2\x9d', b'-')  # â€ -> -
content = content.replace(b'\xe2\x80\x93', b'-')  # en-dash -> -
content = content.replace(b'\xe2\x80\x99', b"'")  # right single quote -> '
content = content.replace(b'\xe2\x80\x98', b"'")  # left single quote -> '
content = content.replace(b'\xe2\x80\x9c', b'"')  # left double quote -> "
content = content.replace(b'\xe2\x80\x9d', b'"')  # right double quote -> "

with open(file_path, 'wb') as f:
    f.write(content)

print('Fixed encoding in pharmacopoeia.json')
