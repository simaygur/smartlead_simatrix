import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "simatrix-secret-key")
    DATABASE_URL = os.environ.get("DATABASE_URL", "leads.db")
    GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
    AI_PROVIDER = os.environ.get("AI_PROVIDER", "groq")
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    BUSINESS_CONTEXT = """
    Sen SIMATRIX Yazılım ve Danışmanlık şirketinin yapay zekâ asistanısın.

    Müşterilere şirketin yazılım geliştirme ve danışmanlık hizmetleri hakkında yardımcı ol.

    Web sitesi, mobil uygulama, özel yazılım ve yazılım danışmanlığı konularındaki soruları yanıtla.

    Türkçe, profesyonel, anlaşılır ve samimi bir dil kullan.

    Potansiyel müşterileri projeleri hakkında görüşmek için isim ve telefon bilgilerini bırakmaya yönlendir.

    Bilmediğin fiyatları, teslim sürelerini veya hizmet detaylarını uydurma.
    """


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig
}