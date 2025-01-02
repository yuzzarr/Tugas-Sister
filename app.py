from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import json  # Import json untuk konversi

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Ganti dengan kunci rahasia Anda

EXCEL_FILE = 'data.xlsx'

def read_data():
    return pd.read_excel(EXCEL_FILE, sheet_name=None)

def save_data(data, sheet_name):
    # Simpan data ke sheet
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mahasiswa', methods=['GET', 'POST'])
def mahasiswa():
    if request.method == 'POST':
        # Baca data yang ada
        mahasiswa_data = read_data().get('mahasiswa', pd.DataFrame())
        
        # Tentukan ID baru
        if not mahasiswa_data.empty:
            new_id = mahasiswa_data['id'].max() + 1  # Mengambil ID maksimum dan menambah 1
        else:
            new_id = 1  # Jika tidak ada data, mulai dari 1

        # Cek apakah mahasiswa dengan email yang sama sudah ada
        if any(mahasiswa_data['email'] == request.form['email']):
            return "Mahasiswa dengan email ini sudah ada!", 400  # Mengembalikan pesan kesalahan

        # Buat data baru
        data = {
            "id": new_id,  # Tambahkan ID baru
            "name": request.form['name'],
            "email": request.form['email'],
            "prodi": request.form['prodi']
        }
        
        new_entry = pd.DataFrame([data])
        
        # Gabungkan data yang ada dengan data baru
        combined_data = pd.concat([mahasiswa_data, new_entry], ignore_index=True)
        
        # Simpan data gabungan ke sheet
        save_data(combined_data, 'mahasiswa')
        
        # Print data mahasiswa ke konsol dalam format JSON
        print(json.dumps(combined_data.to_dict(orient='records'), indent=4))  # Menampilkan JSON di konsol
        
        return redirect(url_for('mahasiswa'))

    mahasiswa_data = read_data().get('mahasiswa', pd.DataFrame())
    # Print data mahasiswa ke konsol dalam format JSON
    print(json.dumps(mahasiswa_data.to_dict(orient='records'), indent=4))  # Menampilkan JSON di konsol
    return render_template('mahasiswa.html', mahasiswa=mahasiswa_data.to_dict(orient='records'))

@app.route('/mahasiswa/update/<int:id>', methods=['GET', 'POST'])
def update_mahasiswa(id):
    mahasiswa_data = read_data().get('mahasiswa', pd.DataFrame())
    
    # Ambil data mahasiswa yang akan diupdate
    mahasiswa = mahasiswa_data[mahasiswa_data['id'] == id]

    # Pastikan mahasiswa ditemukan
    if mahasiswa.empty:
        return "Mahasiswa tidak ditemukan!", 404

    # Ambil nilai dari kolom yang benar
    mahasiswa_name = mahasiswa['name'].values[0]  # Ambil nama
    mahasiswa_email = mahasiswa['email'].values[0]  # Ambil email
    mahasiswa_prodi = mahasiswa['prodi'].values[0]  # Ambil prodi

    if request.method == 'POST':
        # Update data mahasiswa
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'name'] = request.form['name']
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'email'] = request.form['email']
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'prodi'] = request.form['prodi']
        
        # Simpan perubahan
        save_data(mahasiswa_data, 'mahasiswa')
        
        # Print data mahasiswa ke konsol dalam format JSON
        print(json.dumps(mahasiswa_data.to_dict(orient='records'), indent=4))  # Menampilkan JSON di konsol
        
        return redirect(url_for('mahasiswa'))

    # Kirim data mahasiswa ke template
    return render_template('update_mahasiswa.html', mahasiswa={
        'id': id,
        'name': mahasiswa_name,
        'email': mahasiswa_email,
        'prodi': mahasiswa_prodi
    })

@app.route('/mahasiswa/delete/<int:id>', methods=['POST'])
def delete_mahasiswa(id):
    mahasiswa_data = read_data().get('mahasiswa', pd.DataFrame())
    
    # Hapus mahasiswa berdasarkan ID
    mahasiswa_data = mahasiswa_data[mahasiswa_data['id'] != id]
    
    # Simpan perubahan
    save_data(mahasiswa_data, 'mahasiswa')
    
    # Print data mahasiswa ke konsol dalam format JSON
    print(json.dumps(mahasiswa_data.to_dict(orient='records'), indent=4))  # Menampilkan JSON di konsol
    
    return redirect(url_for('mahasiswa'))

if __name__ == '__main__':
    app.run(debug=True)
