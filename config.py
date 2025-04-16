# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# NewsAPI Ayarları
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
NEWSAPI_BASE_URL = "https://newsapi.org/v2/everything" # Veya 'top-headlines' endpoint'i

# Varsayılan Arama Parametreleri
DEFAULT_TOPIC = "artificial intelligence"
DEFAULT_LANGUAGE = "en" # Türkçe haberler için 'tr' dene, ancak API desteği daha az olabilir
DEFAULT_PAGE_SIZE = 10
AVAILABLE_LANGUAGES = {"English": "en", "Türkçe": "tr", "Deutsch": "de", "Français": "fr"}
SORT_BY_OPTIONS = ["relevancy", "popularity", "publishedAt"]

# Duygu Analizi Ayarları (VADER için)
# Compound skoruna göre eşik değerleri
SENTIMENT_THRESHOLD_POSITIVE = 0.05
SENTIMENT_THRESHOLD_NEGATIVE = -0.05

# UI Ayarları
MAX_ARTICLES_TO_DISPLAY = 50 # Maksimum kaç haber gösterilecek