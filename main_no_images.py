import speech_recognition
import openai
import pyttsx3
UserVoiceRecognizer = speech_recognition.Recognizer()

OPENAI_API_KEY = "INSERT HERE"

print("Initiating session with Kavani...")

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)
 
openai.api_key = OPENAI_API_KEY

def speak(wordsToBeSpoken):
    engine.say(wordsToBeSpoken)
    engine.runAndWait()

def sendToAi(speech):

    if "goodbye" in speech:
        speak("Goodbye.")
        print("Ending session with Kavani.")
        exit()
    else:
        response = openai.Completion.create(
        model="text-davinci-003",
        prompt=speech,
        temperature=0.4,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        print(response.choices[0].text)
        speak(response.choices[0].text)
 
while(1):

    try:
 
        with speech_recognition.Microphone() as UserVoiceInputSource:
 
            UserVoiceRecognizer.adjust_for_ambient_noise(UserVoiceInputSource, duration=0.5)
 
            # The Program listens to the user voice input.
            UserVoiceInput = UserVoiceRecognizer.listen(UserVoiceInputSource)
 
            UserVoiceInput_converted_to_Text = UserVoiceRecognizer.recognize_google(UserVoiceInput)
            UserVoiceInput_converted_to_Text = UserVoiceInput_converted_to_Text.lower()

            print(UserVoiceInput_converted_to_Text)
            sendToAi(UserVoiceInput_converted_to_Text)
    
    except KeyboardInterrupt:
        print('A KeyboardInterrupt encountered; Terminating the Program !!!')
        exit(0)
    
    except speech_recognition.UnknownValueError:
        print("")
