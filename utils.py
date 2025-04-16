import streamlit as st
import requests
import json
from config import NEWSAPI_KEY, NEWSAPI_BASE_URL, SENTIMENT_THRESHOLD_POSITIVE, SENTIMENT_THRESHOLD_NEGATIVE
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import pandas as pd
from datetime import datetime
from dateutil import parser  # Tarih parse etmek için

# --- NLTK VADER İndirme Kontrolü ---
# VADER lexicon'ının indirilip indirilmediğini kontrol et, değilse indir.
# Bu, ilk çalıştırmada veya farklı ortamlarda önemlidir.
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except (OSError, LookupError):  # Corrected exception handling
    st.info("VADER lexicon indiriliyor...")
    try:
        nltk.download('vader_lexicon')
        st.success("VADER lexicon başarıyla indirildi.")
    except Exception as e:
        st.error(f"VADER lexicon indirilemedi: {e}")
        # Lexicon olmadan duygu analizi çalışmaz, uygulamayı durdurabiliriz
        st.stop()
except Exception as e:
    st.warning(f"NLTK kontrolü sırasında beklenmedik hata: {e}")


# --- Haber Çekme Fonksiyonu ---
# Cache: Aynı parametrelerle yapılan isteklerin sonuçlarını 30dk sakla
@st.cache_data(ttl=1800, show_spinner="NewsAPI'den haberler çekiliyor...")
def fetch_news(topic: str, language: str = 'en', page_size: int = 10, sort_by: str = 'relevancy') -> tuple[list, list]:
    """
    NewsAPI'den belirtilen konu, dil ve ayarlara göre haberleri çeker.
    Haber listesini ve olası hata/uyarı mesajlarını tuple olarak döndürür.
    """
    if not NEWSAPI_KEY:
        return [], ["❌ Hata: NewsAPI anahtarı bulunamadı. Lütfen .env dosyasını kontrol edin veya Streamlit secrets ayarlayın."]

    params = {
        "q": topic,
        "apiKey": NEWSAPI_KEY,
        "pageSize": min(page_size, 100), # API max 100 izin verir
        "sortBy": sort_by,
        "language": language
    }
    articles = []
    errors = []

    try:
        response = requests.get(NEWSAPI_BASE_URL, params=params, timeout=15) # Timeout ekle

        # HTTP Hata Kodlarını Kontrol Et
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("status") == "ok":
                    articles = data.get("articles", [])
                    if not articles:
                        errors.append(f"ℹ️ '{topic}' konusu için {language} dilinde haber bulunamadı.")
                else:
                    # API kendi içinde hata döndürdüyse (örn. parametre hatası)
                    errors.append(f"❌ NewsAPI Hatası: {data.get('code')} - {data.get('message')}")
            except json.JSONDecodeError:
                errors.append(f"❌ Hata: NewsAPI'den gelen yanıt JSON formatında değil.")
        # Sık karşılaşılan API hata kodlarını ele al
        elif response.status_code == 400:
             errors.append(f"❌ API Hatası (400): Geçersiz istek parametreleri. Lütfen girdilerinizi kontrol edin.")
        elif response.status_code == 401:
             errors.append(f"❌ API Hatası (401): Geçersiz API anahtarı. Anahtarınızı kontrol edin.")
        elif response.status_code == 429:
             errors.append(f"❌ API Hatası (429): Çok fazla istek gönderildi. Lütfen biraz bekleyip tekrar deneyin (API limiti aşıldı).")
        elif response.status_code >= 500:
             errors.append(f"❌ API Sunucu Hatası ({response.status_code}): NewsAPI sunucusunda geçici bir sorun olabilir. Lütfen daha sonra tekrar deneyin.")
        else:
             # Diğer HTTP hataları
             errors.append(f"❌ HTTP Hatası: {response.status_code} - {response.reason}")

    except requests.exceptions.Timeout:
        errors.append("❌ Hata: NewsAPI isteği zaman aşımına uğradı.")
    except requests.exceptions.ConnectionError:
        errors.append("❌ Hata: NewsAPI'ye bağlanılamadı. İnternet bağlantınızı kontrol edin.")
    except requests.exceptions.RequestException as e:
        errors.append(f"❌ Genel Ağ Hatası: {e}")
    except Exception as e:
         errors.append(f"❌ Beklenmedik Hata: {e}")

    return articles, errors

# --- Duygu Analizi Fonksiyonu ---
@st.cache_resource # Analyzer objesini cache'le
def get_sentiment_analyzer():
    """VADER Sentiment Analyzer objesini yükler ve döndürür."""
    return SentimentIntensityAnalyzer()

def analyze_sentiment_vader(text: str) -> tuple[str, float]:
    """
    Verilen metnin VADER kullanarak duygu skorunu ve etiketini döndürür.
    Döndürülenler: (Etiket ('Olumlu', 'Olumsuz', 'Nötr'), Compound Skoru)
    """
    if not isinstance(text, str) or not text.strip():
        return "Nötr", 0.0  # Boş veya geçersiz metin için nötr dön

    analyzer = get_sentiment_analyzer()
    try:
        vs = analyzer.polarity_scores(text)
        compound_score = vs['compound']

        if compound_score >= SENTIMENT_THRESHOLD_POSITIVE:
            return "Olumlu", compound_score
        elif compound_score <= SENTIMENT_THRESHOLD_NEGATIVE:
            return "Olumsuz", compound_score
        else:
            return "Nötr", compound_score
    except Exception as e:
        # Nadiren de olsa VADER hatası olabilir
        st.warning(f"Duygu analizi sırasında hata: {e}")
        return "Nötr", 0.0


# --- Yardımcı Fonksiyon: Tarih Formatlama ---
def format_datetime(date_string: str) -> str:
    """ISO formatındaki tarih string'ini daha okunaklı hale getirir."""
    if not date_string:
        return "Tarih Yok"
    try:
        # Tarihi parse et
        dt_object = parser.isoparse(date_string)
        # Türkiye saatine göre formatla (veya sadece tarih/saat)
        # Yerelleştirme için daha gelişmiş kütüphaneler kullanılabilir ama basit tutalım
        return dt_object.strftime("%d %B %Y, %H:%M") # Örn: 25 Aralık 2023, 15:30
    except Exception:
        # Parse edilemezse orijinal string'i (veya bir kısmını) dön
        return date_string.split('T')[0] # Sadece tarih kısmı