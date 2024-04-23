from flask import Flask, jsonify
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import request
import base64

app = Flask(__name__)

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PORT'] = 3308
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'uts_eaiteladan_hotel'
mysql = MySQL(app)

# Function to generate timestamp
def generate_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.route('/hotel', methods=['GET'])
def get_all_destinasi():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM hotel")
    columns = [i[0] for i in cursor.description]
    data = []
    for row in cursor.fetchall():
        # Convert BLOB image data to base64 encoded string
        row_data = list(row)
        row_data[columns.index('foto_hotel')] = base64.b64encode(row_data[columns.index('foto_tujuan')]).decode('utf-8')
        data.append(dict(zip(columns, row_data)))
    cursor.close()
    timestamp = generate_timestamp()
    return jsonify({'timestamp': timestamp, 'data': data})

@app.route('/hotel/create', methods=['POST'])
def add_hotel():
    if request.method == 'POST':
        # Mengambil data dari permintaan POST
        id_hotel = request.form['id_hotel']
        lokasi_hotel = request.form['lokasi_hotel']
        harga_sewa = request.form['harga_sewa']

        # Menyimpan data gambar dari permintaan
        foto_hotel = request.files['foto_hotel'].read()
        
        # Menyimpan data ke dalam database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO hotel (id_hotel, lokasi_hotel, harga_sewa, foto_hotel) VALUES (%s, %s, %s, %s)", (id_hotel, lokasi_hotel, harga_sewa, foto_hotel))
        mysql.connection.commit()
        cursor.close()
        
        # Menyusun respons
        timestamp = generate_timestamp()
        response = jsonify({'timestamp': timestamp, 'message': 'Data hotel berhasil ditambahkan'})
        response.status_code = 201  # Created
        return response
    else:
        return jsonify({'message': 'Method not allowed'}), 405  # Method Not Allowed


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)