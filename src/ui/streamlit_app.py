"""
Beautiful and aesthetic Streamlit UI for GlobalMind
Multilingual mental health support interface
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import numpy as np
from PIL import Image
import io
import base64
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.translations import get_translation, get_language_name, get_supported_languages
from ui.friend_bot import friend_bot_page
from ui.global_chat import global_chat
from ui.music_lounge import music_lounge
from ui.community_hub import community_hub

# Configure page
st.set_page_config(
    page_title="GlobalMind - Mental Health Support",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
def load_css():
    """Load custom CSS for therapeutic and beautiful design"""
    st.markdown("""
    <style>
    /* Import Google Fonts for better typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global font and color improvements */
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #1a202c !important;
    }
    
    /* Main app styling with softer background */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #cbd5e0 100%) !important;
        background-attachment: fixed;
    }
    
    /* Streamlit specific overrides for better readability */
    .stMarkdown, .stMarkdown p, .stText {
        color: #2d3748 !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Headers with better contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #1a202c !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
    }
    
    h1 { color: #2b6cb0 !important; font-size: 2.5rem !important; }
    h2 { color: #2c5282 !important; font-size: 2rem !important; }
    h3 { color: #2a4365 !important; font-size: 1.5rem !important; }
    
    /* Sidebar styling with better contrast */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2d3748 0%, #4a5568 100%) !important;
        color: #f7fafc !important;
    }
    
    .sidebar .sidebar-content .stMarkdown {
        color: #f7fafc !important;
    }
    
    .sidebar .sidebar-content h1, .sidebar .sidebar-content h2, .sidebar .sidebar-content h3 {
        color: #ffffff !important;
    }
    
    /* Header styling with improved readability */
    .header {
        background: rgba(255, 255, 255, 0.98) !important;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06) !important;
        backdrop-filter: blur(10px);
        text-align: center;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Chat container with better contrast */
    .chat-container {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Message bubbles with improved readability */
    .user-message {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        color: #ffffff !important;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 5px 20px;
        margin: 1rem 0;
        max-width: 70%;
        float: right;
        clear: both;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(66, 153, 225, 0.3);
    }
    
    .ai-message {
        background: rgba(237, 242, 247, 0.9) !important;
        color: #1a202c !important;
        padding: 1rem 1.5rem;
        border-radius: 20px 20px 20px 5px;
        margin: 1rem 0;
        max-width: 70%;
        float: left;
        clear: both;
        font-weight: 500;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    }
    
    /* Progress cards with better contrast */
    .progress-card {
        background: rgba(255, 255, 255, 0.98) !important;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
        text-align: center;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .progress-card h3 {
        color: #2b6cb0 !important;
        margin-bottom: 1rem;
        font-family: 'Poppins', sans-serif !important;
    }
    
    .progress-card p {
        color: #4a5568 !important;
        line-height: 1.6;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Cultural theme colors with better contrast */
    .western-theme {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        color: #ffffff !important;
    }
    
    .eastern-theme {
        background: linear-gradient(135deg, #fed7d7 0%, #fbb6ce 100%) !important;
        color: #2d3748 !important;
    }
    
    .african-theme {
        background: linear-gradient(135deg, #fbb6ce 0%, #f687b3 100%) !important;
        color: #2d3748 !important;
    }
    
    .latin-theme {
        background: linear-gradient(135deg, #c6f6d5 0%, #9ae6b4 100%) !important;
        color: #2d3748 !important;
    }
    
    /* Enhanced Typography */
    .main-title {
        font-family: 'Poppins', sans-serif !important;
        font-size: 3rem;
        font-weight: 700;
        color: #1a202c !important;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.05);
        letter-spacing: -0.025em;
    }
    
    .subtitle {
        font-family: 'Inter', sans-serif !important;
        font-size: 1.2rem;
        color: #4a5568 !important;
        margin-bottom: 2rem;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Enhanced Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 14px rgba(66, 153, 225, 0.3) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(66, 153, 225, 0.4) !important;
        background: linear-gradient(135deg, #3182ce 0%, #2c5282 100%) !important;
    }
    
    /* Enhanced Input fields */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 10px !important;
        color: #2d3748 !important;
        font-family: 'Inter', sans-serif !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #4299e1 !important;
        box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.1) !important;
    }
    
    /* Enhanced Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.98) !important;
        border: 1px solid rgba(226, 232, 240, 0.8);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
    }
    
    .metric-card h3 {
        color: #2b6cb0 !important;
        font-family: 'Poppins', sans-serif !important;
        margin-bottom: 0.5rem;
    }
    
    .metric-card p {
        color: #4a5568 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.9rem;
    }
    
    /* Enhanced Footer */
    .footer {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%) !important;
        color: #f7fafc !important;
        padding: 2rem;
        text-align: center;
        margin-top: 3rem;
        border-radius: 15px 15px 0 0;
        border-top: 1px solid rgba(226, 232, 240, 0.2);
    }
    
    .footer p {
        color: #e2e8f0 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .main-title {
            font-size: 2rem;
        }
        
        .chat-container {
            padding: 1rem;
        }
        
        .user-message, .ai-message {
            max-width: 90%;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Load custom CSS
load_css()

# Initialize session state
if 'current_language' not in st.session_state:
    st.session_state.current_language = 'en'
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}
if 'cultural_theme' not in st.session_state:
    st.session_state.cultural_theme = 'western'

# Sidebar
with st.sidebar:
    # Try to load logo, fallback to text if not available
    try:
        logo_path = Path(__file__).parent.parent.parent / "resources" / "logo.png"
        if logo_path.exists():
            logo_img = Image.open(logo_path)
            st.image(logo_img, width=150)
        else:
            st.markdown("### GlobalMind")
    except Exception:
        st.markdown("### GlobalMind")
    
    st.markdown("---")
    
    # Language selection
    languages = get_supported_languages()
    current_lang_name = get_language_name(st.session_state.current_language)
    
    selected_language = st.selectbox(
        get_translation(st.session_state.current_language, 'language_label'),
        options=list(languages.keys()),
        format_func=lambda x: languages[x],
        index=list(languages.keys()).index(st.session_state.current_language)
    )
    
    if selected_language != st.session_state.current_language:
        st.session_state.current_language = selected_language
        st.rerun()
    
    st.markdown("---")
    
    # Navigation
    nav_options = [
        ('', 'home', get_translation(st.session_state.current_language, 'welcome')),
        ('', 'chat', get_translation(st.session_state.current_language, 'chat_title')),
        ('', 'friendbot', 'Friend Bot'),
        ('', 'music', 'Music Lounge'),
        ('', 'community', 'Community Hub'),
        ('', 'global', 'Global Chat'),
        ('', 'progress', get_translation(st.session_state.current_language, 'progress_title')),
        ('', 'settings', get_translation(st.session_state.current_language, 'settings_title')),
        ('', 'crisis', get_translation(st.session_state.current_language, 'crisis_help')),
        ('', 'resources', get_translation(st.session_state.current_language, 'resources'))
    ]
    
    page = st.radio(
        "Navigation",
        options=[opt[1] for opt in nav_options],
        format_func=lambda x: next(opt[0] + " " + opt[2] for opt in nav_options if opt[1] == x),
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Quick actions
    st.markdown("### Quick Actions")
    if st.button(get_translation(st.session_state.current_language, 'crisis_help'), key="crisis_btn"):
        page = 'crisis'
    
    if st.button(get_translation(st.session_state.current_language, 'emergency_contacts'), key="emergency_btn"):
        st.info("Emergency: 988 (US)\n116 123 (UK)\n1-833-456-4566 (CA)")

# Main content area
def home_page():
    """Home page with welcome message and overview"""
    st.markdown(f"""
    <div class="header fade-in">
        <h1 class="main-title">{get_translation(st.session_state.current_language, 'welcome')}</h1>
        <p class="subtitle">{get_translation(st.session_state.current_language, 'intro')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="progress-card fade-in">
            <h3>Multilingual Support</h3>
            <p>Support for 50+ languages with cultural adaptation</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="progress-card fade-in">
            <h3>Privacy First</h3>
            <p>End-to-end encryption and complete anonymity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="progress-card fade-in">
            <h3>Personalized Care</h3>
            <p>Culturally-aware therapeutic approaches</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Start chat button
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Start Conversation", key="start_chat", use_container_width=True):
            st.session_state.page = 'chat'
            st.rerun()

def chat_page():
    """Chat interface with AI assistant"""
    st.markdown(f"""
    <div class="header fade-in">
        <h1 class="main-title">💬 {get_translation(st.session_state.current_language, 'chat_title')}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <strong>GlobalMind:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Message",
            placeholder=get_translation(st.session_state.current_language, 'chat_placeholder'),
            key="chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("Send", key="send_btn", use_container_width=True):
            if user_input:
                # Add user message to history
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now()
                })
                
                # Generate AI response (placeholder)
                ai_response = generate_ai_response(user_input, st.session_state.current_language)
                
                # Add AI response to history
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response,
                    'timestamp': datetime.now()
                })
                
                st.rerun()
    
    # Quick response buttons
    st.markdown("### Quick Responses")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("I'm feeling anxious", key="anxiety_btn"):
            handle_quick_response("I'm feeling anxious")
    
    with col2:
        if st.button("I need someone to talk to", key="talk_btn"):
            handle_quick_response("I need someone to talk to")
    
    with col3:
        if st.button("I'm having a hard day", key="hard_day_btn"):
            handle_quick_response("I'm having a hard day")

def progress_page():
    """Progress tracking and analytics"""
    st.markdown(f"""
    <div class="header fade-in">
        <h1 class="main-title">{get_translation(st.session_state.current_language, 'progress_title')}</h1>
        <p class="subtitle">{get_translation(st.session_state.current_language, 'progress_intro')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>42</h3>
            <p>Total Sessions</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>87%</h3>
            <p>Mood Improvement</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>15</h3>
            <p>Days Streak</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>4.8/5</h3>
            <p>Satisfaction</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Mood trend chart
        dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
        mood_scores = np.random.normal(7, 1.5, 30)
        mood_scores = np.clip(mood_scores, 1, 10)
        
        fig = px.line(
            x=dates, 
            y=mood_scores,
            title="Mood Trend (Last 30 Days)",
            labels={'x': 'Date', 'y': 'Mood Score'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Session frequency chart
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        sessions = [3, 4, 2, 5, 3, 1, 2]
        
        fig = px.bar(
            x=days,
            y=sessions,
            title="Weekly Session Frequency",
            labels={'x': 'Day', 'y': 'Sessions'}
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

def settings_page():
    """Settings and customization"""
    st.markdown(f"""
    <div class="header fade-in">
        <h1 class="main-title">{get_translation(st.session_state.current_language, 'settings_title')}</h1>
        <p class="subtitle">{get_translation(st.session_state.current_language, 'settings_intro')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Settings sections
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Appearance")
        
        theme_options = ['Light', 'Dark', 'Culturally Adaptive']
        selected_theme = st.selectbox(
            get_translation(st.session_state.current_language, 'theme_label'),
            theme_options
        )
        
        cultural_backgrounds = ['Western', 'Eastern', 'African', 'Latin']
        selected_cultural = st.selectbox(
            get_translation(st.session_state.current_language, 'cultural_background'),
            cultural_backgrounds
        )
        
        st.markdown("### Notifications")
        
        enable_notifications = st.checkbox("Enable notifications")
        daily_reminders = st.checkbox("Daily check-in reminders")
        crisis_alerts = st.checkbox("Crisis support alerts")
    
    with col2:
        st.markdown("### Privacy")
        
        data_sharing = st.checkbox("Share anonymized data for research")
        session_recording = st.checkbox("Record sessions for quality improvement")
        
        st.markdown("### Data")
        
        if st.button("Export My Data", key="export_data"):
            st.success("Data export initiated. You'll receive a download link shortly.")
        
        if st.button("Delete My Data", key="delete_data"):
            st.error("This action cannot be undone. Please contact support to proceed.")
        
        st.markdown("### Emergency")
        
        emergency_contact = st.text_input("Emergency Contact Number")
        auto_escalation = st.checkbox("Auto-escalate crisis situations")

def crisis_page():
    """Crisis support and emergency resources"""
    st.markdown("""
    <div class="header fade-in" style="background: linear-gradient(135deg, #ff6b6b 0%, #ffa500 100%); color: white;">
        <h1 class="main-title" style="color: white;">🆘 Crisis Support</h1>
        <p class="subtitle" style="color: white;">You're not alone. Help is available 24/7.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Emergency contacts
    st.markdown("### Emergency Hotlines")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="progress-card">
            <h3>🇺🇸 United States</h3>
            <h2>988</h2>
            <p>Suicide & Crisis Lifeline</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="progress-card">
            <h3>🇬🇧 United Kingdom</h3>
            <h2>116 123</h2>
            <p>Samaritans</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="progress-card">
            <h3>🇨🇦 Canada</h3>
            <h2>1-833-456-4566</h2>
            <p>Talk Suicide Canada</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Immediate coping strategies
    st.markdown("### Immediate Coping Strategies")
    
    if st.button("Breathing Exercise", key="breathing"):
        st.info("Take a deep breath in for 4 counts, hold for 4, exhale for 4. Repeat 5 times.")
    
    if st.button("Grounding Technique", key="grounding"):
        st.info("Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste.")
    
    if st.button("Positive Affirmation", key="affirmation"):
        st.info("Repeat: 'This feeling will pass. I am stronger than I think. I deserve support and care.'")

def resources_page():
    """Educational resources and self-help tools"""
    st.markdown(f"""
    <div class="header fade-in">
        <h1 class="main-title">{get_translation(st.session_state.current_language, 'resources')}</h1>
        <p class="subtitle">Educational materials and self-help tools</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Resource categories
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Educational Articles")
        articles = [
            "Understanding Anxiety in Different Cultures",
            "The Role of Family in Mental Health",
            "Mindfulness Practices Across Traditions",
            "Building Resilience Through Community"
        ]
        for article in articles:
            st.markdown(f"• {article}")
    
    with col2:
        st.markdown("### Video Resources")
        videos = [
            "Breathing Exercises for Anxiety",
            "Cultural Approaches to Depression",
            "Building Support Networks",
            "Meditation Techniques"
        ]
        for video in videos:
            st.markdown(f"• {video}")

def generate_ai_response(user_input: str, language: str) -> str:
    """Generate AI response (placeholder)"""
    # This would integrate with the actual AI models
    responses = {
        'en': "I understand you're going through a difficult time. Let's work through this together. Can you tell me more about what's bothering you?",
        'es': "Entiendo que estás pasando por un momento difícil. Trabajemos juntos en esto. ¿Puedes contarme más sobre lo que te molesta?",
        'fr': "Je comprends que vous traversez une période difficile. Travaillons ensemble sur cela. Pouvez-vous me parler davantage de ce qui vous dérange?",
        'de': "Ich verstehe, dass Sie eine schwierige Zeit durchmachen. Lassen Sie uns das gemeinsam durcharbeiten. Können Sie mir mehr darüber erzählen, was Sie beschäftigt?",
        'zh': "我理解您正在经历困难时期。让我们一起努力解决这个问题。您能告诉我更多关于困扰您的事情吗？"
    }
    
    return responses.get(language, responses['en'])

def handle_quick_response(response: str):
    """Handle quick response buttons"""
    st.session_state.chat_history.append({
        'role': 'user',
        'content': response,
        'timestamp': datetime.now()
    })
    
    ai_response = generate_ai_response(response, st.session_state.current_language)
    
    st.session_state.chat_history.append({
        'role': 'assistant',
        'content': ai_response,
        'timestamp': datetime.now()
    })
    
    st.rerun()

# Main navigation
if page == 'home':
    home_page()
elif page == 'chat':
    chat_page()
elif page == 'friendbot':
    friend_bot_page()
elif page == 'music':
    music_lounge()
elif page == 'community':
    community_hub()
elif page == 'global':
    global_chat()
elif page == 'progress':
    progress_page()
elif page == 'settings':
    settings_page()
elif page == 'crisis':
    crisis_page()
elif page == 'resources':
    resources_page()

# Footer
st.markdown(f"""
<div class="footer">
    <p>{get_translation(st.session_state.current_language, 'footer')}</p>
    <p>© 2024 GlobalMind. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)
