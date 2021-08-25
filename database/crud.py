from database.database import users

# returns user details
async def read_user(username: str):
    user = await users.find_one({"username": username}, {"_id": 0})
    return user

# creates user
async def create_user(username: str, income: int, pay_date: int):
    user = await read_user(username)
    if user:
        new_data = dict(income=income, pay_date=pay_date)
        user.update(new_data)
        result = await update_user(username=username, data=user)
        return result
        
    else:
        result = await users.insert_one({
            "username": username,
            "pay_date": pay_date,
            "income": income,
            "mi": 0,
            "me": 0
        })
        if result.inserted_id:
            return True
        else:
            return False

# updates user
async def update_user(username: str, data: dict):
    result = await users.update_one({"username": username}, {"$set": data})
    if result.modified_count:
        return True
    else: 
        return False
    
