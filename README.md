# 🧠 AI News Dashboard

🔍 **Real World Problem**: During my internship, I was asked by my managers to track and analyze current AI news. However, manually collecting news was time-consuming and unsustainable.

🚀 **My Solution**: I developed a dashboard that pulls news using NewsAPI, automatically performs sentiment analysis, and provides an interactive interface with Streamlit.

---

## 📌 Features
- 🔄 Automatic news extraction (NewsAPI)
- 💬 Sentiment analysis (TextBlob / VADER)
- 🧭 Keyword search
- 📊 Beautiful visualization interface (Streamlit)
- 📁 All parts of the code are written modularly

---

## 🛠️ Technologies Used
- Python, Streamlit
- TextBlob / NLTK
- NewsAPI
- Matplotlib / Seaborn

---

## 🖥️ Demo

![demo](images/demo.gif)

---

## 🧪 How to Run?

```bash
git clone https://github.com/hasangumus/ai-news-dashboard.git
cd ai-news-dashboard
pip install -r requirements.txt
streamlit run app.py
