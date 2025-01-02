from spyne import Application, rpc, ServiceBase, Iterable, Integer, Unicode, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.protocol.soap import Soap11
from spyne.model.primitive import Integer, Unicode
import pandas as pd

EXCEL_FILE = 'data.xlsx'

# Model untuk Mahasiswa
class Mahasiswa(ComplexModel):
    id = Integer
    name = Unicode
    email = Unicode
    prodi = Unicode

# Layanan SOAP
class MahasiswaService(ServiceBase):
    
    @rpc(_returns=Array(Mahasiswa))
    def get_mahasiswa(self):
        mahasiswa_data = read_data().get('mahasiswa', pd.DataFrame())
        mahasiswa_data = mahasiswa_data.convert_dtypes()
        return [Mahasiswa(id=row['id'], name=row['name'], email=row['email'], prodi=row['prodi']) for index, row in mahasiswa_data.iterrows()]

    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def add_mahasiswa(self, name, email, prodi):
        mahasiswa_data = read_data().get('mahasiswa', pd.DataFrame())
        
        # Tentukan ID baru
        new_id = mahasiswa_data['id'].max() + 1 if not mahasiswa_data.empty else 1

        # Cek apakah mahasiswa dengan email yang sama sudah ada
        if any(mahasiswa_data['email'] == email):
            return "Mahasiswa dengan email ini sudah ada!"

        # Buat data baru
        data = {
            "id": new_id,
            "name": name,
            "email": email,
            "prodi": prodi
        }
        
        new_entry = pd.DataFrame([data])
        
        # Gabungkan data yang ada dengan data baru
        combined_data = pd.concat([mahasiswa_data, new_entry], ignore_index=True)
        
        # Simpan data gabungan ke sheet
        save_data(combined_data, 'mahasiswa')
        
        return f"Mahasiswa {name} berhasil ditambahkan dengan ID {new_id}."

    @rpc(Integer, Unicode, Unicode, Unicode, _returns=Unicode)
    def update_mahasiswa(self, id, name, email, prodi):
        mahasiswa_data = read_data().get('mahasiswa', pd.DataFrame())
        
        # Pastikan mahasiswa ditemukan
        if id not in mahasiswa_data['id'].values:
            return "Mahasiswa tidak ditemukan!"

        # Update data mahasiswa
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'name'] = name
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'email'] = email
        mahasiswa_data.loc[mahasiswa_data['id'] == id, 'prodi'] = prodi
        
        # Simpan perubahan
        save_data(mahasiswa_data, 'mahasiswa')
        
        return f"Mahasiswa dengan ID {id} berhasil diperbarui."

    @rpc(Integer, _returns=Unicode)
    def delete_mahasiswa(self, id):
        mahasiswa_data = read_data().get('mahasiswa', pd.DataFrame())
        
        # Hapus mahasiswa berdasarkan ID
        if id not in mahasiswa_data['id'].values:
            return "Mahasiswa tidak ditemukan!"
        
        mahasiswa_data = mahasiswa_data[mahasiswa_data['id'] != id]
        
        # Simpan perubahan
        save_data(mahasiswa_data, 'mahasiswa')
        
        return f"Mahasiswa dengan ID {id} berhasil dihapus."

def read_data():
    return pd.read_excel(EXCEL_FILE, sheet_name=None)

def save_data(data, sheet_name):
    # Simpan data ke sheet
    with pd.ExcelWriter(EXCEL_FILE, engine='openpyxl', mode='w') as writer:
        data.to_excel(writer, sheet_name=sheet_name, index=False)

# Membuat aplikasi SOAP
application = Application([MahasiswaService],
                          tns='spyne.examples.hello.soap',
                          in_protocol=Soap11(),
                          out_protocol=Soap11())

if __name__ == '__main__':
    from wsgi import WSGIServer
    server = WSGIServer(application)
    server.run()
