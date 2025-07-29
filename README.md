<<<<<<< HEAD
# GlobalMind
=======
# GlobalMind

GlobalMind is a culturally-adaptive mental health AI support system designed to assist diverse populations with multilingual and culturally-intelligent support.

## Features
- **🌍 Real-time support for 50+ languages** with automatic detection
- **🎭 Culturally-relevant therapeutic methodologies** adapted to regional contexts
- **🎤 Multi-modal interaction**: text, voice, SMS fallback
- **🔒 Privacy-focused** with end-to-end encryption and anonymization
- **📱 Offline availability** with resource-efficient processing
- **📊 Advanced analytics** with mood tracking and progress monitoring
- **🆘 Crisis detection** with immediate emergency protocols
- **🎯 Evidence-based therapy** including CBT, mindfulness, and cultural approaches

## Installation

### Prerequisites
- Python 3.8+
- Virtualenv (recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd GlobalMind
   ```

2. Run the setup script:
   ```bash
   python setup.py
   ```

3. Start the application:
   ```bash
   python main.py
   ```

## Configuration
Configuration settings can be found in `config/config.yaml` and an optional `.env` file for environment-specific overrides.

## Usage

### Starting GlobalMind
- **Backend System**: Run `python main.py` to start the core system.
- **Web UI**: Run `python launch_ui.py` to start the beautiful web interface.
- **Direct Streamlit**: Run `streamlit run src/ui/streamlit_app.py` for development.

### Features
- **🌍 Multilingual Support**: 50+ languages with real-time switching
- **🎨 Cultural Themes**: Adaptive UI based on cultural preferences
- **💬 Real-time Chat**: Instant AI responses with WebSocket support
- **📊 Progress Tracking**: Visual analytics and mood tracking
- **🆘 Crisis Support**: Immediate resources and emergency protocols
- **🔒 Privacy First**: End-to-end encryption and data anonymization

### Running Tests
- Use `python -m pytest tests/` to run the test suite.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

---

For more information, contributions, or to report issues, please contact the development team at [support@globalmind.ai](mailto:support@globalmind.ai).
>>>>>>> 1fd34cf (first commit)
