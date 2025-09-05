# ================================
# GPT News to Social (app.py)
# ================================
import streamlit as st
import requests
import subprocess
import time
import os
import sys
import json

API_PORT = int(os.getenv("NEWS_API_PORT", "5001"))
API_BASE_URL = f"http://127.0.0.1:{API_PORT}"


# ---------- Helpers ----------
def start_flask_api():
    """Start the Flask API in a background process if it's not already running."""
    try:
        api_dir = os.path.dirname(os.path.abspath(__file__))
        api_path = os.path.join(api_dir, "flask_api.py")
        env = os.environ.copy()
        env["NEWS_API_PORT"] = str(API_PORT)
        subprocess.Popen(
            [sys.executable, api_path],
            cwd=api_dir,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            env=env,
        )
        time.sleep(2.5)
    except Exception as e:
        st.error(f"Failed to start Flask API: {e}")


def call_api(path, method="GET", data=None, params=None, timeout=45):
    try:
        url = f"{API_BASE_URL}{path}"
        if method == "GET":
            r = requests.get(url, params=params, timeout=timeout)
        else:
            r = requests.post(url, json=data, timeout=timeout)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}


# ---------- App ----------
def main():
    st.set_page_config(
        page_title="📰 From Headlines to Hashtags",
        page_icon="📰",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar config (includes Dark/Light toggle)
    with st.sidebar:
        st.header("⚙️ Configuration")
        news_category = st.selectbox(
            "Category",
            ["general", "technology", "business", "health", "science", "sports", "entertainment"],
            index=0,
        )
        news_country = st.selectbox(
            "Country", ["us", "in", "uk", "ca", "au", "fr", "de", "jp"], index=0
        )
        platform = st.selectbox(
            "Platform", ["twitter", "linkedin", "instagram", "facebook", "tiktok"], index=0
        )
        tone = st.selectbox(
            "Tone", ["informative", "engaging", "professional", "casual", "humorous"], index=0
        )
        dark_mode = st.toggle("🌙 Dark Mode", value=True)

    # Theme CSS variables
    if dark_mode:
        st.markdown(
            """
            <style>
            :root {
              --bg:#101114; --panel:#1b1d22; --panel-soft:#24272e;
              --text:#f2f2f2; --muted:#c6c6c6; --accent:#e84a5f;
            }
            .stApp { background: var(--bg); color: var(--text); }
            .news-card {
              background: var(--panel); color: var(--text);
              padding: 1rem; border-radius: 12px;
              border-left: 4px solid var(--accent); margin: 1rem 0;
              box-shadow: 0 2px 10px rgba(0,0,0,.35);
            }
            .content-card {
              background: var(--panel-soft); color: var(--text);
              padding: 1rem; border-radius: 12px; border: 1px solid var(--accent);
              margin: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,.35);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <style>
            :root {
              --bg:#ffffff; --panel:#f9f9fb; --panel-soft:#f3f7ff;
              --text:#0f172a; --muted:#475569; --accent:#1f77b4;
            }
            .stApp { background: var(--bg); color: var(--text); }
            .news-card {
              background: var(--panel); color: var(--text);
              padding: 1rem; border-radius: 12px;
              border-left: 4px solid var(--accent); margin: 1rem 0;
              box-shadow: 0 2px 8px rgba(0,0,0,.08);
            }
            .content-card {
              background: var(--panel-soft); color: var(--text);
              padding: 1rem; border-radius: 12px; border: 1px solid var(--accent);
              margin: 1rem 0; box-shadow: 0 2px 8px rgba(0,0,0,.08);
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
   
  

    st.markdown(
    """
    <h1 style='text-align:center; font-size:2.6rem; margin-top:-8px;'>
        📰 From Headlines to Hashtags
    </h1>
    <p style='text-align:center; font-size:1.15rem; color: var(--muted); margin-top:-10px;'>
        A Social Media Content Generator — Powered by OpenAI ChatGPT!
    </p>
    """,
    unsafe_allow_html=True,
    )

   
    # Start API once
    if "api_started" not in st.session_state:
        start_flask_api()
        st.session_state.api_started = True

    tab1, tab2, tab3, tab4 = st.tabs(
        ["📰 Fetch News", "📝 Create Content", "📊 Series", "📈 Analytics"]
    )

    # === Tab 1: Fetch News ===
    with tab1:
        st.header("📰 Fetch News")
        if st.button("🔄 Fetch Latest News", type="primary"):
            with st.spinner("Generating fresh headlines..."):
                data = call_api(
                    "/generate_news",
                    params={"category": news_category, "country": news_country, "limit": 5},
                )
                if data.get("success"):
                    st.session_state.news = data["articles"]
                    st.success(f"Fetched {data['count']} fresh articles")
                else:
                    st.error(data.get("error"))

        if "news" in st.session_state and st.session_state.news:
            for i, art in enumerate(st.session_state.news):
                with st.container():
                    st.markdown(
                        f"""
                        <div class="news-card">
                          <h3 style="margin:.1rem 0 0.6rem 0;">{art.get('title','')}</h3>
                          <p style="margin:.2rem 0; color: var(--muted);">{art.get('source','Unknown')} — {art.get('published_at','')}</p>
                          <p style="margin:.4rem 0 0.6rem 0;">{art.get('description','')}</p>
                          {"<a href='"+art.get("url","")+"' target='_blank'>Read more</a>" if art.get("url") else ""}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        if st.button("📝 Create Content", key=f"create_{i}"):
                            # Save the selected article for Tab 2 to render
                            st.session_state.selected = art
                            st.session_state.show_selected_in_tab2 = True
                            st.success("Selected for Create Content. Open the 'Create Content' tab to continue.")
                    with c2:
                        if art.get("url"):
                            st.link_button("🔗 Open Article", art["url"])

    # === Tab 2: Create Content ===
    with tab2:
        st.header("📝 Create Social Media Content")

        # Show the selected article card right below the title
        if st.session_state.get("selected"):
            art = st.session_state["selected"]
            st.markdown(
                f"""
                <div class="content-card">
                  <h4 style="margin:0 0 .5rem 0;">{art.get('title','(No title)')}</h4>
                  <p style="margin:.25rem 0;"><strong>Source:</strong> {art.get('source','Unknown')}</p>
                  <p style="margin:.25rem 0; opacity:.9;">{art.get('description','')}</p>
                  <small>{art.get('published_at','')}</small>
                  {"<p style='margin-top:.5rem;'><a href='"+art.get("url","")+"' target='_blank'>Read full article</a></p>" if art.get("url") else ""}
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.caption(f"Platform: {platform.title()} • Tone: {tone}")

            if st.button("🚀 Generate Post", type="primary"):
                with st.spinner("Generating post..."):
                    res = call_api(
                        "/create_social_content",
                        method="POST",
                        data={
                            "article": art,
                            "platform": platform,
                            "tone": tone,
                            "include_hashtags": True,
                            "include_link": True,
                        },
                    )
                    if res.get("success"):
                        st.text_area("Generated Content", res["content"], height=180)
                    else:
                        st.error(res.get("error"))
        else:
            st.info("Select an article in the 'Fetch News' tab (click its Create Content button).")

    # === Tab 3: Series ===
    with tab3:
        st.header("📊 Create Content Series")
        if "news" in st.session_state and len(st.session_state.news) >= 2:
            if st.button("🎬 Generate Series"):
                with st.spinner("Creating series..."):
                    res = call_api(
                        "/create_content_series",
                        method="POST",
                        data={
                            "articles": st.session_state.news[:3],
                            "platform": platform,
                            "theme": "Daily Update",
                            "tone": tone,
                        },
                    )
                    if res.get("success"):
                        st.text_area("Series Content", res["series"], height=320)
                    else:
                        st.error(res.get("error"))
        else:
            st.info("Fetch at least 2 articles to build a series.")

    # === Tab 4: Analytics ===
    with tab4:
        st.header("📈 News Analysis & Strategy")
        if "news" in st.session_state and st.session_state.news:
            if st.button("🔍 Analyze"):
                with st.spinner("Analyzing..."):
                    res = call_api("/analyze_news", method="POST", data={"articles": st.session_state.news})
                    if res.get("success"):
                        st.text_area("Analysis", res["analysis"], height=320)
                    else:
                        st.error(res.get("error"))
        else:
            st.info("Fetch articles first to run analytics.")


# --- Spacer so content never hides behind the sticky footer ---
st.markdown("<div style='height:72px'></div>", unsafe_allow_html=True)

# --- Sticky Footer (centered text, theme-aware) ---
st.markdown(
    """
    <style>
        /* Ensure the main content leaves space for the footer */
        section.main > div.block-container { padding-bottom: 80px; }

        /* Footer bar */
        .app-sticky-footer {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            width: 100%;
            z-index: 9999; /* stay above cards/buttons */
            padding: 10px 16px;
            box-sizing: border-box;

            text-align: Center;  /* <-- centers the text */
            font-size: 0.92rem;

            background: var(--panel, #0e1117);
            color: var(--text, #f2f2f2);
            border-top: 1px solid var(--muted, #3a3a3a);
            box-shadow: 0 -2px 10px rgba(0,0,0,.25);
        }

        /* Footer links (optional) */
        .app-sticky-footer a {
            color: inherit;
            text-decoration: underline;
            text-underline-offset: 2px;
            opacity: .9;
        }

        /* Small screens */
        @media (max-width: 640px) {
            .app-sticky-footer { font-size: 0.88rem; padding: 10px; }
        }
    </style>

    <div class="app-sticky-footer">
         ✨ Dreamed, Designed & Delivered by <b>Shaid</b>⚡ | Guided by <b>Social Eagle</b> 🦅
    </div>
    """,
    unsafe_allow_html=True,
)
if __name__ == "__main__":
    main()