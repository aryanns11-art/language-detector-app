import customtkinter as ctk
from tkinter import END
import speech_recognition as sr
from lingua import Language, LanguageDetectorBuilder


languages = [
    Language.ENGLISH,
    Language.HINDI,
    Language.MARATHI,
    Language.FRENCH,
    Language.GERMAN,
    Language.SPANISH,
    Language.ITALIAN,
    Language.PORTUGUESE,
    Language.CHINESE,
    Language.JAPANESE,
    Language.KOREAN,
    Language.RUSSIAN,
    Language.ARABIC
]

detector = LanguageDetectorBuilder.from_languages(*languages).build()


def detect_text_language():
    text = textbox.get("1.0", END).strip()

    if text == "":
        result_label.configure(text="Please enter some text.")
        return

    language = detector.detect_language_of(text)

    if language:
        result_label.configure(text=f"Detected Language : {language.name.title()}")
    else:
        result_label.configure(text="Could not detect the language.")


def detect_speech_language():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        result_label.configure(text="Listening...")
        root.update()

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        textbox.delete("1.0", END)
        textbox.insert("1.0", text)

        language = detector.detect_language_of(text)

        if language:
            result_label.configure(text=f"Recognized Text:\n{text}\n\nDetected Language: {language.name.title()}")
        else:
            result_label.configure(text="Language could not be detected.")

    except sr.UnknownValueError:
        result_label.configure(text="Speech could not be understood.")

    except sr.RequestError:
        result_label.configure(text="Speech Recognition service unavailable.")


def clear():
    textbox.delete("1.0", END)
    result_label.configure(text="")


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

root.title("Automatic Language Detection")
root.geometry("650x500")

title = ctk.CTkLabel(root,text="Automatic Language Detection",font=("Arial", 24, "bold"))
title.pack(pady=20)

textbox = ctk.CTkTextbox(root,width=550,height=150,font=("Arial", 16))
textbox.pack(pady=10)

text_btn = ctk.CTkButton(root,text="Detect Language from Text",command=detect_text_language,width=250)
text_btn.pack(pady=10)

speech_btn = ctk.CTkButton(root,text="Detect Language from Speech",command=detect_speech_language,width=250)
speech_btn.pack(pady=10)

clear_btn = ctk.CTkButton(root,text="Clear",command=clear,width=250)
clear_btn.pack(pady=10)

result_label = ctk.CTkLabel(root,text="",font=("Arial", 16),wraplength=600,justify="left")
result_label.pack(pady=20)

root.mainloop()