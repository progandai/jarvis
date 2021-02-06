import os
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr


def speech_to_text(question='Comment puis-je vous aider ?'):
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(question)
        text_to_speech(text=question, filename='question_de_jarviset')
        audio = r.listen(source)

    voice_data = None
    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        voice_data = r.recognize_google(audio, language='fr-FR')
    except sr.UnknownValueError:
        text_to_speech(text="Je n'ai pas compris ce que vous avez dis", filename='erreur_enregistrement')
        #print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        text_to_speech(text="Le service n'est pas disponible pour le moment", filename='erreur_api_google')
        #print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    return voice_data


def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='fr') # text to speech
    tts.save(filename + '.mp3')
    playsound(filename + '.mp3')
    os.remove(filename + '.mp3')
    
def is_keywords(text, key_words):
    split_text = text.split()
    for k_w in key_words:
        for w in split_text:
            if k_w in w:
                return True
    return False
        