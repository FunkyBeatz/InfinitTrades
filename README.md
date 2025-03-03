# INF TRADES Discord Bot

## Overview

Welcome to the **INF TRADES Discord Bot**, a specialized tool designed exclusively for administrators to calculate and display Profit & Loss (P&L) for options trading on SPY, QQQ, IWM, and NVDA. This bot delivers a minimalist, sleek design with a black background, using `+` for profit and `-` for loss indicators, ensuring a clean and professional user experience in Discord.

### Key Features
- **Admin-Only Access:** Restricted to users with Administrator permissions for secure usage.
- **P&L Calculation:** Computes profit/loss percentages for options (calls/puts) on SPY, QQQ, IWM, and NVDA, supporting long and short positions.
- **Custom Output:** Generates a 400x200 pixel black-background image with centered white text for the symbol/strike, entry price, and green/red text for P&L (with `+`/`-` indicators), including optional “Late close” and position (Long/Short).
- **Font Support:** Utilizes the Roboto font (if available) or the default system font, ensuring consistent readability.
- **Embed Display:** Presents results in a professional darker blue embed in Discord for a polished look.

## Prerequisites

Before setting up the bot, ensure you have the following:

| **Requirement**         | **Details**                                                                 |
|-------------------------|-----------------------------------------------------------------------------|
| **Python**              | Python 3.8+ installed on your system.                                       |
| **Discord Bot Token**   | Obtainable from the [Discord Developer Portal](https://discord.com/developers/applications). |
| **Hosting Environment**  | An IDE to run the bot.                           |
| **Python Libraries**    | Install `discord.py` and `Pillow` (PIL) via pip: `pip install discord.py Pillow`. |

## Installation

### 1. Clone or Download the Repository
Clone this repository to your local machine or download the ZIP file from GitHub:
```bash
git clone <your-repo-url>
cd inf-trades-bot
```

### 2. Set Up a Virtual Environment (Optional)
Create and activate a virtual environment to manage dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
Install the required Python libraries:
```bash
pip install discord.py Pillow
```

### 4. Configure the Bot
Create a `.env` file in your project root (or use a Secrets tab if available) to store your Discord bot token:
```env
DISCORD_TOKEN=your_discord_bot_token_here
```
Replace `your_discord_bot_token_here` with your token from the Discord Developer Portal.

### 5. Upload Optional Files
Optionally, download the Roboto font from Google Fonts, save it as `Roboto.ttf`, and upload it to your Replit project or directory for a cleaner font in output images. This is optional—the bot defaults to the system font if Roboto isn’t provided.

### 6. Run the Bot
“Run” the bot with a button if available.

Alternatively, on your local machine, run:
```bash
python main.py
```
The bot will log into Discord and sync its slash commands. Ensure your bot is invited to your Discord server with Administrator permissions.

## Usage

The bot features a single slash command, `/option`, restricted to administrators. Use it as follows:

| **Parameter** | **Description**           | **Example**        |
|---------------|---------------------------|--------------------|
| `symbol`     | Stock symbol (SPY, QQQ, IWM, NVDA). | `SPY`              |
| `strike`     | Strike price with option type (`450c`, `400p`). | `600c`             |
| `entry_price`| Entry price of the option (`10.00`). | `12.00`            |
| `current_price`| Current price of the option (`12.00`). | `45.00`           |
| `position`   | Position type (`long`, `short`). | `long`            |
| `late_call`  | Optional, `true` for “Late close”. | `true`             |

### Example Commands

| **Scenario** | **Command** | **Expected Output** |
|--------------|--------------|---------------------|
| Profit (Long Call) | `/option symbol:SPY strike:600c entry_price:12.00 current_price:45.00 position:long late_call:false` | `+ $45.00 (275.00%) (Long)` (green) |
| Super Negative Loss (Long Call) | `/option symbol:NVDA strike:150c entry_price:10.00 current_price:2.00 position:long` | `- $2.00 (-80.00%) (Long)` (red) |
| Loss with Late Call (Long Call) | `/option symbol:SPY strike:597c entry_price:7.00 current_price:8.00 position:long late_call:true` | `- $8.00 (14.29%) (Late close) (Long)` (red) |

## Configuration

Ensure the `DISCORD_TOKEN` environment variable is set in `.env` or Replit Secrets.
Optionally upload `Roboto.ttf` for a cleaner font; otherwise, the default system font is used.

## Troubleshooting

| **Issue**                    | **Solution**                                                               |
|------------------------------|---------------------------------------------------------------------------|
| Symbols Not Showing          | Ensure `Roboto.ttf` is uploaded or use a default font that supports ASCII. |
| Black Rectangle with “X”     | Check `create_pnl_image` uses `Image.new('RGB', (400, 200), color='#000000')`. |
| Permission Errors            | Confirm the bot and user have Administrator permissions in Discord.        |

## Contributing

This bot is tailored for INF TRADES and currently accepts contributions only from the project owner. For suggestions or custom features, contact the maintainer via his [Main 𝕏 Account](https://x.com/FunkyxBeatz) or WebFrens Discord *(Coming Soon)*.

## Credits

| **Contributor**     | **Role**                    |  **Contact**                  |
|---------------------|-----------------------------|-------------------------------|
| Web Frens           | Developer & Maintainer      | email and Website coming soon |
| INF TRADES Community| Inspiration & Feedback      | Via Discord Server            |

### Libraries Used

- **discord.py:** Discord Integration ([discordpy.readthedocs.io](https://discordpy.readthedocs.io))
- **Pillow (PIL):** Image Generation ([python-pillow.org](https://python-pillow.org))
- **Roboto Font:** Typography (Optional) ([fonts.google.com/specimen/Roboto](https://fonts.google.com/specimen/Roboto))

---

## Follow Me on Social Media

Stay connected and follow my work on social media:

- **Main 𝕏 Account:** [FunkyxBeatz](https://x.com/FunkyxBeatz)
- **Projects 𝕏 Account:** [WebFrens_](https://x.com/WebFrens_)
