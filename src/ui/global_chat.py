"""
Global Chat Community for GlobalMind
Real-time chat system for users worldwide
"""

import streamlit as st
import json
import datetime
from typing import List, Dict
import random
import time

# Global chat database file
GLOBAL_CHAT_FILE = "global_chat_messages.json"

def load_global_messages() -> List[Dict]:
    """Load global chat messages from JSON file"""
    try:
        with open(GLOBAL_CHAT_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Initialize with welcome messages from different countries
        welcome_messages = [
            {
                "id": 1,
                "username": "GlobalMind_Bot",
                "message": "Welcome to the Global Mental Health Community! Connect with people from around the world.",
                "timestamp": "2025-07-29T08:00:00",
                "country": "🌐 System",
                "likes": 12,
                "language": "en"
            },
            {
                "id": 2,
                "username": "Sarah_NYC",
                "message": "Good morning everyone! Starting my day with gratitude. What's one thing you're grateful for today?",
                "timestamp": "2025-07-29T09:15:00",
                "country": "🇺🇸 USA",
                "likes": 8,
                "language": "en"
            },
            {
                "id": 3,
                "username": "Akira_Tokyo",
                "message": "こんにちは！Today I practiced mindfulness meditation for 20 minutes. Feeling much more centered now.",
                "timestamp": "2025-07-29T10:30:00",
                "country": "🇯🇵 Japan",
                "likes": 6,
                "language": "en"
            },
            {
                "id": 4,
                "username": "Maria_Madrid",
                "message": "¡Hola amigos! Just finished a beautiful walk in the park. Nature therapy is so healing",
                "timestamp": "2025-07-29T11:45:00",
                "country": "🇪🇸 Spain",
                "likes": 9,
                "language": "en"
            },
            {
                "id": 5,
                "username": "Ahmed_Cairo",
                "message": "Sending positive energy to everyone here! Remember, every small step towards healing matters",
                "timestamp": "2025-07-29T12:20:00",
                "country": "🇪🇬 Egypt",
                "likes": 15,
                "language": "en"
            }
        ]
        save_global_messages(welcome_messages)
        return welcome_messages

def save_global_messages(messages: List[Dict]):
    """Save global chat messages to JSON file"""
    with open(GLOBAL_CHAT_FILE, 'w', encoding='utf-8') as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)

def add_global_message(username: str, message: str, country: str = "🌐 Unknown", language: str = "en"):
    """Add a new message to the global chat"""
    messages = load_global_messages()
    new_message = {
        "id": len(messages) + 1,
        "username": username,
        "message": message,
        "timestamp": datetime.datetime.now().isoformat(),
        "country": country,
        "likes": 0,
        "language": language
    }
    messages.append(new_message)
    save_global_messages(messages)

def like_global_message(message_id: int):
    """Like a global message"""
    messages = load_global_messages()
    for msg in messages:
        if msg["id"] == message_id:
            msg["likes"] = msg.get("likes", 0) + 1
            break
    save_global_messages(messages)

def get_online_users_count():
    """Simulate online users count"""
    return random.randint(150, 500)

def get_countries_online():
    """Get list of countries with active users"""
    countries = [
        "🇺🇸 USA", "🇬🇧 UK", "🇨🇦 Canada", "🇦🇺 Australia", "🇩🇪 Germany",
        "🇫🇷 France", "🇪🇸 Spain", "🇮🇹 Italy", "🇯🇵 Japan", "🇰🇷 South Korea",
        "🇮🇳 India", "🇧🇷 Brazil", "🇲🇽 Mexico", "🇦🇷 Argentina", "🇿🇦 South Africa",
        "🇪🇬 Egypt", "🇳🇬 Nigeria", "🇸🇪 Sweden", "🇳🇴 Norway", "🇳🇱 Netherlands"
    ]
    return random.sample(countries, random.randint(12, 18))

