from flask import Flask, request, jsonify

app = Flask(__name__)

# Geçici veritabanı (Gerçek uygulamada SQLite/PostgreSQL kullanın)
hwid_uses = {}  # {hwid: kalan_kullanım_sayısı}
valid_keys = {"SW-1234-ABCD-5678"}  # Geçerli lisans anahtarları

@app.route('/api/check_license', methods=['POST'])
def check_license():
    data = request.json
    hwid = data.get('hwid')
    
    if not hwid:
        return jsonify({"status": "error", "message": "HWID eksik"}), 400
    
    # HWID daha önce görülmemişse, 2 kullanım hakkı tanı
    if hwid not in hwid_uses:
        hwid_uses[hwid] = 2
    
    remaining = hwid_uses[hwid]
    
    if remaining > 0:
        hwid_uses[hwid] -= 1
        return jsonify({"status": "allowed", "remaining_uses": remaining})
    else:
        return jsonify({"status": "blocked", "message": "Ücretsiz limit doldu"})

@app.route('/api/activate', methods=['POST'])
def activate():
    data = request.json
    hwid = data.get('hwid')
    key = data.get('key')
    
    if key in valid_keys:
        hwid_uses[hwid] = 9999  # Sınırsız yap
        return jsonify({"status": "success", "message": "Lisans aktif"})
    else:
        return jsonify({"status": "error", "message": "Geçersiz anahtar"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)