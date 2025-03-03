import discord
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
import io
import re
import os
import logging

# Set up logging to Replit console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up bot with intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# Function to calculate P&L percentage
def calculate_pnl(entry_price, current_price, is_call, is_long):
    if is_long:
        if is_call:
            pnl = ((current_price - entry_price) / entry_price) * 100
        else:  # put
            pnl = ((entry_price - current_price) / entry_price) * 100
    else:  # short
        if is_call:
            pnl = ((entry_price - current_price) / entry_price) * 100
        else:  # put
            pnl = ((current_price - entry_price) / entry_price) * 100
    return round(pnl, 2)


# Function to create P&L image with black background, 400x200, matching the screenshot
def create_pnl_image(symbol,
                     strike,
                     option_type,
                     pnl_percentage,
                     entry_price,
                     current_price,
                     late_call=False,
                     position=None):
    # Create a new image with black background, 400x200
    final_img = Image.new(
        'RGB', (400, 200),
        color='#000000')  # Solid black background, no transparency

    draw = ImageDraw.Draw(final_img)

    try:
        # Try to use Roboto font (if uploaded as "Roboto.ttf") with consistent size
        font = ImageFont.truetype("Roboto.ttf",
                                  size=24)  # Size for readability in 400x200
        # Test rendering with green and red to ensure consistency
        draw.text((0, 0), "Test", font=font, fill='#00FF00')  # Green test
        draw.text((0, 0), "Test", font=font, fill='#FF0000')  # Red test
    except Exception:
        # Fallback: Use default font
        font = ImageFont.load_default()

    # Position text to match the screenshot format (centered vertically, left-aligned or centered as needed)
    # Symbol + Strike (e.g., "SPY $597 Call") - centered horizontally, top
    symbol_strike_text = f"{symbol} ${strike[:-1]} {option_type}"
    draw.text(
        ((400 - draw.textlength(symbol_strike_text, font)) // 2,
         20),  # Centered horizontally, 20px from top
        symbol_strike_text,
        font=font,
        fill='#FFFFFF')  # White text

    # Entry Price (e.g., "$0.97") - centered horizontally, middle
    draw.text(
        ((400 - draw.textlength(f"${entry_price:.2f}", font)) // 2,
         80),  # Centered horizontally, 80px from top
        f"${entry_price:.2f}",
        font=font,
        fill='#FFFFFF')  # White text

    # P&L with triangle, price, %, and Late close/Long or Short - centered horizontally, bottom
    # Ensure triangle symbols display correctly with multiple fallbacks
    triangle_options = [
        ("▲", "▼"),  # Unicode up/down triangles (U+25B2, U+25BC)
        ("△", "▽"),  # Unicode white up/down triangles (U+25B3, U+25BD)
        (
            "▶", "▼"
        ),  # Unicode right triangle/down triangle (U+25B6, U+25BC) as alternative
        (
            "▴", "▾"
        )  # Unicode black up/down triangles (U+25B4, U+25BE) as final Unicode fallback
    ]

    triangle = None
    for up, down in triangle_options:
        try:
            # Test if the font can render this triangle pair
            draw.text((0, 0), up if pnl_percentage >= 0 else down, font=font)
            triangle = up if pnl_percentage >= 0 else down
            break
        except UnicodeEncodeError:
            continue

    if triangle is None:
        # Fallback to graphical symbols (e.g., ASCII or simple characters) if Unicode fails completely
        triangle = "^" if pnl_percentage >= 0 else "v"  # Simple ASCII caret/down arrow as last resort

    color = '#00FF00' if pnl_percentage >= 0 else '#FF0000'  # Green for profit, red for loss
    pnl_text = f"{triangle} ${current_price:.2f} ({pnl_percentage:.2f}%)"
    if late_call:
        pnl_text += " (Late close)"
    if position and position.lower() in ["long", "short"]:
        pnl_text += f" ({position.capitalize()})"

    draw.text(
        ((400 - draw.textlength(pnl_text, font)) // 2,
         140),  # Centered horizontally, 140px from top
        pnl_text,
        font=font,
        fill=color)  # Green or red text

    buffer = io.BytesIO()
    final_img.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)
    return buffer


