import os

def token():
    env_token = os.environ.get('TOKEN')
    if env_token:
        return env_token
    else:
        return 'zz'

def smtp_username():
    env_username = os.environ.get('SMTP_USERNAME')
    if env_username:
        return env_username
    else:
        return 'zz@gmail.com'

def smtp_password():
    env_password = os.environ.get('SMTP_PASSWORD')
    if env_password:
        return env_password
    else:
        return 'zz123'

def telegram_bot_token():
    env_bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if env_bot_token:
        return env_bot_token
    else:
        return 'zz'
    
def base_url():
    return 'https://bato.to/series/'
