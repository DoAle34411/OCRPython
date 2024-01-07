# -*- coding: utf-8 -*-
import cv2
import pytesseract
import time

# Set the path to the Tesseract executable (update the path accordingly)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def perform_ocr(image):
    # Perform OCR on the image using pytesseract
    text = pytesseract.image_to_string(image)
    return text

# Set the path to your MP4 file
video_path = 'videoPrueba.mp4'

# Open the video file
cap = cv2.VideoCapture(video_path)
fps=cap.get(cv2.CAP_PROP_FPS)
delay=int(1000/(fps/2))

while cap.isOpened():
    ret, frame = cap.read()

    # If the frame is not read, the video has ended
    if not ret:
        break

    # Perform OCR on each frame
    text = perform_ocr(frame)

    # Print the OCR results
    print("OCR Output:")
    print(text)

    # Display the frame
    
    
    cv2.imshow('Video Frame', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    time.sleep(delay/1000.0)

# Release the video capture object
cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
