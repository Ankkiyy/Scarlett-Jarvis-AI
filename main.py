import pyttsx3 as pyttsx
import aiml
import speech_recognition as sr
import subprocess
import os

TALK_SPEED = 140

engine = pyttsx.init()
voices = engine.getProperty('voices')
print(voices)
for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")

def speak(jarvis_speech):
    engine.setProperty('rate', TALK_SPEED)  # Set the talk speed
    engine.say(jarvis_speech)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Talk to J.A.R.V.I.S: ")
        audio = r.listen(source)
    try:
        recognized_text = r.recognize_google(audio)
        print(recognized_text)
        return recognized_text
    except sr.UnknownValueError:
        speak("I couldn't understand what you said! Would you like to repeat?")
        return listen()
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


brain_file = "aiml_brain.brn"

kernel = aiml.Kernel()

# Check if the AIML brain file exists
if os.path.isfile(brain_file):
    # If the brain file exists, load it
    kernel.bootstrap(brainFile=brain_file)
else:
    # If the brain file doesn't exist, load AIML files and save the brain
    kernel.learn("startup.xml")
    kernel.respond("load aiml")
    kernel.saveBrain(brain_file)
    print(f"AIML brain saved to {brain_file}")

while True:
    user_input = listen()
    if user_input.strip().lower() == "exit":
        break

    print(user_input)
    aiml_response = kernel.respond(user_input)
    print(aiml_response)

    if "python" in aiml_response:
        script = aiml_response.split("python")[1].strip()
        subprocess.call(script, shell=True)
    elif "TALK SPEED" in aiml_response:
        TALK_SPEED = int(aiml_response.split("TALK SPEED")[1].strip())
        speak("Talk speed changed to " + str(TALK_SPEED))
    else:
        speak(aiml_response)
