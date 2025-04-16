# app.py
import streamlit as st

# Set page configuration as the first Streamlit command
st.set_page_config(
    page_title="Google News Güncel Haber Alma",
    page_icon="📰",
    layout="wide",
)

# Other imports
import pandas as pd # İstatistikler veya tablolar için
from config import (
    DEFAULT_TOPIC, DEFAULT_LANGUAGE, DEFAULT_PAGE_SIZE, AVAILABLE_LANGUAGES,
    SORT_BY_OPTIONS, MAX_ARTICLES_TO_DISPLAY
)
from utils import fetch_news, analyze_sentiment_vader, format_datetime
import os # API Key kontrolü için

# --- Kenar Çubuğu (Sidebar) ---
with st.sidebar:
    st.header("🧠 Akıllı Haber Akışı")
    st.markdown("NewsAPI kullanarak güncel haberleri alın ve duygu analizini görün.")
    st.divider()

    # API Anahtarı Kontrolü (Sadece bilgilendirme)
    if not os.getenv("NEWSAPI_KEY"):
        st.error("NewsAPI Anahtarı bulunamadı!")
        st.caption("Lütfen `.env` dosyasına veya Streamlit Secrets'a ekleyin.")

    st.header("📰 Arama Ayarları")
    # Konu Girişi
    topic = st.text_input("Haber Konusu:", value=DEFAULT_TOPIC)
    # Dil Seçimi
    lang_label = st.selectbox("Haber Dili:", options=list(AVAILABLE_LANGUAGES.keys()), index=0)
    language = AVAILABLE_LANGUAGES[lang_label] # Seçilen etiketten dil kodunu al
    # Haber Sayısı
    page_size = st.slider("Maksimum Haber Sayısı:", min_value=5, max_value=MAX_ARTICLES_TO_DISPLAY, value=DEFAULT_PAGE_SIZE, step=5)
    # Sıralama Ölçütü
    sort_by = st.selectbox("Sıralama Ölçütü:", options=SORT_BY_OPTIONS, index=0)
    st.divider()

    # Arama Butonu
    search_button = st.button("🔍 Haberleri Getir")


# --- Ana İçerik Alanı ---
st.title("🧠 Akıllı Haber Akışı")

# Arama butonu tıklandıysa ve konu girildiyse haberleri çek
if search_button and topic:
    # Haberleri çekme fonksiyonunu çağır
    articles, errors = fetch_news(topic, language, page_size, sort_by)

    # Önce hataları göster (varsa)
    if errors:
        for error in errors:
            st.error(error)

    # Haber bulunduysa işlem yap
    if articles:
        st.success(f"'{topic}' konusunda {len(articles)} adet haber bulundu.")
        st.divider()

        # Duygu analizi sonuçlarını toplamak için listeler
        sentiments = []
        sentiment_scores = []

        # Her bir haberi işle ve göster
        for article in articles:
            col1, col2 = st.columns([1, 3]) # Resim için küçük, metin için büyük sütun

            with col1:
                # Resim varsa göster (hata kontrolü ile)
                if article.get('urlToImage'):
                    try:
                        st.image(article['urlToImage'], use_column_width=True)
                    except Exception as img_err:
                        st.caption(f"Resim yüklenemedi: {img_err}")
                else:
                     st.caption("Resim Yok")

            with col2:
                # Başlık
                st.subheader(article.get('title', 'Başlık Yok'))
                # Kaynak ve Tarih
                source_name = article.get('source', {}).get('name', 'Kaynak Yok')
                published_at = format_datetime(article.get('publishedAt'))
                st.caption(f"Kaynak: {source_name} | Yayınlanma: {published_at}")

                # Açıklama (varsa)
                description = article.get('description')
                if description:
                    st.write(description)

                    # --- Duygu Analizi ---
                    sentiment_label, sentiment_score = analyze_sentiment_vader(description)
                    sentiments.append(sentiment_label)
                    sentiment_scores.append(sentiment_score)

                    # Duygu etiketini ve skorunu göster
                    emoji = "🙂" if sentiment_label == "Olumlu" else ("😠" if sentiment_label == "Olumsuz" else "😐")
                    st.markdown(f"**Duygu:** {emoji} {sentiment_label} (Skor: {sentiment_score:.2f})")
                    # --- Duygu Analizi Sonu ---

                # Haberin linki
                if article.get('url'):
                    st.markdown(f"[🔗 Haberin Tamamı]({article['url']})", unsafe_allow_html=True)

            st.divider() # Haberler arasına ayırıcı koy

        # --- Genel Duygu Özeti ---
        if sentiments:
             st.subheader("📊 Genel Duygu Dağılımı")
             sentiment_counts = pd.Series(sentiments).value_counts()
             # Renkleri belirle
             colors = {'Olumlu': 'green', 'Olumsuz': 'red', 'Nötr': 'grey'}
             try:
                st.bar_chart(sentiment_counts, color=[colors.get(x, '#888888') for x in sentiment_counts.index])
             except Exception as chart_err:
                 st.warning(f"Grafik çizilirken hata: {chart_err}")
                 st.write(sentiment_counts) # Grafik çizilemezse veriyi yazdır


    # Haber bulunamadıysa (ve API hatası yoksa)
    elif not errors:
         st.info(f"'{topic}' konusu için {language} dilinde haber bulunamadı.")

# Eğer konu girilmemişse veya buton tıklanmamışsa başlangıç mesajı
elif not topic:
    st.info("Lütfen aramak istediğiniz bir konu girin.")