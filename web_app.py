"""
Sarah AI Web Interface
A Flask web application with WebSocket support for real-time communication with the Sarah AI assistant.
"""

import threading
import time
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
from typing import Optional, Dict, Any

# Import Sarah AI components
from core.voice_input import listen_with_timeout
from core.command_router import route_command
from core.conversation import handle_conversation
from core.tts import speak
from core.wake_word_listener import listen_continuously, SARAH_WAKE_WORDS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sarah-ai-web-interface-2024'
socketio = SocketIO(app, cors_allowed_origins="*")

class SarahWebInterface:
    """Manages the web interface state and communication with Sarah AI"""
    
    def __init__(self):
        self.current_state = "listening"  # listening, thinking, speaking, idle
        self.current_speech = ""
        self.wake_word_thread: Optional[threading.Thread] = None
        self.is_running = False
        
    def update_state(self, new_state: str, speech_text: str = ""):
        """Update the AI state and broadcast to connected clients"""
        self.current_state = new_state
        self.current_speech = speech_text
        
        # Broadcast to all connected clients
        socketio.emit('state_update', {
            'state': new_state,
            'speech': speech_text,
            'timestamp': time.time()
        })
        
        print(f"[WEB] State updated: {new_state} - {speech_text}")
    
    def start_wake_word_detection(self):
        """Start the wake word detection in a separate thread"""
        if not self.is_running:
            self.is_running = True
            self.wake_word_thread = threading.Thread(
                target=self._wake_word_loop, 
                daemon=True
            )
            self.wake_word_thread.start()
            self.update_state("listening", "Listening for wake word 'Sarah'...")
    
    def stop_wake_word_detection(self):
        """Stop the wake word detection"""
        self.is_running = False
        self.update_state("idle", "Wake word detection stopped")
    
    def _wake_word_loop(self):
        """Main wake word detection loop"""
        try:
            listen_continuously(self._handle_wake_word_activation)
        except Exception as e:
            print(f"[WEB ERROR] Wake word detection failed: {e}")
            self.update_state("idle", f"Error: {str(e)}")
    
    def _handle_wake_word_activation(self, wake_word: str):
        """Handle wake word detection - web interface version"""
        print(f"[WEB] Wake word detected: {wake_word}")
        
        if wake_word.lower() == "sarah":
            self.update_state("speaking", "Yes, Sir?")
            
            # Original speak function for audio
            speak("Yes, Sir?")
            
            # Enter continuous mode
            self._sarah_continuous_mode()
    
    def _sarah_continuous_mode(self):
        """Web version of continuous conversation mode"""
        exit_phrases = [
            "that's all", "thats all", "that is all",
            "bye", "goodbye", "stop listening", "stop", 
            "enough", "dismiss", "thank you that's all"
        ]
        
        conversation_count = 0
        
        try:
            while self.is_running:
                self.update_state("listening", "Listening for your command...")
                
                command = listen_with_timeout(15)
                
                if command == "TIMEOUT":
                    self.update_state("speaking", "I haven't heard anything for a while, Sir. Returning to silent mode.")
                    speak("I haven't heard anything for a while, Sir. I'll return to silent mode now.")
                    self.update_state("listening", "Listening for wake word 'Sarah'...")
                    break
                
                if not command or not command.strip():
                    if conversation_count == 0:
                        response = "How may I assist you, Sir?"
                    else:
                        response = "Anything else, Sir?"
                    
                    self.update_state("speaking", response)
                    speak(response)
                    continue
                
                conversation_count += 1
                command_lower = command.lower().strip()
                
                # Check for exit phrases
                if any(phrase in command_lower for phrase in exit_phrases):
                    response = "You're welcome, Sir. I live to serve."
                    self.update_state("speaking", response)
                    speak(response)
                    self.update_state("listening", "Listening for wake word 'Sarah'...")
                    break
                
                # Check for wake word reinforcement
                if any(word in command_lower.split() for word in SARAH_WAKE_WORDS):
                    response = "Yes, Sir? I'm still listening."
                    self.update_state("speaking", response)
                    speak(response)
                    continue
                
                # Process the command
                try:
                    self.update_state("thinking", f"Processing: {command}")
                    
                    handled = route_command(command)
                    
                    if not handled:
                        # Use conversation AI
                        response = handle_conversation(command)
                        if response:
                            self.update_state("speaking", response)
                        
                except Exception as e:
                    error_response = "I apologize, Sir. I encountered an error. Please try again."
                    self.update_state("speaking", error_response)
                    speak(error_response)
                    print(f"[WEB ERROR] Command processing failed: {e}")
                        
        except KeyboardInterrupt:
            speak("Goodbye, Sir.")
            self.update_state("idle", "Session ended")
        except Exception as e:
            error_response = "I apologize, Sir. I need to step away for a moment."
            speak(error_response)
            self.update_state("idle", f"Error occurred: {str(e)}")
            print(f"[WEB ERROR] Continuous mode failed: {e}")


# Global instance
sarah_interface = SarahWebInterface()

@app.route('/')
def index():
    """Serve the main web interface"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"[WEB] Client connected: {request.sid}")
    
    # Send current state to newly connected client
    emit('state_update', {
        'state': sarah_interface.current_state,
        'speech': sarah_interface.current_speech,
        'timestamp': time.time()
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"[WEB] Client disconnected: {request.sid}")

@socketio.on('start_listening')
def handle_start_listening():
    """Start wake word detection"""
    print("[WEB] Starting wake word detection...")
    sarah_interface.start_wake_word_detection()

@socketio.on('stop_listening')
def handle_stop_listening():
    """Stop wake word detection"""
    print("[WEB] Stopping wake word detection...")
    sarah_interface.stop_wake_word_detection()

@socketio.on('get_status')
def handle_get_status():
    """Get current system status"""
    emit('state_update', {
        'state': sarah_interface.current_state,
        'speech': sarah_interface.current_speech,
        'timestamp': time.time()
    })

if __name__ == '__main__':
    print("🌐 Starting Sarah AI Web Interface...")
    print("📱 Open your browser to: http://localhost:5000")
    
    # Auto-start wake word detection
    sarah_interface.start_wake_word_detection()
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)