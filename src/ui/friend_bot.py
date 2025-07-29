"""
Friend Bot - A supportive AI companion for users
Provides casual, friendly conversation and emotional support
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
import random

# Friendly bot responses for different emotional states
FRIEND_RESPONSES = {
    'greeting': [
        "Hey there! I'm so glad you decided to chat with me today. How are you feeling?",
        "Hi friend! 😊 I'm here to listen and chat. What's on your mind?",
        "Hello! I'm your friendly companion. I'm here for you - what would you like to talk about?",
        "Hey! Nice to see you here. I'm ready to be your listening ear. How's your day going?"
    ],
    'positive': [
        "That's wonderful to hear! I'm really happy for you. 😊",
        "That sounds amazing! Your positivity is contagious!",
        "I love hearing good news! Tell me more about what made you happy.",
        "That's fantastic! It's so nice to share in your joy."
    ],
    'sad': [
        "I'm sorry you're going through a tough time. I'm here to listen. 💙",
        "That sounds really difficult. You're not alone in this.",
        "I hear you, and I want you to know that your feelings are valid.",
        "Thank you for sharing with me. It takes courage to open up about difficult feelings."
    ],
    'anxious': [
        "Anxiety can be really overwhelming. Let's take this one step at a time.",
        "I understand how anxiety feels. Would you like to talk about what's making you feel anxious?",
        "Anxiety is tough, but you're tougher. I'm here to support you through this.",
        "That sounds stressful. Sometimes it helps to share what's worrying you."
    ],
    'encouragement': [
        "You're doing great by reaching out and taking care of yourself.",
        "I believe in you! You've got this, even when it doesn't feel like it.",
        "Every small step forward is progress. Be proud of yourself.",
        "You're stronger than you know, and I'm here to remind you of that."
    ],
    'default': [
        "I'm here to listen. Tell me more about how you're feeling.",
        "That's interesting. How does that make you feel?",
        "I appreciate you sharing that with me. What else is on your mind?",
        "Thanks for opening up. I'm here to support you however I can."
    ]
}

# Conversation starters
CONVERSATION_STARTERS = [
    "How was your day today?",
    "What's something that made you smile recently?",
    "Is there anything you're looking forward to?",
    "What's been on your mind lately?",
    "How are you taking care of yourself today?",
    "What's one thing you're grateful for right now?"
]

def get_bot_response(user_message, conversation_history):
    """
    Generate a friendly, supportive response based on user input
    """
    message_lower = user_message.lower()
    
    # Check for emotional keywords
    if any(word in message_lower for word in ['happy', 'good', 'great', 'amazing', 'wonderful', 'excited']):
        response_type = 'positive'
    elif any(word in message_lower for word in ['sad', 'upset', 'down', 'depressed', 'hurt', 'cry']):
        response_type = 'sad'
    elif any(word in message_lower for word in ['anxious', 'worried', 'nervous', 'scared', 'stress']):
        response_type = 'anxious'
    elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
        response_type = 'greeting'
    else:
        response_type = 'default'
    
    # Add encouragement randomly
    if random.random() < 0.3:  # 30% chance to add encouragement
        if response_type != 'greeting':
            response = random.choice(FRIEND_RESPONSES[response_type])
            encouragement = random.choice(FRIEND_RESPONSES['encouragement'])
            return f"{response} {encouragement}"
    
    return random.choice(FRIEND_RESPONSES[response_type])

def save_friend_chat(user_id, conversation):
    """
    Save friend bot conversation to file
    """
    try:
        chat_dir = Path("data/friend_chats")
        chat_dir.mkdir(parents=True, exist_ok=True)
        
        chat_file = chat_dir / f"{user_id}_friend_chat.json"
        
        chat_data = {
            'user_id': user_id,
            'conversations': conversation,
            'last_updated': datetime.now().isoformat()
        }
        
        with open(chat_file, 'w') as f:
            json.dump(chat_data, f, indent=2, default=str)
            
    except Exception as e:
        st.error(f"Error saving chat: {str(e)}")

def load_friend_chat(user_id):
    """
    Load friend bot conversation from file
    """
    try:
        chat_file = Path("data/friend_chats") / f"{user_id}_friend_chat.json"
        
        if chat_file.exists():
            with open(chat_file, 'r') as f:
                chat_data = json.load(f)
            return chat_data.get('conversations', [])
        else:
            return []
            
    except Exception as e:
        st.error(f"Error loading chat: {str(e)}")
        return []

def friend_bot_page():
    """
    Main friend bot interface
    """
    st.markdown("""
    <div class="header fade-in">
        <h1 class="main-title">🤖 Friend Bot</h1>
        <p class="subtitle">Your supportive AI companion - here to listen and chat</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize friend bot session state
    if 'friend_chat_history' not in st.session_state:
        st.session_state.friend_chat_history = []
    
    if 'friend_user_id' not in st.session_state:
        st.session_state.friend_user_id = f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Load existing conversation
    if not st.session_state.friend_chat_history:
        st.session_state.friend_chat_history = load_friend_chat(st.session_state.friend_user_id)
    
    # Welcome message for new users
    if not st.session_state.friend_chat_history:
        welcome_message = {
            'role': 'bot',
            'content': random.choice(FRIEND_RESPONSES['greeting']),
            'timestamp': datetime.now()
        }
        st.session_state.friend_chat_history.append(welcome_message)
    
    # Chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.friend_chat_history:
        if message['role'] == 'user':
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="ai-message">
                <strong>Friend Bot:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input(
            "Message",
            placeholder="Type your message here... I'm here to listen! 😊",
            key="friend_chat_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("Send", key="friend_send_btn", use_container_width=True):
            if user_input:
                # Add user message to history
                user_message = {
                    'role': 'user',
                    'content': user_input,
                    'timestamp': datetime.now()
                }
                st.session_state.friend_chat_history.append(user_message)
                
                # Generate bot response
                bot_response = get_bot_response(user_input, st.session_state.friend_chat_history)
                
                # Add bot response to history
                bot_message = {
                    'role': 'bot',
                    'content': bot_response,
                    'timestamp': datetime.now()
                }
                st.session_state.friend_chat_history.append(bot_message)
                
                # Save conversation
                save_friend_chat(st.session_state.friend_user_id, st.session_state.friend_chat_history)
                
                st.rerun()
    
    # Conversation starters
    st.markdown("### 💭 Conversation Starters")
    st.markdown("Not sure what to talk about? Try one of these:")
    
    cols = st.columns(3)
    for i, starter in enumerate(CONVERSATION_STARTERS[:6]):
        with cols[i % 3]:
            if st.button(starter, key=f"starter_{i}"):
                # Add starter as user message
                starter_message = {
                    'role': 'user',
                    'content': starter,
                    'timestamp': datetime.now()
                }
                st.session_state.friend_chat_history.append(starter_message)
                
                # Generate bot response
                bot_response = get_bot_response(starter, st.session_state.friend_chat_history)
                
                # Add bot response
                bot_message = {
                    'role': 'bot',
                    'content': bot_response,
                    'timestamp': datetime.now()
                }
                st.session_state.friend_chat_history.append(bot_message)
                
                # Save conversation
                save_friend_chat(st.session_state.friend_user_id, st.session_state.friend_chat_history)
                
                st.rerun()
    
    # Quick emotional check-ins
    st.markdown("### 🎭 How are you feeling?")
    st.markdown("Click on how you're feeling right now:")
    
    feeling_cols = st.columns(4)
    feelings = [
        ("😊", "I'm feeling good"),
        ("😔", "I'm feeling down"),
        ("😰", "I'm feeling anxious"),
        ("😴", "I'm feeling tired")
    ]
    
    for i, (emoji, feeling) in enumerate(feelings):
        with feeling_cols[i]:
            if st.button(f"{emoji} {feeling.split()[-1].title()}", key=f"feeling_{i}"):
                # Add feeling as user message
                feeling_message = {
                    'role': 'user',
                    'content': feeling,
                    'timestamp': datetime.now()
                }
                st.session_state.friend_chat_history.append(feeling_message)
                
                # Generate bot response
                bot_response = get_bot_response(feeling, st.session_state.friend_chat_history)
                
                # Add bot response
                bot_message = {
                    'role': 'bot',
                    'content': bot_response,
                    'timestamp': datetime.now()
                }
                st.session_state.friend_chat_history.append(bot_message)
                
                # Save conversation
                save_friend_chat(st.session_state.friend_user_id, st.session_state.friend_chat_history)
                
                st.rerun()
    
    # Clear conversation option
    st.markdown("---")
    if st.button("🗑️ Clear Conversation", key="clear_friend_chat"):
        st.session_state.friend_chat_history = []
        # Add welcome message back
        welcome_message = {
            'role': 'bot',
            'content': random.choice(FRIEND_RESPONSES['greeting']),
            'timestamp': datetime.now()
        }
        st.session_state.friend_chat_history.append(welcome_message)
        save_friend_chat(st.session_state.friend_user_id, st.session_state.friend_chat_history)
        st.rerun()
    
    # Privacy note
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #f0f8ff; padding: 15px; border-radius: 10px; margin-top: 20px;">
        <p style="margin: 0; font-size: 14px;">
            💙 <strong>Privacy Note:</strong> Your conversations with Friend Bot are stored locally 
            and are designed to provide you with a supportive, non-judgmental space to express yourself. 
            If you're experiencing a crisis, please reach out to professional help or use our crisis support features.
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    friend_bot_page()
