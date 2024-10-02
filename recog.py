import cv2
from deepface import DeepFace

def capture_and_recognize(reference_image_path):
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

    # Save the captured frame to a temporary image file
    captured_image_path = "captured_image.jpg"
    cv2.imwrite(captured_image_path, frame)

    # Release the webcam
    cap.release()

    try:
        # Use DeepFace to verify the captured image against the reference image
        result = DeepFace.verify(img1_path=reference_image_path, img2_path=captured_image_path)
        
        if result['verified']:
            print("Face verified successfully.")
            return True
        else:
            print("Face not recognized.")
            return False

    except Exception as e:
        print(f"Error during face recognition: {e}")
        return False

if __name__ == "__main__":
    # Path to your reference image (an image of your face stored locally)
    reference_image = "your_face.jpg"
    
    # Capture and recognize face
    is_authenticated = capture_and_recognize(reference_image)
    if is_authenticated:
        print("Access Granted")
    else:
        print("Access Denied")
