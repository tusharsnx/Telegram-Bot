from users import (
    save_income_and_paydate,
    save_me,
    save_mi,
    get_detail
)

states_list = ["start", "income_and_date", "mi", "me", "show_detail", "close_conversation", "cancel"]
states = dict()
state_ids = dict()

for i, state in enumerate(states_list):
    state_ids[state]=i
    states[i]=state


async def start(text, username):
    state_id = state_ids["start"]
    response_text = """
        Hey! I’m Nerd - your budgeting assistant. I’ll help setup budget, weekly targets and keep you on track. Select a goal to begin 🔥

    Type option number👇
    1. New Gadget, vacation etc
    2. Investing money
    3. Building emergency fund
    4. Paying off debt
    5. Just saving
        """
    
    return state_id+1, response_text


async def income_and_date(text, username):
    restart = check_restart(text)
    if restart:
        return await start(text)
    state_id = state_ids["income_and_date"]
    is_ok, result = await check_prev_state(text, state_id-1, username)
    
    # checking if user came from close_conversation state
    if not is_ok:
        is_ok, result = await check_prev_state(text, state_ids["close_conversation"]-1, username)
    
    if not is_ok:
        print("income error")
        return state_id, result
    
    else:
        response_text = [
            "👍 Awesome! I’ve a few more questions to ask. Note: Answers can’t be edited. To restart setup, type restart",
            """
            🤑 Your Income & Pay date?
        👉 Type (eg): 15000, 27
        👉 Income is salary/ allowance/ stipend etc per month
        """]
        return state_id+1, response_text


async def mi(text, username):
    restart = check_restart(text)
    if restart:
        return await start(text, username)
    state_id = state_ids["mi"]
    is_ok, result = await check_prev_state(text, state_id-1, username)
    if not is_ok:
        print("mi error")
        return state_id, result
    
    else:
        response_text = """
        🌲 Monthly Investments (SIP etc)
        
    👉 Enter total amount
        """
        return state_id+1, response_text


async def me(text, username):
    restart = check_restart(text)
    if restart:
        return await start(text, username)
    state_id = state_ids["me"]
    is_ok, result = await check_prev_state(text, state_id-1, username)
    if not is_ok:
        print("me error")
        return state_id, result

    else:
        response_text = """
        👽 Expenses every month?

    Home: Rent, Maids, Cook etc.
    Bills: Electricity, Water, DTH, Landline, Mobile, Wifi, Gas etc.
    EMI: Loans, Insurance etc.

    👉 Enter total amount

    (Don't include credit card bill payment, grocery)
        """
        return state_id+1, response_text


async def show_details(text, username):
    restart = check_restart(text)
    if restart:
        return await start(text, username)
    state_id = state_ids["show_detail"]
    is_ok, result = await check_prev_state(text, state_id-1, username)
    if not is_ok:
        print("show details error")
        return state_id, result

    else:
        # call api to get data back
        result = await get_detail(username)
        if result:
            income, pay_date, mi, me = result
            response_text =f"""
            🤑  income : {income}
        🔥 Pay date : {pay_date}
        🌲 Monthly Investments : {mi}
        👽 Expenses : {me}
        
        type Y for continue type N for input again
            """
            return state_id+1, response_text
        
        else:
            response_text = "sorry! something went wrong. Kindly start again."
            return state_ids["start"], response_text
    

async def close_conversation(text, username):
    restart = check_restart(text)
    if restart:
        return await start(text, username)
    state_id = state_ids["close_conversation"]
    is_ok, result = await check_prev_state(text, state_id-1, username)
    if not is_ok:
        print("closing error")
        return state_id, result
    
    else:
        if result.lower()=="y":
            response_text = "😍 Awesome"
            return -1, response_text
        
        else:
            return await income_and_date(text, username)


def cancel(text, username):
    response_text = "Bye!"
    return -1, response_text


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


# check if user input is legal and save the information to the database
async def check_prev_state(text, state_id, username):
    result = None
    
    if states[state_id]=="start":
        result = check_start(text)
        if result is None:
            response_text = "Enter correct response please..."
            return False, response_text
        else:
            return True, result

    elif states[state_id]=="income_and_date":
        result = check_income_and_paydate(text)
        if result is None:
            response_text = "Enter correct response please..."
            return False, response_text
        else:
            income, pay_date = result
            await save_income_and_paydate(username, float(income), int(pay_date))
            return True, (income, pay_date)
        
    elif states[state_id]=="mi":
        result = check_money(text)
        if result is None:
            response_text = "Enter correct response please..."
            return False, response_text
        else:
            mi = result
            await save_mi(username, mi=mi)
            return True, mi
    
    elif states[state_id]=="me":
        result = check_money(text)
        if result is None:
            response_text = "Enter correct response please..."
            return False, response_text
        else:
            me = result
            await save_me(username, me=me)
            return True, me
    
    elif states[state_id]=="show_detail":
        result = check_show_detail(text)
        if result is None:
            response_text = "Enter correct response please..."
            return False, response_text
        else:
            return True, result
        
    else:
        return False

    



