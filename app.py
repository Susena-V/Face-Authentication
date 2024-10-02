from flask import Flask, render_template, request, jsonify
import face_recognition
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # Ensure your HTML file is named index.html

@app.route('/page')
def page():
    return render_template('page.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    print("Received a request at /upload")  # Debugging line
    if 'image' not in request.files:
        return jsonify({'message': 'No image part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    # Save the uploaded image temporarily
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    # Load the reference image (you need to have this image for comparison)
    reference_image_path = 'Susena.jpg'
    reference_image = face_recognition.load_image_file(reference_image_path)
    reference_encoding = face_recognition.face_encodings(reference_image)[0]

    # Load the uploaded image and encode it
    uploaded_image = face_recognition.load_image_file(file_path)
    uploaded_encoding = face_recognition.face_encodings(uploaded_image)

    if not uploaded_encoding:
        os.remove(file_path)  # Remove uploaded image if no face is found
        return jsonify({'message': 'No face found in the image'}), 400

    # Compare the uploaded face with the reference face
    matches = face_recognition.compare_faces([reference_encoding], uploaded_encoding[0])

    # Clean up by removing the uploaded image
    os.remove(file_path)

    if True in matches:
        return jsonify({'message': 'Access Granted'}), 200
    else:
        return jsonify({'message': 'Access Denied'}), 403

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)  # Ensure uploads directory exists
    app.run(debug=True)
