import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def translate_en_to_ar(text: str) -> str:
    if not text or not text.strip():
        return ""

    prompt = (
        "You are a professional medical translator. Translate the following text into clear, "
        "fluent Modern Standard Arabic suitable for a patient to read and understand. "
        "Use simple and natural language while keeping medical information accurate. "
        "Translate medical terms into commonly used Arabic equivalents (for example, "
        "'HbA1c' → 'السكري التراكمي'). "
        "Make sentences short, clear, and easy for a non-medical reader to understand. "
        "Just write the translation without annotating that this text is being translated to Arabic or any other notations.\n\n"
        f"Text to translate:\n{text}"
    )

    model_name = "gemini-2.0-flash"
    
    # محاولة الاستدعاء مع إعادة المحاولة تلقائياً عند تجاوز Rate Limit
    for attempt in range(3):
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)

            if response and hasattr(response, "text") and response.text:
                return response.text.strip()
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower():
                print(f"Rate limit hit. Waiting 5 seconds before retry (Attempt {attempt + 1}/3)...")
                time.sleep(5)
            else:
                print(f"Translation error: {e}")
                break

    return text