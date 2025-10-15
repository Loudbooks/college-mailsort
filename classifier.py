import requests
import config

class Classifier:
    def __init__(self):
        self.api_url = config.OLLAMA_API
        self.model = config.MODEL
        self.auth_key = config.AUTHENTICATION_KEY

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

Subject: {subject}
Body: {body[:500]}
"""
        try:
            response = requests.post(
                self.api_url,
                json={"model": self.model, "prompt": prompt, "stream": True},
                headers={"X-API-Key": f"{self.auth_key}"},
                timeout=120,
                stream=True
            )
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            return None
        
        output = ""
        if response.status_code == 200:
            output = response.json().get("response", "")
            import re
            output = re.sub(r"<think>.*?</think>", "", output, flags=re.DOTALL).strip()
        else:
            output = "Anything Else"
        
        return output
