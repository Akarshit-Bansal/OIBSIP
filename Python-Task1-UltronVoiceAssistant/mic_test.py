import speech_recognition as sr

recognizer = sr.Recognizer()

MICROPHONE_INDEX = 1

print(f"Using microphone #{MICROPHONE_INDEX}")
print("Adjusting for background noise...")

with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
    recognizer.adjust_for_ambient_noise(source, duration=2)

    print("Listening...")
    print("Say clearly: Hello Ultron")

    try:
        audio = recognizer.listen(
            source,
            timeout=10,
            phrase_time_limit=7
        )

        print("Processing...")

        text = recognizer.recognize_google(audio)
        print("You said:", text)

    except sr.WaitTimeoutError:
        print("No speech detected within the timeout.")

    except sr.UnknownValueError:
        print("Speech was captured, but I could not understand it.")

    except sr.RequestError as e:
        print("Google Speech Recognition error:", e)