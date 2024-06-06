# CandleGod's Discord Bot

CandleGod's Discord Bot is a powerful tool designed to enhance the safety and transparency of your Discord server. The bot offers features such as scanning links to check for malicious content and logging deleted messages to a designated channel.

## Features

- **Link Scanning**: Automatically scans links posted in the server to check if they are malicious.
- **Deleted Message Logging**: Logs deleted messages to a specified channel for moderation purposes.

## Installation

Run it in visual studio code be sure to add the nescesary libraries visual studio debugger should tell you the exact ones if missing from this file
- pip install discord
- pip install python-dotenv
- pip install requests

### Link Scanning

Whenever a user posts a link in the server, the bot will automatically scan the link for potential threats. If the link is found to be malicious, the bot will delete the message and notify the user and moderators.

### Deleted Message Logging

The bot can log deleted messages to a specific channel. To set up the logging channel, use the following command:

