import json
import logging
import re
from openai import OpenAI
from app.core.config import settings

# Configure logger for this module
logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = OpenAI(api_key=settings.OPENAI_API_KEY)


def analyze_ticket(title: str, description: str) -> dict:
    """
    Analyze a support ticket using AI and return structured metadata.

    This function:
    - Sends the ticket to the OpenAI API for classification
    - Expects a strict JSON response
    - Cleans and parses the response safely
    - Falls back to default values on failure

    Args:
        title (str): Ticket title
        description (str): Ticket description

    Returns:
        dict: Structured ticket metadata including summary, category,
              issue type, sub-issue type, ticket type, and priority
    """

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

        # Remove markdown/code block formatting if present
        content = re.sub(r"^```json|```$", "", content, flags=re.MULTILINE).strip()

        logger.info("AI RAW OUTPUT: %s", content)

        parsed = json.loads(content)

        return parsed

    except Exception as e:
        logger.error("AI ERROR: %s", e)

        # Fallback response to prevent system failure
        return {
            "summary": None,
            "category": None,
            "issue_type": None,
            "sub_issue_type": None,
            "ticket_type": None,
            "priority": "medium",
        }
