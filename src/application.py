import flask
from flask import request, jsonify
import logging, os, json, imageDetection
import csv
from csv import writer
from azure.storage.blob import BlobServiceClient
import time

app = flask.Flask(__name__)
app.config["DEBUG"] = True

with open('dddsList.json') as json_file:
    dddDict = json.load(json_file)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
OUTPUT_FOLDER = '{}/output/'.format(PROJECT_HOME)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)

container_data = 'user-data'
container_pictures = 'user-pictures'

def find_location_ddd(phone_number):
    ddd = phone_number[:2]
    location = dddDict[ddd]

    return location

def save_csv(name, email, phone, location, auth, img_name):

    blob_client = blob_service_client.get_blob_client(container=container_data, blob='user.csv')

    with open('user.csv', "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    with open('user.csv', 'a+', newline='') as write_obj:
        row_contents = [name, email, phone, location, auth, img_name]
        csv_writer = writer(write_obj)
        csv_writer.writerow(row_contents)
    
    with open('user.csv', "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    os.remove('user.csv')

def save_image(output_path, img_name):

    blob_client = blob_service_client.get_blob_client(container=container_pictures, blob=img_name)

    with open(output_path, "rb") as data:
        blob_client.upload_blob(data)

@app.route('/eyebrows', methods=['POST'])
def eyebrows():

    img = request.files['image']

    file_extension = img.filename[-4:]

    img_name = request.form['email'] + str(time.time()) + file_extension

    saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
    img.save(saved_path)

    imageDetection.main(img_name)

    output_path = os.path.join(app.config['OUTPUT_FOLDER'], img_name)
    save_image(output_path, img_name)

    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    auth = request.form['auth']

    location = request.form['location']

    if location == '':
        location = request.form['location']
    else:
        location = find_location_ddd(phone)

    os.remove(saved_path)

    os.remove(output_path)

    save_csv(name, email, phone, location, auth, img_name)
    
    return jsonify({'image': 'http://dellaedelle.blob.core.windows.net/user-pictures/' + img_name})

@app.route('/', methods=['GET'])
def hello():
    return jsonify({'image': 'Hello'})

if __name__ == '__main__':
    app.run(port=8000)