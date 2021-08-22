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

API_KEY = "1986359551:AAECz0XkMwPiWPk9DCn10-Es5kD1V4VBBco" 
print(API_KEY)

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
updater.start_polling()
updater.idle()