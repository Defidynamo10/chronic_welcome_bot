import os
import asyncio
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
WELCOME_GIF = os.getenv("WELCOME_GIF", "welcome_bot.mp4")

if not TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN is missing in .env file!")

# Welcome message handler
async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        # Inline buttons for socials
        keyboard = [
            [
                InlineKeyboardButton("🌐 Web", url="https://chroniccoin.com"),
                InlineKeyboardButton("𝕏 Twitter", url="https://x.com/chroniccoin"),
                InlineKeyboardButton("💱 DEX", url="https://dexscreener.com/base/0xd996A4C4721037cA0AbB92c53d380aae0cBfD3ca")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Caption text with stoner vibes
        welcome_text = f"""
🌿🔥 Welcome, {member.mention_html()}! 🔥🌿  

You just stepped into the $CHRONIC Garden 🌱✨  
Here, the vibe is high, the memes are dank,  
and the stoner army is always ready to pump 🚀💨  

💚 Puff, chill & HODL strong. Together we rise 🌎🍀  

👇 Connect with the stoners
"""

        # Send GIF with caption + buttons
        gif_msg = await context.bot.send_animation(
            chat_id=update.effective_chat.id,
            animation=open(WELCOME_GIF, "rb"),
            caption=welcome_text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

        # Delete after 60 seconds
        await asyncio.sleep(60)
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=gif_msg.message_id)
            print("✅ Deleted welcome message (gif + caption + socials) after 1 minute")
        except Exception as e:
            print(f"⚠️ Could not delete message: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
    print("🤖 $CHRONIC Welcome Bot running... 🚀🔥")
    app.run_polling()

if __name__ == "__main__":
    main()
