import facedetect.py
import facefeedback.py
import facetrack.py
def faceID():
    facedetect
    facefeedback
    facetrack 
import cv2
import numpy as np
import face_recognition
import os
import time

class FaceID:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

    def load_known_faces(self, faces_dir):
        for filename in os.listdir(faces_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(faces_dir, filename)
                face_image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(face_image)[0]
                self.known_face_encodings.append(face_encoding)
                self.known_face_names.append(os.path.splitext(filename)[0])
        print(f"Loaded {len(self.known_face_names)} known faces")

    def process_frame(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if self.process_this_frame:
            self.face_locations = face_recognition.face_locations(rgb_small_frame)
            self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

            self.face_names = []
            for face_encoding in self.face_encodings:
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]

                self.face_names.append(name)

        self.process_this_frame = not self.process_this_frame

        for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        return frame

def main():
    face_id = FaceID()
    faces_dir = "known_faces"
    
    if not os.path.exists(faces_dir):
        os.makedirs(faces_dir)
        print(f"Created directory: {faces_dir}")
        print("Please add some face images to this directory and run the script again.")
        return

    face_id.load_known_faces(faces_dir)

    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()

        if not ret:
            print("Failed to grab frame")
            break

        processed_frame = face_id.process_frame(frame)

        cv2.imshow('Video', processed_frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('a'):
            name = input("Enter name for the new face: ")
            cv2.imwrite(os.path.join(faces_dir, f"{name}.jpg"), frame)
            print(f"Added new face: {name}")
            face_id.load_known_faces(faces_dir)

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

