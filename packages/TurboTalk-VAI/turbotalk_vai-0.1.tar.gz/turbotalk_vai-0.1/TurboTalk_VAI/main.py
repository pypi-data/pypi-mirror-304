# main.py

import speech_recognition as sr
import pyttsx3
import TurboTalk_VAI
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
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

def main():
    company_name = "Rango Productions"
    bot_name = "Claud AI"
    behaviour = "like a Professor"

    turbo_talk_instance = TurboTalk_VAI.TurboTalk(company_name, bot_name, behaviour)

    print(Fore.BLUE + "Speak your message or say 'exit' to quit.")

    try:
        while True:
            user_input = listen()
            if user_input:
                if user_input.lower() == "exit":
                    print(Fore.MAGENTA + "\nExiting the program. Goodbye!")
                    break

                turbo_talk_instance.generate_response(user_input)
                response = turbo_talk_instance.get_response()
                
                print(Fore.YELLOW + bot_name + ": ")
                print(Fore.WHITE + response)
                speak(response)
            else:
                continue
    except KeyboardInterrupt:
        print(Fore.MAGENTA + "\nExiting the program. Goodbye!")

if __name__ == "__main__":
    main()
