import os

IMAP_HOST = os.getenv("IMAP_HOST", "imap.gmail.com")
IMAP_USER = os.getenv("IMAP_USER", "")
IMAP_PASS = os.getenv("IMAP_PASS", "")

OLLAMA_API = os.getenv("OLLAMA_API", "")
MODEL = os.getenv("MODEL", "gpt-oss")
AUTHENTICATION_KEY = os.getenv("AUTHENTICATION_KEY", "")

FOLDERS = {
    "College Advertising": "College"
}