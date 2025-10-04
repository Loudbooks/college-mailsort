from imap_client import IMAPClient
from classifier import Classifier
from router import Router
import config
import time

def main():
    imap_client = IMAPClient(config.IMAP_HOST, config.IMAP_USER, config.IMAP_PASS)
    classifier = Classifier()
    router = Router(imap_client)

    messages = imap_client.fetch_unseen()
    for e_id, subject, from_, body in messages:
        label = classifier.classify(subject, body)
        
        if label not in config.FOLDERS:
            
            print(f"Unknown label '{label}' for email ID {e_id}. Skipping routing.")
            continue
        
        router.route(e_id, label)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(60)