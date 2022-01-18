from __future__ import division, print_function
import os
import numpy as np
from flask import Flask,render_template,request,send_from_directory

# Keras
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

# Define a flask app
app = Flask(__name__,template_folder='template')

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'

# Load your trained model
model1 = load_model('pepper_model.h5')
model2 = load_model('pepper_model.h5')
model3 = load_model('pepper_model.h5')

def api(full_path):
    data = image.load_img(full_path, target_size=(256, 256,3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255
    predicted = model1.predict(data)
    return predicted

def api1(full_path):
    data = image.load_img(full_path, target_size=(256, 256,3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255
    predicted = model2.predict(data)
    return predicted

def api3(full_path):
    data = image.load_img(full_path, target_size=(256, 256,3))
    data = np.expand_dims(data, axis=0)
    data = data * 1.0 / 255
    predicted = model3.predict(data)
    return predicted

@app.route('/upload', methods=['POST','GET'])
def upload_file():

    if request.method == 'GET':
        return render_template('index1.html')
    else:
        #try:
        file = request.files['image']
        full_name = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(full_name)
        indices = {0: 'EARLY_BLIGHT', 1: 'HEALTHY', 2: 'LATE_BLIGHT'}
        result = api(full_name)
        print(result)
        predicted_class = np.asscalar(np.argmax(result, axis=1))
        accuracy = round(result[0][predicted_class] * 100, 2)
        label = indices[predicted_class]
        return render_template('predict.html', image_file_name = file.filename, label = label, accuracy = accuracy)
        #except:
            #flash("Please select the image first !!", "danger")      
            #return redirect(url_for("Potato"))

@app.route('/upload2', methods=['POST','GET'])
def upload_file2():

    if request.method == 'GET':
        return render_template('index2.html')
    else:
        #try:
        file = request.files['image']
        full_name = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(full_name)
        indices = {0: 'INFECTED', 1: 'HEALTHY'}
        result = api1(full_name)
        print(result)
        predicted_class = np.asscalar(np.argmax(result, axis=1))
        accuracy = round(result[0][predicted_class] * 100, 2)
        label = indices[predicted_class]
        return render_template('predict1.html', image_file_name = file.filename, label = label, accuracy = accuracy)
        #except:
            #flash("Please select the image first !!", "danger")      
            #return redirect(url_for("Pepper"))

@app.route('/upload3', methods=['POST','GET'])
def upload_file3():

    if request.method == 'GET':
        return render_template('index3.html')
    else:
        #try:
        file = request.files['image']
        full_name = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(full_name)
        indices = {0: 'BROWNSPOT', 1: 'HEALTHY',2: 'HISPA',3: 'LEAFBLAST'}
        result = api1(full_name)
        print(result)
        predicted_class = np.asscalar(np.argmax(result, axis=1))
        accuracy = round(result[0][predicted_class] * 100, 2)
        label = indices[predicted_class]
        return render_template('predict2.html', image_file_name = file.filename, label = label, accuracy = accuracy)
        
@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/Potato")
def Potato():
    return render_template("index1.html")

@app.route("/Pepper")
def Pepper():
    return render_template("index2.html")

@app.route("/Rice")
def Rice():
    return render_template("index3.html")

if __name__ == '__main__':
    app.run(debug=True)