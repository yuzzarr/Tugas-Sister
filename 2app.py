from flask import Flask, jsonify, request, abort
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sister'  # Ganti dengan kunci rahasia Anda

EXCEL_FILE = 'data.xlsx'

def read_data():
    return pd.read_excel(EXCEL_FILE, sheet_name='mahasiswa')

def save_data(data):
    # Simpan data ke sheet
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name='mahasiswa', index=False)

@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    if request.method == 'GET':
        mahasiswa_data = read_data()
        # Mengonversi DataFrame ke tipe yang dapat diserialisasi
        mahasiswa_data = mahasiswa_data.convert_dtypes()
        return jsonify(mahasiswa_data.to_dict(orient='records'))

    if request.method == 'POST':
        mahasiswa_data = read_data()
        
        # Tentukan ID baru
        new_id = mahasiswa_data['id'].max() + 1 if not mahasiswa_data.empty else 1

        # Cek apakah mahasiswa dengan email yang sama sudah ada
        if any(mahasiswa_data['email'] == request.json['email']):
            abort(400, description="Mahasiswa dengan email ini sudah ada!")

        # Buat data baru
        data = {
            "id": new_id,
            "name": request.json['name'],
            "email": request.json['email'],
            "prodi": request.json['prodi']
        }
        
        new_entry = pd.DataFrame([data])
        
        # Gabungkan data yang ada dengan data baru
        combined_data = pd.concat([mahasiswa_data, new_entry], ignore_index=True)
        
        # Simpan data gabungan ke sheet
        save_data(combined_data)
        
        return jsonify(data), 201  # Mengembalikan data baru dengan status 201 Created

@app.route('/mahasiswa/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def mahasiswa_by_id(id):
    mahasiswa_data = read_data()
    mahasiswa = mahasiswa_data[mahasiswa_data['id'] == id]

    if mahasiswa.empty:
        abort(404, description="Mahasiswa tidak ditemukan!")

    if request.method == 'GET':
        # Mengonversi DataFrame ke tipe yang dapat diserialisasi
        mahasiswa = mahasiswa.convert_dtypes()
        return jsonify(mahasiswa.to_dict(orient='records')[0])

    if request.method == 'PUT':
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'name'] = request.json['name']
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'email'] = request.json['email']
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'prodi'] = request.json['prodi']
        
        # Simpan perubahan
        save_data(mahasiswa_data)
        return jsonify(mahasiswa_data[mahasiswa_data['id'] == id].convert_dtypes().to_dict(orient='records')[0])

    if request.method == 'DELETE':
        mahasiswa_data = mahasiswa_data[mahasiswa_data['id'] != id]
        save_data(mahasiswa_data)
        return jsonify({"message": "Mahasiswa berhasil dihapus!"}), 204  # No Content

if __name__ == '__main__':
    app.run(debug=True)