from openrouter import OpenRouter
import config

class Classifier:
    def __init__(self):
        self.api_url = config.OPENROUTER_KEY
        self.model = config.MODEL

    def classify(self, subject, body):
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
Results for an application to that college should be classified as Anything Else. 
Anything regarding my active, already submitted application should be classified as Anything Else.
Anything from Case Western Reserve University should be classified as Anything Else.

Subject: {subject}
Body: {body[:500]}
"""

        with OpenRouter(
            api_key=config.OPENROUTER_KEY
        ) as client:
            response = client.chat.send(
                model=config.MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
        output = response.choices[0].message.content.strip()
        print(f"Classifier output for email UID {subject}: {output}")
        
        return output
