import streamlit as st
import requests
import json
from datetime import datetime
import random

def music_lounge():
    """Enhanced Music Lounge with therapeutic music recommendations"""
    
    # Custom CSS for music lounge
    st.markdown("""
    <style>
    .music-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .music-title {
        font-size: 1.3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    .music-artist {
        font-size: 1rem;
        color: #e8e8e8;
        margin-bottom: 1rem;
    }
    .mood-button {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        color: white;
        margin: 0.25rem;
        cursor: pointer;
    }
    .playlist-container {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="color: #2c3e50; text-align: center; margin-bottom: 2rem;">Therapeutic Music Lounge</h1>', unsafe_allow_html=True)
    
    # Mood-based music recommendations
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="music-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white;">Choose Your Mood</h3>', unsafe_allow_html=True)
        
        mood = st.selectbox(
            "How are you feeling today?",
            ["Anxious - Need Calming", "Sad - Need Uplifting", "Stressed - Need Relaxation", 
             "Energetic - Need Focus", "Peaceful - Maintain Calm"]
        )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="music-card">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: white;">Music Therapy Benefits</h3>', unsafe_allow_html=True)
        st.markdown("""
        <ul style="color: white;">
        <li>Reduces anxiety and stress</li>
        <li>Improves mood and emotional well-being</li>
        <li>Enhances focus and concentration</li>
        <li>Promotes better sleep quality</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Therapeutic playlists based on mood
    therapeutic_playlists = {
        "Anxious - Need Calming": [
            {"title": "Weightless", "artist": "Marconi Union", "description": "Scientifically designed to reduce anxiety by 65%"},
            {"title": "Clair de Lune", "artist": "Claude Debussy", "description": "Classical piece known for its calming effects"},
            {"title": "Aqueous Transmission", "artist": "Incubus", "description": "Ambient rock for deep relaxation"},
            {"title": "Spiegel im Spiegel", "artist": "Arvo Pärt", "description": "Minimalist composition for peace"},
        ],
        "Sad - Need Uplifting": [
            {"title": "Here Comes the Sun", "artist": "The Beatles", "description": "Uplifting classic to brighten your day"},
            {"title": "Good as Hell", "artist": "Lizzo", "description": "Empowering anthem for self-love"},
            {"title": "Happy", "artist": "Pharrell Williams", "description": "Instant mood booster"},
            {"title": "Three Little Birds", "artist": "Bob Marley", "description": "Reassuring reggae for positivity"},
        ],
        "Stressed - Need Relaxation": [
            {"title": "River", "artist": "Max Richter", "description": "Neo-classical for stress relief"},
            {"title": "Gymnopédie No. 1", "artist": "Erik Satie", "description": "Gentle piano for relaxation"},
            {"title": "Porcelain", "artist": "Moby", "description": "Electronic ambient for unwinding"},
            {"title": "The Blue Notebooks", "artist": "Max Richter", "description": "Contemplative modern classical"},
        ],
        "Energetic - Need Focus": [
            {"title": "Focused", "artist": "Brain.fm", "description": "AI-generated music for concentration"},
            {"title": "Vivaldi's Four Seasons", "artist": "Antonio Vivaldi", "description": "Classical energy for productivity"},
            {"title": "Tycho - A Walk", "artist": "Tycho", "description": "Electronic ambient for focus"},
            {"title": "Ludovico Einaudi - Nuvole Bianche", "artist": "Ludovico Einaudi", "description": "Piano for creative flow"},
        ],
        "Peaceful - Maintain Calm": [
            {"title": "Ambient 1: Music for Airports", "artist": "Brian Eno", "description": "Pioneer of ambient music"},
            {"title": "Sleep Baby Sleep", "artist": "Broods", "description": "Gentle lullaby for peace"},
            {"title": "Samsara", "artist": "Audiomachine", "description": "Cinematic peace"},
            {"title": "Metamorphosis", "artist": "Philip Glass", "description": "Minimalist tranquility"},
        ]
    }
    
    # Display recommended playlist
    st.markdown('<h2 style="color: #2c3e50; margin-top: 2rem;">🎼 Recommended for You</h2>', unsafe_allow_html=True)
    
    if mood in therapeutic_playlists:
        playlist = therapeutic_playlists[mood]
        
        for i, track in enumerate(playlist):
            st.markdown(f"""
            <div class="music-card">
                <div class="music-title">🎵 {track['title']}</div>
                <div class="music-artist">by {track['artist']}</div>
                <p style="color: #e8e8e8; font-size: 0.9rem;">{track['description']}</p>
                <button class="mood-button" onclick="alert('Playing {track['title']}...')">▶️ Play Preview</button>
            </div>
            """, unsafe_allow_html=True)
    
    # Music search functionality
    st.markdown('<h2 style="color: #2c3e50; margin-top: 2rem;">🔍 Search Music</h2>', unsafe_allow_html=True)
    
    search_query = st.text_input("Search for therapeutic music, artists, or genres", placeholder="e.g., meditation music, nature sounds, classical")
    
    if search_query:
        # Simulated search results (in real implementation, you'd use Spotify API)
        st.markdown('<div class="playlist-container">', unsafe_allow_html=True)
        st.markdown('<h3 style="color: #2c3e50;">Search Results</h3>', unsafe_allow_html=True)
        
        # Mock search results
        mock_results = [
            {"title": f"Therapeutic {search_query} Mix", "artist": "Various Artists", "duration": "45:30"},
            {"title": f"{search_query} for Healing", "artist": "Meditation Masters", "duration": "32:15"},
            {"title": f"Calm {search_query} Collection", "artist": "Wellness Sounds", "duration": "28:45"},
        ]
        
        for result in mock_results:
            col1, col2, col3 = st.columns([3, 2, 1])
            with col1:
                st.write(f"🎵 **{result['title']}**")
                st.write(f"by {result['artist']}")
            with col2:
                st.write(f"Duration: {result['duration']}")
            with col3:
                st.button("▶️ Play", key=f"play_{result['title']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Spotify Integration Instructions
    with st.expander("🎧 Connect Your Spotify Account"):
        st.markdown("""
        **To enable full Spotify integration:**
        
        1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
        2. Create a new app and get your Client ID and Client Secret
        3. Add the credentials to the app configuration
        4. Enjoy unlimited access to Spotify's music library!
        
        **Current Features:**
        - Curated therapeutic playlists
        - Mood-based recommendations
        - Music therapy guidance
        """)

if __name__ == "__main__":
    music_lounge()
