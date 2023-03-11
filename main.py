import logging
from telegram import __version__ as TG_VER
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from chat import outreq, get_conv
from sql import upd, getuser, new_user, get_conversation
from datetime import datetime

tkn = '5924711064:AAHeiO9ObQoNbGXoAa09csnC23IeYcQvFOM'

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update andncontext.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! My name is Jarvis and I'm your assistant for everything. Ask me anything, I'm happy to help.",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    usr_msg = update.message.text
    now = datetime.now()
    user_id = str(update.message.from_user.id)
    user_name = update.message.from_user.name
    dt = now.strftime("%Y-%m-%d %H:%M:%S")
    rep_text = outreq(usr_msg)

    conv, prem = getuser(user_id)

    #Scenarios for new and existing users
    if conv == 'na':
        #in case the user is new -> add user, answer the prompt
        new_user(user_id, user_name)
        rep_text = outreq(usr_msg)
    else:
        #in case the user is existing -> get last 5 conversations from SQL and continue
        conversation = get_conversation(user_id)
        rep_text = get_conv(conversation, usr_msg)

    #update database
    upd(dt, user_id, usr_msg, rep_text)
    
    #reply to user
    await update.message.reply_text(rep_text)

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(tkn).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, talk))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()

if __name__ == "__main__":
    main()
