from flask import Blueprint, jsonify, render_template, request

from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError


pages_bp = Blueprint("pages", __name__)
api_bp = Blueprint("api", __name__)


@pages_bp.route("/")
def ana_sayfa():
    return render_template("index.html")


@pages_bp.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@api_bp.route("/sohbet", methods=["POST"])
def sohbet():
    data = request.get_json() or {}

    mesaj = data.get("mesaj")
    gecmis = data.get("gecmis", [])

    if not mesaj:
        return jsonify({
            "basari": False,
            "hata": "Mesaj alanı zorunludur."
        }), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            "basari": True,
            "cevap": cevap
        })

    except AIServiceError as e:
        return jsonify({
            "basari": False,
            "hata": str(e)
        }), 503


@api_bp.route("/leads", methods=["POST"])
def lead_kaydet():
    data = request.get_json() or {}

    isim = data.get("isim")
    telefon = data.get("telefon")
    eposta = data.get("eposta")

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "hata": "İsim ve telefon zorunludur."
        }), 400

    lead_ekle(isim, telefon, eposta)

    return jsonify({
        "basari": True,
        "mesaj": "Kayıt başarıyla oluşturuldu."
    }), 201


@api_bp.route("/leads", methods=["GET"])
def leadleri_getir():
    leadler = tum_leadler()

    return jsonify({
        "basari": True,
        "leadler": leadler
    })
