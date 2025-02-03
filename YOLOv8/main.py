from ultralytics import YOLO
import cv2
import os
import sqlite3
from datetime import datetime

# Database setup function
def setup_database():
    conn = sqlite3.connect("detections.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS detections (
        frame_number INTEGER,
        person_count INTEGER,
        timestamp TEXT
    )''')
    conn.commit()
    conn.close()

# Function to store detection results in the database
def store_detections(frame_number, person_count, timestamp):
    conn = sqlite3.connect("detections.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO detections (frame_number, person_count, timestamp) VALUES (?, ?, ?)",
                   (frame_number, person_count, timestamp))
    conn.commit()
    conn.close()

# Main function for processing RTSP stream
def main():
    # Load the YOLOv8 Small model
    model = YOLO('yolov8s.pt')  # Pre-trained YOLOv8 Small model

    # Database setup
    setup_database()
# This part of the code has been disabled to stop it from saving the frames due to privacy reasons.
    # Create the output directory if it doesn't exist
    # output_dir = r"E:\YOLOv8\saved_data"
    # os.makedirs(output_dir, exist_ok=True)

    # Open the RTSP stream
    rtsp_url = "rtsp://Thomas:Thomas1@172.20.6.13/stream1"
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Could not open RTSP stream.")
        return

    print("Press 'q' to quit.")
    frame_count = 0  # To track the frame number

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame from RTSP stream.")
            break

        # Run inference only every 10th frame
        if frame_count % 10 == 0:
            # Run YOLOv8 inference
            results = model.predict(source=frame, save=False, conf=0.5)  # Adjust `conf` for confidence threshold

            # Count the number of people detected
            person_count = sum(1 for result in results[0].boxes if result.cls == 0)  # Assuming class 0 is 'person'

            # Get the current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Store detections in the database
            store_detections(frame_count, person_count, timestamp)

            # Annotate the frame with YOLO results
            annotated_frame = results[0].plot()

            # Save the annotated frame to the output directory
            #frame_filename = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
            #cv2.imwrite(frame_filename, annotated_frame)
            #print(f"Frame {frame_count}: Detected {person_count} people. Saved to {frame_filename}")

            # Display the annotated frame
            cv2.imshow('YOLOv8 RTSP Stream', annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        frame_count += 1

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