def global_chat():
    """Global Chat Community Interface"""
    
    # Custom CSS for global chat
    st.markdown("""
    <style>
    .global-chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    .global-message-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #4299e1;
        transition: transform 0.2s ease;
    }
    .global-message-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }
    .global-username {
        font-weight: bold;
        color: #2b6cb0;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    .global-country {
        font-size: 0.9rem;
        color: #4a5568;
        float: right;
    }
    .global-timestamp {
        color: #718096;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    .global-message-text {
        color: #2d3748;
        line-height: 1.6;
        margin: 1rem 0;
        font-size: 1rem;
    }
    .global-stats-card {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        border: 1px solid #e2e8f0;
    }
    .global-input-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
    }
    .country-tag {
        background: linear-gradient(45deg, #4299e1, #3182ce);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.25rem;
        display: inline-block;
    }
    .language-indicator {
        background: #48bb78;
        color: white;
        padding: 0.2rem 0.5rem;
        border-radius: 10px;
        font-size: 0.7rem;
        margin-left: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="global-chat-header">
        <h1>🌍 Global Mental Health Community</h1>
        <p>Connect with people from around the world on their mental health journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state for global chat
    if "global_username" not in st.session_state:
        st.session_state.global_username = ""
    if "user_country" not in st.session_state:
        st.session_state.user_country = "🌐 Unknown"
    
    # User setup
    if not st.session_state.global_username:
        st.markdown('<div class="global-input-container">', unsafe_allow_html=True)
        st.markdown("### 👋 Join the Global Community")
        
        col1, col2 = st.columns(2)
        with col1:
            username_input = st.text_input(
                "Choose your username:", 
                placeholder="e.g., Alex_London, Maria_NYC"
            )
        
        with col2:
            countries = [
                "🇺🇸 USA", "🇬🇧 UK", "🇨🇦 Canada", "🇦🇺 Australia", "🇩🇪 Germany",
                "🇫🇷 France", "🇪🇸 Spain", "🇮🇹 Italy", "🇯🇵 Japan", "🇰🇷 South Korea",
                "🇮🇳 India", "🇧🇷 Brazil", "🇲🇽 Mexico", "🇦🇷 Argentina", "🇿🇦 South Africa",
                "🇪🇬 Egypt", "🇳🇬 Nigeria", "🇸🇪 Sweden", "🇳🇴 Norway", "🇳🇱 Netherlands",
                "🇨🇳 China", "🇷🇺 Russia", "🇹🇷 Turkey", "🇸🇦 Saudi Arabia", "🇦🇪 UAE",
                "🇮🇩 Indonesia", "🇹🇭 Thailand", "🇵🇭 Philippines", "🇻🇳 Vietnam", "🇲🇾 Malaysia"
            ]
            selected_country = st.selectbox("Select your country:", countries)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🌍 Join Global Chat", use_container_width=True):
                if username_input:
                    st.session_state.global_username = username_input
                    st.session_state.user_country = selected_country
                    st.success(f"Welcome to the global community, {username_input}!")
                    st.rerun()
                else:
                    st.error("Please enter a username")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Show community guidelines
        with st.expander("🌍 Global Community Guidelines"):
            st.markdown("""
            **Welcome to our global mental health community!**
            
            🤝 **Respect Cultural Differences**: We have members from all over the world
            🌈 **Be Inclusive**: Welcome people of all backgrounds and experiences  
            💬 **Use Simple English**: Help everyone understand by using clear language
            🚫 **No Discrimination**: Zero tolerance for racism, sexism, or any form of hate
            🔒 **Protect Privacy**: Don't share personal information
            💚 **Spread Positivity**: Focus on support, encouragement, and healing
            🆘 **Crisis Support**: If someone is in crisis, encourage professional help
            """)
        return
    
    # Global chat interface
    st.markdown(f'<div class="global-stats-card"><h4>Welcome back, {st.session_state.global_username}! {st.session_state.user_country}</h4></div>', unsafe_allow_html=True)
    
    # Stats and online info
    col1, col2, col3 = st.columns(3)
    
    online_count = get_online_users_count()
    countries_online = get_countries_online()
    
    with col1:
        st.markdown(f'<div class="global-stats-card"><h3>{online_count}</h3><p>Users Online Worldwide</p></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="global-stats-card"><h3>{len(countries_online)}</h3><p>Countries Active</p></div>', unsafe_allow_html=True)
    
    with col3:
        total_messages = len(load_global_messages())
        st.markdown(f'<div class="global-stats-card"><h3>{total_messages}</h3><p>Global Messages</p></div>', unsafe_allow_html=True)
    
    # Show active countries
    st.markdown("### 🌍 Active Countries Right Now")
    countries_html = "".join([f'<span class="country-tag">{country}</span>' for country in countries_online])
    st.markdown(f'<div style="margin: 1rem 0;">{countries_html}</div>', unsafe_allow_html=True)
    
    # Auto-refresh toggle
    col1, col2 = st.columns([3, 1])
    with col2:
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)
        if auto_refresh:
            time.sleep(2)
            st.rerun()
    
    # Display global messages
    st.markdown("### 💬 Global Conversation")
    
    messages = load_global_messages()
    
    # Show recent messages (last 20)
    recent_messages = messages[-20:]
    
    for msg in reversed(recent_messages):  # Show newest first
        timestamp = datetime.datetime.fromisoformat(msg["timestamp"])
        likes = msg.get("likes", 0)
        
        st.markdown(f"""
        <div class="global-message-card">
            <div class="global-username">{msg['username']}
                <span class="global-country">{msg.get('country', '🌐 Unknown')}</span>
                <span class="language-indicator">{msg.get('language', 'EN').upper()}</span>
            </div>
            <div class="global-message-text">{msg['message']}</div>
            <div class="global-timestamp">
                {timestamp.strftime('%H:%M - %b %d')} • ❤️ {likes} likes
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Like button
        col1, col2, col3 = st.columns([1, 1, 8])
        with col1:
            if st.button(f"❤️ {likes}", key=f"global_like_{msg['id']}"):
                like_global_message(msg['id'])
                st.rerun()
    
    # Message input
    st.markdown('<div class="global-input-container">', unsafe_allow_html=True)
    st.markdown("### ✍️ Share with the World")
    
    # Quick global responses
    st.markdown("**Quick Messages:**")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_global_responses = [
        "🌅 Good morning world!",
        "💚 Sending love to all",
        "🙏 Grateful for this community",
        "✨ You're not alone"
    ]
    
    for i, (col, response) in enumerate(zip([col1, col2, col3, col4], quick_global_responses)):
        with col:
            if st.button(response, key=f"global_quick_{i}"):
                add_global_message(
                    st.session_state.global_username, 
                    response, 
                    st.session_state.user_country
                )
                st.success("Message sent to the world! 🌍")
                st.rerun()
    
    # Custom message
    new_message = st.text_area(
        "Your message to the global community:",
        height=100,
        placeholder="Share your thoughts, experiences, or words of encouragement with people around the world..."
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🌍 Send to Global Community", use_container_width=True):
            if new_message.strip():
                add_global_message(
                    st.session_state.global_username, 
                    new_message, 
                    st.session_state.user_country
                )
                st.success("Your message has been shared with the global community! 🌍✨")
                st.rerun()
            else:
                st.error("Please enter a message")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Global community features
    with st.expander("🌟 Global Community Features"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **🌍 Worldwide Connection**
            - Chat with people from 30+ countries
            - Share experiences across cultures
            - Learn from diverse perspectives
            
            **💬 Real-time Messaging**
            - Live global conversation
            - Instant message delivery
            - Like and support others
            """)
        
        with col2:
            st.markdown("""
            **🔒 Safe Environment**
            - Moderated community guidelines
            - Cultural sensitivity focus
            - Crisis support awareness
            
            **🌈 Inclusive Space**
            - All backgrounds welcome
            - Multiple language support
            - Respectful dialogue encouraged
            """)

if __name__ == "__main__":
    global_chat()
