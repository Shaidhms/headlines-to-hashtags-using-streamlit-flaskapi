# 📰 From Headlines to Hashtags  
**A Social Media Content Generator — Powered by OpenAI ChatGPT 🤖**  

✨ Dreamed, Designed & Delivered by **Shaid** | Guided by **Social Eagle** 🦅  

---

## 📌 Overview  
**From Headlines to Hashtags** turns the day’s top news into ready-to-post social content.  
It fetches fresh headlines (today or the last 2 days) with GPT and helps you generate:  

- Platform-specific posts  
- Multi-post series/threads  
- A content strategy with sentiment & insights  

Built with:  
- **Frontend:** Streamlit  
- **Backend:** Flask API  
- **AI:** OpenAI `gpt-4.1-nano` (news summaries) & `gpt-4.1` (content + strategy)  

---

## ✨ Key Features  

✅ **Fresh News (Today ±2 Days):** GPT generates country + category specific headlines  
✅ **One-Click Post Creation:** Turn any article into optimized social media posts  
✅ **Thread/Series Builder:** Build 1/n, 2/n… style threads from multiple articles  
✅ **Strategy & Sentiment:** Get insights, themes, and posting recommendations  
✅ **Dark/Light Mode:** Toggle instantly, colors adapt everywhere  
✅ **Sticky Footer:** Personalized footer with signature & credits  
✅ **No External News APIs:** 100% GPT-powered (no NewsAPI or RSS needed)  

---

## 🏗️ Architecture  


flowchart TD
    A[Streamlit UI] -->|HTTP localhost| B[Flask API]
    B --> C[OpenAI API (gpt-4.1 / gpt-4.1-nano)]
    C --> D[Generated News + Social Content]

- /generate_news → GPT returns JSON array of fresh news
- /create_social_content → GPT returns platform-specific post
- /create_content_series → GPT produces threaded series
- /analyze_news → GPT returns sentiment & strategy

⸻

🚀 Quick Start

1️⃣ Clone & Install

git clone `https://github.com/Shaidhms/headlines-to-hashtags-using-streamlit-flaskapi.git`
cd headlines-to-hashtags-using-streamlit-flaskapi
pip install -r requirements.txt

2️⃣ Environment Variables

Create a .env file in the project root:

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
NEWS_API_PORT=5001

3️⃣ Run the App

Open two terminals:

Terminal 1 — Start Flask API
python flask_api.py
Terminal 2 — Start Streamlit app
Terminal 2 — Start Streamlit app
streamlit run app.py

	•	Flask API → http://127.0.0.1:5001
	•	Streamlit UI → http://localhost:8501
	•	Streamlit calls Flask API in background to fetch/generate news

⸻

🧠 Models Used
	•	gpt-4.1-nano → fast, low-cost generation of fresh, concise news (JSON)
	•	gpt-4.1 → higher-quality content generation, series, and strategy outputs
🖥️ UI Guide

📰 Fetch News
	•	Select Country + Category
	•	Fetch latest headlines (within 2 days)
	•	Send an article to “Create Content” tab

📝 Create Content
	•	Selected article card shows at the top
	•	Generate platform-specific content (char limit auto-handled)

📊 Series
	•	Select 2+ articles
	•	Generate a connected thread/series

📈 Analytics
	•	Analyze sentiment, themes, and posting strategy

🌙 Theme Toggle
	•	Sidebar toggle for Dark/Light Mode

⸻

🔌 API Endpoints
-	GET /health → {status: "ok"}
-	GET /generate_news?country=us&category=general&limit=5 → [ {title, description, ...}, ... ]
-	POST /create_social_content → { content }
-	POST /create_content_series → { series }
-	POST /analyze_news → { analysis }

⸻

🧪 Tips & Troubleshooting
-	Blank articles? → Check OPENAI_API_KEY validity
- Duplicate titles? → Remove old st.title(...) if using custom HTML header
-	Footer overlaps content? → Keep spacer & bottom padding
-	Timeouts? → Increase timeout in call_api() (app.py)
-	Model costs? → gpt-4.1-nano for cheap news, gpt-4.1 for quality posts

⸻

🗺️ Roadmap
-	Save & export generated posts (CSV/Notion/GDocs)
-	Image suggestions (royalty-free sources)
-	Multi-language support
-	Per-platform hashtag recommendations

⸻

🤝 Acknowledgements
-	Built by: Shaid
-	Mentorship: Social Eagle 🦅
-	AI Platform: OpenAI ChatGPT

⸻

📄 License

MIT — use it, remix it, ship it.
Please keep credit to Shaid & Social Eagle visible.

⸻
