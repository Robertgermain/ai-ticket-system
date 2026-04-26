from openai import OpenAI
from app.core.config import settings
import json
import re

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_ticket(title: str, description: str) -> dict:
    prompt = f"""
You are an IT support ticket classification system.

Return ONLY a valid JSON object with the following fields:
- summary (short concise summary)
- category (hardware, software, network, security, access, other)
- issue_type (short snake_case label)
- sub_issue_type (more specific snake_case label)
- ticket_type (incident, request, alert)
- priority (low, medium, high)

Ticket:
Title: {title}
Description: {description}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            messages=[
                {"role": "system", "content": "You must return ONLY valid JSON."},
                {"role": "user", "content": prompt},
            ],
        )

        content = response.choices[0].message.content.strip()

        # 🔥 Remove markdown/code block formatting if present
        content = re.sub(r"^```json|```$", "", content, flags=re.MULTILINE).strip()

        # 🧪 Debug (you can remove later)
        print("AI RAW OUTPUT:", content)

        return json.loads(content)

    except Exception as e:
        print("❌ AI ERROR:", e)

        # Fallback response so your app doesn't break
        return {
            "summary": None,
            "category": None,
            "issue_type": None,
            "sub_issue_type": None,
            "ticket_type": None,
            "priority": "medium",
        }
