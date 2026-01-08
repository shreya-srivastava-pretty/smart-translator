from googletrans import Translator

translator = Translator()

def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate text into the selected language."""
    if not text.strip():
        return "No text to translate"

    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        return f"Translation Error: {e}"