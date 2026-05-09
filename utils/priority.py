from groq import Groq
import json
import os
from dotenv import load_dotenv

load_dotenv()
groq_key = os.getenv("GROQ_API_KEY")

PRIORITY_INSTRUCTION = """
You are a property maintenance triage assistant for Dwello.
Read the description and return a JSON object with two keys:
  - priority: one of low, medium, high, urgent
  - reason: one sentence explaining why

Rules for each level:
  urgent: safety hazards, flooding, fire risk, no water, no electricity
  high: broken locks, major leaks, no hot water, structural damage
  medium: appliance failures, minor leaks, broken fixtures
  low: cosmetic issues, painting, general wear and tear

Return only valid JSON, no explanation outside the JSON.
"""
client = Groq(api_key=groq_key)
def get_priority(description):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": PRIORITY_INSTRUCTION},
            {"role": "user", "content": description}
        ],
        temperature=0.1,
        max_tokens=100
    )
    content = response.choices[0].message.content
    try:
        return json.loads(content)
    except Exception:
        return {'priority': 'medium', 'reason':'Could not determine priority'}