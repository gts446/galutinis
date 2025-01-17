from flask import Flask, render_template, request, redirect, session, url_for
from PIL import Image
import os
import models
import html


def filter_image_name(string):
    return html.escape(string)


# Create the Flask app
app = Flask(__name__)
app.secret_key = "123456"  # Required for session to work


# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'static\\uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename: str):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Define a route and its associated view function
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']
    filename = filter_image_name(file.filename)

    filter_artifacts = 'artifact_filter' in request.form

    if file and allowed_file(filename):
        filename = filename.rsplit('.', 1)[0].lower()
        file_path_original = os.path.join(app.config['UPLOAD_FOLDER'], 'original_'+filename+'.png')
        file_path_generated = os.path.join(app.config['UPLOAD_FOLDER'], 'generated_'+filename+'.png')
        uploaded_image = Image.open(file)
        uploaded_image.save(file_path_original, 'png')
        if filter_artifacts:
            uploaded_image = models.filter_artifacts(uploaded_image)
            print('FILTRUOJAMI ARTIFAKTAI')
        generated_image = models.upscale_image(uploaded_image)
        generated_image.save(file_path_generated, 'png')
        session['filename'] = filename
        return f"File successfully processed", 200

    return "File not allowed", 400

@app.route('/success')
def success():
    if 'filename' not in session:
        return redirect(url_for('home'))
    filename = session['filename']
    filepath = {
        'original' : os.path.join(app.config['UPLOAD_FOLDER'], 'original_'+filename+'.png'),
        'generated' : os.path.join(app.config['UPLOAD_FOLDER'], 'generated_'+filename+'.png')
    }
    return render_template('success.html', filename=filename, filepath=filepath)


@app.route('/compare')
def compare_result():
    if 'filename' not in session:
        return redirect(url_for('home'))
    filename = session['filename']
    filepath = {
        'original' : os.path.join(app.config['UPLOAD_FOLDER'], 'original_'+filename+'.png'),
        'generated' : os.path.join(app.config['UPLOAD_FOLDER'], 'generated_'+filename+'.png')
    }
    return render_template('result3.html', filepath=filepath)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
