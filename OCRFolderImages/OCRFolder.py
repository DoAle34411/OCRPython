# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 11:57:21 2024
@author: dome3
"""
import cv2
import pytesseract
import os
# Set the path to the Tesseract executable (update the path accordingly)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def perform_ocr(image):
    # Perform OCR on the image using pytesseract
    text = pytesseract.image_to_string(image)
    return text
# Set the path to the folder containing images
folder_path = 'TestImages'
# List all image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
for image_file in image_files:
    # Construct the full path to the image
    image_path = os.path.join(folder_path, image_file)
    # Read the image
    frame = cv2.imread(image_path)
    # Perform OCR on each image
    text = perform_ocr(frame)
    # Print the OCR results along with the image filename
    print(text)
    # Display the image
    cv2.imshow('Image', frame)
    # Wait for a key press
    cv2.waitKey(1)
# Close OpenCV window
cv2.destroyAllWindows()