###
### Commented out complex background and container code for future reference
###
### # Load background image (use your uploaded "background.png" exclusively at 400x550, no fallbacks)
### try:
###     # Load background.png and resize to 400x550, maintaining aspect ratio
###     bg_img = Image.open("background.png")
###     bg_width, bg_height = bg_img.size
###
###     # Target a 400x550 rectangle (wider at 400px, taller at 550px)
###     target_width = 400
###     target_height = 550
###
###     # Scale background to fit target size while maintaining aspect ratio
###     if bg_width / bg_height > target_width / target_height:
###         # If wider, scale to target width, adjust height
###         new_width = target_width
###         new_height = int(bg_height * (target_width / bg_width))
###     else:
###         # If taller, scale to target height, adjust width
###         new_height = target_height
###         new_width = int(bg_width * (target_height / bg_height))
###
###     img = bg_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
###     # Create a new 400x550 image and paste the resized background, centering it
###     final_img = Image.new('RGB', (400, 550), (0, 0, 0, 0))  # Transparent for exact fit
###     paste_x = (400 - new_width) // 2
###     paste_y = (550 - new_height) // 2
###     final_img.paste(img, (paste_x, paste_y))
### except Exception as e:
###     # Log error but don’t fallback to a color—halt if background.png isn’t found
###     raise Exception(f"Background image 'background.png' not found or invalid: {str(e)}")
###
### draw = ImageDraw.Draw(final_img)
###
### try:
###     # Try to use Roboto font (if uploaded as "Roboto.ttf") with different sizes for each container
###     top_left_font = ImageFont.truetype("Roboto.ttf", size=20)  # Smaller for Symbol + Price + %
###     top_right_font = ImageFont.truetype("Roboto.ttf", size=20)  # Smaller for Position
###     middle_font = ImageFont.truetype("Roboto.ttf", size=22)  # Medium for Symbol + Strike
###     below_middle_font = ImageFont.truetype("Roboto.ttf", size=22)  # Medium for Entry Price
###     bottom_font = ImageFont.truetype("Roboto.ttf", size=26)  # Larger for P&L
### except:
###     # Fallback: Use default font with estimated sizes
###     top_left_font = ImageFont.load_default()
###     top_right_font = ImageFont.load_default()
###     middle_font = ImageFont.load_default()
###     below_middle_font = ImageFont.load_default()
###     bottom_font = ImageFont.load_default()
###
### # Define container positions based on your center coordinates, assuming 80x80 containers
### container_positions = [
###     {
###         "center_x": 158,
###         "center_y": 157,
###         "width": 80,
###         "height": 80
###     },  # Top Left (Symbol + Price + %)
###     {
###         "center_x": 268,
###         "center_y": 157,
###         "width": 80,
###         "height": 80
###     },  # Top Right (Position)
###     {
###         "center_x": 200,
###         "center_y": 230,
###         "width": 80,
###         "height": 80
###     },  # Middle (Symbol + Strike)
###     {
###         "center_x": 200,
###         "center_y": 308,
###         "width": 80,
###         "height": 80
###     },  # Below Middle (Entry Price)
###     {
###         "center_x": 200,
###         "center_y": 378,
###         "width": 80,
###         "height": 80
###     },  # Bottom (P&L)
### ]
###
### # Top Left Container: Symbol + price + % (e.g., "SPY $609.47 (+0.27%)")
### symbol_price = f"{symbol} ${strike[:-1]} {option_type} (+0.27%)"  # Static % for now
### draw.text((container_positions[0]["center_x"] - draw.textlength(symbol_price, top_left_font) // 2,
###            container_positions[0]["center_y"] - top_left_font.size // 2),
###           symbol_price, top_left_font, fill='#FFFFFF')
###
### # Top Right Container: Position (e.g., "Long" or "Short")
### draw.text((container_positions[1]["center_x"] - draw.textlength(position.capitalize(), top_right_font) // 2,
###            container_positions[1]["center_y"] - top_right_font.size // 2),
###           position.capitalize(), top_right_font, fill='#FFFFFF')
###
### # Middle Container: Symbol + strike (e.g., "SPY $606 Call")
### mid_text = f"{symbol} ${strike[:-1]} {option_type}"
### draw.text((container_positions[2]["center_x"] - draw.textlength(mid_text, middle_font) // 2,
###            container_positions[2]["center_y"] - middle_font.size // 2),
###           mid_text, middle_font, fill='#FFFFFF')
###
### # Below Middle Container: Entry price (current price, I assume)
### draw.text((container_positions[3]["center_x"] - draw.textlength(f"Entry: ${entry_price:.2f}", below_middle_font) // 2,
###            container_positions[3]["center_y"] - below_middle_font.size // 2),
###           f"Entry: ${entry_price:.2f}", below_middle_font, fill='#FFFFFF')
###
### # Bottom Container: P&L with triangle, price, %, and Late close/Long or Short
### # Ensure triangle symbols display correctly with fallback characters
### triangle = "▲" if pnl_percentage >= 0 else "▼"
### try:
###     # Try to use Unicode triangles
###     draw.text((0, 0), triangle, font=bottom_font)  # Test render
### except UnicodeEncodeError:
###     # Fallback to ASCII arrows if triangles don’t render
###     triangle = "↑" if pnl_percentage >= 0 else "↓"
###
### color = '#00FF00' if pnl_percentage >= 0 else '#FF0000'  # Green for profit, red for loss
### pnl_text = f"{triangle} Current: ${current_price:.2f} ({pnl_percentage:.2f}%)"
### if late_call:
###     pnl_text += " (Late close)"
### if position.lower() in ["long", "short"]:
###     pnl_text += f" ({position.capitalize()})"
###
### draw.text((container_positions[4]["center_x"] - draw.textlength(pnl_text, bottom_font) // 2,
###            container_positions[4]["center_y"] - bottom_font.size // 2),
###           pnl_text, bottom_font, fill=color)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await tree.sync()
    print("Slash commands synced!")


