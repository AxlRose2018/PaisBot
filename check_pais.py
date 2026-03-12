import imaplib
import email
import requests
import os

# משתני סביבה שיוגדרו ב-GitHub Secrets
GMAIL_USER = os.getenv('GMAIL_USER')
GMAIL_PASS = os.getenv('GMAIL_PASS')
CHAT_ID = "833079885"
TELEGRAM_TOKEN = "8710719112:AAEMijbd1-vo8AK9lE54jWImDSmxDYKPJgE"
MY_NUMBER = "586262"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message})

def run_check():
    try:
        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(GMAIL_USER, GMAIL_PASS)
        mail.select("inbox")

        # חיפוש המייל האחרון מהפיס
        _, data = mail.search(None, '(FROM "noreply@pais.co.il")')
        latest_id = data[0].split()[-1]
        _, msg_data = mail.fetch(latest_id, "(RFC822)")
        
        msg_content = str(msg_data[0][1])
        
        if MY_NUMBER in msg_content:
            send_telegram(f"📢 זכייה! מנוי {MY_NUMBER} מופיע בתוצאות. בדוק את המייל לפרטים!")
        else:
            send_telegram(f"בדיקה שבועית למנוי {MY_NUMBER}: אין זכייה הפעם.")
            
    except Exception as e:
        send_telegram(f"שגיאה באוטומציה: {str(e)}")

if __name__ == "__main__":
    run_check()
