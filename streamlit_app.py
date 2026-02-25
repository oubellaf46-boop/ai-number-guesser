"""
AI NUMBER GUESSER - Version Web Streamlit
Développé par: Fatima Zahra Oubella
Email: fatimazahra.oubella@etu.uae.ac.ma
"""

import streamlit as st
import math

# Configuration de la page
st.set_page_config(
    page_title="AI Number Guesser - Fatima Zahra Oubella",
    page_icon="🤖",
    layout="centered"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
        text-align: center;
    }
    .question-box {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton > button {
        width: 100%;
        height: 3rem;
        font-size: 1.2rem;
        font-weight: bold;
        border-radius: 10px;
        border: none;
    }
    .footer {
        text-align: center;
        color: white;
        margin-top: 3rem;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown("""
<div class="header">
    <h1>🤖 AI NUMBER GUESSER</h1>
    <p>Think of a positive number, I'll guess it!</p>
</div>
""", unsafe_allow_html=True)

# Informations personnelles
st.markdown(f"""
<div class="info-card">
    <h3>👩‍💻 Fatima Zahra Oubella</h3>
    <p>📧 fatimazahra.oubella@etu.uae.ac.ma</p>
    <p>📍 Tangier, Morocco | 🏫 Abdelmalek Essaâdi University</p>
</div>
""", unsafe_allow_html=True)

# Initialisation des variables
if 'step' not in st.session_state:
    st.session_state.step = 'start'
    st.session_state.lower = 0
    st.session_state.upper = 1
    st.session_state.guesses = 0
    st.session_state.games = 0
    st.session_state.total_guesses = 0
    st.session_state.best = float('inf')

# Statistiques
if st.session_state.games > 0:
    avg = st.session_state.total_guesses / st.session_state.games
else:
    avg = 0
best = st.session_state.best if st.session_state.best != float('inf') else '-'

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Games", st.session_state.games)
with col2:
    st.metric("Average", f"{avg:.1f}")
with col3:
    st.metric("Best", best)

# Jeu
if st.session_state.step == 'start':
    st.markdown("""
    <div class="question-box">
        ✨ Click 'New Game' to start!
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🎮 NEW GAME", use_container_width=True):
        st.session_state.step = 'finding'
        st.session_state.lower = 0
        st.session_state.upper = 1
        st.session_state.guesses = 0
        st.rerun()

elif st.session_state.step == 'finding':
    st.markdown(f"""
    <div class="question-box">
        ❓ Is your number between 0 and {st.session_state.upper}?
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✓ YES", use_container_width=True):
            st.session_state.guesses += 1
            st.session_state.step = 'guessing'
            st.session_state.max_range = st.session_state.upper
            st.rerun()
    with col2:
        if st.button("✗ NO", use_container_width=True):
            st.session_state.guesses += 1
            st.session_state.lower = st.session_state.upper + 1
            st.session_state.upper *= 2
            st.rerun()

elif st.session_state.step == 'guessing':
    if st.session_state.lower == st.session_state.upper:
        st.balloons()
        st.success(f"🎉 VICTORY! Your number is {st.session_state.lower}!")
        
        # Stats
        st.session_state.games += 1
        st.session_state.total_guesses += st.session_state.guesses
        if st.session_state.guesses < st.session_state.best:
            st.session_state.best = st.session_state.guesses
        
        if st.button("🔄 PLAY AGAIN", use_container_width=True):
            st.session_state.step = 'start'
            st.rerun()
    else:
        mid = (st.session_state.lower + st.session_state.upper) // 2
        st.markdown(f"""
        <div class="question-box">
            ❓ Is your number between {st.session_state.lower} and {mid}?
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ YES", key="yes", use_container_width=True):
                st.session_state.guesses += 1
                st.session_state.upper = mid
                st.rerun()
        with col2:
            if st.button("✗ NO", key="no", use_container_width=True):
                st.session_state.guesses += 1
                st.session_state.lower = mid + 1
                st.rerun()

# Boutons de contrôle
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("🔄 RESET", use_container_width=True):
        st.session_state.step = 'start'
        st.session_state.games = 0
        st.session_state.total_guesses = 0
        st.session_state.best = float('inf')
        st.rerun()
with col2:
    if st.button("📧 CONTACT", use_container_width=True):
        st.info("📧 fatimazahra.oubella@etu.uae.ac.ma\n📍 Tangier, Morocco")
with col3:
    if st.button("❌ EXIT", use_container_width=True):
        st.warning("Close this tab to exit")

# Pied de page
st.markdown("""
<div class="footer">
    <p>⚡ Complexity: O(log n) | Developed by Fatima Zahra Oubella</p>
</div>
""", unsafe_allow_html=True)