@tree.command(
    name="option",
    description="Calculate P&L for SPY/QQQ/IWM/NVDA options (Admin only)")
@app_commands.describe(
    symbol="SPY, QQQ, IWM, or NVDA",
    strike="Strike price with c/p (e.g., 450c or 400p)",
    entry_price="Entry price of the option",
    current_price="Current price of the option",
    position="Long or Short position",
    late_call="Indicate if it's a late call (optional, defaults to False)")
async def option_pnl(interaction: discord.Interaction,
                     symbol: str,
                     strike: str,
                     entry_price: float,
                     current_price: float,
                     position: str,
                     late_call: bool = False):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "You need Administrator permissions to use this command!",
            ephemeral=True)
        return

    try:
        symbol = symbol.upper()
        valid_symbols = ["SPY", "QQQ", "IWM", "NVDA"]
        if symbol not in valid_symbols:
            await interaction.response.send_message(
                f"Symbol must be one of: {', '.join(valid_symbols)}!",
                ephemeral=True)
            return

        if not re.match(r'^\d+[cp]$', strike, re.IGNORECASE):
            await interaction.response.send_message(
                "Strike must be in format like '450c' or '400p'!",
                ephemeral=True)
            return

        strike_price = float(strike[:-1])
        option_type = 'Call' if strike[-1].lower() == 'c' else 'Put'
        is_call = option_type == 'Call'

        position = position.lower()
        if position not in ["long", "short"]:
            await interaction.response.send_message(
                "Position must be 'long' or 'short'!", ephemeral=True)
            return

        pnl_percentage = calculate_pnl(entry_price, current_price, is_call,
                                       position == "long")

        # Log the command execution and parameters
        logger.info(
            f"Executing /option for {symbol} - Strike: {strike}, Entry: {entry_price}, Current: {current_price}, Position: {position}, Late Call: {late_call}"
        )

        image_buffer = create_pnl_image(symbol, strike, option_type,
                                        pnl_percentage, entry_price,
                                        current_price, late_call, position)

        # Create an embed for a cleaner Discord appearance with darker blue color
        embed = discord.Embed(title=f"INF TRADES Option P&L - {symbol}",
                              color=0x00008B)  # Darker blue (Navy Blue)
        embed.set_image(url="attachment://option_pnl.png")
        await interaction.response.send_message(embed=embed,
                                                file=discord.File(
                                                    image_buffer,
                                                    "option_pnl.png"))

    except Exception as e:
        logger.error(f"Error in /option command: {str(e)}")
        await interaction.response.send_message(f"An error occurred: {str(e)}",
                                                ephemeral=True)


# Run the bot using the token from Replit Secrets
client.run(os.getenv('DISCORD_TOKEN'))
