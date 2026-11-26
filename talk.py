import streamlit as st
import streamlit.components.v1 as components
import pymysql
import hashlib
from google import genai
import speech_recognition as sr   # ✅ NEW

st.set_page_config(page_title="NeuroTalk AI", page_icon="🧠", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--ink:#eef4ff;--muted:#a6b3ca;--mint:#8ef0d0;--violet:#a79bff}
.stApp{background:radial-gradient(ellipse at 82% 5%,#252353 0,transparent 38%),linear-gradient(135deg,#0b1020,#111a2e 58%,#101527);color:var(--ink);font-family:'DM Sans',sans-serif}
[data-testid="stHeader"]{background:transparent}[data-testid="stSidebar"]{background:#0b1020;border-right:1px solid rgba(255,255,255,.08)}
.block-container{padding-top:2.5rem;max-width:1160px}.brand{font:700 1.05rem 'Manrope',sans-serif;color:var(--ink);margin-bottom:3rem}.brand span{color:var(--mint)}
.eyebrow{display:inline-flex;align-items:center;gap:9px;padding:8px 13px;border:1px solid rgba(142,240,208,.24);border-radius:99px;color:#baf5e3;background:rgba(142,240,208,.07);font-size:.79rem;letter-spacing:.04em}.eyebrow:before{content:'';width:7px;height:7px;border-radius:50%;background:var(--mint);box-shadow:0 0 12px var(--mint)}
.hero-title{font:800 clamp(2.8rem,6vw,5.35rem)/1.04 'Manrope',sans-serif;letter-spacing:-.065em;color:var(--ink);margin:22px 0 18px;animation:rise .8s ease both}.hero-title span{background:linear-gradient(95deg,var(--mint),#b0c7ff 55%,var(--violet));-webkit-background-clip:text;background-clip:text;color:transparent}
.hero-copy{max-width:590px;color:var(--muted);font-size:1.08rem;line-height:1.8;animation:rise .9s .08s ease both}
.feature-card{height:100%;min-height:146px;padding:22px;border:1px solid rgba(255,255,255,.09);border-radius:18px;background:linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.025));transition:transform .25s ease,border-color .25s ease,background .25s ease}.feature-card:hover{transform:translateY(-6px);border-color:rgba(142,240,208,.35);background:rgba(255,255,255,.09)}
.feature-icon{font-size:1.5rem;margin-bottom:12px}.feature-title{color:var(--ink);font:700 1rem 'Manrope',sans-serif;margin-bottom:7px}.feature-copy{color:var(--muted);font-size:.88rem;line-height:1.55}.welcome-note{color:#8090aa;font-size:.82rem;margin-top:1.3rem}
div.stButton>button{border-radius:12px!important;font-weight:700!important;transition:transform .2s ease,box-shadow .2s ease,background .2s ease!important}
div.stButton>button[kind="secondary"]{background:rgba(255,82,99,.12)!important;color:#ffe3e6!important;border:1px solid rgba(255,105,118,.52)!important}
div.stButton>button[kind="secondary"]:hover{background:rgba(255,82,99,.22)!important;border-color:#ff6976!important;color:#fff!important}
div.stButton>button[kind="primary"]{background:#ef4052!important;color:#fff!important;border:1px solid #ef4052!important}
div.stButton>button[kind="primary"]:hover{background:#ff5b69!important;border-color:#ff5b69!important;box-shadow:0 8px 26px rgba(239,64,82,.28)!important}
div.stButton>button:hover{transform:translateY(-2px)}
.auth-heading{font:800 clamp(1.85rem,3vw,2.45rem)/1.15 'Manrope',sans-serif;color:var(--ink);letter-spacing:-.045em;margin:0 0 8px;white-space:nowrap}.auth-copy{color:var(--muted);margin:0 0 24px;line-height:1.65}
[data-testid="stTextInput"] label{color:#dce7fa!important;font-weight:600!important;font-size:.92rem!important}
[data-testid="stTextInput"] input,[data-testid="stTextInput"] [data-baseweb="input"]{background:rgba(7,12,25,.72)!important;border:1px solid rgba(177,196,225,.24)!important;border-radius:11px!important;color:#f5f8ff!important;min-height:48px!important}
[data-testid="stTextInput"] input:focus{border-color:#8ef0d0!important;box-shadow:0 0 0 3px rgba(142,240,208,.13)!important}
[data-testid="stTextInput"] input::placeholder{color:#a6b3ca!important;opacity:1!important}
[data-testid="stVerticalBlockBorderWrapper"]{border-color:rgba(179,198,229,.16)!important;border-radius:22px!important;background:linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.025))!important}
[data-testid="stBottom"],[data-testid="stBottom"]>div,[data-testid="stBottomBlockContainer"]{background:linear-gradient(180deg,rgba(11,16,32,0),#0b1020 28%)!important}
[data-testid="stChatInput"]{background:#151d30!important;border:1px solid rgba(255,82,99,.75)!important;border-radius:14px!important}
[data-testid="stChatInput"] textarea{background:transparent!important;color:#111827!important;-webkit-text-fill-color:#111827!important;caret-color:#111827!important}
[data-testid="stChatInput"] textarea::placeholder{color:#667085!important;-webkit-text-fill-color:#667085!important;opacity:1!important}
[data-testid="stChatInput"] button{background:#ef4052!important;color:#fff!important;border:0!important;border-radius:10px!important}
[data-testid="stChatInput"] button:hover{background:#ff5b69!important;color:#fff!important}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] strong{color:#eef4ff!important}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] a{color:#ff9aa4!important}
[data-testid="stAlert"]{background:rgba(239,64,82,.15)!important;border:1px solid rgba(255,91,105,.68)!important;border-radius:14px!important;color:#ffb4bb!important}
[data-testid="stAlert"] *,[data-testid="stAlert"] p,[data-testid="stAlert"] svg{color:#ffb4bb!important;fill:#ffb4bb!important}
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}@media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# SESSION
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# -----------------------------
# PASSWORD HASH
# -----------------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -----------------------------
# DATABASE
# -----------------------------
def get_db():
    try:
        return pymysql.connect(                             
            host="127.0.0.1",
            user="root",
            password="blessyouharman8102004",
            database="neurotalk_ai"
        )
    except Exception as e:
        st.error(f"DB Error: {e}")
        return None

# -----------------------------
# SIGNUP
# -----------------------------
def signup_user(username, password):
    conn = get_db()
    if conn is None:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password)
            )
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Signup error: {e}")
        return False
    finally:
        conn.close()

# -----------------------------
# LOGIN
# -----------------------------
def login_user(username, password):
    conn = get_db()
    if conn is None:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE username=%s AND password=%s",
                (username, password)
            )
            return cursor.fetchone() is not None
    except Exception as e:
        st.error(f"Login error: {e}")
        return False
    finally:
        conn.close()

# -----------------------------
# GEMINI
# -----------------------------
model = None

api_key = "AIzaSyCiCap33ysnurYqCIVZLoOxE7NweP1F71Y"   # ⚠️ replace

if api_key:
    try:
        client = genai.Client(api_key=api_key)
        model = client
    except Exception as e:
        st.warning(f"AI Error: {e}")

# -----------------------------
# 🎤 SPEECH FUNCTION (NEW)
# -----------------------------
def speech_to_text():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        st.success(f"You said: {text}")
        return text
    except:
        st.error("Could not understand audio")
        return None

# -----------------------------
# UI
# -----------------------------
def go_to_login():
    st.session_state.menu = "Login"

def go_to_signup():
    st.session_state.menu = "Signup"

choice = st.sidebar.selectbox("Menu", ["Home", "Login", "Signup"], key="menu")

if not st.session_state.logged_in:

    if choice == "Home":
        st.markdown('<div class="brand">🧠 Neuro<span>Talk</span> AI</div>', unsafe_allow_html=True)
        st.markdown('<div class="eyebrow">A calmer way to explore your thoughts</div><h1 class="hero-title">Meet your mind<br>with <span>curiosity.</span></h1><p class="hero-copy">A thoughtful AI companion for questions, ideas, and everyday discoveries. Start a conversation and see where your curiosity takes you.</p>', unsafe_allow_html=True)
        action1, action2 = st.columns(2)
        with action1:
            st.button("Get started →", type="primary", on_click=go_to_signup, use_container_width=True)
        with action2:
            st.button("I have an account", on_click=go_to_login, use_container_width=True)
        st.markdown('<div class="welcome-note">Your next great question is a good place to begin.</div>', unsafe_allow_html=True)
        components.html("""
        <div style="height:330px;position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.1);border-radius:26px;background:radial-gradient(circle at 50% 48%,rgba(142,240,208,.15),transparent 34%),linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.015));">
        <canvas id="neuro-canvas" style="position:absolute;inset:0;width:100%;height:100%"></canvas><div style="position:absolute;inset:0;display:grid;place-items:center;pointer-events:none"><div style="font:56px sans-serif;animation:float 4s ease-in-out infinite">🧠</div></div><div style="position:absolute;bottom:20px;left:22px;color:#a6b3ca;font:12px sans-serif;letter-spacing:.12em;text-transform:uppercase">Ideas in motion</div></div>
        <style>@keyframes float{50%{transform:translateY(-9px)}}</style>
        <script>(()=>{const c=document.getElementById('neuro-canvas'),x=c.getContext('2d');let w,h,p=[];function size(){const r=c.getBoundingClientRect(),d=devicePixelRatio||1;w=r.width;h=r.height;c.width=w*d;c.height=h*d;x.setTransform(d,0,0,d,0,0);p=Array.from({length:36},()=>({x:Math.random()*w,y:Math.random()*h,vx:(Math.random()-.5)*.32,vy:(Math.random()-.5)*.32}))}function draw(){x.clearRect(0,0,w,h);for(const a of p){a.x+=a.vx;a.y+=a.vy;if(a.x<0||a.x>w)a.vx*=-1;if(a.y<0||a.y>h)a.vy*=-1}for(let i=0;i<p.length;i++)for(let j=i+1;j<p.length;j++){let a=p[i],b=p[j],d=Math.hypot(a.x-b.x,a.y-b.y);if(d<92){x.strokeStyle='rgba(142,240,208,'+(1-d/92)*.23+')';x.beginPath();x.moveTo(a.x,a.y);x.lineTo(b.x,b.y);x.stroke()}}for(const a of p){x.fillStyle='rgba(180,201,255,.55)';x.beginPath();x.arc(a.x,a.y,1.6,0,7);x.fill()}requestAnimationFrame(draw)}size();new ResizeObserver(size).observe(c);draw()})();</script>
        """, height=340, scrolling=False)
        st.markdown("<br>", unsafe_allow_html=True)
        features = st.columns(3)
        for column, (icon, title, copy) in zip(features, [("💬", "Natural conversations", "Explore ideas at your own pace."), ("🎙️", "Talk it out", "Use your voice to get started."), ("✨", "Curiosity, supported", "Helpful answers for what's on your mind.")]):
            with column:
                st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><div class="feature-title">{title}</div><div class="feature-copy">{copy}</div></div>', unsafe_allow_html=True)
        st.stop()

    elif choice == "Signup":
        _, form_col, _ = st.columns([1, 2.2, 1])
        with form_col:
            with st.container(border=True):
                st.markdown('<div class="auth-heading">Create your account</div><p class="auth-copy">Join NeuroTalk and start exploring your thoughts with a little help.</p>', unsafe_allow_html=True)
                u = st.text_input("Username", placeholder="Choose a username", key="signup_username")
                p = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
                if st.button("Create account", type="primary", use_container_width=True):
                    if not u or not p:
                        st.warning("Enter a username and password to continue.")
                    elif signup_user(u, hash_password(p)):
                        st.success("Account created. Choose Login from the menu to sign in.")
                    else:
                        st.error("Signup failed. That username may already be in use.")
                st.caption("Already have an account? Choose **Login** from the menu.")

    elif choice == "Login":
        _, form_col, _ = st.columns([1, 2.2, 1])
        with form_col:
            with st.container(border=True):
                st.markdown('<div class="auth-heading">Welcome back</div><p class="auth-copy">Sign in to pick up where your curiosity left off.</p>', unsafe_allow_html=True)
                u = st.text_input("Username", placeholder="Enter your username", key="login_username")
                p = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
                if st.button("Sign in", type="primary", use_container_width=True):
                    if login_user(u, hash_password(p)):
                        st.session_state.logged_in = True
                        st.session_state.username = u
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")
                st.caption("New to NeuroTalk? Choose **Signup** from the menu to create an account.")

    st.stop()

# -----------------------------
# AFTER LOGIN
# -----------------------------
st.success(f"✨ **_Welcome {st.session_state.username}_**")

if st.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# -----------------------------
# 🎤 MIC BUTTON (NEW)
# -----------------------------
spoken_text = None
if st.button("🎤 Speak"):
    spoken_text = speech_to_text()

# -----------------------------
# CHAT
# -----------------------------
msg = st.chat_input("Ask something...")

# 🎤 Override if voice used
if spoken_text:
    msg = spoken_text

if msg:
    st.chat_message("user").write(msg)

    msg_lower = msg.lower()

    # CUSTOM RESPONSES
    if any(q in msg_lower for q in [
        "who built you",
        "who created you",
        "who made you"
    ]):
        reply = "I am the creation of Harmandeep Kaur ❤️"

    elif "who do you think harmandeep" in msg_lower:
     reply = "My creator Harmandeep is madly in love with her bestfriend Miss Sneha Verma 💖"

    else:
        if model:
            try:
                with st.spinner("Thinking..."):
                    response = model.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=msg
                    )
                    reply = getattr(response, "text", None)

                    if not reply:
                        reply = str(response)

            except Exception as e:
                reply = f"AI error: {e}"
        else:
            reply = "AI not configured"

    st.chat_message("assistant").write(reply) 
