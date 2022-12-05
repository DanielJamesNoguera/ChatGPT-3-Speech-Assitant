import speech_recognition
import openai
import replicate
import azure.cognitiveservices.speech as speechsdk

AZURE_API_KEY = "INSERT HERE"
AZURE_REGION = "INSERT HERE"
OPENAI_API_KEY = "INSERT HERE"

# This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
speech_config = speechsdk.SpeechConfig(subscription=AZURE_API_KEY, region=AZURE_REGION)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The language of the voice that speaks.
speech_config.speech_synthesis_voice_name='en-IE-EmilyNeural'
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

print("Initiating session...")
 
# The Recognizer is initialized.
UserVoiceRecognizer = speech_recognition.Recognizer()

openai.api_key = OPENAI_API_KEY

def speak(wordsToBeSpoken):
    speech_synthesis_result = speech_synthesizer.speak_text_async(wordsToBeSpoken).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(wordsToBeSpoken))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

def sendToAi(speech):

    if "goodbye" in speech:
        speak("Goodbye.")
        print("Ending session.")
        exit()

    if "picture" in speech:
        Replicate = replicate.Client(api_token="b17591de20bb7d829630bce30b76e7366639f6db")
        model = Replicate.models.get("stability-ai/stable-diffusion")
        version = model.versions.get("27b93a2413e7f36cd83da926f3656280b2931564ff050bf9575f1fdf9bcd7478")

        pr = speech.split("picture of", 1)
        print(pr[1])
        output = version.predict(prompt=pr[1])
        print(output[0])
        speak("Sure. Take a look.")
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

            sendToAi(UserVoiceInput_converted_to_Text)
    
    except KeyboardInterrupt:
        print('A KeyboardInterrupt encountered; Terminating the Program !!!')
        exit(0)
    
    except speech_recognition.UnknownValueError:
        print("")
