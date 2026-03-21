import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings
import os

def initialiser_firebase():
    if not firebase_admin._apps:
        if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        else:
            print(f"Fichier Firebase introuvable à : {settings.FIREBASE_CREDENTIALS_PATH}")

def envoyer_notification_push(fcm_token, titre, message, data_supplementaire=None):
    initialiser_firebase()
    
    if not firebase_admin._apps:
        return False, "Firebase non configuré"

    try:
        message_push = messaging.Message(
            notification=messaging.Notification(
                title=titre,
                body=message,
            ),
            data=data_supplementaire if data_supplementaire else {},
            token=fcm_token,
        )
        
        response = messaging.send(message_push)
        return True, response
        
    except Exception as e:
        return False, str(e)