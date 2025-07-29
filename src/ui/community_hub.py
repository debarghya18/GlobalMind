import streamlit as st
import json
import datetime
from typing import List, Dict
import os
import random

# Mock database for messages (in production, use a real database)
MESSAGES_FILE = "community_messages.json"

def load_messages() -> List[Dict]:
    """Load messages from JSON file"""
    try:
        with open(MESSAGES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Initialize with some sample messages
        sample_messages = [
            {
                "id": 1,
                "username": "Sarah_Wellness",
                "message": "Welcome to our supportive community! Remember, you're not alone in your journey.",
                "channel": "general",
                "timestamp": "2025-07-29T10:00:00",
                "likes": 5
            },
            {
                "id": 2,
                "username": "MindfulMike",
                "message": "Just finished a 10-minute meditation session. Feeling much calmer now. Anyone else practicing mindfulness today?",
                "channel": "mindfulness",
                "timestamp": "2025-07-29T11:30:00",
                "likes": 3
            },
            {
                "id": 3,
                "username": "AnxietyWarrior",
                "message": "Having a tough day with anxiety. The breathing exercises from yesterday's session really helped though!",
                "channel": "support",
                "timestamp": "2025-07-29T12:15:00",
                "likes": 8
            }
        ]
        save_messages(sample_messages)
        return sample_messages

def save_messages(messages: List[Dict]):
    """Save messages to JSON file"""
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f, indent=2)

def add_message(username: str, message: str, channel: str = "general"):
    """Add a new message to the community"""
    messages = load_messages()
    new_message = {
        "id": len(messages) + 1,
        "username": username,
        "message": message,
        "channel": channel,
        "timestamp": datetime.datetime.now().isoformat(),
        "likes": 0
    }
    messages.append(new_message)
    save_messages(messages)

def get_messages_by_channel(channel: str) -> List[Dict]:
    """Get messages for a specific channel"""
    messages = load_messages()
    return [msg for msg in messages if msg["channel"] == channel]

def like_message(message_id: int):
    """Like a message"""
    messages = load_messages()
    for msg in messages:
        if msg["id"] == message_id:
            msg["likes"] = msg.get("likes", 0) + 1
            break
    save_messages(messages)

