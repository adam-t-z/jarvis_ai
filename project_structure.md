# Jarvis AI Project Structure

```
jarvis_ai/
├── assets/
│   ├── apps/
│   │   ├── apps.json                 # Application mappings for launcher
│   │   └── find_exe_start_menu.py    # Script to find executables
│   └── llms/
│       ├── openrouter_models.txt     # OpenRouter model configurations
│       ├── test_gpt2.py             # GPT-2 testing script
│       ├── test_mistral.py          # Mistral model testing
│       ├── test_openrouter.py       # OpenRouter API testing
│       └── test_tinyllama.py        # TinyLlama model testing
├── core/
│   ├── command_router.py            # Routes commands to appropriate skills
│   ├── tts.py                       # Text-to-speech functionality
│   └── voice_input.py               # Voice input capture and processing
├── old/
│   └── core/
│       └── voice_input.txt          # Legacy voice input configuration
├── output/
│   ├── test.json                    # Test output data
│   └── test.txt                     # Test output text
├── skills/
│   ├── general/
│   │   └── hello_skill.py           # Basic greeting functionality
│   └── system/
│       └── app_launcher.py          # Application launching with JSON mapping
├── tests/
│   ├── skills/
│   │   └── test_open_appsjson.py    # Tests for app JSON functionality
│   ├── stt/                         # Speech-to-text tests
│   │   ├── test_fastwhisper.py      # FastWhisper testing
│   │   └── test_whisperX.py         # WhisperX testing
│   ├── tts/                         # Text-to-speech tests
│   │   └── test_tts.py              # TTS functionality testing
│   ├── test.py                      # General test file
│   ├── test_11labs.py               # ElevenLabs TTS testing
│   └── test_listen.py               # Audio listening tests
├── README.md                        # Project documentation
└── main.py                          # Main application entry point
```

## Project Overview

**Jarvis AI** is a voice-controlled AI assistant with a modular architecture designed for extensibility and ease of use.

### Key Components

#### Core Engine (`core/`)
- **command_router.py**: Central command routing with app launch integration
- **tts.py**: Text-to-speech output system
- **voice_input.py**: Voice input capture and processing
- **wake_word_listener.py**: Speech recognition-based wake word detection
- **conversation.py**: LLM-powered conversational responses
- **openrouter_client.py**: OpenRouter API client with error handling

#### Skills System (`skills/`)
- **general/hello_skill.py**: Basic conversational responses
- **system/app_launcher.py**: Enhanced app launching with JSON mapping and fuzzy matching

#### Assets (`assets/`)
- **apps/apps.json**: Comprehensive application mapping (90+ apps)
- **llms/**: Language model testing and configuration files

#### Testing (`tests/`)
- Comprehensive test suite covering skills, STT, TTS, and core functionality
- Modular testing approach matching the project architecture

### Architecture Highlights

1. **Modular Design**: Pluggable skills system for easy extension
2. **Voice Integration**: End-to-end voice command processing
3. **Smart App Launching**: Fuzzy matching and natural language app commands
4. **Extensible**: Easy to add new skills and capabilities
5. **Well-Tested**: Comprehensive test coverage across all components

### Recent Enhancements

- ✅ Enhanced app launcher with JSON mapping support
- ✅ Fuzzy matching for app names
- ✅ Integrated command routing with natural language processing
- ✅ Support for 90+ applications via JSON configuration
- ✅ **Sarah-Only Activation**: Responds only to "Sarah" wake word and variations
- ✅ **Continuous Mode**: Stays active until dismissed with "that's all", "bye", or "stop listening"
- ✅ **Speech Recognition**: Uses Google Speech Recognition for wake word detection
- ✅ **Natural Interaction**: Supports multiple pronunciations ("Sarah", "Sara", "Sari", etc.)
- ✅ **Polite Responses**: Respectful language with "Sir" addressing throughout
- ✅ **Simplified Architecture**: Removed unnecessary fallback complexity