from openrouter import OpenRouter
import config
import time


class Classifier:
    def __init__(self):
        self.model = config.MODEL
        self.client = OpenRouter(api_key=config.OPENROUTER_KEY)

    def classify(self, subject: str, body: str) -> str:
        prompt = f"""
Classify this email into either College Advertising or Anything Else.
Only respond with one of those two categories and nothing else.
Decide if the email is marketable college advertising content or not.
If it is, respond with "College Advertising".
If it is not, respond with "Anything Else".
Do not respond with anything else.
Do not explain your reasoning.
Do not use any punctuation.
Do not use any other words.
Only respond with one of those two categories and nothing else.
When I say college I mean universities, colleges, community colleges, trade schools, and other post-secondary educational institutions.
If the intention is to get me to apply to, attend, or engage with such an institution, classify it as College Advertising.
Anything from Case Western Reserve University should be classified as Anything Else.

Subject: {subject}
Body: {body[:500]}
""".strip()

        for attempt in range(3):
            try:
                response = self.client.chat.send(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}]
                )

                output = response.choices[0].message.content.strip()
                print(f"Classifier output for subject '{subject}': {output}")
                return output

            except Exception as e:
                if attempt == 2:
                    raise
                
                print(f"Error during classification attempt {attempt + 1}: {e}. Retrying...")
                time.sleep(2 ** attempt)
