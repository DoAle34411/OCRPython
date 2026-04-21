# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 11:57:21 2024
@author: dome3
"""
import cv2
import pytesseract
import os
import tkinter as tk
from tkinter import filedialog

# Set the path to the Tesseract executable (update the path accordingly)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\PC\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def perform_ocr(image):
    # Perform OCR on the image using pytesseract
    text = pytesseract.image_to_string(image)
    return text

# 1. Hide the main tkinter window so only the dialog box shows
root = tk.Tk()
root.withdraw()

# 2. Open a dialog to let the user select a folder
print("Waiting for folder selection...")
folder_path = filedialog.askdirectory(title="Select Folder with Images")

# If the user clicks "Cancel" on the dialog, exit the script gracefully
if not folder_path:
    print("No folder was selected. Exiting...")
    exit()

print(f"Folder selected: {folder_path}")

# List all image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]

# 3. Create the path for the output text file (saved inside the selected folder)
output_filepath = os.path.join(folder_path, "ocr_extracted_text.txt")

# 4. Open the text file in write mode ('w'). Using utf-8 encoding prevents errors with special characters.
with open(output_filepath, 'w', encoding='utf-8') as txt_file:
    
    for image_file in image_files:
        # Construct the full path to the image
        image_path = os.path.join(folder_path, image_file)
        
        # Read the image
        frame = cv2.imread(image_path)
        
        # Perform OCR on each image
        text = perform_ocr(frame)
        
        # Print the OCR results to the terminal
        print(f"\n--- Reading: {image_file} ---")
        print(text)
        
        txt_file.write(text + "\n\n")
        
        # Display the image
        cv2.imshow('Image', frame)
        
        # Wait for a key press (1 millisecond)
        cv2.waitKey(1)

print(f"\nFinished! All text has been saved to: {output_filepath}")

# Close OpenCV window
cv2.destroyAllWindows()