INF TRADES Discord Bot
Welcome to the INF TRADES Discord Bot, a specialized tool designed for calculating and displaying Profit & Loss (P&L) for options trading on SPY, QQQ, IWM, and NVDA. This bot is tailored for administrators, providing a clean, professional interface in Discord to track option trades with a simple black-background output.
Overview
The INF TRADES bot is a Discord slash command bot that allows authorized administrators to calculate and visualize the P&L for options trades. It features a minimalist design with a black background, using + for profit and - for loss indicators, and supports custom formatting for long/short positions and late calls. The bot is built using Python, Discord.py, and PIL (Python Imaging Library) for image generation.
Features
Admin-Only Access: Only users with Administrator permissions can use the /option command.

P&L Calculation: Computes profit/loss percentages for options (calls/puts) on SPY, QQQ, IWM, and NVDA, supporting long and short positions.

Custom Output: Generates a 400x200 pixel black-background image with centered white text for the symbol/strike, entry price, and green/red text for P&L (with +/- indicators), including optional “Late close” and position (Long/Short).

Font Support: Uses Roboto (if available) or the default system font, with consistent sizing for readability.

Embed Display: Presents results in a professional darker blue embed in Discord for a clean look.

Prerequisites
Before setting up the bot, ensure you have the following:
Python 3.8+ installed on your system.

A Discord bot token (obtainable from the Discord Developer Portal).

A Replit account (or equivalent hosting environment) to run the bot.

The following Python libraries installed:
discord.py (for Discord interaction)

Pillow (PIL, for image generation)

Installation
1. Clone or Download the Repository
Clone this repository to your local machine or download the ZIP file from GitHub:
bash

git clone <your-repo-url>
cd inf-trades-bot

2. Set Up a Virtual Environment (Optional)
Create and activate a virtual environment to manage dependencies:
bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install Dependencies
Install the required Python libraries:
bash

pip install discord.py Pillow

4. Configure the Bot
Create a .env file in your project root directory (or use Replit Secrets) to store your Discord bot token:

DISCORD_TOKEN=your_discord_bot_token_here

Replace your_discord_bot_token_here with the token you obtained from the Discord Developer Portal.

5. Upload Optional Files
If desired, download the Roboto font from Google Fonts, save it as Roboto.ttf, and upload it to your Replit project or project directory for a cleaner, modern font in the output images. This is optional—the bot uses the default system font if Roboto isn’t provided.

6. Run the Bot
In Replit, click the “Run” button to start the bot.

Alternatively, on your local machine, run:
bash

python main.py

The bot will log into Discord and sync its slash commands. Ensure your bot is invited to your Discord server with the necessary permissions (Administrator for command execution).

Usage
The bot uses a single slash command, /option, which is restricted to administrators. Use it as follows:
Command: /option
Description: Calculate and display the P&L for an option trade.
Parameters:
symbol: The stock symbol (SPY, QQQ, IWM, or NVDA).

strike: The strike price with option type (e.g., 450c for a call, 400p for a put).

entry_price: The entry price of the option (e.g., 10.00).

current_price: The current price of the option (e.g., 12.00).

position: The position type (long or short).

late_call: Optional, indicate if it’s a late call (defaults to False, set to true for “Late close”).

Example Commands:
Profit (Long Call):

/option symbol:SPY strike:600c entry_price:12.00 current_price:45.00 position:long late_call:false

Expected Output: “SPY $600 Call” (white), “$12.00” (white), “+ $45.00 (275.00%) (Long)” (green).

Super Negative Loss (Long Call):

/option symbol:NVDA strike:150c entry_price:10.00 current_price:2.00 position:long

Expected Output: “NVDA $150 Call” (white), “$10.00” (white), “- $2.00 (-80.00%) (Long)” (red).

Loss with Late Call (Long Call):

/option symbol:SPY strike:597c entry_price:7.00 current_price:8.00 position:long late_call:true

Expected Output: “SPY $597 Call” (white), “$7.00” (white), “- $8.00 (14.29%) (Late close) (Long)” (red).

Notes:
Only users with Administrator permissions can execute this command.

The output is displayed in a 400x200 black-background image within a darker blue Discord embed.

Configuration
Ensure the DISCORD_TOKEN environment variable is set in .env or Replit Secrets.

Optionally upload Roboto.ttf for a cleaner font; otherwise, the default system font is used.

Troubleshooting
Triangles/Arrows Not Showing: If symbols don’t display, ensure Roboto.ttf is uploaded, or the default font supports ASCII symbols (+/-). The code uses + for profit and - for loss, which are universally supported.

Black Rectangle with “X”: If a black rectangle with an “X” appears, ensure create_pnl_image uses Image.new('RGB', (400, 200), color='#000000') and check for file corruption or Discord rendering issues.

Permission Errors: Verify the bot and user have Administrator permissions in Discord.

Contributing
This bot is tailored for INF TRADES and currently accepts contributions only from the project owner. If you have suggestions or need custom features, contact the maintainer.
License
This project is licensed under the MIT License - see the LICENSE file for details (if applicable, create a LICENSE file with MIT terms or specify your preferred license).
Credits
Developed by: [Your Name or Team Name] (e.g., INF TRADES Team)

Inspired by: Options trading community and INF TRADES branding.

Libraries Used:
discord.py for Discord integration.

Pillow (PIL) for image generation.

Roboto font from Google Fonts (optional).

