import speech_recognition as sr
import pyttsx3
import pywhatkit
import webbrowser

# Initialize speech engine and recognizer
listener = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Make the assistant speak."""
    engine.say(text)
    engine.runAndWait()

def hear_command():
    """Listen for a voice command and return it."""
    command = ""
    try:
        with sr.Microphone() as mic:
            print("🎤 Listening...")
            voice = listener.listen(mic)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"🗣️ You said: {command}")
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Speech recognition service is unavailable.")
    return command

def run_assistant():
    """Process the command."""
    command = hear_command()

    if 'open youtube' in command:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif 'play' in command:
        song = command.replace('play', '').strip()
        if song:
            speak(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)
        else:
            speak("Please tell me what to play.")

    else:
        speak("I can only open or play videos on YouTube right now.")


run_assistant()
