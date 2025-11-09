import cv2
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import json
import time

# Load the face detection model
model = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/fpnlite_320x320/1")

# Initialize the camera
cap = cv2.VideoCapture(0)

def read_shared_data():
    try:
        with open('shared_face_data.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Prepare the frame for the model
    input_tensor = tf.convert_to_tensor(frame)
    input_tensor = input_tensor[tf.newaxis, ...]

    # Run the model
    detections = model(input_tensor)

    # Extract detection results
    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(np.int32)
    scores = detections['detection_scores'][0].numpy()

    # Get frame dimensions
    height, width, _ = frame.shape

    # Read shared data from facedetect.py
    shared_data = read_shared_data()

    # Loop through detections and draw bounding boxes for faces
    for i in range(len(scores)):
        if scores[i] > 0.5 and classes[i] == 1:  # Class 1 is face in the COCO dataset
            # Get bounding box coordinates
            ymin, xmin, ymax, xmax = boxes[i]
            xmin = int(xmin * width)
            xmax = int(xmax * width)
            ymin = int(ymin * height)
            ymax = int(ymax * height)

            # Draw bounding box
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

            # Add label
            label = f"Face: {scores[i]:.2f}"
            cv2.putText(frame, label, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Add information from shared data
            if shared_data and shared_data['face_detected']:
                cv2.putText(frame, f"Position: {shared_data['position']}", (xmin, ymax + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
                cv2.putText(frame, f"Smiling: {shared_data['smiling']}", (xmin, ymax + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, f"Moving: {shared_data['moving']}", (xmin, ymax + 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # Combined feedback
            feedback = "Neutral"
            if shared_data and shared_data['face_detected']:
                if shared_data['smiling'] and shared_data['moving']:
                    feedback = "You seem happy and active!"
                elif shared_data['smiling']:
                    feedback = "You're smiling! That's great!"
                elif shared_data['moving']:
                    feedback = "You're quite active. What's going on?"
                elif shared_data['position'] != "Center":
                    feedback = f"I see you looking to the {shared_data['position'].lower()}. What's there?"

            cv2.putText(frame, f"Feedback: {feedback}", (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Face Tracking', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()

print("Face tracking session ended.")

