import speech_recognition as sr
import webbrowser
import datetime
import pyjokes
import pyttsx3
import time

def sptxt():  # Speech to text
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=10)  # Added timeout for listen
            print("Recognizing...")
            data = recognizer.recognize_google(audio)
            print(f"Recognized: {data}")
            return data
        except sr.UnknownValueError:
            print("Not Understanding")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out")
            return None

def txtsp(x):  # Text to speech
    engine = pyttsx3.init()
    voice = engine.getProperty('voices')
    engine.setProperty('voice', voice[1].id)  # Change index if needed
    engine.setProperty('rate', 150)
    engine.say(x)
    engine.runAndWait()

def main():
    while True:
        print("Waiting for command...")
        text = sptxt()  # Get speech to text
        if text:  # Check if text is not None
            text = text.lower()
            print(f"Processing command: {text}")  # Debugging statement

            if text == "hey alina":
                txtsp("Hello, how can I help you?")
                time.sleep(1)  # Give user a moment to say the next command
                data1 = sptxt()
                if data1:
                    data1 = data1.lower()
                    print(f"Sub-command received: {data1}")  # Debugging statement
                    if "your name" in data1:
                        name = "My name is Alina."
                        txtsp(name)
                    elif "how old are you" in data1:
                        age = "I am just a few minutes old."
                        txtsp(age)
                    elif 'what time is it' in data1:
                        time_now = datetime.datetime.now().strftime("%I:%M %p")
                        txtsp(f"The time is {time_now}.")
                    elif "youtube" in data1:
                        txtsp("Opening YouTube")
                        webbrowser.open("https://youtube.com")
                    elif "joke" in data1:
                        joke = pyjokes.get_joke(languages="en", category="neutral")
                        print(joke)
                        txtsp(joke)
                    elif "play song" in data1:
                        # Example URL or path for playing a song
                        txtsp("Playing song")
                        webbrowser.open("https://example.com/song.mp3")  # Replace with a valid URL or path
                    elif "exit" in data1:
                        txtsp("Okay, see you later!")
                        break
                    else:
                        txtsp("Sorry, I didn't understand that.")
                else:
                    txtsp("Sorry, I didn't catch that.")
            else:
                txtsp("Sorry, I didn't recognize the wake word.")
            time.sleep(2)  # Sleep to prevent rapid repeated queries
        else:
            print("No command recognized, please try again.")

if __name__ == '__main__':
    main()

