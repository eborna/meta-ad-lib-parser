import cv2
import numpy as np
import os

def extract_card_rows(image_path, output_folder):
    # Read the image
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter and sort contours (assuming cards are larger than a certain size)
    card_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]
    card_contours.sort(key=lambda c: cv2.boundingRect(c)[1])  # Sort by y-coordinate
    
    # Group contours into rows
    rows = []
    current_row = []
    last_y = 0
    for cnt in card_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if abs(y - last_y) > h/2 and current_row:
            rows.append(current_row)
            current_row = []
        current_row.append((x, y, w, h))
        last_y = y
    if current_row:
        rows.append(current_row)
    
    # Extract and save rows
    for i, row in enumerate(rows):
        if len(row) == 3:  # Only process rows with exactly 3 cards
            row_img = np.zeros((max(r[3] for r in row), sum(r[2] for r in row), 3), dtype=np.uint8)
            x_offset = 0
            for x, y, w, h in sorted(row):
                card = img[y:y+h, x:x+w]
                row_img[0:h, x_offset:x_offset+w] = card
                x_offset += w
            
            cv2.imwrite(os.path.join(output_folder, f'row_{i+1}.jpg'), row_img)

# Usage
extract_card_rows('screencapture-facebook-ads-library-2024-07-22-13_52_41 copy 5.png', 'opencv_output')