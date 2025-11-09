import cv2
import numpy as np

# Initialize face and smile detection cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Start video capture
cap = cv2.VideoCapture(0)

# Get the width and height of the frame
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Variables for tracking face movement
prev_face_center = None
movement_threshold = 50  # pixels

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        # Draw rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Get the center of the face
        face_center = (x + w//2, y + h//2)

        # Check face position
        if face_center[0] < frame_width // 3:
            position_text = "Left"
        elif face_center[0] > 2 * frame_width // 3:
            position_text = "Right"
        else:
            position_text = "Center"

        # Detect smile
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

        if len(smiles) > 0:
            cv2.putText(frame, "Smiling", (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Check for movement
        if prev_face_center is not None:
            movement = np.sqrt((face_center[0] - prev_face_center[0])**2 + 
                               (face_center[1] - prev_face_center[1])**2)
            if movement > movement_threshold:
                cv2.putText(frame, "Moving", (x, y-60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        prev_face_center = face_center

        # Display position text
        cv2.putText(frame, position_text, (x, y-90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Interaction', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and destroy windows
cap.release()
cv2.destroyAllWindows()

print("Face interaction session ended.")