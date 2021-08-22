import asyncio

from telegram.ext import ConversationHandler
from telegram.update import Update

from users import (
    save_income_and_paydate,
    save_me,
    save_mi,
    get_detail
)

loop = asyncio.get_event_loop()
states_list = ["start", "income_and_date", "mi", "me", "show_detail", "close_conversation", "cancle"]
states = dict()
state_ids = dict()

for i, state in enumerate(states_list):
    state_ids[state]=i
    states[i]=state


def start(update, context):
    state_id = state_ids["start"]
    update.message.reply_text(
        """Hey! I’m Nerd - your budgeting assistant. I’ll help setup budget, weekly targets and keep you on track. Select a goal to begin 🔥

        Type option number👇
        1. New Gadget, vacation etc
        2. Investing money
        3. Building emergency fund
        4. Paying off debt
        5. Just saving"""
    )
    
    return state_id+1


def income_and_date(update: Update, context):
    restart = check_restart(update.message.text)
    if restart:
        return start(update, context)
    state_id = state_ids["income_and_date"]
    result = loop.run_until_complete(check_prev_state(update, state_id=state_id-1))
    
    if result is None:
        print("income error")
        return state_id
    
    else:
        update.message.reply_text(
            """
            👍 Awesome! I’ve a few more questions to ask. Note: Answers can’t be edited. To restart setup, type restart
            🤑 Your Income & Pay date?
            👉 Type (eg): 15000, 27

            👉 Income is salary/ allowance/ stipend etc per month"""
        )
        return state_id+1


def mi(update, context):
    restart = check_restart(update.message.text)
    if restart:
        return start(update, context)
    state_id = state_ids["mi"]
    result = loop.run_until_complete(check_prev_state(update, state_id=state_id-1))
    if result is None:
        print("mi error")
        return state_id
    
    else:
        update.message.reply_text(
            """
            🌲 Monthly Investments (SIP etc)

            👉 Enter total amount"""
        )
        return state_id+1


def me(update, context):
    restart = check_restart(update.message.text)
    if restart:
        return start(update, context)
    state_id = state_ids["me"]
    result = loop.run_until_complete(check_prev_state(update, state_id=state_id-1))
    if result is None:
        print("me error")
        return state_id

    else:
        update.message.reply_text(
            """
            👽 Expenses every month?

            Home: Rent, Maids, Cook etc.
            Bills: Electricity, Water, DTH, Landline, Mobile, Wifi, Gas etc.
            EMI: Loans, Insurance etc.

            👉 Enter total amount

            (Don't include credit card bill payment, grocery)"""
        )
        return state_id+1


def show_details(update, context):
    restart = check_restart(update.message.text)
    if restart:
        return start(update, context)
    state_id = state_ids["show_detail"]
    result = loop.run_until_complete(check_prev_state(update, state_id=state_id-1))
    if result is None:
        print("show details error")
        return state_id

    else:
        # call api to get data back
        result = loop.run_until_complete(get_detail(update.message.from_user.username))
        if result:
            income, pay_date, mi, me = result
            update.message.reply_text(
                f"""
                🤑  income : {income}
                🔥 Pay date : {pay_date}
                🌲 Monthly Investments : {mi} 
                👽 Expenses : {me}

                type Y for continue type N for input again"""
            )
            return state_id+1
        else:
            update.message.reply_text("sorry! something went wrong. Kindly start again.")
            return state_ids["start"]
    

def close_conversation(update, context):
    restart = check_restart(update.message.text)
    if restart:
        return start(update, context)
    state_id = state_ids["close_conversation"]
    result = loop.run_until_complete(check_prev_state(update, state_id=state_id-1))
    if result is None:
        print("closing error")
        return state_id
    
    else:
        if result.lower()=="y":
            update.message.reply_text("😍 Awesome")
            return ConversationHandler.END
        
        else:
            return income_and_date(update, context)


def cancel(update, context):
    update.message.reply_text("Bye!")
    return ConversationHandler.END


# check if user input is legal and save the information to the database
async def check_prev_state(update: Update, state_id):
    result = None
    
    if states[state_id]=="start":
        result = check_start(update.message.text)
        if result is None:
            update.message.reply_text("Enter correct response please...")
            return None
        else:
            return result

    if states[state_id]=="income_and_date":
        result = check_income_and_paydate(update.message.text)
        if result is None:
            update.message.reply_text("Enter correct response please...")
            return None
        else:
            income, pay_date = result
            await save_income_and_paydate(update.message.from_user.username, float(income), float(pay_date))
            return income, pay_date
        
    elif states[state_id]=="mi":
        result = check_money(update.message.text)
        if result is None:
            update.message.reply_text("Enter correct response please...")
            return None
        else:
            mi = result
            await save_mi(update.message.from_user.username, mi=mi)
            return mi
    
    elif states[state_id]=="me":
        result = check_money(update.message.text)
        if result is None:
            update.message.reply_text("Enter correct response please...")
            return None
        else:
            me = result
            await save_me(update.message.from_user.username, me=me)
            return me
    
    elif states[state_id]=="show_detail":
        result = check_show_detail(update.message.text)
        if result is None:
            update.message.reply_text("Enter correct response please...")
            return None
        else:
            return result
        
    else:
        return None

    
def check_start(text):
    try:
        choice = int(text.lower())
        if choice>=1 and choice<=5:
            return choice
        else:
            return None
    except:
        return None


def check_income_and_paydate(text):
    texts = text.split(",")
    try:
        if len(texts)==2:
            income = texts[0]
            date = int(texts[1])
            if date>=1 and date<31 and check_money(income):
                return income, date
            
            else:
                return None
        
        else:
            return None 
    
    except:
        return None


def check_money(text):
    try:
        mi = int(text)
        if mi>=0:
            return mi
        else:
            return None
    except:
        return None


def check_show_detail(text):
    text = text.lower()
    if text=="y" or text=="n":
        return text
    else:
        return None


def check_restart(text):
    text = text.lower()
    if text=="restart":
        return True
    else:
        return False



