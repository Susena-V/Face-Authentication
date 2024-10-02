import cv2
import face_recognition
import numpy as np

def capture_and_recognize(reference_image_path):
    # Load the reference image and encode it
    reference_image = face_recognition.load_image_file(reference_image_path)
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return False

    # Read a single frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from webcam.")
        cap.release()
        return False

    # Convert the frame from BGR to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Find all the faces in the captured frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    # Release the webcam
    cap.release()

    # Check if any faces were found in the frame
    for face_encoding in face_encodings:
        # Compare the captured face with the reference face
        matches = face_recognition.compare_faces([reference_encoding], face_encoding)

        if True in matches:
            print("Face verified successfully.")
            return True

    print("Face not recognized.")
    return False

if __name__ == "__main__":
    # Path to your reference image (an image of your face stored locally)
    reference_image ="Susena.jpg"
    
    # Capture and recognize face
    is_authenticated = capture_and_recognize(reference_image)
    if is_authenticated:
        print("Access Granted")
    else:
        print("Access Denied")
