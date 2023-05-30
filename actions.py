import database
import bato
import config
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def check_for_new():
    # Get all tracked series from the database
    tracked_series = database.cursor.execute("SELECT * FROM monitored").fetchall()

    for series in tracked_series:
        uid, series_id, last_chapter, friendly_name = series

        # Get the current number of chapters from Bato.to
        current_chapters = bato.get_chapters(series_id)
        print(f"{friendly_name}: {current_chapters} {last_chapter}")
        # Check if there is a difference in the number of chapters
        if current_chapters > last_chapter:
            # Trigger the desired action (e.g., send a DM/email/Telegram message)
            trigger_action(uid, series_id, friendly_name, current_chapters)

            # Update the last chapter in the database
            database.cursor.execute("UPDATE monitored SET lastChapter = ? WHERE uid = ?", (current_chapters, uid))
            database.connection.commit()

def trigger_action(uid, series_id, friendly_name, current_chapters):
    # Implement the action you want to perform when a new chapter is available
    # You can use the uid, series_id, and current_chapters as needed
    # For example, send a DM, email, or Telegram message to the user
    # Example code for sending a DM using a fictional messaging API:
    msg = f'A new chapter is available for series "{friendly_name}".\nTotal chapters: {current_chapters}\nhttps://bato.to/series/{series_id}'
    print(msg)
    email = database.knotifier.db.get_email(uid)
    if email:
        send_mail('New chapter released', msg, email)
    telegram_chat_id = database.knotifier.db.get_telegram_chat_id(uid)
    if telegram_chat_id:
        send_telegram(telegram_chat_id, msg)

def send_mail(subj, body, recipient):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = config.smtp_username()
    smtp_password = config.smtp_password()

    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = recipient
    message['Subject'] = subj
    message.attach(MIMEText(body, 'plain'))
    # Connect to the SMTP server and send the email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)

    print(f'Email sent to {recipient} successfully!')

def send_telegram(chat_id, message):
    url = f'https://api.telegram.org/bot{config.telegram_bot_token()}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
        'disable_web_page_preview': True
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        print(f'Telegram message sent to chat ID {chat_id} successfully!')
    else:
        print(f'Failed to send Telegram message to chat ID {chat_id}. Error: {response.text}')

