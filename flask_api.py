from flask import Flask, request
from pymongo import MongoClient
import gridfs
import datetime

app = Flask(__name__)

# Koneksi ke MongoDB
client = MongoClient("mongodb+srv://neta_sic:neta_sic@backenddb.rfmwzg6.mongodb.net/?retryWrites=true&w=majority&appName=BackendDB")
db = client["locations"]
realtime_collection = db["realtime_location"]
vulnerable_location_collection = db["vulnerable_location"]

# FS Grid
fs = gridfs.GridFS(db)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return {'message': 'File tidak ditemukan'}, 400

    file = request.files['file']
    device_id = request.form.get('device_id') 

    if not device_id:
        return {'message': 'Device ID tidak boleh kosong'}, 400

    if file.filename == '':
        return {'message': 'Nama file kosong'}, 400

    file_id = fs.put(file, device_id=device_id ,filename=file.filename, content_type=file.content_type, uploadDate=datetime.datetime.utcnow())
    return {'message': 'Upload berhasil', 'device_id':str(device_id), 'file_id': str(file_id)}, 200

@app.route('/vulnerable-location', methods=['POST'])
def post_vulnerable_location():
    device_id = request.form.get('device_id')
    lon = request.form.get('lon')
    lat = request.form.get('lat')

    if not lat:
        return {'message': 'Lat tidak boleh kosong'}, 400
    if not lon:
        return {'message': 'Lon tidak boleh kosong'}, 400
    if not device_id:
        return {'message': 'Device ID tidak boleh kosong'}, 400

    result = vulnerable_location_collection.insert_one({
        'device_id': device_id,
        'lat': float(lat),
        'lon': float(lon),
        'timestamp': datetime.datetime.utcnow()
    })

    return {'message': 'Berhasil mengirim data', 'device_id':str(device_id), 'lon': str(lon), lat: str(lat)}, 200

@app.route('/post-location', methods=['POST'])
def post_lang_lot():
    device_id = request.form.get('device_id') 

    lon = request.form.get('lon') 

    lat = request.form.get('lat') 

    if not lat:
        return {'message': 'Lat tidak boleh kosong'}, 400

    if not lon:
        return {'message': 'Lon tidak boleh kosong'}, 400

    if not device_id:
        return {'message': 'Device ID tidak boleh kosong'}, 400
    
    result = realtime_collection.insert_one({
    'device_id': device_id,
    'lat': float(lat),
    'lon': float(lon),
    'timestamp': datetime.datetime.utcnow() 
    })

    return {'message': 'Berhasil mengirim data', 'device_id':str(device_id), 'lon': str(lon), lat: str(lat)}, 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host="0.0.0.0")
