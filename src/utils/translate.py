from langchain_core.messages import HumanMessage
from llm import get_llm

llm = get_llm()


def translate_en_to_ar(text: str) -> str:
    if not text or not text.strip():
        return ""

    prompt = f"""
You are a professional medical translator.

Translate the following medical report into clear, fluent Modern Standard Arabic.

Requirements:
- Preserve all headings exactly.
- Preserve numbering and bullet points.
- Preserve the report structure exactly.
- Translate medical terms into commonly used Arabic equivalents.
- Keep medication names (e.g., Metformin, Empagliflozin, Liraglutide) in English.
- Preserve laboratory values, numbers, units, and measurements exactly.
- Do not add explanations or comments.
- Return ONLY the translated report.

Report:

{text}
"""

    try:
        response = llm.invoke([HumanMessage(content=prompt)])

        if response and hasattr(response, "content") and response.content:
            return response.content.strip()

    except Exception as e:
        print(f"Translation error: {e}")

    return text
