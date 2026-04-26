# -*- coding: utf-8 -*-
import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog
import os # <-- Added to handle file paths

# Set the path to the Tesseract executable (update the path accordingly)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\PC\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def perform_ocr(image):
    print("\nExtracting text... Please wait.")
    # Perform OCR on the image using pytesseract
    text = pytesseract.image_to_string(image)
    return text

# Hide the main tkinter window
root = tk.Tk()
root.withdraw()

# Open a dialog to let the user select a video dynamically
print("Waiting for video selection...")
video_path = filedialog.askopenfilename(
    title="Select a Video File",
    filetypes=[("Video Files", "*.mp4 *.avi *.mkv *.mov"), ("All Files", "*.*")]
)

if not video_path:
    print("No video selected. Exiting...")
    exit()

print(f"Loading video: {video_path}")

# --- NEW: Setup the Output Text File ---
video_dir = os.path.dirname(video_path)
video_filename = os.path.basename(video_path)
# Remove the extension (e.g., .mp4) and add _OCR_results.txt
txt_filename = os.path.splitext(video_filename)[0] + "_OCR_results.txt"
output_filepath = os.path.join(video_dir, txt_filename)

print(f"Results will be saved to: {output_filepath}")

# Create/Clear the file at the start of the session
with open(output_filepath, 'w', encoding='utf-8') as f:
    f.write(f"--- OCR Results for {video_filename} ---\n\n")

# Open the video file
cap = cv2.VideoCapture(video_path)

# Get the native framerate
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0: 
    fps = 30

# Speed Control Variables
base_delay = 1000 / fps  
speed_multiplier = 1.0   

print("\n--- CONTROLS ---")
print("[ s ] - Pause video, Scan current frame, and Save to TXT")
print("[ Space ] - Pause / Play video")
print("[ ] ] - Speed up (x1.5, x2.0, etc.)")
print("[ [ ] - Slow down (x0.5, x1.0, etc.)")
print("[ 1 ] - Reset to normal speed (1.0x)")
print("[ q ] - Quit")
print("----------------\n")

is_paused = False

while cap.isOpened():
    if not is_paused:
        ret, frame = cap.read()
        
        if not ret:
            print("End of video reached.")
            break
            
        cv2.imshow('Video Playback', frame)

    # Calculate current delay based on the multiplier
    current_delay = int(base_delay / speed_multiplier)
    current_delay = max(1, current_delay)

    # Wait for key press
    wait_time = 0 if is_paused else current_delay
    key = cv2.waitKey(wait_time) & 0xFF

    # Handle keyboard controls
    if key == ord('q'):
        break
        
    elif key == ord(' '):  # Spacebar to pause/play
        is_paused = not is_paused
        state = "Paused" if is_paused else "Playing"
        print(f"Video {state} at {speed_multiplier}x speed")
        
    elif key == ord('s'):  # Scan frame and Save
        is_paused = True 
        
        # Calculate the current timestamp in the video
        current_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        current_time_sec = current_frame_num / fps
        mins, secs = divmod(current_time_sec, 60)
        timestamp = f"{int(mins):02d}:{secs:05.2f}"
        
        text = perform_ocr(frame)
        clean_text = text.strip()
        
        # Print to console
        print(f"\n--- OCR Output [Time: {timestamp}] ---")
        print(clean_text if clean_text else "[No text detected in this frame]")
        print("-----------------------------------")
        print("Press [Space] to resume playback.")
        
        # --- NEW: Append to the text file ---
        with open(output_filepath, 'a', encoding='utf-8') as f:
            f.write(clean_text + "\n\n")
            if not clean_text:
                 f.write("[No text detected]\n\n")
        
    # Speed Adjustment Controls
    elif key == ord(']'):  
        speed_multiplier += 0.5
        print(f"Playback speed: {speed_multiplier}x")
        
    elif key == ord('['):  
        speed_multiplier = max(0.5, speed_multiplier - 0.5)
        print(f"Playback speed: {speed_multiplier}x")
        
    elif key == ord('1'):  
        speed_multiplier = 1.0
        print(f"Playback speed reset: {speed_multiplier}x")

print(f"\nFinished! All text was saved to: {output_filepath}")

cap.release()
cv2.destroyAllWindows()