jarvis_ai/
├── main.py                      # Entry point
├── core/                        # Core engine logic
│   ├── voice_input.py           # Handles listening
│   ├── tts.py                   # Handles speaking
│   ├── command_router.py        # Routes parsed commands to skills
│   └── parser.py                # NLP or keyword parser (basic now, LLM later)
├── skills/                      # Feature modules (independent)
│   ├── base_skill.py            # Base class/interface for all skills
│   ├── general/                 # General commands (hello, help, etc.)
│   │   └── hello_skill.py
│   ├── system/                  # System-related commands
│   │   └── app_launcher.py
│   └── (future skills...)       # weather/, youtube/, screen_reader/, etc.
├── utils/
│   ├── logger.py                # Logging utility
│   └── config.py                # Global settings
├── assets/                      # Icons, screenshots, audio, etc.
├── requirements.txt
└── README.md
