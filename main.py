import asyncio
import os

from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    Filters,
)


from response import (
    start,
    income_and_date,
    mi,
    me,
    show_details,
    close_conversation,
    cancel,
    states,
    state_ids
)

async def main():
    API_KEY = "1986359551:AAECz0XkMwPiWPk9DCn10-Es5kD1V4VBBco"
    
    updater = Updater(API_KEY)
   

    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            state_ids["income_and_date"]: [MessageHandler(Filters.text, income_and_date)],
            state_ids["mi"]: [MessageHandler(Filters.text, mi)],
            state_ids["me"]: [MessageHandler(Filters.text, me)],
            state_ids["show_detail"]: [MessageHandler(Filters.text & ~Filters.command, show_details)],
            state_ids["close_conversation"]: [MessageHandler(Filters.text, close_conversation)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    if os.getenv("MODE", False):
        PORT= int(os.getenv("PORT"))
        ip = "0.0.0.0" 
        webhook_url = os.getenv("WEBHOOK")
        updater.start_webhook(ip, port=PORT, url_path=API_KEY)
        updater.bot.setWebhook(webhook_url+"/"+API_KEY)
    
    else:
        updater.start_polling()

if __name__=="__main__":
    asyncio.run(main())