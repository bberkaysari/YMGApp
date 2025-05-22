from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
import time
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
CORS(app)

# Ortam değişkeni varsayılanla birlikte alınsın
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:123456@db:5432/personeldb')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Personel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(50), nullable=False)
    soyad = db.Column(db.String(50), nullable=False)
    pozisyon = db.Column(db.String(50), nullable=False)

@app.route('/api/personel', methods=['GET'])
def get_personel():
    try:
        data = Personel.query.all()
        return jsonify([{'id': p.id, 'ad': p.ad, 'soyad': p.soyad, 'pozisyon': p.pozisyon} for p in data])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/personel', methods=['POST'])
def add_personel():
    try:
        data = request.get_json()
        p = Personel(ad=data['ad'], soyad=data['soyad'], pozisyon=data['pozisyon'])
        db.session.add(p)
        db.session.commit()
        return jsonify({'id': p.id, 'ad': p.ad, 'soyad': p.soyad, 'pozisyon': p.pozisyon}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        for i in range(10):
            try:
                db.create_all()
                print("Veritabanı bağlantısı başarılı.")
                break
            except OperationalError as e:
                print("Veritabanı hazır değil, 2 saniye bekleniyor...", str(e))
                time.sleep(2)

    app.run(host='0.0.0.0', port=9090)
