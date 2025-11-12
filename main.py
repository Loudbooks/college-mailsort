from imap_client import IMAPClient
from classifier import Classifier
from router import Router
import config
import time

def main():
    imap_client = IMAPClient(config.IMAP_HOST, config.IMAP_USER, config.IMAP_PASS)
    classifier = Classifier()
    router = Router(imap_client)
    
    print("Email service started. Checking for new emails every 60 seconds.")
    
    while True:
        try:
            messages = imap_client.fetch_unseen()
            for uid, subject, from_, body in messages:
                label = classifier.classify(subject, body)
                
                if label is None:
                    print(f"Classification failed for email UID: {uid}. Skipping.")
                    continue
                
                if label not in config.FOLDERS:
                    continue
                
                router.route(uid, label)
        except Exception as e:
            print(f"An error occurred: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    main()