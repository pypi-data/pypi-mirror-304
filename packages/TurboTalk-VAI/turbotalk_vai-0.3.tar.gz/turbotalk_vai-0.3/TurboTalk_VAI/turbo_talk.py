# TurboTalk_VAI/turbo_talk.py
import speech_recognition as sr
import pyttsx3
import TurboTalk_Custom
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for audio input from the user and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(Fore.GREEN + "Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(Fore.CYAN + f"You: {text}")
            return text
        except sr.UnknownValueError:
            print(Fore.RED + "Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            print(Fore.RED + "Could not request results from Google Speech Recognition service.")
            return None

def start_voice_chat(company_name, bot_name, behaviour):
    """Start the voice chat with the specified parameters."""
    print(Fore.BLUE + "Speak your message or say 'exit' to quit.")
    
    try:
        while True:
            user_input = listen()
            if user_input:
                # Check for exit command
                if user_input.lower() == "exit":
                    print(Fore.MAGENTA + "\nExiting the program. Goodbye!")
                    break

                full_input = (user_input + 
                              f" Only introduce yourself as {bot_name} by {company_name} when asked to do so, "
                              "else not. Always give direct answers to questions or messages in simple words.")
                
                # Call the TurboTalk response generation
                TurboTalk_Custom.turbo_talk_instance.give_response(company_name, bot_name, behaviour, full_input)
                response = TurboTalk_Custom.turbo_talk_instance.get_response()
                
                print(Fore.YELLOW + f"{bot_name}: ")
                print(Fore.WHITE + response)
                speak(response)
            else:
                # If user_input is None, continue listening
                continue
    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\nExiting the program. Goodbye!")
