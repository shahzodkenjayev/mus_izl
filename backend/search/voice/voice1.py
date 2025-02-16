import speech_recognition as sr

# Terminlar ro'yxatini txt fayldan yuklash
def load_terms(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [line.strip().lower() for line in file]

# Matnni terminlarga nisbatan tekshirish
def check_terms_in_text(text, terms):
    found_terms = [term for term in terms if term in text.lower()]
    return found_terms

# Audio yozuvni matnga aylantirish
def transcribe_audio(audio_file, recognizer):
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio, language='uz-UZ')  # Tilni moslang
    except sr.UnknownValueError:
        return "Tushunarsiz audio"
    except sr.RequestError as e:
        return f"Xatolik: {e}"

# Asosiy funksiya
def main():
    terms_file = "terms.txt"  # Terminlar saqlangan fayl
    audio_file = "audio.wav"  # Ovozli yozuv fayli
    terms = load_terms(terms_file)
    
    recognizer = sr.Recognizer()
    text = transcribe_audio(audio_file, recognizer)
    
    print(f"Transkriptsiya: {text}")
    
    found_terms = check_terms_in_text(text, terms)
    if found_terms:
        print(f"Topilgan terminlar: {', '.join(found_terms)}")
    else:
        print("Terminlar topilmadi.")

if __name__ == "__main__":
    main()
