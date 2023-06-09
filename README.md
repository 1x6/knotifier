# knotifier

knotifier is a Discord bot that tracks titles on bato.to and sends you a notification when a new chapter is released.


## Installation

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/sK1U4R?referralCode=tJrkZx)

 - Clone the repository:
`git clone https://github.com/1x6/knotifier.git`

 - Install the required dependencies: `pip install -r requirements.txt`

 - Set the enviroment vairables in config.py (token, SMTP details, and Telegram bot token)
 - Alternatively, you can edit the strings in the config.py file

 - Run the bot: `python main.py`

## Usage

Once the bot is running, you can interact with it using the following commands:

    /track <link> - Tracks a series by providing a link to a valid bato.to series.
    /email <email> - Sets your email to receive notifications.
    /telegram <channel_id> - Sets your Telegram channel ID to receive notifications.
    /list - Lists the series you are currently tracking.

![ezgif-3-306d53e844](https://github.com/1x6/knotifier/assets/44981148/582f7de1-a58f-45d5-b3cf-d4a1615bd417)
![Telegram_QgqhfAMcCx](https://github.com/1x6/knotifier/assets/44981148/1ffc4674-c612-4a75-a30c-7f6d2f4e638b)
![firefox_CYNC0vxi6M](https://github.com/1x6/knotifier/assets/44981148/ceeb0379-aa23-4a72-b8f0-b49a3f93985c)


## Contributing

Contributions are welcome! If you have any improvements or bug fixes, feel free to submit a pull request.
