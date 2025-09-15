# Jarvis AI - Voice-Controlled AI Assistant

## 🎥 Project Demonstration

[**Watch the project demonstration video here**](https://youtu.be/UScktVhRJ8Y)

> Replace `YOUR_VIDEO_LINK_HERE` with your actual video URL

---

## 🔍 Face Recognition System

The `face_rec/` folder contains a comprehensive face recognition implementation:

- **📓 Training Notebook** - Complete dataset training pipeline with **92% accuracy**
- **🗜️ Model Weights** - Pre-trained model weights stored in zip file format
- **🎯 Recognition Engine** - Real-time face detection and recognition capabilities

This component can be integrated with the main Jarvis AI system for personalized user interactions and enhanced security features.

## 🤖 Open Source AI Components

Jarvis AI is built entirely on **open source technologies**:

- **🧠 Large Language Models (LLMs)** - Utilizes open source models via OpenRouter API
  - Supports various open source models (Mistral, etc.)
  - No dependency on proprietary AI services

- **🗣️ Text-to-Speech** - **Kokoro TTS** for natural voice synthesis
  - High-quality, open source TTS engine
  - Customizable voice characteristics
  - Local processing for privacy

---

## 📋 Overview

Jarvis AI is a modular voice-controlled AI assistant designed to interpret and execute user commands through natural voice interaction. The system provides hands-free control of various functions and features an extensible architecture for adding new capabilities.

## ✨ Key Features

- 🎤 **Voice Input Processing** - Real-time speech recognition and processing
- 🗣️ **Text-to-Speech Output** - Natural voice responses using TTS
- 🎯 **Wake Word Activation** - Responds to "Sarah" and variations
- 🧠 **Command Routing** - Intelligent command parsing and execution
- 🔧 **Modular Skills System** - Easy to extend with new capabilities
- 💬 **Conversational AI** - Context-aware conversations with LLM integration

## 🏗️ Project Structure

```
jarvis_ai/
├── 📁 core/                    # Core engine components
│   ├── command_router.py       # Routes commands to skills
│   ├── conversation.py         # Handles AI conversations
│   ├── openrouter_client.py    # LLM API client
│   ├── tts.py                  # Text-to-speech synthesis
│   ├── voice_input.py          # Voice input processing
│   └── wake_word_listener.py   # Wake word detection
│
├── 📁 skills/                  # Pluggable skill modules
│   ├── 📁 general/
│   │   └── hello_skill.py      # Basic greeting responses
│   ├── 📁 system/
│   │   └── app_launcher.py     # Application launching
│   ├── browser_skill.py        # Web browser automation
│   ├── email_skill.py          # Email operations
│   ├── read_screen.py          # Screen reading & OCR
│   ├── weather_skill.py        # Weather information
│   └── whatsapp_skill.py       # WhatsApp messaging
│
├── 📁 assets/                  # Static resources
│   ├── 📁 apps/               # Application mappings
│   └── 📁 llms/               # LLM test scripts
│
├── 📁 tests/                   # Test suites
│   ├── 📁 skills/             # Skill-specific tests
│   ├── 📁 stt/                # Speech-to-text tests
│   └── 📁 tts/                # Text-to-speech tests
│
├── main.py                     # Application entry point
└── requirements.txt            # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Microphone access
- Speaker/headphone output

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd jarvis_ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (optional)
   Create a `.env` file with your API keys:
   ```env
   OPENROUTER_API_KEY=your_openrouter_key
   OPENWEATHER_API_KEY=your_weather_key
   EMAIL_ADDRESS=your_email@example.com
   EMAIL_PASSWORD=your_app_password
   ```

### Running the Application

**Normal Mode:**
```bash
python main.py
```

**Silent Mode:**
```bash
python main.py --silent
```

In silent mode, the assistant runs quietly in the background and only responds when the wake word "Sarah" is detected.

## 🎯 Core Components

### 1. **Wake Word Listener** (`core/wake_word_listener.py`)
- Continuously monitors audio input for the wake word "Sarah"
- Supports variations: sara, sarra, sahra, sahara, sari, sarae
- Activates the system when wake word is detected

### 2. **Voice Input Processing** (`core/voice_input.py`)
- Captures audio from microphone
- Converts speech to text using speech recognition
- Handles audio preprocessing and noise reduction

### 3. **Command Router** (`core/command_router.py`)
- Analyzes user input to determine intent
- Routes commands to appropriate skill modules
- Manages the flow between different system components

### 4. **Conversation System** (`core/conversation.py`)
- Handles AI-powered conversations
- Integrates with LLM APIs for natural language understanding
- Maintains context across interactions

### 5. **Text-to-Speech** (`core/tts.py`)
- Converts text responses to natural speech
- Provides audio feedback to users
- Configurable voice settings

## 🛠️ Available Skills

### System Skills
- **App Launcher** - Launch applications by voice command
- **Browser Control** - Automate web browser tasks

### Communication Skills
- **Email Management** - Send and read emails
- **WhatsApp Messaging** - Send WhatsApp messages

### Information Skills
- **Weather Reports** - Get current weather and forecasts
- **Screen Reading** - Read and analyze screen content with OCR

### General Skills
- **Greetings** - Responds to hello and greeting commands
- **Conversations** - General AI-powered conversations

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENROUTER_API_KEY` | API key for LLM services | Optional |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | For weather |
| `WEATHERAPI_KEY` | WeatherAPI key | For weather |
| `EMAIL_ADDRESS` | Email account | For email skills |
| `EMAIL_PASSWORD` | Email app password | For email skills |
| `WHATSAPP_API_KEY` | WhatsApp Python Library | For WhatsApp |
| `DEFAULT_LOCATION` | Default weather location | Optional |

### Application Settings
- Wake word sensitivity can be adjusted in `wake_word_listener.py`
- TTS voice and speed settings in `tts.py`
- Skill registration and routing in `command_router.py`

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific test categories:
```bash
# Test skills
python -m pytest tests/skills/

# Test TTS functionality
python -m pytest tests/tts/

# Test speech-to-text
python -m pytest tests/stt/
```

## 🔌 Extending the System

### Adding New Skills

1. Create a new skill file in the `skills/` directory
2. Implement the required functions for your skill
3. Follow the existing skill patterns for consistency
4. Add command routing logic in `command_router.py`

### Skill Development Guidelines

- Each skill should be self-contained
- Include proper error handling and logging
- Add type hints and documentation
- Write corresponding tests

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

[Add your license information here]

## 🆘 Troubleshooting

### Common Issues

**Microphone not working:**
- Check microphone permissions
- Verify audio input device in system settings

**Wake word not detected:**
- Ensure clear pronunciation of "Sarah"
- Check microphone sensitivity settings
- Test in a quiet environment

**API errors:**
- Verify API keys are correctly set in environment variables
- Check internet connection for external API calls

**Module import errors:**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version compatibility

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the test files for usage examples

---

**Built with ❤️ for voice-controlled automation**