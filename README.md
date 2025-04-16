# Google News Güncel Haber Alma ve Duygu Analizi

Bu proje, **Google News API** kullanarak güncel haberleri çekmek ve **NLTK VADER** duygu analizi ile haberlerin duygusal tonunu belirlemek için geliştirilmiştir. Proje, **Streamlit** kullanılarak bir web uygulaması olarak sunulmaktadır.

## Özellikler

- **Haber Çekme**: Belirli bir konu, dil ve sıralama kriterine göre haberleri Google News API'den çeker.
- **Duygu Analizi**: Haberlerin metinlerini analiz ederek "Olumlu", "Olumsuz" veya "Nötr" olarak sınıflandırır.
- **Kullanıcı Dostu Arayüz**: Streamlit ile kolayca kullanılabilir bir web arayüzü sağlar.
- **Gerçek Zamanlı Güncellemeler**: Haber sonuçları ve analizler dinamik olarak güncellenir.

---

## Kurulum

### Gereksinimler

- Python 3.9 veya üzeri
- Aşağıdaki Python kütüphaneleri:
  - `streamlit`
  - `requests`
  - `nltk`
  - `pandas`
  - `python-dateutil`

### Adımlar

1. **Proje Deposu**: Bu projeyi bilgisayarınıza klonlayın veya indirin.
   ```bash
   git clone https://github.com/kullanici/google-news-duygu-analizi.git
   cd google-news-duygu-analizi

**Gerekli Kütüphaneleri Yükleyin**:
1.     
1.     pip install \-r requirements.txt
1.     
1. 3.  **NLTK VADER Lexicon'u İndirin**: İlk çalıştırmada, uygulama otomatik olarak VADER lexicon'u indirir. Ancak manuel olarak indirmek isterseniz:
1.     
1.     import nltk
1.     
1.     nltk.download('vader\_lexicon')
1.     
1. 4.  **API Anahtarı Ayarları**:
1.     
1.     * *   `config.py` dosyasını oluşturun ve aşağıdaki bilgileri ekleyin:
1.     *     
1.     *     NEWSAPI\_KEY \= "Sizin\_NewsAPI\_Anahtarınız"
1.     *     
1.     *     NEWSAPI\_BASE\_URL \= "https://newsapi.org/v2/everything"
1.     *     
1.     *     SENTIMENT\_THRESHOLD\_POSITIVE \= 0.05
1.     *     
1.     *     SENTIMENT\_THRESHOLD\_NEGATIVE \= \-0.05
1.     *     
1. 5.  **Uygulamayı Çalıştırın**:
1.     
1.     streamlit run app.py
1.     

* * *

## Kullanım

1. 1.  **Konu Seçimi**: Uygulama arayüzünde bir konu girin (örneğin: "teknoloji", "spor").
1. 2.  **Dil ve Sıralama**: Haberlerin dilini ve sıralama kriterini seçin.
1. 3.  **Sonuçlar**: Haberler listelenir ve her haberin duygusal analizi gösterilir.

* * *

## Dosya Yapısı

.

├── \[app.py\](http://\_vscodecontentref\_/0)                # Ana Streamlit uygulama dosyası

├── \[utils.py\](http://\_vscodecontentref\_/1)              # Yardımcı fonksiyonlar (haber çekme, duygu analizi vb.)

├── \[config.py\](http://\_vscodecontentref\_/2)             # API anahtarları ve eşik değerleri

├── \[requirements.txt\](http://\_vscodecontentref\_/3)      # Gerekli Python kütüphaneleri

└── README.md             # Proje açıklaması

* * *

## Örnek Ekran Görüntüsü

<img alt="Ekran Görüntüsü" src="https://via.placeholder.com/800x400?text=Ekran+Görüntüsü">

* * *

## Katkıda Bulunma

Katkıda bulunmak isterseniz, lütfen bir **pull request** gönderin veya bir **issue** açın.

* * *

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına göz atabilirsiniz.

Bu \`README.md\` dosyası, projenizin temel özelliklerini, kurulum adımlarını ve kullanımını açıkça anlatır. Eğer başka bir şey eklemek isterseniz, lütfen belirtin! 😊