def community_hub():
    """Enhanced Community Hub with multiple chat channels and better UI"""
    
    # Custom CSS for community hub
    st.markdown("""
    <style>
    .chat-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    .message-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        border-left: 3px solid #667eea;
    }
    .username {
        font-weight: bold;
        color: #2c3e50;
        font-size: 1rem;
    }
    .timestamp {
        color: #7f8c8d;
        font-size: 0.8rem;
        float: right;
    }
    .message-text {
        color: #2c3e50;
        margin: 0.5rem 0;
        line-height: 1.5;
    }
    .channel-header {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 1rem 0;
    }
    .like-button {
        background: #e74c3c;
        color: white;
        border: none;
        padding: 0.25rem 0.5rem;
        border-radius: 15px;
        font-size: 0.8rem;
        cursor: pointer;
    }
    .online-users {
        background: #ecf0f1;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="color: #2c3e50; text-align: center; margin-bottom: 2rem;">GlobalMind Community Hub</h1>', unsafe_allow_html=True)
    
    # User authentication (simplified)
    if "username" not in st.session_state:
        st.session_state.username = ""

    if not st.session_state.username:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #2c3e50;">Join Our Supportive Community</h3>', unsafe_allow_html=True)
        st.markdown('<p style="color: #7f8c8d;">Connect with others on their mental health journey. Share experiences, find support, and grow together.</p>', unsafe_allow_html=True)
        
        username_input = st.text_input("Choose your username:", placeholder="e.g., MindfulSarah, WellnessWarrior")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Join Community", use_container_width=True):
                if username_input:
                    st.session_state.username = username_input
                    st.success(f"Welcome to the community, {username_input}!")
                    st.rerun()
                else:
                    st.error("Please enter a username")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Community guidelines
        with st.expander("Community Guidelines"):
            st.markdown("""
            **Our community is built on:**
            - 🤝 **Respect**: Treat everyone with kindness and empathy
            - 🔒 **Privacy**: Keep personal information confidential
            - 🌱 **Support**: Offer encouragement and positive feedback
            - 🚫 **No judgment**: This is a safe space for all experiences
            - 🎨 **Authenticity**: Share genuinely and honestly
            """)
        return

    # Welcome back message
    st.markdown(f'<div class="online-users"><h4 style="color: #2c3e50;">Welcome back, {st.session_state.username}! 😊</h4></div>', unsafe_allow_html=True)
    
    # Channel selection with descriptions
    col1, col2 = st.columns([2, 1])
    
    with col1:
        channel_info = {
            "general": "💬 General Discussion - Open chat for all topics",
            "support": "🤗 Peer Support - Share challenges and get encouragement", 
            "mindfulness": "🧘 Mindfulness & Meditation - Practice together",
            "music-therapy": "🎵 Music Therapy - Discuss healing through music",
            "wellness": "🌱 Wellness Tips - Share healthy habits and tips",
            "crisis-support": "🆘 Crisis Support - Immediate support (monitored 24/7)"
        }
        
        selected_channel = st.selectbox(
            "Choose a channel:", 
            list(channel_info.keys()),
            format_func=lambda x: channel_info[x]
        )
    
    with col2:
        # Online users simulation
        online_count = random.randint(15, 45)
        st.markdown(f'<div class="online-users"><strong>🟢 {online_count} users online</strong></div>', unsafe_allow_html=True)
    
    # Channel header
    st.markdown(f'<div class="channel-header"><h2>#{selected_channel}</h2><p>{channel_info[selected_channel].split(" - ")[1]}</p></div>', unsafe_allow_html=True)
    
    # Display messages
    messages = get_messages_by_channel(selected_channel)
    
    # Chat container with scrollable area
    chat_container = st.container()
    with chat_container:
        if not messages:
            st.markdown('<div class="message-card"><p style="color: #7f8c8d; text-align: center;">No messages yet. Be the first to start the conversation!</p></div>', unsafe_allow_html=True)
        else:
            for msg in messages[-15:]:  # Show last 15 messages
                timestamp = datetime.datetime.fromisoformat(msg["timestamp"])
                likes = msg.get("likes", 0)
                
                st.markdown(f"""
                <div class="message-card">
                    <div class="username">{msg['username']}
                        <span class="timestamp">{timestamp.strftime('%H:%M - %b %d')}</span>
                    </div>
                    <div class="message-text">{msg['message']}</div>
                    <small style="color: #e74c3c;">❤️ {likes} likes</small>
                </div>
                """, unsafe_allow_html=True)
                
                # Like button
                if st.button(f"❤️ Like", key=f"like_{msg['id']}"):
                    like_message(msg['id'])
                    st.rerun()
    
    # Message input section
    st.markdown('<h3 style="color: #2c3e50; margin-top: 2rem;">Share Your Thoughts</h3>', unsafe_allow_html=True)
    
    # Quick response buttons for common supportive messages
    st.markdown('<p style="color: #7f8c8d;">Quick responses:</p>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    
    quick_responses = [
        "🤗 Sending you support!",
        "🌱 You've got this!", 
        "🙏 Thank you for sharing",
        "🌈 Better days ahead"
    ]
    
    for i, (col, response) in enumerate(zip([col1, col2, col3, col4], quick_responses)):
        with col:
            if st.button(response, key=f"quick_{i}"):
                add_message(st.session_state.username, response, selected_channel)
                st.success("Message sent!")
                st.rerun()
    
    # Custom message input
    new_message = st.text_area(
        "Write your message:", 
        height=100, 
        placeholder="Share your thoughts, experiences, or offer support to others..."
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💬 Send Message", use_container_width=True):
            if new_message.strip():
                add_message(st.session_state.username, new_message, selected_channel)
                st.success("Message sent successfully!")
                st.rerun()
            else:
                st.error("Please enter a message")
    
    # Community stats
    with st.expander("📊 Community Stats"):
        total_messages = len(load_messages())
        channels_with_activity = len(set(msg["channel"] for msg in load_messages()))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Messages", total_messages)
        with col2:
            st.metric("Active Channels", channels_with_activity)
        with col3:
            st.metric("Online Users", online_count)
    
    # Community Guidelines
    with st.expander("📋 Community Guidelines"):
        st.markdown("""
        ### 🤝 Community Guidelines
        
        - **Share safely**: Only share what you're comfortable with
        - **No judgment**: Everyone's journey is different
        - **Confidentiality**: What's shared here stays here
        - **Get help**: If you're in crisis, please reach out to professional help
        
        **Crisis Resources:**
        - National Suicide Prevention Lifeline: 988
        - Crisis Text Line: Text HOME to 741741
        """)

if __name__ == "__main__":
    community_hub()
